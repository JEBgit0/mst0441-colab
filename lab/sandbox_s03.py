"""
sandbox_s03.py - session 3 sandbox: comparative statics, everything visible.

    demand   Lab 1  demand and Engel curves, and what kind of good this is
    effects  Lab 2  a tariff split into substitution and income effects,
                    and the deadweight loss against a lump-sum tax
    labour   Lab 3  labour supply: the windfall, a wage change decomposed,
                    and (beyond the notes) a backward-bending curve

Released with the session 3 solutions. The maths is consumer_theory.py; the
drawing pieces are shared with sandbox_s02.py.
"""

import numpy as np

import consumer_theory as ct
from sandbox import (Lab, BEFORE, CURVE, DIRECT, INK, LINE, MUTE, NEW, legend, num,
                     pct, style_axes, table)
from sandbox_s02 import (CES_NAME, FAMILIES as COURSE_FAMILIES, choice_text,
                         draw_choice, greek, make_utility, preferences_text)

FAMILIES = COURSE_FAMILIES + [CES_NAME]
# Families with a smooth tangency, where splitting a price change into
# substitution and income effects is well defined.
SMOOTH = {"Cobb-Douglas", "Log", "Quasilinear", CES_NAME}

PREF_SLIDERS = [
    ("a", 0.05, 3.0, 0.01, 1.0, ".2f"),
    ("b", 0.05, 3.0, 0.01, 1.0, ".2f"),
    ("s", 0.1, 3.0, 0.05, 0.5, ".2f"),
]


def relabel_prefs(w, n1="x1", n2="x2"):
    # Only the sliders a family actually reads stay live.
    family = w["family"].value
    w["a"].description = "&alpha;, weight on %s" % n1
    quasi = family == "Quasilinear"
    w["b"].description = "&beta; (not used)" if quasi else "&beta;, weight on %s" % n2
    w["b"].disabled = quasi
    ces = family == CES_NAME
    w["s"].description = "&sigma;, substitution" if ces else "&sigma; (CES only)"
    w["s"].disabled = not ces
    greek(w)


def utility(v):
    return make_utility(v["family"], v["a"], v["b"], v.get("s", 0.5))


def bars(ax, groups, title):
    # The decomposition as bars: substitution, income and their sum, per good.
    style_axes(ax)
    labels = ["substitution", "income", "total"]
    width = 0.8 / max(len(groups), 1)
    colours = [LINE, CURVE]
    for i, (name, vals) in enumerate(groups):
        xs = np.arange(3) + (i - (len(groups) - 1) / 2) * width
        ax.bar(xs, vals, width=width * 0.92, color=colours[i % 2], alpha=0.85, label=name)
        for x, val in zip(xs, vals):
            ax.annotate(num(val), (x, val), textcoords="offset points",
                        xytext=(0, 3 if val >= 0 else -11), ha="center",
                        color=INK, fontsize=8)
    ax.axhline(0, color=MUTE, lw=0.8)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    lo, hi = ax.get_ylim()
    pad = 0.15 * max(hi - lo, 1e-9)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    legend(ax, loc="best")


# ======================================================================
# Lab 1: demand and Engel curves
# ======================================================================

def demand_formula(family):
    return {
        "Cobb-Douglas": "x<sub>1</sub>* = &alpha;/(&alpha; + &beta;) &middot; m/p<sub>1</sub>",
        "Log": "x<sub>1</sub>* = &alpha;/(&alpha; + &beta;) &middot; m/p<sub>1</sub>",
        "Quasilinear": "x<sub>1</sub>* = &alpha;p<sub>2</sub>/p<sub>1</sub> while "
                       "m &ge; &alpha;p<sub>2</sub>, otherwise m/p<sub>1</sub>",
        "Perfect substitutes": "x<sub>1</sub>* = m/p<sub>1</sub> if &alpha;/p<sub>1</sub> "
                               "&gt; &beta;/p<sub>2</sub>, otherwise 0",
        "Perfect complements": "x<sub>1</sub>* = &beta;m/(&beta;p<sub>1</sub> + "
                               "&alpha;p<sub>2</sub>)",
        CES_NAME: "x<sub>1</sub>* = m / (p<sub>1</sub> + p<sub>2</sub>(&beta;p<sub>1</sub>"
                  "/&alpha;p<sub>2</sub>)<sup>&sigma;</sup>)",
    }[family]


