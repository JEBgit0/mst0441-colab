"""
sandbox_s02.py - session 2 sandbox: every value shown, every slider live.

    goods    budget, preferences and choice (A2.1, review question 6)
    leisure  the leisure budget and labour supply (A2.2, the Try-it boxes)

This is the page that shows answers, so it is released once the problem set's
solutions are out. The maths is consumer_theory.py, which reproduces every
number in the session 2 solutions; this file only arranges and draws it.
"""

import numpy as np

import consumer_theory as ct
from sandbox import (Lab, BEFORE, CURVE, DIRECT, INK, LINE, MUTE, legend, num,
                     pct, style_axes, table)

FAMILIES = ["Cobb-Douglas", "Log", "Perfect substitutes", "Perfect complements",
            "Quasilinear"]
# Not in the course notes. Session 3's sandbox offers it so the labour supply
# curve can bend backward, and the name says so wherever it appears.
CES_NAME = "CES (beyond the notes)"

FORMULAS = {
    "Cobb-Douglas": "U = %s<sup>&alpha;</sup> %s<sup>&beta;</sup>",
    "Log": "U = &alpha; ln %s + &beta; ln %s",
    "Perfect substitutes": "U = &alpha;%s + &beta;%s",
    "Perfect complements": "U = min{&alpha;%s, &beta;%s}",
    "Quasilinear": "U = &alpha; ln %s + %s",
    CES_NAME: "U = (&alpha;%s<sup>&rho;</sup> + &beta;%s<sup>&rho;</sup>)<sup>1/&rho;</sup>",
}


def make_utility(family, a, b, s=0.5):
    # s is CES's elasticity of substitution; every other family ignores it.
    if family == CES_NAME:
        return ct.CES(a, b, s)
    if family == "Log":
        return ct.LogUtility(a, b)
    if family == "Perfect substitutes":
        return ct.PerfectSubstitutes(a, b)
    if family == "Perfect complements":
        return ct.PerfectComplements(a, b)
    if family == "Quasilinear":
        return ct.Quasilinear(a, "log")          # beta unused, so locked
    return ct.CobbDouglas(a, b)


def preferences_text(v, names):
    f = FORMULAS[v["family"]] % names
    if v["family"] == "Quasilinear":
        return "%s with &alpha; = %s" % (f, num(v["a"]))
    if v["family"] == CES_NAME:
        return ("%s with &alpha; = %s, &beta; = %s and elasticity of substitution "
                "&sigma; = %s (&rho; = (&sigma; &minus; 1)/&sigma;)"
                % (f, num(v["a"]), num(v["b"]), num(v["s"])))
    return "%s with &alpha; = %s, &beta; = %s" % (f, num(v["a"]), num(v["b"]))


def choice_text(ch, budget, required):
    # Says which rule picked the bundle: the tangency, or a corner or kink
    # where the tangency rule fails. "required" names the price ratio.
    n1, n2 = budget.names
    if ch.tied:
        return "Tied: |MRS| = %s, so every bundle on the line is equally good." % required
    if ch.kind == "interior" and ch.mrs is not None:
        return "Tangency: |MRS| = %s = %s." % (num(ch.mrs), required)
    if ch.kind == "kink":
        return ("Kink: the optimum sits where the L bends. The MRS is not "
                "defined there, so tangency cannot pick it.")
    cap = budget.x1_cap
    if cap is not None and ch.x1 >= cap - 1e-9:
        where = "%s = %s, so no time is sold" % (n1, num(cap))
    elif ch.x1 <= 1e-9:
        where = "everything on %s" % n2
    else:
        where = "everything on %s" % n1
    tail = ""
    if ch.mrs is not None:
        tail = " |MRS| = %s does not equal %s, and it doesn't have to at a corner." % (
            num(ch.mrs), required)
    return "Corner: %s.%s" % (where, tail)


