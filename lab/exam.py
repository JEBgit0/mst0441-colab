"""
exam.py - the engine behind the mock exam pages (the workshops).

A guided page (guided.py) hands out one step at a time. A mock exam is sat the
other way round: the whole paper is on the table, you work through it with pen
and paper, and only then type your final answers in. So an exam page shows
every part of a problem at once and marks them together, out of the points the
paper gives that problem.

    Part          one part of a problem, e.g. 1(c): a Question worth points
    ExamProblem   a problem: its text, its parts and a figure
    ExamPaper     the problems together, for the score table

The marking follows the guided pages. Answers are salted hashes (see
guided.py), and a wrong answer gets a hint, never the answer. The score of the
first marking is kept beside the current one: that is the number to compare
with an exam, where there is no second try.

A paper's content lives in its own file (exam_w01.py and so on); this file
knows nothing about economics.
"""

import warnings

from guided import BOX, Choices, Question, canon, hash_choice, hash_number
from style import MUTE, render

GOOD, BAD, WARN = "#15803d", "#b91c1c", "#b45309"


class Part(Question):
    """A Question with the label it has on the paper and the points it carries.

    A part is all or nothing: every box right, or the option right, earns the
    points. So keep a part small, and split a long one in two.
    """

    def __init__(self, qid, label, points, prompt, **kw):
        super().__init__(qid, prompt, **kw)
        self.label = label
        self.points = points


def points_text(n):
    return "1 point" if n == 1 else "%d points" % n


def grade(q, raw):
    """Mark what was typed for one part.

    Returns (state, right, notes): state is "blank", "invalid", "right" or
    "wrong"; right says which boxes are right; notes are the targeted hints
    for the mistakes we expect.
    """
    if q.choices:
        if raw[0] is None:
            return "blank", [], []
        hashes = [hash_choice("%s.c" % q.qid, raw[0])]
    else:
        if all(not str(r).strip() for r in raw):
            return "blank", [], []
        if any(canon(r) is None for r in raw):
            return "invalid", [], []
        hashes = [hash_number("%s.%d" % (q.qid, i), r) for i, r in enumerate(raw)]
    right = [h in a if isinstance(a, (list, tuple)) else h == a
             for h, a in zip(hashes, q.answers)]
    notes = []
    for h, ok in zip(hashes, right):
        if not ok and h in q.mistakes and q.mistakes[h] not in notes:
            notes.append(q.mistakes[h])
    return ("right" if all(right) else "wrong"), right, notes


