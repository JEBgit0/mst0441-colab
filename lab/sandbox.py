"""
sandbox.py - shared pieces for the sandbox pages.

The sandbox is the open page: every value is shown, every slider is live.
It is the counterpart of the guided page (guided.py) and is released once the
problem set's solutions are out.

This file has no economics in it either. It holds what every sandbox lab
needs: drawing a figure to PNG (the same trick as guided.py, so VS Code shows
it once), a slider with sensible defaults, number formatting for the readout,
and the "sticky" axes that keep a pivot visible.
"""

import io
import math

# Light palette, shared with the guided pages so the two look like one course.
INK = "#1f2937"
MUTE = "#6b7280"
GRID = "#e5e7eb"
LINE = "#2563eb"          # the live budget line
CURVE = "#db2777"         # indifference curves
BEFORE = "#9ca3af"        # the frozen "before" state
DIRECT = "#059669"        # a comparison budget (equal-revenue direct charge)
NEW = "#ea580c"


def render(draw, figsize, dpi=110):
    # A bare Figure with its own canvas never touches pyplot, so the notebook
    # cannot show it a second time. draw(fig) fills it in.
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)
    draw(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    return buf.getvalue()


def style_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTE)
    ax.tick_params(colors=MUTE, labelsize=8)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def legend(ax, loc="upper right"):
    leg = ax.legend(loc=loc, fontsize=8.5, frameon=False)
    for text in leg.get_texts():
        text.set_color(INK)


def num(x, digits=2):
    # Integers print as integers, everything else with at most two decimals
    # and no trailing zeros. The course's answers are integers or simple
    # fractions, so a long decimal in the readout means a slider is off.
    if x is None or not math.isfinite(x):
        return "&ndash;"
    if abs(x) < 0.5 * 10 ** -digits:
        return "0"                     # not "-0" from a search that stopped at -1e-7
    r = round(x)
    if abs(x - r) < 1e-6:
        return "%d" % (r + 0)          # + 0 turns -0 into 0
    return ("%.*f" % (digits, x)).rstrip("0").rstrip(".")


def pct(x):
    return "%d%%" % round(100 * x)


def sticky(prev, need, pad=1.2, shrink=0.45):
    # An axis limit that holds still. Rescaling to fit every redraw would
    # cancel a pivot out: the line would always meet the axes at the same
    # place and the picture would never seem to move. So keep the old limit
    # unless the new picture spills out of it or shrinks to a corner of it.
    need = max(float(need), 1e-9)
    if prev is None or need > prev or need < shrink * prev:
        return need * pad
    return prev


def slider(description, lo, hi, step, value, fmt=".2f"):
    import ipywidgets as W
    return W.FloatSlider(
        value=value, min=lo, max=hi, step=step, description=description,
        readout_format=fmt, continuous_update=False,
        style={"description_width": "130px"},
        layout=W.Layout(width="340px"))


def preset_button(label, kind, on_click):
    # Blue for the problem set, green for the notes: the same colours as the
    # source tags on the guided page. Orange marks anything beyond the course.
    import ipywidgets as W
    style = {"problem": "info", "notes": "success"}.get(kind, "warning")
    b = W.Button(description=label, button_style=style,
                 layout=W.Layout(width="auto", margin="2px"))
    b.on_click(lambda _: on_click())
    return b


def table(rows):
    # The readout: a label column and a sentence column, one row per fact.
    cells = "".join("<tr><td style='padding:3px 12px 3px 0;vertical-align:top;"
                    "color:%s;white-space:nowrap'><b>%s</b></td>"
                    "<td style='padding:3px 0'>%s</td></tr>" % (MUTE, k, v)
                    for k, v in rows)
    return "<table style='border-collapse:collapse;margin-top:6px'>%s</table>" % cells


# ------------------------------------------------------------------- labs ---

