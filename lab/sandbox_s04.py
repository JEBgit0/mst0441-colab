"""
sandbox_s04.py - session 4 sandbox: intertemporal choice, everything visible.

    choice  Lab 1  the two-period budget, the Euler equation, the bond,
                   inflation and the credit constraint
    two     Lab 2  two households on one line: who gains from a rate change,
                   and patience versus demographics
    taxes   Lab 3  problems A4.1 and A4.2 (session 3's effects lab, with a tax)

Released with the session 4 solutions.
"""

import numpy as np

import consumer_theory as ct
from sandbox import Lab, html_label, legend, num, style_axes, table
from sandbox_s03 import CES_NAME, EffectsLab
from style import BEFORE, CURVE, INK, LINE, MUTE

LOG = "Log"
CRRA = "CRRA (beyond the notes)"
LINEAR = "Linear (beyond the notes)"
TIME_FAMILIES = [LOG, CRRA, LINEAR]


def time_utility(family, beta, sigma):
    # u(c1) + beta u(c2). The notes use log; CRRA and linear are beyond them:
    # log is CRRA at sigma = 1, linear is CRRA at sigma = 0.
    if family == CRRA:
        return ct.DiscountedCRRA(sigma, beta)
    if family == LINEAR:
        return ct.PerfectSubstitutes(1.0, beta)
    return ct.LogUtility(1.0, beta)


def lifetime_budget(v, no_credit=False):
    # Assets arrive with period-1 income; every r is the real rate.
    rho = ct.real_rate(v["r"], v["pi"])
    b = ct.Budget.intertemporal(rho, v["a1"] + v["m1"], v["m2"])
    if no_credit:
        b = b.replace(x1_cap=v["a1"] + v["m1"])
    return rho, b


def draw_time(ax, live, before, frame, label_e="e"):
    """The intertemporal picture: the line through e, the choice, the bond."""
    b, u, ch = live
    style_axes(ax)
    npv = b.m / b.p1                        # the uncapped intercepts
    fv = b.max_x2
    e1, e2 = b.e1, b.e2
    capped = b.x1_cap is not None and b.x1_cap < npv - 1e-9

    xs = np.linspace(0, b.max_x1, 100)
    ax.fill_between(xs, 0, b.x2_at(xs), color=LINE, alpha=0.07, lw=0)
    if before is not None:
        b0, u0, c0 = before
        ax.plot([0, b0.m / b0.p1], [b0.max_x2, 0], color=BEFORE, lw=1.8,
                label="before, slope %s" % num(b0.slope))
        ax.plot([c0.x1], [c0.x2], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8, zorder=6)
    if capped:
        ax.plot([e1, npv], [e2, 0], color=LINE, lw=1.4, ls=":", alpha=0.4)
        ax.axvline(e1, color=MUTE, lw=0.9, ls="--")
    for s in (0.75, 1.3):
        lvl = float(u.u(max(ch.x1, 1e-9) * s, max(ch.x2, 1e-9) * s))
        cx, cy = u.indifference_curve(lvl, frame * 0.004, frame, 300)
        ax.plot(cx, cy, color=CURVE, lw=0.9, ls=":", alpha=0.45)
    cx, cy = u.indifference_curve(ch.utility, frame * 0.004, frame, 400)
    ax.plot(cx, cy, color=CURVE, lw=2, label="indifference curve")
    ax.plot(xs, b.x2_at(xs), color=LINE, lw=2.2, ls="--" if before is not None else "-",
            label="%sbudget, slope %s" % ("new " if before else "", num(b.slope)))

    ax.annotate("NPV %s" % num(npv), (npv, 0), textcoords="offset points", xytext=(-4, 8),
                ha="right", color=LINE, fontsize=8.5)
    ax.annotate("FV %s" % num(fv), (0, fv), textcoords="offset points", xytext=(6, 2),
                color=LINE, fontsize=8.5)
    ax.plot([e1], [e2], "s", color=LINE, ms=7, zorder=6)
    # e's label goes on the side the trade does not use: the arrow to the
    # choice leaves up-left for a lender and down-right for a borrower. Near
    # the left edge it has to go right whatever happens, or it is cut off.
    lending = ch.x1 < e1 - 1e-9
    right = lending or e1 < 0.3 * frame
    ax.annotate("%s = (%s, %s)" % (label_e, num(e1), num(e2)), (e1, e2),
                textcoords="offset points", xytext=(10, 6) if right else (-10, 8),
                ha="left" if right else "right", color=LINE, fontsize=9)
    at_e = abs(ch.x1 - e1) <= frame * 0.01 and abs(ch.x2 - e2) <= frame * 0.01
    if not at_e:
        ax.annotate("", xy=(ch.x1, ch.x2), xytext=(e1, e2),
                    arrowprops=dict(arrowstyle="-|>", color=CURVE, lw=1.3, shrinkA=6,
                                    shrinkB=7))
    ax.plot([ch.x1], [ch.x2], "o", color=CURVE, ms=8, zorder=7)
    if not at_e:                       # at e, e's own label already gives the numbers
        ax.annotate("(%s, %s)" % (num(ch.x1), num(ch.x2)), (ch.x1, ch.x2),
                    textcoords="offset points", xytext=(9, 7), color=INK, fontsize=9.5)
    ax.set_xlim(0, frame)
    ax.set_ylim(0, frame)
    ax.set_xlabel("c1  today", color=INK, loc="right")
    ax.set_ylabel("c2  tomorrow", color=INK, loc="top")
    legend(ax)