class ExamProblem:
    """One problem of a paper: every part on the page at once.

    draw(ax, done) draws the figure, where done is the set of part ids marked
    right so far. With whole_figure=True it gets the Figure instead of one
    Axes. A problem with no figure, such as a list of multiple-choice
    questions, leaves draw out.
    """

    def __init__(self, title, text, parts, draw=None, figsize=(6.4, 4.6),
                 whole_figure=False):
        self.title = title
        self.text = text
        self.parts = parts
        self.draw = draw
        self.figsize = figsize
        self.whole_figure = whole_figure
        self.done = set()
        self.first = None                  # points at the first marking

    @property
    def points(self):
        return sum(q.points for q in self.parts)

    def score(self):
        return sum(q.points for q in self.parts if q.qid in self.done)

    # -- building the widgets ---------------------------------------------
    def show(self):
        import ipywidgets as W
        from IPython.display import display

        self.W = W
        self.rows = {}
        blocks = []
        for q in self.parts:
            prompt = W.HTML("<p style='margin:12px 0 4px'><b>%s</b> &nbsp;<span "
                            "style='color:%s'>%s</span><br>%s</p>"
                            % (q.label, MUTE, points_text(q.points), q.prompt))
            if q.choices:
                inputs = [Choices(W, q.choices)]
                line = inputs[0].box
            else:
                inputs, items = [], []
                for item in q.form:
                    if item is BOX:
                        box = W.Text(placeholder="?", layout=W.Layout(width="80px"))
                        inputs.append(box)
                        items.append(box)
                    elif item:
                        items.append(W.HTML("<span style='padding:0 6px'>%s</span>" % item))
                line = W.HBox(items, layout=W.Layout(align_items="center",
                                                     flex_flow="row wrap"))
            feedback = W.HTML()
            self.rows[q.qid] = (inputs, feedback)
            blocks += [prompt, line, feedback]

        mark = W.Button(description="Mark this problem", button_style="primary", icon="check",
                        layout=W.Layout(width="180px", margin="14px 8px 0 0"))
        again = W.Button(description="Start over", icon="refresh",
                         layout=W.Layout(width="130px", margin="14px 0 0 0"))
        mark.on_click(lambda _: self._mark())
        again.on_click(lambda _: self._restart())
        self.total = W.HTML()
        side = W.VBox(blocks + [W.HBox([mark, again]), self.total],
                      layout=W.Layout(flex="1 1 360px", padding="0 0 0 16px"))
        head = W.HTML("<h3 style='margin:4px 0'>%s &nbsp;<span style='color:%s;"
                      "font-weight:normal'>%s</span></h3><p>%s</p>"
                      % (self.title, MUTE, points_text(self.points), self.text))
        if self.draw:
            self.fig_img = W.Image(format="png",
                                   layout=W.Layout(width="520px", min_width="320px"))
            body = W.HBox([self.fig_img, side],
                          layout=W.Layout(flex_flow="row wrap", align_items="flex-start"))
        else:
            self.fig_img = None
            body = side
        self.root = W.VBox([head, body])
        self._restart()
        display(self.root)

    def _restart(self):
        self.done = set()
        self.first = None
        self.tries = {}
        for inputs, feedback in self.rows.values():
            for w in inputs:
                w.disabled = False
                w.value = None if hasattr(w, "options") else ""
            feedback.value = ""
        self.total.value = ("<p style='color:%s;margin:8px 0'>Work the problem on paper "
                            "first, then type your answers in and mark them together.</p>"
                            % MUTE)
        self._redraw()

    def _redraw(self):
        if self.fig_img is None:
            return

        def draw(fig):
            if self.whole_figure:
                self.draw(fig, self.done)
            else:
                self.draw(fig.add_subplot(), self.done)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                fig.tight_layout()

        self.fig_img.value = render(draw, self.figsize)

    # -- marking --------------------------------------------------------------
    def _mark(self):
        for q in self.parts:
            if q.qid in self.done:
                continue
            inputs, feedback = self.rows[q.qid]
            state, right, notes = grade(q, [w.value for w in inputs])
            if state == "blank":
                self._say(feedback, MUTE, "Not answered: 0 of %d." % q.points)
            elif state == "invalid":
                self._say(feedback, WARN, "Fill in every box with a number, e.g. 12, -3 or "
                                          "5/2. 0 of %d." % q.points)
            elif state == "right":
                self.done.add(q.qid)
                for w in inputs:
                    w.disabled = True
                self._say(feedback, GOOD, "&#10003; %d of %d. <span style='color:#374151'>%s"
                                          "</span>" % (q.points, q.points, q.explain))
            else:
                self.tries[q.qid] = self.tries.get(q.qid, 0) + 1
                if not notes and q.hints:
                    notes = [q.hints[min(self.tries[q.qid], len(q.hints)) - 1]]
                marks = ""
                if len(right) > 1:
                    marks = " &nbsp; ".join(
                        "box %d %s" % (i + 1, "&#10003;" if ok else "&#10007;")
                        for i, ok in enumerate(right)) + "<br>"
                self._say(feedback, BAD, "%s&#10007; 0 of %d. %s"
                          % (marks, q.points, " ".join(notes)))
        if self.first is None:
            self.first = self.score()
        self.total.value = ("<p style='margin:8px 0'><b>%d of %d points.</b> &nbsp;<span "
                            "style='color:%s'>First marking: %d of %d.</span></p>"
                            % (self.score(), self.points, MUTE, self.first, self.points))
        self._redraw()

    @staticmethod
    def _say(feedback, colour, text):
        feedback.value = "<p style='color:%s;margin:4px 0'>%s</p>" % (colour, text)


class ExamPaper:
    """The problems of one paper, for the score table at the end of the page."""

    def __init__(self, title, problems, note=""):
        self.title = title
        self.problems = problems
        self.note = note

    @property
    def points(self):
        return sum(p.points for p in self.problems)

    def show(self):
        import ipywidgets as W
        from IPython.display import display

        self.table = W.HTML()
        update = W.Button(description="Update the score", icon="refresh",
                          layout=W.Layout(width="170px", margin="8px 0 0 0"))
        update.on_click(lambda _: self._fill())
        self._fill()
        display(W.VBox([W.HTML("<h3 style='margin:4px 0'>%s</h3>" % self.title),
                        self.table, update]))

    def _fill(self):
        cell = "<td style='padding:3px 16px 3px 0;text-align:%s'>%s</td>"
        head = "".join(cell % (side, "<b>%s</b>" % text) for side, text in
                       (("left", "Problem"), ("right", "First marking"), ("right", "Now"),
                        ("right", "Points")))
        rows, first, now = [], 0, 0
        for p in self.problems:
            marked = p.first is not None
            first += p.first or 0
            now += p.score()
            rows.append("<tr>%s%s%s%s</tr>" % (
                cell % ("left", p.title),
                cell % ("right", p.first if marked else "&ndash;"),
                cell % ("right", p.score() if marked else "&ndash;"),
                cell % ("right", p.points)))
        rows.append("<tr style='border-top:1px solid %s'>%s%s%s%s</tr>" % (
            MUTE, cell % ("left", "<b>Total</b>"), cell % ("right", "<b>%d</b>" % first),
            cell % ("right", "<b>%d</b>" % now), cell % ("right", "<b>%d</b>" % self.points)))
        self.table.value = (
            "<table style='border-collapse:collapse;margin-top:6px'><tr>%s</tr>%s</table>"
            "<p style='color:%s;margin:8px 0 0'>%s</p>" % (head, "".join(rows), MUTE, self.note))
