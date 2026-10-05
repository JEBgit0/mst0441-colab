"""
guided.py - the engine behind the guided notebook pages.

A guided page asks one question at a time and draws the next piece of the
figure only once the answer is right. A wrong answer gets a hint, never the
answer: the course's tutor does not hand out solutions, so neither does this.

Answers are not stored in the clear. Each one is kept as a salted hash of its
canonical form, and a student's input is hashed the same way and compared.
That stops a glance at the code from giving the answer away. It is NOT
security: every answer here is a small integer or fraction, so a determined
student could brute-force it. It only has to cost more than solving the
problem, and it does.

Lecture content lives in its own file (guided_s02.py and so on); this file
knows nothing about economics.

Authoring: to get the hash for a new answer, run
    python guided.py <qid>.<box> <answer>
e.g.  python guided.py a4.0 -3
"""

import hashlib
import importlib
import sys
import warnings
from fractions import Fraction

from style import render

SALT = "mst0441"
BOX = None                    # marks an answer box inside a Question's form


# ------------------------------------------------------------- answers ---

def canon(text):
    # Turn whatever the student typed into one canonical "n/d" string, so
    # "-3", "−3", "-3.0", "-6/2" and "-3,0" all hash alike. Norwegian keyboards
    # write decimals with a comma, so a comma is read as a decimal point.
    s = str(text).strip()
    for dash in ("−", "–", "—"):
        s = s.replace(dash, "-")
    s = s.replace(" ", "").replace(",", ".")
    if not s:
        return None
    try:
        f = Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None
    # A rounded decimal like 0.33 should count as 1/3. Snap to the nearest
    # fraction with a small denominator, but only when it is really close,
    # so a genuinely wrong decimal is never pulled onto the right answer.
    if "/" not in s and f.denominator > 1:
        near = f.limit_denominator(12)
        if abs(float(f - near)) < 0.005:
            f = near
    return "%d/%d" % (f.numerator, f.denominator)


def canon_choice(text):
    return None if text is None else " ".join(str(text).lower().split())


def digest(key, value):
    return hashlib.sha256(("%s|%s|%s" % (SALT, key, value)).encode()).hexdigest()[:16]


def hash_number(key, text):
    return digest(key, canon(text))


def hash_choice(key, text):
    return digest(key, canon_choice(text))


def answers(session):
    """The two lookups a session file needs, for session "s03" and so on.

        H, M = answers("s03")
        H("d1.0")                      the hash of the right answer to box 0 of d1
        M({"d1.0~4/9": "hint"})        {hash: "hint"}, for a Question's mistakes

    The hashes come from answers_sNN.py, which a key file in the private repo
    generates. Hash keys look like "d1.0" for the right answer to box 0 of
    question d1, and "d1.0~4/9" for an expected mistake.
    """
    try:
        hashes = importlib.import_module("answers_" + session).HASHES
    except ImportError:                 # while the key file is being generated
        hashes = {}

    def H(key):
        return hashes.get(key, "missing:" + key)

    def M(messages):
        return {H(k): v for k, v in messages.items()}

    return H, M


# ------------------------------------------------------------ questions ---

class Question:
    """One step: a prompt, answer boxes or a choice list, and what to say
    when the answer is wrong.

    form      the answer line, as a list of labels with BOX where each input
              box goes, e.g. ["", BOX, "&middot; c +", BOX, "&middot; h =", BOX]
    choices   a list of options instead of boxes (multiple choice)
    answers   one hash per box, or one hash for the choice. Box i of
              question q is hashed under the key "q.i"; a choice under "q.c".
              A box may instead take a list of hashes: any of them is right
    mistakes  {hash: message} for wrong answers worth a targeted hint
    hints     general hints, given one per wrong attempt, in order
    explain   shown once the step is solved: the sentence to remember
    source    where the step comes from in the course, as a (kind, text)
              pair from tag(); shown next to the step number so students can
              find it in the problem set or the notes
    """

    def __init__(self, qid, prompt, form=None, choices=None, answers=(),
                 mistakes=None, hints=(), explain="", source=None):
        self.qid = qid
        self.prompt = prompt
        self.form = form or []
        self.choices = choices
        self.answers = list(answers)
        self.mistakes = mistakes or {}
        self.hints = list(hints)
        self.explain = explain
        self.source = source

    @property
    def n_boxes(self):
        return sum(1 for item in self.form if item is BOX)