# ======================================================================
# Lab 1: intertemporal choice
# ======================================================================

KARI = dict(family=LOG, m1=50.0, m2=60.0, a1=0.0, r=0.20, pi=0.0, beta=2 / 3, sigma=1.0)
SHEET = dict(KARI, m1=60.0, m2=63.0, r=0.05, beta=0.5)
A43 = dict(KARI, a1=5.0, m1=10.0, m2=100.0, r=0.05, beta=1.0)


class ChoiceLab(Lab):
    TITLE = "Lab 1 &middot; Consumption today and tomorrow"
    INTRO = ("Income moves the line in parallel; the interest rate rotates it around "
             "the endowment e. The arrow from e to the choice is the bond: right of e "
             "you borrow, left of e you lend. Inflation turns the nominal rate into "
             "the real rate &rho;.")
    FAMILIES = TIME_FAMILIES
    SLIDERS = [
        ("m1", 0.0, 200.0, 1.0, 50.0, ".0f"),
        ("m2", 0.0, 200.0, 1.0, 60.0, ".0f"),
        ("a1", 0.0, 100.0, 1.0, 0.0, ".0f"),
        ("r", 0.0, 0.5, 0.01, 0.20, ".2f"),
        ("pi", 0.0, 0.25, 0.01, 0.0, ".2f"),
        ("beta", 0.05, 1.5, 0.01, 2 / 3, ".2f"),
        ("sigma", 0.1, 4.0, 0.05, 1.0, ".2f"),
    ]
    CHECKS = [("nocredit", "No borrowing (credit constraint)")]
    FIGSIZE = (6.4, 7.0)
    PRESETS = [
        dict(label="Notes p. 3 income today only", kind="notes",
             values=dict(KARI, m1=8.0, m2=0.0, r=0.05, beta=1.0)),
        dict(label="Notes p. 4 no credit", kind="notes",
             values=dict(KARI, m1=2.0, m2=6.0, r=0.05, beta=1.0), flags={"nocredit": True}),
        dict(label="Notes p. 4 income up", kind="notes",
             before=dict(KARI, m1=2.0, m2=6.0, r=0.05, beta=1.0),
             values=dict(KARI, m1=4.0, m2=6.0, r=0.05, beta=1.0)),
        dict(label="Notes p. 8 Kari", kind="notes", values=KARI),
        dict(label="Try it (c) Sondre", kind="notes", values=dict(KARI, beta=0.25)),
        dict(label="Try it (d) bonus", kind="notes", before=KARI, values=dict(KARI, m2=72.0)),
        dict(label="Worksheet beta 1/2", kind="notes", values=SHEET),
        dict(label="Worksheet beta 1", kind="notes", values=dict(SHEET, beta=1.0)),
        dict(label="Worksheet rate rise", kind="notes", before=SHEET,
             values=dict(SHEET, r=0.25)),
        dict(label="Review Q4 Vilde", kind="notes",
             values=dict(KARI, m1=100.0, m2=110.0, r=0.10)),
        dict(label="Review Q6 real rate", kind="notes", values=dict(KARI, r=0.26, pi=0.05)),
        dict(label="A4.3 (thousands)", kind="problem", values=A43),
        dict(label="A4.3 (3) m1 + 10", kind="problem", before=A43, values=dict(A43, m1=20.0)),
        dict(label="A4.3 (4) m2 + 10", kind="problem", before=A43, values=dict(A43, m2=110.0)),
        dict(label="A4.3 (5) r to 10%", kind="problem", before=A43, values=dict(A43, r=0.10)),
        dict(label="A4.3 (6) no borrowing", kind="problem", values=A43,
             flags={"nocredit": True}),
        dict(label="CRRA, sigma 3", kind="extra",
             values=dict(SHEET, family=CRRA, sigma=3.0)),
    ]

    def relabel(self):
        self.w["m1"].description = "Income today m1"
        self.w["m2"].description = "Income tomorrow m2"
        self.w["a1"].description = "Assets a1"
        self.w["r"].description = "Nominal rate r"
        html_label(self.w["pi"], "Inflation &pi;")
        html_label(self.w["beta"], "&beta;, patience")
        crra = self.w["family"].value == CRRA
        html_label(self.w["sigma"], "&sigma;, curvature" if crra else "&sigma; (CRRA only)")
        self.w["sigma"].disabled = not crra

    def model(self, v, no_credit):
        rho, b = lifetime_budget(v, no_credit)
        u = time_utility(v["family"], v["beta"], v["sigma"])
        return rho, (b, u, u.demand(b))

    def compute(self):
        v = self.values()
        rho, live = self.model(v, self.flag("nocredit"))
        before = self.model(self.before, self.flag("nocredit"))[1] if self.before else None
        need = [live[0].m / live[0].p1, live[0].max_x2]
        if before is not None:
            need += [before[0].m / before[0].p1, before[0].max_x2]
        return dict(v=v, rho=rho, live=live, before=before,
                    frame=self.stick("f", max(need) * 1.05))

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.2], hspace=0.32)
        draw_time(fig.add_subplot(gs[0]), st["live"], st["before"], st["frame"])
        ax = fig.add_subplot(gs[1])
        style_axes(ax)
        v, ch = st["v"], st["live"][2]
        income = [v["a1"] + v["m1"], v["m2"]]
        use = [ch.x1, ch.x2]
        xs = np.arange(2)
        ax.bar(xs - 0.18, income, width=0.34, color=MUTE, alpha=0.6, label="resources")
        ax.bar(xs + 0.18, use, width=0.34, color=CURVE, alpha=0.85, label="consumption")
        for x, a, c in zip(xs, income, use):
            ax.annotate(num(a), (x - 0.18, a), textcoords="offset points", xytext=(0, 3),
                        ha="center", fontsize=8, color=INK)
            ax.annotate(num(c), (x + 0.18, c), textcoords="offset points", xytext=(0, 3),
                        ha="center", fontsize=8, color=INK)
        ax.set_xticks(xs)
        ax.set_xticklabels(["today", "tomorrow"])
        ax.set_ylim(0, max(income + use) * 1.25 + 1e-9)
        ax.set_title("Resources against consumption, period by period", loc="left",
                     color=INK, fontsize=9.5)
        legend(ax, loc="upper left")
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.06)

    def describe(self, st):
        v, rho = st["v"], st["rho"]
        b, u, ch = st["live"]
        have = v["a1"] + v["m1"]
        bond = have - ch.x1
        npv, fv = b.m / b.p1, b.max_x2
        rate = "r = %s%%" % num(100 * v["r"])
        if v["pi"] > 0:
            rate = ("nominal %s%% with inflation %s%%: real &rho; = %s%% (the shortcut "
                    "r &minus; &pi; would say %s%%)"
                    % (num(100 * v["r"]), num(100 * v["pi"]), num(100 * rho),
                       num(100 * (v["r"] - v["pi"]))))
        assets = "a<sub>1</sub> + " if v["a1"] > 0 else ""
        rows = [
            ("Budget", "c<sub>1</sub> + c<sub>2</sub>/(1 + &rho;) = %sm<sub>1</sub> + "
                       "m<sub>2</sub>/(1 + &rho;), with %s. NPV %s, FV %s, slope %s."
             % (assets, rate, num(npv), num(fv), num(b.slope))),
            ("Choice", "c<sub>1</sub>* = %s, c<sub>2</sub>* = %s." % (num(ch.x1), num(ch.x2))),
        ]
        if v["family"] == LOG:
            rows.append(("Euler", "c<sub>2</sub>/c<sub>1</sub> = &beta;(1 + &rho;) = %s: "
                                  "consumption %s over time. Log utility spends 1/(1 + &beta;) "
                                  "= %s of the NPV today."
                         % (num(v["beta"] * (1 + rho)),
                            "grows" if v["beta"] * (1 + rho) > 1 + 1e-9 else
                            "falls" if v["beta"] * (1 + rho) < 1 - 1e-9 else "is flat",
                            num(1 / (1 + v["beta"])))))
        if ch.kind == "corner" and self.flag("nocredit") and ch.x1 >= have - 1e-9:
            rows.append(("Bond", "Credit constrained: she consumes her resources today, "
                                 "%s, and would borrow if she could. The Euler equation "
                                 "holds with inequality: u'(c<sub>1</sub>) &gt; "
                                 "&beta;(1 + &rho;)u'(c<sub>2</sub>)." % num(have)))
        elif abs(bond) < 1e-6:
            rows.append(("Bond", "None: she consumes exactly her resources in each period."))
        else:
            rows.append(("Bond", "b<sub>1</sub> = %s: she %s %s today and %s %s tomorrow."
                         % (num(bond), "lends" if bond > 0 else "borrows", num(abs(bond)),
                            "collects" if bond > 0 else "repays",
                            num(abs(bond) * (1 + rho)))))
        if st["before"] is not None:
            c0 = st["before"][2]
            rows.append(("Before &rarr; after", "c<sub>1</sub> %s &rarr; %s (%s), "
                                                "c<sub>2</sub> %s &rarr; %s"
                         % (num(c0.x1), num(ch.x1), num(ch.x1 - c0.x1), num(c0.x2),
                            num(ch.x2))))
        return table(rows)