WORKHORSE = dict(family="Log", p1=3.0, p2=2.0, m=300.0, a=2.0, b=3.0, s=0.5)
P_MAX, M_MAX = 20.0, 1000.0


class DemandLab(Lab):
    TITLE = "Lab 1 &middot; Demand and Engel curves"
    INTRO = ("Move p<sub>1</sub> and the bundle traces the price offer curve; the "
             "lower left panel keeps only (x<sub>1</sub>, p<sub>1</sub>): the demand "
             "curve. Move m and it traces the income expansion path; the lower "
             "right panel is the Engel curve. The readout classifies the good.")
    FAMILIES = FAMILIES
    SLIDERS = [
        ("p1", 0.5, P_MAX, 0.5, 3.0, ".2f"),
        ("p2", 0.5, P_MAX, 0.5, 2.0, ".2f"),
        ("m", 1.0, M_MAX, 1.0, 300.0, ".0f"),
    ] + PREF_SLIDERS
    CHECKS = [("offer", "Show the price offer curve"),
              ("path", "Show the income expansion path")]
    FIGSIZE = (6.6, 7.4)
    PRESETS = [
        dict(label="Notes p. 1 workhorse", kind="notes", values=WORKHORSE),
        dict(label="Notes p. 17 worksheet", kind="notes",
             values=dict(WORKHORSE, a=1.0, b=1.0, m=120.0, p1=6.0)),
        dict(label="Notes p. 17 review Q1", kind="notes",
             values=dict(WORKHORSE, a=3.0, b=1.0, m=160.0, p1=4.0, p2=2.0)),
        dict(label="A3.1 interior", kind="problem",
             values=dict(WORKHORSE, family="Quasilinear", a=1.0, p1=2.0, p2=4.0, m=20.0)),
        dict(label="A3.1 corner (m < p2)", kind="problem",
             values=dict(WORKHORSE, family="Quasilinear", a=1.0, p1=2.0, p2=4.0, m=3.0)),
        dict(label="A3.2 p1 < p2", kind="problem",
             values=dict(WORKHORSE, family="Perfect substitutes", a=1.0, b=1.0,
                         p1=10.0, p2=15.0, m=60.0)),
        dict(label="A3.2 p1 > p2", kind="problem",
             values=dict(WORKHORSE, family="Perfect substitutes", a=1.0, b=1.0,
                         p1=20.0, p2=15.0, m=60.0)),
        dict(label="CES, sigma 0.5", kind="extra",
             values=dict(WORKHORSE, family=CES_NAME, a=1.0, b=1.0, s=0.5)),
    ]

    def relabel(self):
        self.w["p1"].description = "Price p1"
        self.w["p2"].description = "Price p2"
        self.w["m"].description = "Income m"
        relabel_prefs(self.w)

    @staticmethod
    def choose(v, **change):
        vv = dict(v, **change)
        b = ct.Budget.goods(vv["p1"], vv["p2"], vv["m"], names=("x1", "x2"))
        return b, utility(vv), utility(vv).demand(b)

    def compute(self):
        v = self.values()
        live = self.choose(v)
        ps = np.linspace(0.5, P_MAX, 120)
        ms = np.linspace(1.0, M_MAX, 120)
        by_p = [self.choose(v, p1=p)[2] for p in ps]
        by_m = [self.choose(v, m=m)[2] for m in ms]
        b = live[0]
        return dict(v=v, live=live, ps=ps, ms=ms, by_p=by_p, by_m=by_m,
                    xmax=self.stick("x", b.max_x1), ymax=self.stick("y", b.max_x2))

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 2, height_ratios=[3, 2], hspace=0.38, wspace=0.28)
        ax = fig.add_subplot(gs[0, :])
        draw_choice(ax, st["live"], None, None, st["xmax"], st["ymax"])
        if self.flag("offer"):
            ax.plot([c.x1 for c in st["by_p"]], [c.x2 for c in st["by_p"]], color=NEW,
                    lw=1.4, ls="-.", label="price offer curve")
        if self.flag("path"):
            ax.plot([c.x1 for c in st["by_m"]], [c.x2 for c in st["by_m"]], color=DIRECT,
                    lw=1.4, ls="-.", label="income expansion path")
        if self.flag("offer") or self.flag("path"):
            legend(ax)
        v, ch = st["v"], st["live"][2]

        dm = fig.add_subplot(gs[1, 0])
        style_axes(dm)
        dm.plot([c.x1 for c in st["by_p"]], st["ps"], color=CURVE, lw=1.8)
        dm.plot([ch.x1], [v["p1"]], "o", color=LINE, ms=7, zorder=5)
        dm.set_xlim(0, st["xmax"])
        dm.set_ylim(0, P_MAX)
        dm.set_xlabel("x1", color=INK, loc="right")
        dm.set_ylabel("p1", color=INK, loc="top")
        dm.set_title("Demand curve", loc="left", color=INK, fontsize=9.5)

        en = fig.add_subplot(gs[1, 1])
        style_axes(en)
        en.plot([c.x1 for c in st["by_m"]], st["ms"], color=CURVE, lw=1.8)
        en.plot([ch.x1], [v["m"]], "o", color=LINE, ms=7, zorder=5)
        en.set_xlim(0, st["xmax"])
        en.set_ylim(0, M_MAX)
        en.set_xlabel("x1", color=INK, loc="right")
        en.set_ylabel("income m", color=INK, loc="top")
        en.set_title("Engel curve", loc="left", color=INK, fontsize=9.5)
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.06)

    def elasticity(self, v, key):
        # d ln x1 / d ln(key), by a symmetric 1% step. None where x1 is zero.
        x0 = self.choose(v)[2].x1
        if x0 <= 1e-9:
            return None
        h = 0.01
        up = self.choose(v, **{key: v[key] * (1 + h)})[2].x1
        dn = self.choose(v, **{key: v[key] * (1 - h)})[2].x1
        if up <= 0 or dn <= 0:
            return None
        return (np.log(up) - np.log(dn)) / (np.log(1 + h) - np.log(1 - h))

    def describe(self, st):
        v = st["v"]
        b, u, ch = st["live"]
        req = "p<sub>1</sub>/p<sub>2</sub> = %s" % num(b.price_ratio)
        rows = [
            ("Preferences", preferences_text(v, ("x<sub>1</sub>", "x<sub>2</sub>"))),
            ("Demand", "%s, so here x<sub>1</sub>* = %s and x<sub>2</sub>* = %s. %s"
             % (demand_formula(v["family"]), num(ch.x1), num(ch.x2),
                choice_text(ch, b, req))),
            ("Spending", "%s of income on good 1, %s on good 2."
             % (pct(ch.shares[0]), pct(ch.shares[1]))),
        ]
        eta = self.elasticity(v, "m")
        eps = self.elasticity(v, "p1")
        if eta is None:
            rows.append(("Good 1", "Not bought at these prices, so its income and "
                                   "price responses are zero: neither normal nor inferior."))
        else:
            if abs(eta) < 0.02:
                kind = "does not respond to income (as quasilinear demand promises)"
            elif eta < 0:
                kind = "inferior"
            elif abs(eta - 1) < 0.02:
                kind = "normal, and its budget share holds still as income changes"
                if v["family"] in ("Cobb-Douglas", "Log"):
                    kind += " (homothetic preferences)"
            elif eta > 1:
                kind = "normal and a luxury: its budget share grows with income"
            else:
                kind = "normal and a necessity: its budget share shrinks with income"
            own = "ordinary" if eps < 0 else "Giffen"
            rows.append(("Good 1", "Income elasticity &eta; = %s: %s. Own-price "
                                   "elasticity %s: %s."
                         % (num(eta), kind, num(eps), own)))
        cross_up = self.choose(v, p2=v["p2"] * 1.01)[2].x1 - ch.x1
        if v["family"] == "Perfect substitutes":
            # A3.2 (5): locally flat, but demand jumps when p2 crosses the
            # switch point, and the jump is up.
            cross = ("a small change in p<sub>2</sub> does nothing, but once good 2 "
                     "is the dearer one per unit of utility, x<sub>1</sub> jumps from "
                     "0 to m/p<sub>1</sub>: substitutes")
        elif abs(cross_up) < 1e-6:
            cross = "x<sub>1</sub> ignores p<sub>2</sub>: neither substitutes nor complements"
        elif cross_up > 0:
            cross = "a dearer good 2 raises x<sub>1</sub>: substitutes"
        else:
            cross = "a dearer good 2 lowers x<sub>1</sub>: complements"
        rows.append(("Cross-price", "%s (the sign of dx<sub>1</sub>/dp<sub>2</sub>)." % cross))
        return table(rows)