class Lab:
    """One interactive lab: sliders on the left, figure and readout on the right.

    A subclass fills in the class attributes and four methods:

        relabel()          set slider descriptions and lock unused sliders
        compute()          slider values -> a state object for the next two
        figure(fig, st)    draw the state
        describe(st)       the readout, as HTML (use table())

    The base class owns the plumbing: presets, the before/after freeze, the
    sticky axes and redrawing once per change rather than once per slider.
    """

    TITLE = ""
    INTRO = ""
    SLIDERS = []          # (key, lo, hi, step, value, fmt)
    FAMILIES = None       # options for a "Preferences" dropdown, or None
    PRESETS = []          # dicts: label, kind, values, and optionally before, flags
    CHECKS = []           # extra checkboxes as (key, description)
    DROPDOWNS = []        # extra dropdowns as (key, description, options)
    FIGSIZE = (6.4, 6.4)

    def __init__(self):
        self.before = None
        self.frame = {}
        self._quiet = False

    # -- building ---------------------------------------------------------------
    def show(self):
        import ipywidgets as W
        from IPython.display import display

        self.W = W
        self.w = {}
        if self.FAMILIES:
            self.w["family"] = W.Dropdown(
                options=self.FAMILIES, value=self.FAMILIES[0],
                description="Preferences", style={"description_width": "130px"},
                layout=W.Layout(width="340px"))
        for key, desc, options in self.DROPDOWNS:
            self.w[key] = W.Dropdown(
                options=options, value=options[0], description=desc,
                style={"description_width": "130px"}, layout=W.Layout(width="340px"))
        for key, lo, hi, step, value, fmt in self.SLIDERS:
            self.w[key] = slider(key, lo, hi, step, value, fmt)
        self.compare = W.Checkbox(value=False, indent=False,
                                  description="Freeze a 'before' and compare")
        self.checks = {key: W.Checkbox(value=False, indent=False, description=desc)
                       for key, desc in self.CHECKS}
        for widget in list(self.w.values()) + [self.compare] + list(self.checks.values()):
            widget.observe(self._changed, names="value")

        presets = W.HBox([preset_button(p["label"], p["kind"],
                                        (lambda p=p: self.apply(p)))
                          for p in self.PRESETS],
                         layout=W.Layout(flex_flow="row wrap"))
        controls = W.VBox(
            [W.HTML("<b>Course numbers</b>"), presets,
             W.HTML("<b style='display:block;margin-top:8px'>Controls</b>")]
            + list(self.w.values()) + [self.compare] + list(self.checks.values()),
            layout=W.Layout(width="360px"))
        self.img = W.Image(format="png", layout=W.Layout(width="600px", min_width="320px"))
        self.readout = W.HTML()
        right = W.VBox([self.img, self.readout],
                       layout=W.Layout(flex="1 1 400px", padding="0 0 0 12px"))
        head = W.HTML("<h3 style='margin:4px 0'>%s</h3><p>%s</p>"
                      % (self.TITLE, self.INTRO))
        self.root = W.VBox([head, W.HBox([controls, right], layout=W.Layout(
            flex_flow="row wrap", align_items="flex-start"))])
        self.relabel()
        self.redraw()
        display(self.root)

    # -- state ----------------------------------------------------------------
    def values(self):
        return {k: w.value for k, w in self.w.items()}

    def flag(self, key):
        return self.checks[key].value

    def stick(self, key, need):
        self.frame[key] = sticky(self.frame.get(key), need)
        return self.frame[key]

    def _changed(self, change):
        if self._quiet:
            return
        if change["owner"] is self.compare:
            self.before = self.values() if change["new"] else None
        self._quiet = True
        try:
            self.relabel()
        finally:
            self._quiet = False
        self.redraw()

    def apply(self, preset):
        # Move every widget without redrawing in between, then draw once.
        self._quiet = True
        try:
            self.on_preset(preset)
            for k, v in preset["values"].items():
                self.w[k].value = v
            self.before = dict(preset["before"]) if preset.get("before") else None
            self.compare.value = self.before is not None
            for k, cb in self.checks.items():
                cb.value = preset.get("flags", {}).get(k, False)
            self.frame = {}
            self.relabel()
        finally:
            self._quiet = False
        self.redraw()

    def redraw(self):
        st = self.compute()
        self.img.value = render(lambda fig: self.figure(fig, st), self.FIGSIZE)
        self.readout.value = self.describe(st)

    # -- hooks ----------------------------------------------------------------
    def on_preset(self, preset):
        pass

    def relabel(self):
        pass

    def compute(self):
        raise NotImplementedError

    def figure(self, fig, st):
        raise NotImplementedError

    def describe(self, st):
        raise NotImplementedError