# ======================================================================
# Lab 2: two households on one line
# ======================================================================

def household_text(name, rho0, rho1, m1, m2, beta):
    u = ct.LogUtility(1.0, beta)
    c0 = u.demand(ct.Budget.intertemporal(rho0, m1, m2))
    c1 = u.demand(ct.Budget.intertemporal(rho1, m1, m2))
    side = "lender" if c0.x1 < m1 - 1e-9 else "borrower" if c0.x1 > m1 + 1e-9 else "neither"
    if abs(rho1 - rho0) < 1e-12:
        return ("%s: a %s at (%s, %s), saving %s of %s today."
                % (name, side, num(c0.x1), num(c0.x2), num(m1 - c0.x1), num(m1)))
    better = ("better off" if c1.utility > c0.utility + 1e-9 else
              "worse off" if c1.utility < c0.utility - 1e-9 else "unaffected")
    return ("%s: a %s. c<sub>1</sub> %s &rarr; %s, c<sub>2</sub> %s &rarr; %s; %s."
            % (name, side, num(c0.x1), num(c1.x1), num(c0.x2), num(c1.x2), better))


TWO = dict(r0=0.05, r1=0.25, bB=1.0, mB1=20.0, mB2=100.0, bL=1.0, mL1=100.0, mL2=20.0)