# ---------------------------------------------------------------- sources ---
# Every step says where it comes from, in one of two colours, so a student
# never goes hunting for "Part C" in the problem set. Lecture files build
# their tags with PS(...) for the problem set or NOTES(...) for the notes.

TAG_COLOURS = {
    "problem": ("#1d4ed8", "#dbeafe"),     # problem set: blue
    "notes": ("#047857", "#d1fae5"),       # session notes: green
}


def tag(kind, text):
    return (kind, text)


def PS(part):
    # Problem numbers are the in-person problem set, e.g. PS("A3.1 (b)").
    return tag("problem", "Problem " + part)


def NOTES(where):
    # Page numbers are the printed pages of the session notes, e.g. NOTES("p. 7").
    return tag("notes", "Notes " + where)


def badge(source):
    if not source:
        return ""
    kind, text = source
    fg, bg = TAG_COLOURS.get(kind, ("#374151", "#e5e7eb"))
    return ("<span style='background:%s;color:%s;border-radius:4px;"
            "padding:1px 6px;font-size:0.85em;white-space:nowrap'>%s</span>"
            % (bg, fg, text))


# --------------------------------------------------------------- the page ---

class GuidedProblem:
    """A list of questions and a draw(ax, stage) function.

    stage is the number of questions solved so far, so draw() only has to
    say what the figure looks like after each step. With whole_figure=True,
    draw() gets the Figure instead of one Axes, for pages with several panels.
    """

    def __init__(self, title, intro, questions, draw, figsize=(6.4, 4.6),
                 outro="", whole_figure=False, sources=()):
        self.title = title
        self.intro = intro
        self.sources = list(sources)       # tags for the whole part, under the title
        self.questions = questions
        self.draw = draw
        self.figsize = figsize
        self.outro = outro
        self.whole_figure = whole_figure

    # -- building the widgets ---------------------------------------------
    def show(self):
        # Imported here so the hashing helpers above work without a notebook.
        import ipywidgets as W
        from IPython.display import display

        self.W = W
        self.stage = 0
        self.attempts = 0

        # The figure is an Image widget fed PNG bytes (see render in style.py),
        # not a pyplot figure in an Output widget.
        self.fig_img = W.Image(format="png",
                               layout=W.Layout(width="560px", min_width="320px"))
        self.log = W.VBox()
        self.ask = W.VBox()
        restart = W.Button(description="Start over", icon="refresh",
                           layout=W.Layout(width="130px", margin="12px 0 0 0"))
        restart.on_click(lambda _: self._restart())

        based = ""
        if self.sources:
            based = ("<p style='margin:2px 0 6px'>Based on: %s</p>"
                     % " ".join(badge(s) for s in self.sources))
        head = W.HTML("<h3 style='margin:4px 0'>%s</h3>%s<p>%s</p>"
                      % (self.title, based, self.intro))
        # Figure on the left, the trail of solved steps and the live question on
        # the right. Wraps to one column when the window is narrow.
        side = W.VBox([self.log, self.ask, restart],
                      layout=W.Layout(flex="1 1 320px", padding="0 0 0 16px"))
        body = W.HBox([self.fig_img, side],
                      layout=W.Layout(flex_flow="row wrap", align_items="flex-start"))
        self.root = W.VBox([head, body])
        self._redraw()
        self._next_question()
        display(self.root)

    def _restart(self):
        self.stage = 0
        self.log.children = ()
        self._redraw()
        self._next_question()

    def _redraw(self):
        def draw(fig):
            if self.whole_figure:
                self.draw(fig, self.stage)
            else:
                self.draw(fig.add_subplot(), self.stage)
            # An inset (a zoomed panel) makes tight_layout warn, and a warning
            # would print under the widget. The layout is still fine, so keep
            # it quiet.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                fig.tight_layout()

        self.fig_img.value = render(draw, self.figsize)

    def _next_question(self):
        W = self.W
        self.attempts = 0
        if self.stage >= len(self.questions):
            self.ask.children = (W.HTML(
                "<p style='color:#15803d'><b>Part complete.</b> %s</p>"
                % self.outro),)
            return

        q = self.questions[self.stage]
        prompt = W.HTML("<p style='margin:10px 0 4px'><b>Step %d of %d</b> &nbsp;%s"
                        "<br>%s</p>"
                        % (self.stage + 1, len(self.questions), badge(q.source),
                           q.prompt))

        if q.choices:
            self.inputs = [W.RadioButtons(options=q.choices, value=None,
                                          layout=W.Layout(width="auto"))]
            line = self.inputs[0]
        else:
            self.inputs, parts = [], []
            for item in q.form:
                if item is BOX:
                    box = W.Text(placeholder="?", layout=W.Layout(width="80px"))
                    self.inputs.append(box)
                    parts.append(box)
                elif item:
                    parts.append(W.HTML("<span style='padding:0 6px'>%s</span>" % item))
            line = W.HBox(parts, layout=W.Layout(align_items="center"))

        check = W.Button(description="Check", button_style="primary",
                         layout=W.Layout(width="100px"))
        self.feedback = W.HTML()
        check.on_click(lambda _: self._check(q))
        self.ask.children = (prompt, line, check, self.feedback)

    # -- checking -------------------------------------------------------------
    def _check(self, q):
        if q.choices:
            raw = [self.inputs[0].value]
            if raw[0] is None:
                self._say("Pick one of the options first.", "#b45309")
                return
            hashes = [hash_choice("%s.c" % q.qid, raw[0])]
        else:
            raw = [box.value for box in self.inputs]
            if any(canon(r) is None for r in raw):
                self._say("Fill in every box with a number, e.g. 12, -3 or 5/2.",
                          "#b45309")
                return
            hashes = [hash_number("%s.%d" % (q.qid, i), r)
                      for i, r in enumerate(raw)]

        # An answer is one hash, or a list of hashes when several forms are
        # right, e.g. 4.0625 and the rounded 4.06 from a student who rounds.
        right = [h in a if isinstance(a, (list, tuple)) else h == a
                 for h, a in zip(hashes, q.answers)]
        if all(right):
            self._solved(q, raw)
            return

        # Targeted messages for the mistakes we expect, else the next hint.
        self.attempts += 1
        notes = []
        for h, ok in zip(hashes, right):
            if not ok and h in q.mistakes and q.mistakes[h] not in notes:
                notes.append(q.mistakes[h])
        if not notes and q.hints:
            notes = [q.hints[min(self.attempts, len(q.hints)) - 1]]
        marks = ""
        if len(right) > 1:
            marks = " &nbsp; ".join("box %d %s" % (i + 1, "&#10003;" if ok else "&#10007;")
                                    for i, ok in enumerate(right)) + "<br>"
        self._say("%sNot yet. %s" % (marks, " ".join(notes)), "#b91c1c")

    def _say(self, text, colour):
        self.feedback.value = "<p style='color:%s;margin:4px 0'>%s</p>" % (colour, text)

    def _solved(self, q, raw):
        W = self.W
        given = ", ".join(str(r) for r in raw)
        done = W.HTML("<p style='margin:2px 0;color:#15803d'>&#10003; <b>Step %d</b> "
                      "(%s) %s &nbsp;<span style='color:#374151'>%s</span></p>"
                      % (self.stage + 1, given, badge(q.source), q.explain))
        self.log.children = self.log.children + (done,)
        self.stage += 1
        self._redraw()
        self._next_question()


# ------------------------------------------------------------- authoring ---

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    key, value = sys.argv[1], sys.argv[2]
    if key.endswith(".c"):
        print(hash_choice(key, value))
    else:
        print(canon(value), hash_number(key, value))
