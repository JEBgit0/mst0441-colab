"""
sandbox_s07.py - session 7 sandbox: exchange once more, and the smoke market.

    exchange  Lab 1  session 6's box with this session's economies: the
                     notes' recap economy and problem A7.1
    smoke     Lab 2  the smoke economy: the efficient level, the unpriced
                     corners, the priced market under either property right,
                     and (beyond the notes) income effects that break the
                     Coase invariance

Released with the session 7 solutions. The maths is externality.py.
"""

import math

import numpy as np

from externality import Smoke
from sandbox import (Lab, BEFORE, CURVE, DIRECT, INK, LINE, MUTE, NEW, legend, num,
                     style_axes, table)
from sandbox_s06 import WORKED, MarketLab, html_ok

A_COL, B_COL, CC = LINE, CURVE, DIRECT


# ======================================================================
# Lab 1: exchange, once more
# ======================================================================

RECAP = dict(WORKED, a=1 / 3, b=0.75, wAx=6.0, wAy=4.0, wBx=6.0, wBy=8.0, p=4 / 3, xp=3.0,
             yp=8.0)
TRADE = dict(WORKED, a=0.5, b=0.5, wAx=10.0, wAy=25.0, wBx=5.0, wBy=5.0, p=2.0, xp=5.0,
             yp=10.0)


class ExchangeLab(MarketLab):
    TITLE = "Lab 1 &middot; Exchange, once more"
    SLIDERS = [(k, lo, 40.0 if k.startswith("w") or k in ("xp", "yp") else hi, st, v, f)
               for k, lo, hi, st, v, f in MarketLab.SLIDERS]
    PRESETS = [
        dict(label="Notes p. 1 recap economy", kind="notes", values=RECAP),
        dict(label="Notes p. 2 the core", kind="notes", values=RECAP, flags=dict(lens=True)),
        dict(label="A7.1 contract curve", kind="problem", values=TRADE),
        dict(label="A7.1, a point on it", kind="problem", values=TRADE,
             flags=dict(point=True)),
    ]


# ======================================================================
# Lab 2: the smoke market
# ======================================================================

SQRT = "x + sqrt(αS)  (notes Try it)"
LOG = "x + α ln S  (worksheet, A7.3)"
CD = "ln x + α ln S: income effects (beyond the notes)"
KINDS = {SQRT: "sqrt", LOG: "log", CD: "cd"}

MARKET_B = "Priced: B holds the right to clean air"
MARKET_A = "Priced: A holds the right to smoke"
FREE_A = "No trading: A may smoke"
FREE_B = "No trading: B may insist on clean air"

HOME = dict(family=LOG, regime=MARKET_B, alpha=1.0, beta=3.0, wA=6.0, wB=6.0)
TRY = dict(HOME, family=SQRT)
Q3 = dict(HOME, family=SQRT, alpha=3.0, beta=1.0)
P3 = dict(HOME, alpha=1 / 3, beta=2 / 3, wA=5.0, wB=15.0)
INC = dict(HOME, family=CD)


def outcome(e, regime):
    if regime == MARKET_B:
        return e.market("B")
    if regime == MARKET_A:
        return e.market("A")
    return e.no_trade("A" if regime == FREE_A else "B")


def prefs_text(e):
    a, b = num(e.alpha), num(e.beta)
    if e.family == "sqrt":
        return ("u<sub>A</sub> = x<sub>A</sub> + &radic;(%s&middot;S), u<sub>B</sub> = x<sub>B</sub> + "
                "&radic;(%s&middot;(1 &minus; S))" % (a, b))
    if e.family == "log":
        return ("u<sub>A</sub> = x<sub>A</sub> + %s&middot;ln S, u<sub>B</sub> = x<sub>B</sub> + "
                "%s&middot;ln(1 &minus; S)" % (a, b))
    return ("u<sub>A</sub> = ln x<sub>A</sub> + %s&middot;ln S, u<sub>B</sub> = ln x<sub>B</sub> + "
            "%s&middot;ln(1 &minus; S)" % (a, b))