class TwoLab(Lab):
    TITLE = "Lab 2 &middot; Two households, one interest rate"
    INTRO = ("A borrower and a lender facing the same rate. Move the new rate away "
             "from the old one and each line rotates around its own endowment: the "
             "same move helps one and hurts the other. Both use log utility.")
    SLIDERS = [
        ("r0", 0.0, 0.5, 0.01, 0.05, ".2f"),
        ("r1", 0.0, 0.5, 0.01, 0.25, ".2f"),
        ("bB", 0.05, 1.5, 0.01, 1.0, ".2f"),
        ("mB1", 0.0, 200.0, 1.0, 20.0, ".0f"),
        ("mB2", 0.0, 200.0, 1.0, 100.0, ".0f"),
        ("bL", 0.05, 1.5, 0.01, 1.0, ".2f"),
        ("mL1", 0.0, 200.0, 1.0, 100.0, ".0f"),
        ("mL2", 0.0, 200.0, 1.0, 20.0, ".0f"),
    ]
    FIGSIZE = (6.6, 4.4)
    PRESETS = [
        dict(label="Notes p. 10 rate rise", kind="notes", values=TWO),
        dict(label="Notes p. 10 rate cut", kind="notes", values=dict(TWO, r0=0.25, r1=0.05)),
        dict(label="Notes p. 11 patience", kind="notes",
             values=dict(TWO, r1=0.05, bB=0.5, mB1=60.0, mB2=63.0, bL=1.2, mL1=60.0,
                         mL2=63.0)),
        dict(label="Notes p. 11 demographics", kind="notes",
             values=dict(TWO, r1=0.05, bB=0.9, bL=0.9)),
    ]

    def relabel(self):
        names = dict(r0="Old rate", r1="New rate", bB="Household 1 &beta;",
                     mB1="Household 1 m1", mB2="Household 1 m2", bL="Household 2 &beta;",
                     mL1="Household 2 m1", mL2="Household 2 m2")
        for k, d in names.items():
            html_label(self.w[k], d)
        self.compare.layout.display = "none"     # old vs new rate is built in

    def compute(self):
        v = self.values()
        st = dict(v=v, people=[])
        for who, b, m1, m2 in (("Household 1", v["bB"], v["mB1"], v["mB2"]),
                               ("Household 2", v["bL"], v["mL1"], v["mL2"])):
            u = ct.LogUtility(1.0, b)
            b0 = ct.Budget.intertemporal(v["r0"], m1, m2)
            b1 = ct.Budget.intertemporal(v["r1"], m1, m2)
            st["people"].append((who, (b1, u, u.demand(b1)), (b0, u, u.demand(b0)), m1, m2, b))
        need = [max(p[1][0].m, p[2][0].m, p[1][0].max_x2, p[2][0].max_x2)
                for p in st["people"]]
        st["frame"] = self.stick("f", max(need) * 1.05)
        return st

    def figure(self, fig, st):
        axes = fig.subplots(1, 2)
        changed = abs(st["v"]["r1"] - st["v"]["r0"]) > 1e-12
        for ax, (who, live, old, m1, m2, b) in zip(axes, st["people"]):
            draw_time(ax, live, old if changed else None, st["frame"])
            ax.set_title(who, loc="left", color=INK, fontsize=9.5)
            ax.get_legend().remove() if ax.get_legend() else None
        fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.12, wspace=0.25)

    def describe(self, st):
        v = st["v"]
        rows = [("Rate", "%s%% &rarr; %s%%" % (num(100 * v["r0"]), num(100 * v["r1"])))]
        for who, live, old, m1, m2, b in st["people"]:
            rows.append((who, household_text("&beta; = %s" % num(b), v["r0"], v["r1"],
                                             m1, m2, b)))
        rows.append(("Read it", "Whoever chose left of e (a lender) gains from a higher "
                                "rate; whoever chose right of e (a borrower) loses. Same "
                                "line, different &beta;: patience. Same &beta;, different e: "
                                "demographics."))
        return table(rows)