def greek(widgets):
    # Greek letters need HTML in a slider description. ipywidgets 8 has a flag
    # for it; older versions (Colab may still ship 7) would show "&alpha;" as
    # text, so fall back to plain letters there.
    for key in ("a", "b", "s"):
        if key not in widgets:
            continue
        w = widgets[key]
        if hasattr(w, "description_allow_html"):
            w.description_allow_html = True
        else:
            w.description = (w.description.replace("&alpha;", "alpha")
                             .replace("&beta;", "beta").replace("&sigma;", "sigma"))


# ---------------------------------------------------------------- drawing ---

def _line(ax, budget, **kw):
    # From the vertical intercept to the far end, which is the horizontal
    # intercept or, for leisure, the endowment at L = T.
    x_end = budget.max_x1
    ax.plot([0, x_end], [budget.max_x2, float(budget.x2_at(x_end))], **kw)


def _curve(ax, u, level, xmax, **kw):
    xs, ys = u.indifference_curve(level, xmax * 0.004, xmax, 400)
    ax.plot(xs, ys, **kw)


def _neighbours(u, ch):
    # Two more curves, found by scaling the bundle along a ray. Works for
    # every family, unlike scaling the utility number.
    if ch.x1 <= 1e-9 and ch.x2 <= 1e-9:
        return []
    return [float(u.u(ch.x1 * s, ch.x2 * s)) for s in (0.72, 1.3)]


def draw_choice(ax, live, before, direct, xmax, ymax, direct_label=None):
    b, u, ch = live
    n1, n2 = b.names
    style_axes(ax)
    leisure = b.x1_cap is not None

    xs = np.linspace(0, b.max_x1, 200)
    ax.fill_between(xs, 0, b.x2_at(xs), color=LINE, alpha=0.07, lw=0)

    # The frozen "before": solid grey, so the live line can be dashed, as the
    # problem set asks ("a dashed line for the new one").
    if before is not None:
        b0, u0, c0 = before
        _line(ax, b0, color=BEFORE, lw=1.8, label="before, slope %s" % num(b0.slope))
        _curve(ax, u0, c0.utility, xmax, color=BEFORE, lw=1, ls=":")
        ax.plot([c0.x1], [c0.x2], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8, zorder=6)

    for level in _neighbours(u, ch):
        _curve(ax, u, level, xmax, color=CURVE, lw=0.9, ls=":", alpha=0.45)
    _curve(ax, u, ch.utility, xmax, color=CURVE, lw=2, label="indifference curve")
    _line(ax, b, color=LINE, lw=2.2, ls="--" if before is not None else "-",
          label="%sbudget, slope %s" % ("new " if before is not None else "", num(b.slope)))

    if direct is not None:
        bd, cd, revenue = direct
        _line(ax, bd, color=DIRECT, lw=1.8, ls=":",
              label=direct_label or "direct charge of %s, old prices" % num(revenue))
        _curve(ax, u, cd.utility, xmax, color=DIRECT, lw=1, alpha=0.6)
        ax.plot([cd.x1], [cd.x2], "o", color=DIRECT, ms=7, zorder=7)

    # Intercepts and the endowment, with their values: this page shows numbers.
    ax.annotate(num(b.max_x2), (0, b.max_x2), textcoords="offset points",
                xytext=(6, 4), color=LINE, fontsize=9)
    if leisure:
        ax.plot([b.e1], [b.e2], "s", color=LINE, ms=7, zorder=6)
        ax.annotate("E = (%s, %s)" % (num(b.e1), num(b.e2)), (b.e1, b.e2),
                    textcoords="offset points", xytext=(8, 0), color=LINE, fontsize=9,
                    va="center")
    else:
        ax.annotate(num(b.max_x1), (b.max_x1, 0), textcoords="offset points",
                    xytext=(0, 6), ha="center", color=LINE, fontsize=9)

    # The optimum, with guides to both axes.
    ax.plot([ch.x1, ch.x1], [0, ch.x2], color=CURVE, lw=0.8, ls="--", alpha=0.6)
    ax.plot([0, ch.x1], [ch.x2, ch.x2], color=CURVE, lw=0.8, ls="--", alpha=0.6)
    ax.plot([ch.x1], [ch.x2], "o", color=CURVE, ms=8, zorder=7)
    right = ch.x1 < 0.6 * xmax
    ax.annotate("(%s, %s)" % (num(ch.x1), num(ch.x2)), (ch.x1, ch.x2),
                textcoords="offset points", xytext=(9 if right else -9, 7),
                ha="left" if right else "right", color=INK, fontsize=9.5)

    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xlabel(n1, color=INK, loc="right")
    ax.set_ylabel(n2, color=INK, loc="top")
    legend(ax)