class SmokeLab(Lab):
    TITLE = "Lab 2 &middot; The smoke market"
    INTRO = ("A smokes, B breathes, and they share one unit of air: smoke S from A's corner, "
             "clean air 1 &minus; S from B's. Good 1 is the numeraire, so p is the price of "
             "smoke in units of good 1. Pick who holds the right, and whether it can be "
             "traded. The right panel compares A's marginal benefit of smoke with B's marginal "
             "damage.")
    FAMILIES = [SQRT, LOG, CD]
    DROPDOWNS = [("regime", "Regime", [MARKET_B, MARKET_A, FREE_A, FREE_B])]
    SLIDERS = [
        ("alpha", 0.1, 5.0, 0.05, 1.0, ".2f"),
        ("beta", 0.1, 5.0, 0.05, 3.0, ".2f"),
        ("wA", 0.5, 30.0, 0.5, 6.0, ".1f"),
        ("wB", 0.5, 30.0, 0.5, 6.0, ".1f"),
    ]
    FIGSIZE = (8.6, 4.4)
    PRESETS = [
        dict(label="Notes p. 6 Try it", kind="notes", values=TRY),
        dict(label="Review Q3 (i) Aksel may smoke", kind="notes",
             values=dict(Q3, regime=FREE_A)),
        dict(label="Review Q3 (ii) Brita insists", kind="notes",
             values=dict(Q3, regime=FREE_B)),
        dict(label="Worksheet: B holds the right", kind="notes", values=HOME),
        dict(label="Worksheet: A holds the right", kind="notes", before=HOME,
             values=dict(HOME, regime=MARKET_A)),
        dict(label="A7.3 B owns clean air", kind="problem", values=P3),
        dict(label="A7.3 A owns the right", kind="problem", before=P3,
             values=dict(P3, regime=MARKET_A)),
        dict(label="Income effects: B's right", kind="extra", values=INC),
        dict(label="Income effects: A's right", kind="extra", before=INC,
             values=dict(INC, regime=MARKET_A)),
    ]

    def relabel(self):
        html_ok(self.w["alpha"], "&alpha;: A's taste for smoke")
        html_ok(self.w["beta"], "&beta;: B's taste for air")
        html_ok(self.w["wA"], "A's good 1, &omega;<sub>A</sub>")
        html_ok(self.w["wB"], "B's good 1, &omega;<sub>B</sub>")

    def compute(self):
        v = self.values()
        e = Smoke(KINDS[v["family"]], v["alpha"], v["beta"], v["wA"], v["wB"])
        st = dict(v=v, e=e, out=outcome(e, v["regime"]))
        st["other"] = outcome(e, MARKET_A if v["regime"] == MARKET_B else MARKET_B)
        if self.before:
            b = self.before
            eb = Smoke(KINDS[b["family"]], b["alpha"], b["beta"], b["wA"], b["wB"])
            st["before"] = (eb, outcome(eb, b["regime"]))
        return st

    def figure(self, fig, st):
        gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1], wspace=0.28)
        ax = fig.add_subplot(gs[0])
        e, o = st["e"], st["out"]
        style_axes(ax)
        ax.grid(False)
        for side in ax.spines.values():
            side.set_visible(True)
            side.set_color(MUTE)
        X = e.X
        top = ax.secondary_xaxis("top", functions=(lambda x: X - x, lambda x: X - x))
        right = ax.secondary_yaxis("right", functions=(lambda s: 1 - s, lambda s: 1 - s))
        for sec in (top, right):
            sec.tick_params(colors=B_COL, labelsize=8)
        ax.tick_params(colors=A_COL, labelsize=8)
        ax.set_xlim(0, X)
        ax.set_ylim(0, 1)
        ax.set_xlabel(r"good 1 for A ($x_B$ along the top)", color=INK, fontsize=9, loc="right")
        ax.set_ylabel(r"smoke S (clean air $1 - S$ on the right)", color=INK, fontsize=9, loc="top")

        xs = np.linspace(X * 0.002, X * 0.998, 200)
        ax.plot(xs, [e.contract(x) for x in xs], color=CC, lw=2, label="contract curve")
        if "before" in st:
            eb, ob = st["before"]
            ax.plot([ob["xA"]], [ob["S"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8,
                    zorder=6, label="before")
        for S0, name in ((1.0, "e_A"), (0.0, "e_B")):
            ax.plot([e.wA], [S0], "s", color=MUTE, ms=6, clip_on=False, zorder=6)
            ax.annotate("$%s$" % name, (e.wA, S0), textcoords="offset points",
                        xytext=(6, -12 if S0 else 5), color=MUTE, fontsize=9)
        if o["p"] is not None:
            Ss = np.array([0.0, 1.0])
            ax.plot(e.wA - o["p"] * (Ss - o["S0"]), Ss, color=INK, lw=1.5,
                    label="budget line, p = %s" % num(o["p"]))
        interior = 0.002 < o["S"] < 0.998
        if interior or e.family == "sqrt":
            Ss = np.linspace(0.002, 0.998, 300)
            la, lb = e.uA(o["xA"], o["S"]), e.uB(o["xB"], o["S"])
            ax.plot([e.icA(la, s) for s in Ss], Ss, color=A_COL, lw=1.3)
            ax.plot([e.icB(lb, s) for s in Ss], Ss, color=B_COL, lw=1.3)
        ax.plot([o["xA"]], [o["S"]], "o", color=NEW, ms=8, zorder=7, clip_on=False)
        legend(ax, loc="upper right")
        ax.get_legend().set_zorder(10)

        mx = fig.add_subplot(gs[1])
        style_axes(mx)
        Ss = np.linspace(0.01, 0.99, 300)
        xa = o["xA"] if e.family == "cd" else None
        xb = o["xB"] if e.family == "cd" else None
        mb = np.array([e.mb(s, xa) for s in Ss])
        md = np.array([e.md(s, xb) for s in Ss])
        mx.plot(Ss, mb, color=A_COL, lw=2, label="A's marginal benefit")
        mx.plot(Ss, md, color=B_COL, lw=2, label="B's marginal damage")
        S_eff = e.efficient()
        if S_eff is not None:
            mx.axvline(S_eff, color=CC, lw=1, ls=":")
            mx.plot([S_eff], [e.mb(S_eff)], "o", color=CC, ms=7, zorder=5)
        mx.axvline(o["S"], color=NEW, lw=1.2)
        if o["p"] is not None:
            mx.axhline(o["p"], color=INK, lw=0.8, ls="--")
        ref = o["p"] if o["p"] is not None else (e.mb(S_eff) if S_eff else e.mb(0.5, xa))
        mx.set_ylim(0, max(ref, 1e-6) * 3)
        mx.set_xlim(0, 1)
        mx.set_xlabel("smoke S", color=INK, fontsize=9, loc="right")
        mx.set_title("In units of good 1%s" % (" (at the current split)" if e.family == "cd" else ""),
                     loc="left", color=INK, fontsize=9.5)
        legend(mx, loc="upper center")
        fig.subplots_adjust(left=0.08, right=0.97, top=0.88, bottom=0.12)

    def describe(self, st):
        e, o, v = st["e"], st["out"], st["v"]
        rows = [("Preferences", prefs_text(e) + ".")]
        S_eff = e.efficient()
        if S_eff is not None:
            rows.append(("Efficient", "A's marginal benefit equals B's marginal damage at S* = "
                                      "&alpha;/(&alpha; + &beta;) = %s, where both equal %s, in units "
                                      "of good 1. Quasi-linear, so the contract curve is flat: every "
                                      "efficient allocation has the same smoke."
                         % (num(S_eff), num(e.mb(S_eff)))))
        else:
            rows.append(("Efficient", "With income effects the efficient smoke level depends on who "
                                      "holds the good 1: the contract curve is S = &alpha;x<sub>A</sub>/"
                                      "(&alpha;x<sub>A</sub> + &beta;x<sub>B</sub>), not flat."))
        if o["p"] is None:
            corner = "A smokes as much as she can, S = 1" if v["regime"] == FREE_A else \
                "B allows no smoke at all, S = 0"
            xa = o["xA"] if e.family == "cd" else None
            xb = o["xB"] if e.family == "cd" else None
            if v["regime"] == FREE_A:
                gap = ("At S = 1, B's marginal damage is %s and A's marginal benefit %s: B would pay "
                       "more for cleaner air than A needs to give it up. Over-pollution."
                       % ("unbounded" if e.family != "sqrt" else num(e.md(0.999, xb)),
                          num(e.mb(0.999, xa))))
            else:
                gap = ("At S = 0, A's marginal benefit is %s and B's marginal damage %s: A would pay "
                       "more for the first puffs than they cost B. Under-pollution."
                       % ("unbounded" if e.family != "sqrt" else num(e.mb(0.001, xa)),
                          num(e.md(0.001, xb))))
            rows.append(("Outcome", "Nobody can pay anybody, so %s. Smoke is free to the owner of the "
                                    "air, so she ignores the other side." % corner))
            rows.append(("Missed gains", gap))
            loss = e.surplus_loss(o["S"])
            if loss is not None:
                rows.append(("Lost surplus", "Against S*, the corner wastes %s units of good 1."
                             % ("an unbounded number of" if math.isinf(loss) else num(loss))))
        else:
            owner = "B holds the right, so A buys smoke" if v["regime"] == MARKET_B else \
                "A holds the right, so B buys clean air from her"
            pay = o["pay"]
            who = ("A pays B %s" % num(pay) if pay > 1e-9 else
                   "B pays A %s" % num(-pay) if pay < -1e-9 else "No payment")
            rows.append(("Market", "%s at p = %s. Smoke S = %s; %s units of good 1." % (
                owner, num(o["p"]), num(o["S"]), who)))
            rows.append(("Good 1", "A ends with %s, B with %s." % (num(o["xA"]), num(o["xB"]))))
            xa = o["xA"] if e.family == "cd" else None
            xb = o["xB"] if e.family == "cd" else None
            rows.append(("Tangency", "A's marginal benefit %s = B's marginal damage %s = p: both "
                                     "curves touch the same price line, on the contract curve."
                         % (num(e.mb(o["S"], xa)), num(e.md(o["S"], xb)))))
            t = st["other"]
            same = abs(t["S"] - o["S"]) < 1e-6
            rows.append(("Coase", "Flip the right and the market gives S = %s, p = %s, with A at %s "
                                  "and B at %s. %s" % (
                                      num(t["S"]), num(t["p"]), num(t["xA"]), num(t["xB"]),
                                      "Same smoke, different money: invariance holds because "
                                      "utility is quasi-linear." if same else
                                      "Different smoke: with income effects, whoever is made richer "
                                      "by the right buys more of what she likes. Efficiency survives; "
                                      "invariance does not.")))
        if "before" in st:
            eb, ob = st["before"]
            rows.append(("Before &rarr; after", "S %s &rarr; %s; A's good 1 %s &rarr; %s"
                         % (num(ob["S"]), num(o["S"]), num(ob["xA"]), num(o["xA"]))))
        return table(rows)


exchange = ExchangeLab()
smoke = SmokeLab()