# ======================================================================
# Lab 2: substitution and income effects
# ======================================================================

TARIFF_NOTES = dict(family="Log", p1=3.0, p2=2.0, m=300.0, tau=0.5, a=2.0, b=3.0, s=0.5,
                    good="good 2")


class EffectsLab(Lab):
    TITLE = "Lab 2 &middot; Substitution and income effects"
    INTRO = ("A tariff raises one price. A &rarr; B slides along the original "
             "indifference curve to the new relative price (substitution); B &rarr; C "
             "is the lost purchasing power (income). Compare a lump-sum tax that "
             "raises the same money to see the deadweight loss.")
    FAMILIES = FAMILIES
    WORD = "Tariff"           # session 4 reuses this lab for an ad valorem tax
    DROPDOWNS = [("good", "Tariff on", ["good 2", "good 1"])]
    SLIDERS = [
        ("p1", 0.5, P_MAX, 0.5, 3.0, ".2f"),
        ("p2", 0.5, P_MAX, 0.5, 2.0, ".2f"),
        ("m", 1.0, M_MAX, 1.0, 300.0, ".0f"),
        ("tau", 0.0, 2.0, 0.05, 0.5, ".2f"),
    ] + PREF_SLIDERS
    CHECKS = [("lump", "Compare a lump-sum tax raising the same revenue")]
    FIGSIZE = (6.6, 7.0)
    PRESETS = [
        dict(label="Notes p. 9 tariff", kind="notes", values=TARIFF_NOTES,
             flags={"lump": True}),
        dict(label="Notes p. 18 review Q4", kind="notes",
             values=dict(TARIFF_NOTES, a=1.0, b=1.0, m=80.0, p1=1.0, p2=2.0, tau=1.0),
             flags={"lump": True}),
        dict(label="CES, sigma 0.5", kind="extra",
             values=dict(TARIFF_NOTES, family=CES_NAME, a=1.0, b=1.0, s=0.5),
             flags={"lump": True}),
    ]

    def relabel(self):
        self.w["p1"].description = "Price p1"
        self.w["p2"].description = "Price p2"
        self.w["m"].description = "Income m"
        self.w["tau"].description = "%s rate (tau)" % self.WORD
        self.w["good"].description = "%s on" % self.WORD
        relabel_prefs(self.w)
        # The before/after freeze is built in here: the "before" is always the
        # untaxed situation, so the generic compare box would only confuse.
        self.compare.layout.display = "none"

    def compute(self):
        v = self.values()
        u = utility(v)
        names = ("x1", "x2")
        b0 = ct.Budget.goods(v["p1"], v["p2"], v["m"], names=names)
        on2 = v["good"] == "good 2"
        p1t = v["p1"] * (1 if on2 else 1 + v["tau"])
        p2t = v["p2"] * (1 + v["tau"] if on2 else 1)
        b1 = ct.Budget.goods(p1t, p2t, v["m"], names=names)
        A, C = u.demand(b0), u.demand(b1)
        B = None
        if v["family"] in SMOOTH and v["tau"] > 0:
            d = ct.slutsky(u, b0, b1)
            B = d["B"]
        revenue = v["tau"] * (v["p2"] * C.x2 if on2 else v["p1"] * C.x1)
        D = bd = None
        if self.flag("lump") and revenue > 1e-9:
            bd = ct.Budget.goods(v["p1"], v["p2"], v["m"] - revenue, names=names)
            D = u.demand(bd)
        return dict(v=v, u=u, b0=b0, b1=b1, A=A, B=B, C=C, D=D, bd=bd, on2=on2,
                    revenue=revenue, xmax=self.stick("x", b0.max_x1),
                    ymax=self.stick("y", b0.max_x2))

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.4], hspace=0.3)
        ax = fig.add_subplot(gs[0])
        u = st["u"]
        direct = (st["bd"], st["D"], st["revenue"]) if st["D"] is not None else None
        draw_choice(ax, (st["b1"], u, st["C"]), (st["b0"], u, st["A"]), direct,
                    st["xmax"], st["ymax"],
                    direct_label="lump sum of %s, old prices" % num(st["revenue"]))
        if st["B"] is not None:
            bx, by = st["B"]
            b1 = st["b1"]
            income = b1.p1 * bx + b1.p2 * by
            ax.plot([0, income / b1.p1], [income / b1.p2, 0], color=MUTE, lw=1, ls="--",
                    label="new prices, old utility")
            ax.plot([bx], [by], "o", color=INK, ms=7, zorder=8)
            ax.annotate("B", (bx, by), textcoords="offset points", xytext=(7, 5),
                        color=INK, fontsize=10)
            arrow = dict(arrowstyle="-|>", color=INK, lw=1.3, shrinkA=6, shrinkB=6)
            ax.annotate("", xy=(bx, by), xytext=st["A"].bundle, arrowprops=arrow)
            ax.annotate("", xy=st["C"].bundle, xytext=(bx, by), arrowprops=arrow)
            legend(ax)
        for name, pt in (("A", st["A"].bundle), ("C", st["C"].bundle)):
            ax.annotate(name, pt, textcoords="offset points", xytext=(-12, -14),
                        color=INK, fontsize=10)

        bx_ = fig.add_subplot(gs[1])
        if st["B"] is None:
            style_axes(bx_)
            bx_.text(0.5, 0.5, "No smooth tangency for this family, so no clean split "
                     "into the two effects." if st["v"]["tau"] > 0 else
                     "Set a tariff to see the decomposition.",
                     transform=bx_.transAxes, ha="center", va="center", color=MUTE,
                     fontsize=9)
            bx_.set_xticks([])
            bx_.set_yticks([])
        else:
            A, B, C = st["A"].bundle, st["B"], st["C"].bundle
            g = [("good 1", [B[0] - A[0], C[0] - B[0], C[0] - A[0]]),
                 ("good 2", [B[1] - A[1], C[1] - B[1], C[1] - A[1]])]
            bars(bx_, g, "Change in each good:  A -> B is substitution,  B -> C is income")
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.06)

    def describe(self, st):
        v, A, C = st["v"], st["A"], st["C"]
        taxed = "good 2" if st["on2"] else "good 1"
        price = v["p2"] if st["on2"] else v["p1"]
        rows = [
            ("Preferences", preferences_text(v, ("x<sub>1</sub>", "x<sub>2</sub>"))),
            (self.WORD, "%s%% on %s: its consumer price goes from %s to %s."
             % (num(100 * v["tau"]), taxed, num(price), num(price * (1 + v["tau"])))),
            ("Bundles", ("A = (%s, %s) before, C = (%s, %s) with the " + self.WORD.lower() + ".")
             % (num(A.x1), num(A.x2), num(C.x1), num(C.x2))),
        ]
        if st["B"] is not None:
            B = st["B"]
            i = 1 if st["on2"] else 0
            sub = B[i] - A.bundle[i]
            inc = C.bundle[i] - B[i]
            rows.append(("Decomposition",
                         "B = (%s, %s). On %s: substitution %s, income %s, total %s. "
                         "%s"
                         % (num(B[0]), num(B[1]), taxed, num(sub), num(inc),
                            num(sub + inc),
                            "Both push the same way: a normal good." if sub * inc > 0
                            else "They pull apart." if sub * inc < 0 else "")))
        if st["D"] is not None:
            D = st["D"]
            rows.append(("Lump sum", ("Taking the same %s directly at the old prices "
                                     "gives D = (%s, %s) with U = %s, against U = %s "
                                     "under the " + self.WORD.lower() + ". Deadweight loss: %s utils.")
                         % (num(st["revenue"]), num(D.x1), num(D.x2),
                            num(D.utility), num(C.utility),
                            num(D.utility - C.utility))))
        rows.append(("Revenue", "&tau; &middot; price &middot; quantity at C = %s."
                     % num(st["revenue"])))
        return table(rows)