def draw_mrs(ax, live, required):
    # Willing vs required, the notes' sentence as a picture: the optimum is
    # where the curve crosses the flat line.
    b, u, ch = live
    style_axes(ax)
    ratio = b.price_ratio
    hi = b.max_x1
    if isinstance(u, ct.PerfectComplements):
        ax.text(0.5, 0.8, "Complements: the MRS jumps from infinite to zero at the "
                "kink,\nso there is no crossing to find.", transform=ax.transAxes,
                ha="center", va="center", color=MUTE, fontsize=8.5)
        mrs = np.array([np.nan])
    else:
        xs = np.linspace(hi * 0.01, hi * 0.99, 300)
        with np.errstate(all="ignore"):
            mrs = np.abs(np.asarray(u.mrs(xs, b.x2_at(xs)), dtype=float))
        mrs = np.where(np.isfinite(mrs), mrs, np.nan)
        ax.plot(xs, mrs, color=CURVE, lw=1.8, label="|MRS| along the line (willing)")
    ax.axhline(ratio, color=LINE, lw=1.8, label="%s (required)" % required)
    if ch.kind == "interior" and not ch.tied:
        ax.plot([ch.x1], [ratio], "o", color=CURVE, ms=6, zorder=5)
    # Frame the crossing, not the spike: the MRS shoots up near the axis and
    # would otherwise flatten the one place where the panel says something.
    ax.set_ylim(0, ratio * 3)
    ax.set_xlim(0, hi)
    ax.set_xlabel(b.names[0], color=INK, loc="right")
    ax.set_title("Willing vs required", loc="left", color=INK, fontsize=9.5)
    legend(ax)


# ================================================================== goods ===

SONDRE = dict(family="Cobb-Douglas", p1=3.0, p2=1.0, m=90.0, a=2 / 3, b=1 / 3)