# ======================================================================
# Lab 3: taxes (A4.1, A4.2): session 3's effects lab with an ad valorem tax
# ======================================================================

A41 = dict(family="Perfect substitutes", p1=30.0, p2=25.0, m=300.0, tau=0.6, a=0.5,
           b=0.5, s=0.5, good="good 2")


class TaxLab(EffectsLab):
    TITLE = "Lab 3 &middot; Taxes: A4.1 and A4.2"
    INTRO = ("An ad valorem tax on one good, split into substitution and income "
             "effects, against an income tax that raises the same money. With perfect "
             "substitutes the tax base can vanish altogether.")
    WORD = "Tax"
    SLIDERS = [
        ("p1", 1.0, 60.0, 1.0, 30.0, ".0f"),
        ("p2", 1.0, 60.0, 1.0, 25.0, ".0f"),
        ("m", 10.0, 1000.0, 1.0, 300.0, ".0f"),
        ("tau", 0.0, 2.0, 0.05, 0.6, ".2f"),
        ("a", 0.05, 3.0, 0.01, 0.5, ".2f"),
        ("b", 0.05, 3.0, 0.01, 0.5, ".2f"),
        ("s", 0.1, 3.0, 0.05, 0.5, ".2f"),
    ]
    PRESETS = [
        dict(label="A4.1 substitutes", kind="problem", values=A41, flags={"lump": True}),
        dict(label="A4.2 Cobb-Douglas", kind="problem",
             values=dict(A41, family="Cobb-Douglas"), flags={"lump": True}),
        dict(label="CES, sigma 0.5", kind="extra",
             values=dict(A41, family=CES_NAME, a=1.0, b=1.0), flags={"lump": True}),
    ]


choice = ChoiceLab()
two = TwoLab()
taxes = TaxLab()