# ======================================================================
# Lab 3: labour supply
# ======================================================================

WORKED = dict(family="Log", w=20.0, V=1000.0, T=112.0, pc=10.0, t=0.0, a=1.0, b=1.0,
              s=0.5)
W_MAX = 60.0


class LabourLab(Lab):
    TITLE = "Lab 3 &middot; Labour supply"
    INTRO = ("The leisure budget from session 2, now with the session 3 questions. "
             "Freeze a 'before', change the wage, and the readout splits the change "
             "in hours into substitution and income effects. Change V instead and "
             "you see a pure income effect.")
    FAMILIES = FAMILIES
    SLIDERS = [
        ("w", 1.0, W_MAX, 0.5, 20.0, ".2f"),
        ("V", 0.0, 2000.0, 10.0, 1000.0, ".0f"),
        ("T", 8.0, 168.0, 1.0, 112.0, ".0f"),
        ("pc", 1.0, 20.0, 0.5, 10.0, ".2f"),
        ("t", 0.0, 0.9, 0.05, 0.0, ".2f"),
    ] + PREF_SLIDERS
    FIGSIZE = (6.6, 7.0)
    PRESETS = [
        dict(label="Notes p. 16 worked example", kind="notes", values=WORKED),
        dict(label="Notes p. 16 wage 20 to 40", kind="notes", before=WORKED,
             values=dict(WORKED, w=40.0)),
        dict(label="Notes p. 14 windfall", kind="notes",
             before=dict(WORKED, w=10.0, V=100.0, T=110.0, pc=1.0),
             values=dict(WORKED, w=10.0, V=200.0, T=110.0, pc=1.0)),
        dict(label="Notes p. 17 worksheet", kind="notes",
             values=dict(WORKED, w=10.0, V=60.0, T=10.0, pc=1.0)),
        dict(label="Notes p. 18 review Q6", kind="notes",
             values=dict(WORKED, w=6.0, V=48.0, T=16.0, pc=1.0)),
        dict(label="CES backward bend", kind="extra",
             values=dict(WORKED, family=CES_NAME, w=10.0, V=100.0, T=100.0, pc=1.0)),
    ]

    def relabel(self):
        self.w["w"].description = "Wage w"
        self.w["V"].description = "Non-labour income"
        self.w["T"].description = "Hours T"
        self.w["pc"].description = "Price of C"
        self.w["t"].description = "Labour tax t"
        relabel_prefs(self.w, "L", "C")

    @staticmethod
    def model(v):
        b = ct.Budget.leisure(w=v["w"] * (1 - v["t"]), V=v["V"], T=v["T"], pc=v["pc"])
        u = utility(v)
        return b, u, u.demand(b)

    @staticmethod
    def supply(v):
        u = utility(v)
        ws = np.linspace(0.25, W_MAX, 160)
        hs = [max(0.0, v["T"] - u.demand(ct.Budget.leisure(
                  w=w * (1 - v["t"]), V=v["V"], T=v["T"], pc=v["pc"])).x1) for w in ws]
        return ws, np.array(hs)

    def compute(self):
        v = self.values()
        live = self.model(v)
        before = self.model(self.before) if self.before else None
        B = None
        same_taste = before is not None and all(
            self.before[k] == v[k] for k in ("family", "a", "b", "s", "T"))
        if same_taste and v["family"] in SMOOTH:
            # Cheapest (L, C) on the old curve at the new prices: point B.
            b1, u, _ = live
            bx, by, _ = ct.expenditure(u, b1.p1, b1.p2, before[2].utility,
                                       x1_hi=v["T"] * 5)
            B = (bx, by)
        Ts = [v["T"]] + ([self.before["T"]] if self.before else [])
        # Frame the choices, not full income: at a high wage the intercept
        # towers over everything and squashes the tangency into the floor.
        # The line may run off the top; the endowment and optimum never do.
        states = [live] + ([before] if before else [])
        tops = [min(b.max_x2, max(2.2 * c.x2, 1.6 * b.e2)) for b, _, c in states]
        ws, hs = self.supply(v)
        return dict(v=v, live=live, before=before, B=B, same_taste=same_taste,
                    ws=ws, hs=hs, xmax=max(Ts) * 1.35,
                    ymax=self.stick("y", max(tops)),
                    hmax=min(max(Ts), self.stick("h", max(hs.max(), 1.0) * 1.15)))

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.7], hspace=0.32)
        ax = fig.add_subplot(gs[0])
        draw_choice(ax, st["live"], st["before"], None, st["xmax"], st["ymax"])
        if st["B"] is not None and st["before"] is not None:
            bx, by = st["B"]
            ax.plot([bx], [by], "o", color=INK, ms=7, zorder=8)
            ax.annotate("B", (bx, by), textcoords="offset points", xytext=(7, 5),
                        color=INK, fontsize=10)
            arrow = dict(arrowstyle="-|>", color=INK, lw=1.3, shrinkA=6, shrinkB=6)
            ax.annotate("", xy=(bx, by), xytext=st["before"][2].bundle, arrowprops=arrow)
            ax.annotate("", xy=st["live"][2].bundle, xytext=(bx, by), arrowprops=arrow)

        sp = fig.add_subplot(gs[1])
        style_axes(sp)
        v = st["v"]
        if self.before:
            ws, hs = self.supply(self.before)
            sp.plot(hs, ws, color=BEFORE, lw=1.6, label="before")
        sp.plot(st["hs"], st["ws"], color=CURVE, lw=2, label="hours at each wage")
        sp.plot([v["T"] - st["live"][2].x1], [v["w"]], "o", color=LINE, ms=7, zorder=5)
        sp.set_xlim(0, st["hmax"])       # the hours actually used, not all of T
        sp.set_ylim(0, W_MAX)
        sp.set_xlabel("hours worked  h = T - L", color=INK, loc="right")
        sp.set_ylabel("gross wage w", color=INK, loc="top")
        sp.set_title("Labour supply", loc="left", color=INK, fontsize=9.5)
        legend(sp, loc="upper right")
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.06)

    def describe(self, st):
        v = st["v"]
        b, u, ch = st["live"]
        wn = v["w"] * (1 - v["t"])
        h = v["T"] - ch.x1
        rows = [
            ("Preferences", preferences_text(v, ("L", "C"))),
            ("Budget", "p<sub>C</sub>&middot;C = %s&middot;(%s &minus; L) + %s. "
                       "Real wage %s baskets per hour; endowment E = (%s, %s)."
             % (num(wn), num(v["T"]), num(v["V"]), num(wn / v["pc"]), num(v["T"]),
                num(v["V"] / v["pc"]))),
            ("Choice", "L* = %s, hours h* = %s, C* = %s. %s"
             % (num(ch.x1), num(h), num(ch.x2),
                choice_text(ch, b, "the real wage %s" % num(b.price_ratio)))),
        ]
        try:
            wr = ct.reservation_wage(u, v["V"], v["T"], v["pc"])
            if np.isfinite(wr):
                rows.append(("Reservation wage", "%s (net): the MRS at E, times p<sub>C</sub>."
                             % num(wr)))
        except Exception:
            pass
        if st["before"] is not None:
            c0 = st["before"][2]
            h0 = self.before["T"] - c0.x1
            text = "h* %s &rarr; %s (%s)." % (num(h0), num(h), num(h - h0))
            if st["B"] is not None:
                sub = -(st["B"][0] - c0.x1)          # hours, not leisure
                inc = -(ch.x1 - st["B"][0])
                text += (" Substitution effect on hours %s, income effect %s. %s"
                         % (num(sub), num(inc),
                            "No price changed, so it is all income effect."
                            if abs(sub) < 0.01 else
                            "Substitution wins." if abs(sub) > abs(inc) else
                            "Income wins: hours fall as the wage rises."
                            if inc * sub < 0 else ""))
            elif not st["same_taste"]:
                text += (" Preferences or T changed too, so there is no clean "
                         "decomposition.")
            rows.append(("Before &rarr; after", text))
        return table(rows)


demand = DemandLab()
effects = EffectsLab()
labour = LabourLab()