class GoodsLab(Lab):
    TITLE = "Lab 1 &middot; Budget, preferences and choice"
    INTRO = ("Two goods, a budget and a taste. Move a price or income and watch "
             "the line pivot or shift; change the preferences and watch the "
             "optimum move. Freeze a 'before' to compare two situations, as the "
             "problem set's diagrams do.")
    FAMILIES = FAMILIES
    SLIDERS = [
        ("p1", 0.5, 20.0, 0.5, 3.0, ".2f"),
        ("p2", 0.5, 20.0, 0.5, 1.0, ".2f"),
        ("m", 10.0, 1000.0, 1.0, 90.0, ".0f"),
        ("a", 0.05, 3.0, 0.01, 2 / 3, ".2f"),
        ("b", 0.05, 3.0, 0.01, 1 / 3, ".2f"),
    ]
    CHECKS = [("direct", "Add a direct charge raising the same money")]
    PRESETS = [
        dict(label="A2.1 Sondre", kind="problem", names=("h", "c"), values=SONDRE),
        dict(label="A2.1 (e) levy", kind="problem", names=("h", "c"),
             before=SONDRE, values=dict(SONDRE, p1=6.0)),
        dict(label="A2.1 (g) levy vs charge", kind="problem", names=("h", "c"),
             before=SONDRE, values=dict(SONDRE, p1=6.0), flags={"direct": True}),
        # The notes put good 2 across and good 1 up: P2 = 4 is the horizontal price.
        dict(label="Notes p. 2 Try it", kind="notes", names=("C2", "C1"),
             values=dict(family="Cobb-Douglas", p1=4.0, p2=2.0, m=100.0, a=1.0, b=1.0)),
        dict(label="Notes p. 14 review Q6", kind="notes", names=("x1", "x2"),
             values=dict(family="Cobb-Douglas", p1=2.0, p2=3.0, m=18.0, a=1 / 3, b=2 / 3)),
    ]

    def __init__(self):
        super().__init__()
        self.names = ("h", "c")              # Sondre's axes until a preset says otherwise

    def on_preset(self, preset):
        self.names = preset.get("names", self.names)

    def relabel(self):
        n1, n2 = self.names
        self.w["p1"].description = "Price of %s" % n1
        self.w["p2"].description = "Price of %s" % n2
        self.w["m"].description = "Income m"
        self.w["a"].description = "&alpha;, weight on %s" % n1
        quasi = self.w["family"].value == "Quasilinear"
        self.w["b"].description = "&beta; (not used)" if quasi else "&beta;, weight on %s" % n2
        self.w["b"].disabled = quasi
        self.checks["direct"].disabled = not self.compare.value
        greek(self.w)

    def model(self, v):
        b = ct.Budget.goods(v["p1"], v["p2"], v["m"], names=self.names)
        u = make_utility(v["family"], v["a"], v["b"])
        return b, u, u.demand(b)

    def compute(self):
        live = self.model(self.values())
        before = self.model(self.before) if self.before else None
        direct = None
        if before is not None and self.flag("direct"):
            # A2.1 (g): what the price change raised, taken as a lump sum at
            # the old prices instead.
            b, u, ch = live
            b0 = before[0]
            revenue = (b.p1 - b0.p1) * ch.x1 + (b.p2 - b0.p2) * ch.x2
            if revenue > 1e-9:
                bd = ct.Budget.goods(b0.p1, b0.p2, b.m - revenue, names=self.names)
                direct = (bd, u.demand(bd), revenue)
        budgets = [live[0]] + [x[0] for x in (before, direct) if x is not None]
        xmax = self.stick("x", max(bb.max_x1 for bb in budgets))
        ymax = self.stick("y", max(bb.max_x2 for bb in budgets))
        return dict(v=self.values(), live=live, before=before, direct=direct,
                    xmax=xmax, ymax=ymax)

    def required(self):
        n1, n2 = self.names
        return "p<sub>%s</sub>/p<sub>%s</sub>" % (n1, n2)

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.25], hspace=0.32)
        draw_choice(fig.add_subplot(gs[0]), st["live"], st["before"], st["direct"],
                    st["xmax"], st["ymax"])
        n1, n2 = self.names
        draw_mrs(fig.add_subplot(gs[1]), st["live"],
                 "$p_{%s}/p_{%s}$ = %s" % (n1, n2, num(st["live"][0].price_ratio)))
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.07)

    def describe(self, st):
        b, u, ch = st["live"]
        n1, n2 = b.names
        req = "%s = %s" % (self.required(), num(b.price_ratio))
        rows = [
            ("Preferences", preferences_text(st["v"], self.names)),
            ("Budget", "%s&middot;%s + %s&middot;%s = %s. Intercepts %s = %s and "
                       "%s = %s. Slope %s: one more %s costs %s %s."
             % (num(b.p1), n1, num(b.p2), n2, num(b.m), n1, num(b.max_x1), n2,
                num(b.max_x2), num(b.slope), n1, num(-b.slope), n2)),
            ("Choice", "%s* = %s, %s* = %s. %s" % (n1, num(ch.x1), n2, num(ch.x2),
                                                 choice_text(ch, b, req))),
            ("Spending", "%s of income on %s, %s on %s."
             % (pct(ch.shares[0]), n1, pct(ch.shares[1]), n2)),
        ]
        if st["before"] is not None:
            c0 = st["before"][2]
            rows.append(("Before &rarr; after", "%s* %s &rarr; %s, &nbsp; %s* %s &rarr; %s"
                         % (n1, num(c0.x1), num(ch.x1), n2, num(c0.x2), num(ch.x2))))
        if st["direct"] is not None:
            bd, cd, revenue = st["direct"]
            better = ("better" if cd.utility > ch.utility + 1e-9 else
                      "worse" if cd.utility < ch.utility - 1e-9 else "equally good")
            rows.append(("Direct charge",
                         "The price change raises %s. Taking %s directly at the old "
                         "prices gives (%s, %s) and U = %s, against U = %s with the "
                         "price change: the direct charge is %s."
                         % (num(revenue), num(revenue), num(cd.x1), num(cd.x2),
                            num(cd.utility, 3), num(ch.utility, 3), better)))
        elif self.flag("direct"):
            rows.append(("Direct charge", "Raise a price after freezing a 'before' to "
                                          "see the comparison."))
        return table(rows)


# ================================================================ leisure ===

KARI = dict(family="Cobb-Douglas", w=25.0, V=600.0, T=120.0, t=0.0, a=1.0, b=1.0)
W_MAX = 60.0               # the wage slider's top, and the supply panel's frame


class LeisureLab(Lab):
    TITLE = "Lab 2 &middot; The leisure budget and labour supply"
    INTRO = ("Time is the scarce good and the wage is its price. Move the wage, "
             "the transfer or the tax and watch the line pivot around the "
             "endowment E, or move with it. The lower panel solves the same "
             "problem at every wage: that is the labour supply curve.")
    FAMILIES = FAMILIES
    SLIDERS = [
        ("w", 1.0, W_MAX, 0.5, 25.0, ".2f"),
        ("V", 0.0, 2000.0, 10.0, 600.0, ".0f"),
        ("T", 8.0, 168.0, 1.0, 120.0, ".0f"),
        ("t", 0.0, 0.9, 0.05, 0.0, ".2f"),
        ("a", 0.05, 3.0, 0.01, 1.0, ".2f"),
        ("b", 0.05, 3.0, 0.01, 1.0, ".2f"),
    ]
    PRESETS = [
        dict(label="A2.2 Kari", kind="problem", values=KARI),
        dict(label="A2.2 (c) 40% tax", kind="problem", before=KARI,
             values=dict(KARI, t=0.4)),
        dict(label="Notes p. 5 Try it", kind="notes",
             values=dict(KARI, w=20.0, V=100.0, T=16.0)),
        dict(label="Notes p. 14 review Q2", kind="notes",
             values=dict(KARI, w=15.0, V=60.0, T=12.0)),
    ]

    def relabel(self):
        self.w["w"].description = "Wage w"
        self.w["V"].description = "Transfer V"
        self.w["T"].description = "Hours T"
        self.w["t"].description = "Labour tax t"
        self.w["a"].description = "&alpha;, weight on L"
        quasi = self.w["family"].value == "Quasilinear"
        self.w["b"].description = "&beta; (not used)" if quasi else "&beta;, weight on C"
        self.w["b"].disabled = quasi
        greek(self.w)

    def model(self, v):
        b = ct.Budget.leisure(w=v["w"] * (1 - v["t"]), V=v["V"], T=v["T"])
        u = make_utility(v["family"], v["a"], v["b"])
        return b, u, u.demand(b)

    def compute(self):
        v = self.values()
        live = self.model(v)
        before = self.model(self.before) if self.before else None
        Ts = [v["T"]] + ([self.before["T"]] if self.before else [])
        tops = [live[0].max_x2] + ([before[0].max_x2] if before else [])
        return dict(v=v, live=live, before=before,
                    xmax=max(Ts) * 1.35,              # room right of E for its label
                    ymax=self.stick("y", max(tops)))

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.6], hspace=0.32)
        draw_choice(fig.add_subplot(gs[0]), st["live"], st["before"], None,
                    st["xmax"], st["ymax"])
        self.draw_supply(fig.add_subplot(gs[1]), st)
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.07)

    @staticmethod
    def supply(v):
        # Hours worked at every gross wage, with this tax, transfer and taste.
        u = make_utility(v["family"], v["a"], v["b"])
        ws = np.linspace(0.25, W_MAX, 160)
        hours = [max(0.0, v["T"] - u.demand(ct.Budget.leisure(
                     w=w * (1 - v["t"]), V=v["V"], T=v["T"])).x1) for w in ws]
        return ws, np.array(hours)

    def draw_supply(self, ax, st):
        v = st["v"]
        style_axes(ax)
        if self.before:
            ws, hs = self.supply(self.before)
            ax.plot(hs, ws, color=BEFORE, lw=1.6, label="before")
        ws, hs = self.supply(v)
        ax.plot(hs, ws, color=CURVE, lw=2, label="hours at each wage")
        ch = st["live"][2]
        ax.plot([v["T"] - ch.x1], [v["w"]], "o", color=LINE, ms=7, zorder=5)
        wr = self.reservation(st)
        if wr is not None and wr < W_MAX:
            ax.axhline(wr, color=MUTE, lw=1, ls=":")
            label = "reservation wage %s" % num(wr)
            if v["t"] > 0:
                label = "gross wage needed to start: %s" % num(wr)
            ax.annotate(label, (0.98, wr),
                        xycoords=("axes fraction", "data"), textcoords="offset points",
                        xytext=(0, 4), ha="right", color=MUTE, fontsize=8.5)
        Tmax = max([v["T"]] + ([self.before["T"]] if self.before else []))
        ax.set_xlim(0, Tmax)
        ax.set_ylim(0, W_MAX)
        ax.set_xlabel("hours worked  h = T - L",
                      color=INK, loc="right")
        ax.set_ylabel("gross wage w", color=INK, loc="top")
        ax.set_title("Labour supply", loc="left", color=INK, fontsize=9.5)
        legend(ax, loc="upper right")

    def reservation(self, st):
        # The gross wage at which working starts: the MRS at E, grossed up by
        # the tax. None when the MRS at E is not a number (complements).
        v = st["v"]
        u = st["live"][1]
        try:
            net = ct.reservation_wage(u, v["V"], v["T"])
        except Exception:
            return None
        if not np.isfinite(net) or v["t"] >= 1:
            return None
        return net / (1 - v["t"])

    def describe(self, st):
        v = st["v"]
        b, u, ch = st["live"]
        wn = v["w"] * (1 - v["t"])
        h = v["T"] - ch.x1
        wage = "net wage (1 &minus; t)w = %s" % num(wn) if v["t"] > 0 else "wage %s" % num(wn)
        rows = [
            ("Preferences", preferences_text(v, ("L", "C"))),
            ("Budget", "C = %s&middot;(%s &minus; L) + %s, with %s. Full income %s; "
                       "endowment E = (%s, %s). Slope %s: an hour of leisure costs "
                       "%s of consumption."
             % (num(wn), num(v["T"]), num(v["V"]), wage, num(b.max_x2), num(v["T"]),
                num(v["V"]), num(b.slope), num(wn))),
            ("Choice", "L* = %s, hours h* = %s, C* = %s. %s"
             % (num(ch.x1), num(h), num(ch.x2), choice_text(ch, b, "the net wage %s" % num(wn)))),
        ]
        wr = self.reservation(st)
        if wr is not None:
            # Lead with the net figure: it is what A2.2 (d) asks for, and it
            # does not depend on the tax. The gross figure is what the lower
            # panel's wage axis shows, so mention it when a tax is on.
            net = wr * (1 - v["t"])
            works = h > 1e-9
            gross = ("" if v["t"] <= 0 else
                     " With the tax, that takes a gross wage of %s." % num(wr))
            rows.append(("Reservation wage",
                         "%s, the MRS at E: what an hour must pay her to start "
                         "working.%s Her net wage is %s, so she %s."
                         % (num(net), gross, num(wn),
                            "works" if works else "does not work")))
        if st["before"] is not None:
            c0 = st["before"][2]
            h0 = self.before["T"] - c0.x1
            rows.append(("Before &rarr; after", "L* %s &rarr; %s, &nbsp; h* %s &rarr; %s, "
                                                "&nbsp; C* %s &rarr; %s"
                         % (num(c0.x1), num(ch.x1), num(h0), num(h), num(c0.x2),
                            num(ch.x2))))
        return table(rows)


goods = GoodsLab()
leisure = LeisureLab()
