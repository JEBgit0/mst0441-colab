"""
guided_s07.py - session 7 guided page: market failure and externalities.

    Part 1  recap      one more exchange economy (notes p. 1-2)
    Part 2  define     what is, and is not, an externality (review question 1)
    Part 3  efficient  the efficient smoke level, and the unpriced corners
    Part 4  pricing    the homework smoke market and the Coase theorem
    Part 5  satellite  coordination without a price (review question 5)
    Part 6  trade      problem A7.1: a contract curve with numbers
    Part 7  air        problem A7.2: clean air, property rights, clearing
    Part 8  invariance problem A7.3: quasi-linear invariance, and its limits

Answers are hashes in answers_s07.py, generated from
answer_keys/s07_keys.py in the private repo. The maths is externality.py and
equilibrium.py.
"""

import numpy as np

import edgeworth_plots as ed
import guided_plots as gp
from equilibrium import Economy
from externality import Smoke
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW, RED

H, M = answers("s07")

XA, YA, XB, YB = "x<sub>A</sub>", "y<sub>A</sub>", "x<sub>B</sub>", "y<sub>B</sub>"
X1A, X1B = "x<sup>1</sup><sub>A</sub>", "x<sup>1</sup><sub>B</sub>"
MA, MB = "m<sub>A</sub>", "m<sub>B</sub>"
A_COL, B_COL = LINE, CURVE


# ------------------------------------------------------- the smoke box ---

def _sbox(ax, X, up="S", down="1 − S"):
    # Good 1 across; smoke up from A's corner, clean air down from B's.
    ax.set_xlim(0, X)
    ax.set_ylim(0, 1)
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    kw = dict(color=INK, fontsize=10)
    ax.text(X, -0.03, r"$x^1_A$ $\rightarrow$", ha="right", va="top", **kw)
    ax.text(-0.015 * X, 1, up + r" $\uparrow$", ha="right", va="top", **kw)
    ax.text(0, 1.03, r"$\leftarrow$ $x^1_B$", ha="left", va="bottom", **kw)
    ax.text(1.015 * X, 0, down + r" $\downarrow$", ha="left", va="bottom", **kw)
    ax.text(-0.015 * X, -0.03, "A", ha="right", va="top", color=A_COL, fontsize=12,
            weight="bold")
    ax.text(1.015 * X, 1.03, "B", ha="left", va="bottom", color=B_COL, fontsize=12,
            weight="bold")


def _s_icA(ax, e, x, S, **kw):
    level = e.uA(x, S)
    Ss = np.linspace(0.004, 0.996, 300)
    ax.plot([e.icA(level, s) for s in Ss], Ss, **kw)


def _s_icB(ax, e, x, S, **kw):
    level = e.uB(e.X - x, S)
    Ss = np.linspace(0.004, 0.996, 300)
    ax.plot([e.icB(level, s) for s in Ss], Ss, **kw)


def _s_budget(ax, x0, S0, p, **kw):
    # Good 1 falls by p for each unit of smoke A takes on: x = x0 - p (S - S0).
    Ss = np.array([0.0, 1.0])
    ax.plot(x0 - p * (Ss - S0), Ss, **kw)


# ======================================================================
# Part 1: competitive equilibrium, once more (notes p. 1-2)
# ======================================================================

RECAP = Economy(1 / 3, 3 / 4, (6, 4), (6, 8))


def draw_recap(ax, stage):
    e = RECAP
    ed.box(ax, e.X, e.Y)
    gp.dot(ax, 6, 4, r"$\omega$", 8, -12, colour=INK)
    if stage in (1,):
        for p in (0.5, 3):
            ed.price_line(ax, e, p, 6, 4, color=GREY, lw=1)
    if stage >= 2:
        ed.price_line(ax, e, 4 / 3, 6, 4, color=INK, lw=1.6, label="price line")
    if stage >= 3:
        gp.dot(ax, 3, 8, "(3, 8)", -8, 6, colour=GREEN, ha="right")
    if stage >= 4:
        gp.arrow(ax, (6, 4), (3, 8), GREEN)
    if stage >= 5:
        ed.ic_a(ax, e, 3, 8, color=A_COL, lw=1.3, label="A")
        ed.ic_b(ax, e, 3, 8, color=B_COL, lw=1.3, label="B")
    if stage >= 6:
        ed.contract(ax, e, color=GREEN, lw=2, label="contract curve")
    gp.legend(ax, loc="lower right")


EXT_ASSUMPTION = "No externalities: each agent cares only about her own bundle"
TAKERS = "Agents take prices as given"
EXISTS = "An equilibrium exists"
CONVEX_R = "Preferences are convex"

RECAP_QUESTIONS = [
    Question(
        "c1",
        "u<sub>A</sub> = x<sup>1/3</sup>y<sup>2/3</sup>, u<sub>B</sub> = x<sup>3/4</sup>y<sup>1/4</sup>, "
        "&omega;<sub>A</sub> = (6, 4), &omega;<sub>B</sub> = (6, 8), p<sub>y</sub> = 1. Both incomes?",
        form=["%s =" % MA, BOX, "p +", BOX, "&nbsp; %s =" % MB, BOX, "p +", BOX],
        answers=[H("c1.0"), H("c1.1"), H("c1.2"), H("c1.3")],
        mistakes=M({"c1.0~4": "x comes first: &omega;<sub>A</sub> = (6, 4) means 6 units of x."}),
        explain="Every budget line passes through &omega;."),
    Question(
        "c2",
        "A spends 1/3 of her income on x and B 3/4 of his. Clear the market for x: p* = ?",
        form=["p* =", BOX],
        answers=[H("c2.0")],
        mistakes=M({"c2.0~3/4": "Upside down. (6p + 4)/(3p) + (9p + 12)/(2p) = 12.",
                    "c2.0~1": "Equal totals are not enough: the tastes differ."}),
        hints=["Multiply (6p + 4)/(3p) + (9p + 12)/(2p) = 12 through by 6p."],
        explain="Walras' law takes care of market y."),
    Question(
        "c3",
        "The allocation, A's bundle then B's.",
        form=["A: (", BOX, ",", BOX, ") &nbsp; B: (", BOX, ",", BOX, ")"],
        answers=[H("c3.0"), H("c3.1"), H("c3.2"), H("c3.3")],
        mistakes=M({"c3.0~4": "x<sub>A</sub> = (1/3)&middot;%s/p with %s = 12 and p = 4/3." % (MA, MA)}),
        explain="3 + 9 = 12 and 8 + 4 = 12."),
    Question(
        "c4",
        "A's net trade: how much x does she sell, and how much y does she buy?",
        form=["sells", BOX, "x, buys", BOX, "y"],
        answers=[H("c4.0"), H("c4.1")],
        explain="3 &middot; 4/3 = 4: equal value, as the budget demands."),
    Question(
        "c5",
        "Each MRS at the allocation?",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("c5.0"), H("c5.1")],
        mistakes=M({"c5.0~8/3": "MRS = (a/(1 &minus; a))&middot;y/x with a = 1/3, so multiply y/x by 1/2."}),
        explain="Both equal p*: the first welfare theorem."),
    Question(
        "c6",
        "The contract curve is %s = 72%s/(12 + 5%s). Which %s goes with %s = 4?"
        % (YA, XA, XA, YA, XA),
        form=["%s =" % YA, BOX],
        answers=[H("c6.0")],
        explain="It runs from corner to corner, through (3, 8)."),
    Question(
        "c7",
        "So why do governments put a price on carbon? Which condition of the first welfare "
        "theorem fails?",
        choices=[EXT_ASSUMPTION, TAKERS, EXISTS, CONVEX_R],
        answers=[H("c7.c")],
        mistakes=M({
            "c7.c~" + TAKERS: "Carbon emitters are mostly small. What lands in other people's "
                              "utility without a price?",
            "c7.c~" + EXISTS: "Existence is not the issue: think about what the emitter ignores.",
            "c7.c~" + CONVEX_R: "Convexity is the second theorem's condition.",
        }),
        explain="Carbon emitted in one country lands in the utility of people in another, and "
                "no market prices it."),
]

recap = GuidedProblem(
    "Part 1 &middot; Competitive equilibrium, once more",
    "Session 6's machinery with fresh numbers, before we break it.",
    RECAP_QUESTIONS, draw_recap, figsize=(6.0, 5.6),
    outro="Now knock out the third assumption.",
    sources=[NOTES("p. 1&ndash;2")],
)


# ======================================================================
# Part 2: what is (and is not) an externality
# ======================================================================

def draw_define(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.set_xlabel("output", color=INK, fontsize=10, loc="right")
    ax.set_ylabel("price", color=INK, fontsize=10, loc="top")
    q = np.linspace(0, 10, 50)
    ax.plot(q, 10 - q, color=INK, lw=1.8, label="demand")
    ax.plot(q, 2 + 0.5 * q, color=A_COL, lw=1.8, label="private cost")
    qm, qs = 16 / 3, 10 / 3
    if stage >= 1:
        ax.plot(q, 5 + 0.5 * q, color=RED, lw=1.8, label="social cost")
        gp.arrow(ax, (8.6, 6.3), (8.6, 9.0), RED)
        ax.text(8.75, 7.3, "damage", color=RED, fontsize=9)
    if stage >= 4:
        gp.dot(ax, qm, 10 - qm, "market", 8, 4, colour=A_COL)
    if stage >= 5:
        gp.dot(ax, qs, 10 - qs, "efficient", -8, 6, colour=GREEN, ha="right")
        ax.fill([qs, qm, qm], [10 - qs, 10 - qm, 5 + 0.5 * qm], color=RED, alpha=0.18,
                label="the loss")
    gp.legend(ax, loc="upper right")


NEG = "A negative externality"
POS = "A positive externality"
NOT_PRICE = "Not an externality: the effect came through a price"
NOT_OWN = "Not an externality: she acts in her own home"

PART1_FAILS = "Not an externality: part 1 fails, since nobody is made worse off"
PART2_FAILS = "Not an externality: part 2 fails, since the effect reached her through a price"

AT_PRIVATE = "Where demand meets the private cost: too much"
AT_SOCIAL = "Where demand meets the social cost"
AT_ZERO = "Zero, because the output harms others"
AT_DAMAGE = "Where the damage is largest"

EFF_SOCIAL = "Where demand meets the social cost"
EFF_PRIVATE = "Where demand meets the private cost"
EFF_ZERO = "Zero"
EFF_BOTH = "Halfway between the two cost lines"

DEFINE_QUESTIONS = [
    Question(
        "d1",
        "An externality needs two parts: (1) one agent's action makes another better or worse "
        "off, and (2) she neither bears the cost nor receives the benefit. Review question 1 (a): "
        "Trude's nightly drum practice keeps her neighbour awake.",
        choices=[NEG, POS, NOT_PRICE, NOT_OWN],
        answers=[H("d1.c")],
        mistakes=M({
            "d1.c~" + POS: "Is the neighbour better or worse off?",
            "d1.c~" + NOT_PRICE: "Does the neighbour get paid, or pay, for the noise?",
            "d1.c~" + NOT_OWN: "Where she acts doesn't matter: whose utility does it land in?",
        }),
        explain="The cost lands on the neighbour and nobody pays for it. The figure adds that "
                "damage to the producer's private cost."),
    Question(
        "d2",
        "(b) Odd's beehives pollinate the orchard next door.",
        choices=[POS, NEG, NOT_PRICE, NOT_OWN],
        answers=[H("d2.c")],
        mistakes=M({
            "d2.c~" + NEG: "Is the orchard owner better or worse off?",
            "d2.c~" + NOT_PRICE: "Does the orchard pay Odd for the pollination?",
            "d2.c~" + NOT_OWN: "The bees don't stay home.",
        }),
        explain="Like a vaccination: a benefit nobody pays for."),
    Question(
        "d3",
        "(c) A surge in demand for electricians raises the price Kaja pays for rewiring.",
        choices=[PART2_FAILS, PART1_FAILS, NEG, POS],
        answers=[H("d3.c")],
        mistakes=M({
            "d3.c~" + PART1_FAILS: "Kaja is worse off, so part 1 holds. How did the effect reach her?",
            "d3.c~" + NEG: "Check part 2: did it reach her without a price?",
            "d3.c~" + POS: "Kaja pays more. And how did it reach her?",
        }),
        explain="The market doing its job: a price carried the effect."),
    Question(
        "d4",
        "Back to a negative externality like the drumming or a factory's smoke. Where does "
        "the market produce?",
        choices=[AT_PRIVATE, AT_SOCIAL, AT_ZERO, AT_DAMAGE],
        answers=[H("d4.c")],
        mistakes=M({
            "d4.c~" + AT_SOCIAL: "That would need the polluter to count the damage. Does she?",
            "d4.c~" + AT_ZERO: "The polluter pays nothing for the harm, so why would she stop?",
            "d4.c~" + AT_DAMAGE: "The polluter never sees the damage.",
        }),
        explain="She does not internalize the harm."),
    Question(
        "d5",
        "And the efficient output?",
        choices=[EFF_SOCIAL, EFF_PRIVATE, EFF_ZERO, EFF_BOTH],
        answers=[H("d5.c")],
        mistakes=M({
            "d5.c~" + EFF_PRIVATE: "That ignores the damage to others.",
            "d5.c~" + EFF_ZERO: "The first units are worth more than all their costs together.",
            "d5.c~" + EFF_BOTH: "Efficient means counting the whole cost.",
        }),
        explain="The shaded triangle is what producing too much costs society."),
]

define = GuidedProblem(
    "Part 2 &middot; What is an externality?",
    "The two-part definition, review question 1, and the picture of why the market "
    "over-produces a bad.",
    DEFINE_QUESTIONS, draw_define, figsize=(6.0, 4.6),
    outro="The failure is always the same thing: a missing price.",
    sources=[NOTES("p. 3&ndash;4"), NOTES("p. 11, review question 1")],
)


# ======================================================================
# Part 3: the efficient smoke level (Try it, Figure 5, review question 3)
# ======================================================================

def draw_efficient(fig, stage):
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.55)
    ax = fig.add_subplot(gs[0])
    e = Smoke("sqrt", 1, 3, 6, 6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 3)
    ax.set_xlabel("smoke S", color=INK, fontsize=10, loc="right")
    ax.set_ylabel("value, in good 1", color=INK, fontsize=10, loc="top")
    ax.set_title(r"Drawn for $\alpha = 1$, $\beta = 3$", loc="left", color=MUTE, fontsize=9)
    Ss = np.linspace(0.03, 0.97, 200)
    if stage >= 1:
        ax.plot(Ss, [e.mb(s) for s in Ss], color=A_COL, lw=2, label="A's marginal benefit")
        ax.plot(Ss, [e.md(s) for s in Ss], color=B_COL, lw=2, label="B's marginal damage")
    if stage >= 2:
        gp.dot(ax, 0.25, 1, "S*", 8, 6, colour=GREEN)
        ax.axvline(0.25, color=GREEN, lw=0.8, ls=":")
    gp.legend(ax, loc="upper center")

    nl = fig.add_subplot(gs[1])
    nl.set_xlim(-0.05, 1.05)
    nl.set_ylim(-1, 1)
    nl.axis("off")
    nl.plot([0, 1], [0, 0], color=INK, lw=1.5)
    nl.text(0, -0.75, "S = 0", ha="center", color=INK, fontsize=9)
    nl.text(1, -0.75, "S = 1", ha="center", color=INK, fontsize=9)
    nl.set_title(r"Review question 3: $\alpha = 3$, $\beta = 1$", loc="left", color=MUTE, fontsize=9)
    if stage >= 5:
        nl.plot([0.75], [0], "o", color=GREEN, ms=8)
        nl.text(0.75, 0.35, "planner", ha="center", color=GREEN, fontsize=9)
        nl.plot([1], [0], "o", color=A_COL, ms=8)
        nl.text(1, 0.35, "A's right", ha="center", color=A_COL, fontsize=9)
        nl.plot([0], [0], "o", color=B_COL, ms=8)
        nl.text(0, 0.35, "B's right", ha="center", color=B_COL, fontsize=9)


NOT_ZERO = "Near S = 0, A's marginal benefit is far above B's marginal damage: the first puffs are worth more to A than they cost B"
RIGHT_A = "Because A holds the right to smoke"
GOOD_BOTH = "Because smoke is a good for both"
ZERO_EFF = "It is: zero smoke is the efficient level"

CORNERS = "Without a price the owner of the air goes to a corner, 1 or 0; the efficient level lies in between"
A_WINS = "The market gets it right when A holds the right"
B_WINS = "The market gets it right when B holds the right"
ALL_SAME = "All three are the same"

EFFICIENT_QUESTIONS = [
    Question(
        "s1",
        "Try it: u<sub>A</sub> = %s + &radic;(&alpha;S) and u<sub>B</sub> = %s + &radic;(&beta;(1 "
        "&minus; S)). The partial derivatives with respect to good 1?" % (X1A, X1B),
        form=["&part;u<sub>A</sub>/&part;%s =" % X1A, BOX, "&nbsp; &part;u<sub>B</sub>/&part;%s =" % X1B, BOX],
        answers=[H("s1.0"), H("s1.1")],
        explain="Quasi-linear: money enters flat, so a marginal utility of smoke is already "
                "measured in good 1. The figure shows A's marginal benefit, &alpha;/(2&radic;(&alpha;S)), "
                "and B's marginal damage, &beta;/(2&radic;(&beta;(1 &minus; S)))."),
    Question(
        "s2",
        "Equation (1) sets them equal. With &alpha; = 1 and &beta; = 3, what is the efficient "
        "smoke level?",
        form=["S* =", BOX],
        answers=[H("s2.0")],
        mistakes=M({"s2.0~3/4": "Swapped: A's weight &alpha; goes on top. Who likes smoke?",
                    "s2.0~0": "Smoke hurts B, but zero is not efficient. Compare the two "
                              "curves near S = 0."}),
        hints=["Square both sides: &alpha;/S = &beta;/(1 &minus; S)."],
        explain="S* = &alpha;/(&alpha; + &beta;)."),
    Question(
        "s3",
        "Check: A's marginal benefit and B's marginal damage at S*?",
        form=["MB =", BOX, "&nbsp; MD =", BOX],
        answers=[H("s3.0"), H("s3.1")],
        mistakes=M({"s3.0~2": "Don't drop the 1/2: &alpha;/(2&radic;(&alpha;S)).",
                    "s3.1~2": "Don't drop the 1/2: &beta;/(2&radic;(&beta;(1 &minus; S)))."}),
        explain="Equal: the next puff is worth exactly what it costs B."),
    Question(
        "s4",
        "Smoke hurts B. Why is zero smoke still not efficient?",
        choices=[NOT_ZERO, RIGHT_A, GOOD_BOTH, ZERO_EFF],
        answers=[H("s4.c")],
        mistakes=M({
            "s4.c~" + RIGHT_A: "The planner ignores who holds rights.",
            "s4.c~" + GOOD_BOTH: "Smoke is a bad for B.",
            "s4.c~" + ZERO_EFF: "Cut the first puffs and A loses more than B gains.",
        }),
        explain="The efficient amount of pollution is not zero."),
    Question(
        "s5",
        "Review question 3: &alpha; = 3, &beta; = 1. The efficient level, then the outcome with no "
        "trading when (i) Aksel (A) may smoke and (ii) Brita (B) may insist on clean air?",
        form=["S* =", BOX, "&nbsp; (i) S =", BOX, "&nbsp; (ii) S =", BOX],
        answers=[H("s5.0"), H("s5.1"), H("s5.2")],
        mistakes=M({"s5.0~1/4": "That was &alpha; = 1, &beta; = 3. Now A cares more.",
                    "s5.1~3/4": "Without a price, smoke costs Aksel nothing. Why stop?",
                    "s5.2~3/4": "Brita gets nothing for allowing smoke. Why allow any?"}),
        explain="Over-pollution with A's right, under-pollution with B's."),
    Question(
        "s6",
        "Compare the three numbers.",
        choices=[CORNERS, A_WINS, B_WINS, ALL_SAME],
        answers=[H("s6.c")],
        mistakes=M({
            "s6.c~" + A_WINS: "1 is not 3/4.",
            "s6.c~" + B_WINS: "0 is not 3/4.",
            "s6.c~" + ALL_SAME: "Look at your three answers.",
        }),
        explain="Whoever owns the air, the unpriced outcome misses. The gap is the harm "
                "nobody paid for."),
]

efficient = GuidedProblem(
    "Part 3 &middot; The efficient level of smoke",
    "A smokes, B breathes, and they share one unit of air: S from A's end, 1 &minus; S "
    "from B's. Both have quasi-linear utility.",
    EFFICIENT_QUESTIONS, draw_efficient, figsize=(6.0, 5.4), whole_figure=True,
    outro="The planner counts the harm; the unpriced market does not.",
    sources=[NOTES("p. 4&ndash;7"), NOTES("p. 11, review question 3")],
)


# ======================================================================
# Part 4: pricing smoke, the homework (alpha = 1, beta = 3, w = 6, 6)
# ======================================================================

HOME = Smoke("log", 1, 3, 6, 6)


def draw_pricing(ax, stage):
    e = HOME
    _sbox(ax, 12)
    gp.dot(ax, 6, 1, r"$e_A$", 8, -14, colour=MUTE)
    gp.dot(ax, 6, 0, r"$e_B$", 8, 6, colour=MUTE)
    if stage >= 1:
        ax.axhline(0.25, color=GREEN, lw=2, label="contract curve")
    if stage >= 2:
        _s_budget(ax, 6, 0, 4, color=INK, lw=1.6, label="budget line")
    if stage >= 3:
        gp.dot(ax, 5, 0.25, "B's right", -8, 8, colour=NEW, ha="right")
        _s_icA(ax, e, 5, 0.25, color=A_COL, lw=1.2)
        _s_icB(ax, e, 5, 0.25, color=B_COL, lw=1.2)
    if stage >= 4:
        _s_budget(ax, 6, 1, 4, color=INK, lw=1.6, ls="--")
        gp.dot(ax, 9, 0.25, "A's right", 8, 8, colour=NEW)
        _s_icA(ax, e, 9, 0.25, color=A_COL, lw=1.2, ls="--")
        _s_icB(ax, e, 9, 0.25, color=B_COL, lw=1.2, ls="--")
    gp.legend(ax, loc="center right")


EFF_INV = "Efficiency: with clear, tradable rights and low transaction costs, bargaining reaches the efficient level. Invariance: that level is the same whoever holds the right, and this one needs quasi-linearity"
BOTH_QL = "Both claims need quasi-linear preferences"
EFF_QL = "Efficiency needs quasi-linearity; invariance always holds"
INV_ALWAYS = "Both always hold, whatever the preferences"

WHO_RICH = "Who ends up with how much good 1: the right is a transfer of wealth"
SMOKE_DIFF = "The amount of smoke"
PRICE_DIFF = "The price of smoke"
NOTHING_DIFF = "Nothing at all"

PRICING_QUESTIONS = [
    Question(
        "h1",
        "Worksheet task 1: u<sub>A</sub> = %s + &alpha; ln S, u<sub>B</sub> = %s + &beta; ln(1 &minus; S), "
        "&alpha; = 1, &beta; = 3, and 6 units of good 1 each. The efficient smoke level?" % (X1A, X1B),
        form=["S* =", BOX],
        answers=[H("h1.0")],
        mistakes=M({"h1.0~3/4": "Swapped: &alpha;/S = &beta;/(1 &minus; S) with &alpha; A's."}),
        explain="With these preferences every tangency has the same smoke: the contract curve "
                "is flat."),
    Question(
        "h2",
        "B holds the right to clean air, so A must buy smoke at a price p (good 1 is the "
        "numeraire). A's first-order condition is &alpha;/S = p. What price clears the smoke market?",
        form=["p =", BOX],
        answers=[H("h2.0")],
        mistakes=M({"h2.0~1/4": "That is S*. The price is A's marginal benefit there, &alpha;/S*.",
                    "h2.0~1": "&alpha;/S at S = 1/4."}),
        explain="Good 1 given up per unit of smoke: the worksheet's budget lines have slope "
                "&minus;4 in those units."),
    Question(
        "h3",
        "Starting from e<sub>B</sub> (no smoke, 6 each), A buys S* at that price. Who ends up "
        "with how much good 1?",
        form=["%s =" % X1A, BOX, "&nbsp; %s =" % X1B, BOX],
        answers=[H("h3.0"), H("h3.1")],
        mistakes=M({"h3.0~7": "A pays, B receives.",
                    "h3.0~2": "She pays 4 per unit, for 1/4 of a unit."}),
        explain="A pays B 1 unit of good 1 for the right to smoke 1/4."),
    Question(
        "h4",
        "Now flip it: A holds the right, starts at e<sub>A</sub> (S = 1), and B buys clean air "
        "1 &minus; S. The smoke level, then the good 1 for each?",
        form=["S =", BOX, "&nbsp; %s =" % X1A, BOX, "&nbsp; %s =" % X1B, BOX],
        answers=[H("h4.0"), H("h4.1"), H("h4.2")],
        mistakes=M({"h4.0~1": "B can now pay A to cut back. Is S = 1 efficient?",
                    "h4.1~5": "That was B's right. Now B pays A for 3/4 of clean air."}),
        explain="Same smoke, same price, different money."),
    Question(
        "h5",
        "Worksheet task 2: state Coase's two claims separately.",
        choices=[EFF_INV, BOTH_QL, EFF_QL, INV_ALWAYS],
        answers=[H("h5.c")],
        mistakes=M({
            "h5.c~" + BOTH_QL: "Bargaining reaches an efficient point with any preferences.",
            "h5.c~" + EFF_QL: "It is the other way round.",
            "h5.c~" + INV_ALWAYS: "With income effects, the richer side wants more of its good.",
        }),
        explain="Efficiency and invariance are two separate claims: the exam will separate them."),
    Question(
        "h6",
        "With quasi-linear preferences, what differs between the two assignments?",
        choices=[WHO_RICH, SMOKE_DIFF, PRICE_DIFF, NOTHING_DIFF],
        answers=[H("h6.c")],
        mistakes=M({
            "h6.c~" + SMOKE_DIFF: "S = 1/4 both times.",
            "h6.c~" + PRICE_DIFF: "p = 4 both times.",
            "h6.c~" + NOTHING_DIFF: "Compare A's good 1: 5 or 9.",
        }),
        explain="The property right is a transfer; the price does the coordinating."),
]

pricing = GuidedProblem(
    "Part 4 &middot; Pricing smoke: the Coase theorem",
    "Worksheet tasks 1&ndash;3: the smoke market and its box. Good 1 across, smoke up from A's corner. "
    "e<sub>A</sub>: A holds the right (S = 1); e<sub>B</sub>: B does (S = 0).",
    PRICING_QUESTIONS, draw_pricing, figsize=(6.6, 4.6),
    outro="A single price for smoke removes the failure, whichever side holds the right.",
    sources=[NOTES("p. 7&ndash;10"), NOTES("p. 10&ndash;11, worksheet")],
)


# ======================================================================
# Part 5: coordination without a price (review question 5)
# ======================================================================

def draw_satellite(ax, stage):
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    def card(x, y, text, colour, fill):
        ax.text(x, y, text, ha="center", va="center", color=colour, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.6", fc=fill, ec=colour))

    grey, light = MUTE, "#f3f4f6"
    ok, okf, bad, badf = GREEN, "#d1fae5", RED, "#fee2e2"
    card(1.7, 4.5, "Measurement\nwho imposes what", ok if stage >= 1 else grey,
         okf if stage >= 1 else light)
    card(5.0, 4.5, "Aggregation\none number for\neveryone's damage", grey, light)
    card(8.3, 4.5, "Matching\nwho could trade", ok if stage >= 1 else grey,
         okf if stage >= 1 else light)
    if stage >= 2:
        card(5.0, 2.0, "Incentives\nnobody reveals what\nthe externality is worth", bad, badf)
    if stage >= 3:
        ax.text(5.0, 0.4, "and whoever controls the measurement controls the policy",
                ha="center", color=NEW, fontsize=9)


MEAS_MATCH = "Measurement and matching"
ALL_THREE = "All three"
AGG_ONLY = "Aggregation only"
NONE_HELP = "None of them"

INCENTIVE = "The incentive problem: when your report sets what you pay, you shade it"
DATA = "A shortage of data"
COMPUTE = "Too little computing power"
LAW = "Nothing: with measurement, everything is solved"

POWER = "A concentration of power: whoever controls the measurement controls the policy"
PRIVACY_ONLY = "Nothing: measurement is a neutral instrument"
SLOWER = "Slower markets"
PRICES_UP = "Higher prices for everyone"

SATELLITE_QUESTIONS = [
    Question(
        "v1",
        "Review question 5: a startup says satellite monitoring of emissions will solve the smoke "
        "problem between two countries. Which of measurement, aggregation and matching can "
        "it help with?",
        choices=[MEAS_MATCH, ALL_THREE, AGG_ONLY, NONE_HELP],
        answers=[H("v1.c")],
        mistakes=M({
            "v1.c~" + ALL_THREE: "Aggregation needs a price that collects everyone's marginal "
                                 "damage. Can a satellite create one?",
            "v1.c~" + AGG_ONLY: "What does a satellite actually observe?",
            "v1.c~" + NONE_HELP: "Observed, attributable emissions are a big gain.",
        }),
        explain="Observable, attributable emissions let you define and enforce a property right."),
    Question(
        "v2",
        "Which problem can no amount of computation solve?",
        choices=[INCENTIVE, DATA, COMPUTE, LAW],
        answers=[H("v2.c")],
        mistakes=M({
            "v2.c~" + DATA: "Satellites supply the data. What do people still hide?",
            "v2.c~" + COMPUTE: "This is a strategic problem, not a data-processing one.",
            "v2.c~" + LAW: "Measuring emissions is not the same as knowing what they are worth.",
        }),
        explain="Satellites make the externality measurable and tradable, but nobody is made "
                "to reveal what it is worth to them."),
    Question(
        "v3",
        "And what new cost should you weigh?",
        choices=[POWER, PRIVACY_ONLY, SLOWER, PRICES_UP],
        answers=[H("v3.c")],
        mistakes=M({
            "v3.c~" + PRIVACY_ONLY: "Is the measurer's position really neutral?",
            "v3.c~" + SLOWER: "Matching gets faster, not slower.",
            "v3.c~" + PRICES_UP: "Think about who controls the numbers.",
        }),
        explain="A new concentration of power, not a neutral instrument."),
]

satellite = GuidedProblem(
    "Part 5 &middot; Coordination without a price",
    "The smoke market worked because smoke could be priced. Carbon, hedgerows and fish "
    "stocks have no such price, and three things break at once.",
    SATELLITE_QUESTIONS, draw_satellite, figsize=(6.4, 3.8),
    outro="Technology helps with measurement and matching; incentives stay an economic problem.",
    sources=[NOTES("p. 9&ndash;10"), NOTES("p. 11, review question 5")],
)


# ======================================================================
# Part 6: problem A7.1, a contract curve with numbers
# ======================================================================

TRADE = Economy(0.5, 0.5, (10, 25), (5, 5))


def draw_trade(ax, stage):
    e = TRADE
    if stage == 0:
        ax.axis("off")
        gp.start(ax)
        return
    ed.box(ax, e.X, e.Y)
    gp.dot(ax, 10, 25, r"$\omega$", 8, -12, colour=INK)
    if stage >= 3:
        ed.contract(ax, e, color=GREEN, lw=2, label="contract curve")
        for x in (4, 10):
            ed.ic_a(ax, e, x, 2 * x, color=A_COL, lw=1)
            ed.ic_b(ax, e, x, 2 * x, color=B_COL, lw=1)
    gp.legend(ax, loc="lower right")


CANCEL = "Identical tastes: the cross terms cancel on both sides, leaving no curvature"
BIG_A = "A is the bigger country"
EQUAL_P = "The price ratio is 1"
DOUBLE = "Country A has twice as much"

TRADE_QUESTIONS = [
    Question(
        "p1",
        "A7.1: u = x<sup>1/2</sup>c<sup>1/2</sup> for both. A has 10 of services x and 25 "
        "of goods c; B has 5 and 5 (billion). The box's dimensions?",
        form=["&omega;<sup>x</sup> =", BOX, "&nbsp; &omega;<sup>c</sup> =", BOX],
        answers=[H("p1.0"), H("p1.1")],
        mistakes=M({"p1.0~10": "Add B's 5.", "p1.1~25": "Add B's 5."}),
        explain="A tall box: goods are twice as plentiful as services."),
    Question(
        "p2",
        "Set c<sub>A</sub>/x<sub>A</sub> = (30 &minus; c<sub>A</sub>)/(15 &minus; x<sub>A</sub>), "
        "cross-multiply and cancel the common term. What is left?",
        form=["15c<sub>A</sub> =", BOX, "x<sub>A</sub>"],
        answers=[H("p2.0")],
        mistakes=M({"p2.0~15": "Cross-multiply: c<sub>A</sub>(15 &minus; x<sub>A</sub>) = "
                               "x<sub>A</sub>(30 &minus; c<sub>A</sub>)."}),
        explain="The c<sub>A</sub>x<sub>A</sub> terms cancel."),
    Question(
        "p3",
        "So the contract curve is c<sub>A</sub> = k&middot;x<sub>A</sub>. Its slope k?",
        form=["slope =", BOX],
        answers=[H("p3.0")],
        mistakes=M({"p3.0~1/2": "Upside down: c<sub>A</sub> on the left."}),
        explain="&omega;<sup>c</sup>/&omega;<sup>x</sup>: each extra unit of services for A comes "
                "with 2 units of goods."),
    Question(
        "p4",
        "Why is it a straight line?",
        choices=[CANCEL, BIG_A, EQUAL_P, DOUBLE],
        answers=[H("p4.c")],
        mistakes=M({
            "p4.c~" + BIG_A: "Size does not enter the MRS condition.",
            "p4.c~" + EQUAL_P: "There are no prices in a contract curve.",
            "p4.c~" + DOUBLE: "The endowments set where &omega; sits, not the contract curve's shape.",
        }),
        explain="Session 6's A6.1, with numbers attached: the box's diagonal."),
]

trade = GuidedProblem(
    "Part 6 &middot; A contract curve with numbers: A7.1",
    "Session 6's contract curve with numbers attached. The equal-MRS condition is handed to "
    "you here; on an exam you write it down yourself.",
    TRADE_QUESTIONS, draw_trade, figsize=(4.8, 5.8),
    outro="About 10% of a full exam paper.",
    sources=[PS("A7.1")],
)


# ======================================================================
# Part 7: problem A7.2, clean air (an illustrative quasi-linear economy)
# ======================================================================
# A likes clean air C, B likes pollution P = 1 - C. For the picture only:
# u_A = x + 4C - 2C^2 and u_B = x + 2P - P^2, so A will pay 4 - 4C for clean
# air and B asks 2 - 2P to give up pollution. Clearing is at pC = 4/3.

def _air_icA(ax, level, **kw):
    P = np.linspace(0, 1, 200)
    C = 1 - P
    ax.plot(level - (4 * C - 2 * C ** 2), P, **kw)


def _air_icB(ax, level, X, **kw):
    P = np.linspace(0, 1, 200)
    ax.plot(X - (level - (2 * P - P ** 2)), P, **kw)


def _air_point(q, who):
    # Where A (buying clean air) or B (selling it) wants to be at price q.
    C = 1 - q / 4 if who == "A" else q / 2
    return 6 - q * C, 1 - C


def _air_levels(x, P):
    C = 1 - P
    return x + 4 * C - 2 * C ** 2, (12 - x) + 2 * P - P ** 2


def draw_air(ax, stage):
    _sbox(ax, 12, "P", "C")
    gp.dot(ax, 6, 1, "M", 8, -14, colour=INK)
    uA, uB = _air_levels(6, 1)
    if stage >= 1:
        _air_icA(ax, uA, color=A_COL, lw=1.3)
        _air_icB(ax, uB, 12, color=B_COL, lw=1.3)
        P = np.linspace(0, 1, 200)
        lo = uA - (4 * (1 - P) - 2 * (1 - P) ** 2)
        hi = 12 - (uB - (2 * P - P ** 2))
        ax.fill_betweenx(P, lo, hi, where=lo < hi, color=HALF, alpha=0.15, lw=0)
        ax.annotate("gains from trade", xy=(4.9, 0.6), xytext=(1.0, 0.75), color=HALF,
                    fontsize=9, arrowprops=dict(arrowstyle="-|>", color=HALF, lw=1))
    if stage >= 4:
        q = 0.6
        _s_budget(ax, 6, 1, -q, color=GREY, lw=1.4, label="price too low")
        for who, col in (("A", A_COL), ("B", B_COL)):
            x, Pp = _air_point(q, who)
            gp.dot(ax, x, Pp, "", colour=col)
    if stage >= 5:
        q = 4 / 3
        _s_budget(ax, 6, 1, -q, color=INK, lw=1.6, label="clearing price")
        x, Pp = _air_point(q, "A")
        gp.dot(ax, x, Pp, "E", 8, 4, colour=GREEN)
        ax.axhline(1 / 3, color=GREEN, lw=1.6, ls="--", label="contract curve")
    gp.legend(ax, loc="lower right")


NO_COST = "B pollutes fully, P = 1: clean air is missing from B's budget, so B never faces the cost to A, and at that corner A would pay more for cleaner air than B needs to give it up"
EFF_M = "The equilibrium is efficient, because the goods market clears"
B_ZERO = "B chooses P = 0, because pollution is costly"
A_ALL = "A chooses C = 1, because she likes clean air"

BUD_OK = "A: p1·xA + pC·C = p1·ωA;  B: p1·xB = p1·ωB + pC·C"
BUD_REV = "A: p1·xA = p1·ωA + pC·C;  B: p1·xB + pC·C = p1·ωB"
BUD_BOTH = "Both: p1·x + pC·C = p1·ω"
BUD_NONE = "Unchanged: p1·xA = p1·ωA and p1·xB = p1·ωB"

TRANSFER = "They cancel: the quota payment is a transfer, so goods still add up (Walras' law)"
ADD_UP = "They add up to 2·pC·C, an extra cost to the economy"
DOUBLE_C = "They make clean air count twice"
LEFT_OVER = "They leave a surplus for the government"

YES_APART = "Yes: each country is at a tangency, but at different points on the line, so the market does not clear"
NO_DIFFER = "No: at the wrong price the MRSs differ"
CLEARS_ANY = "Yes, and so the market clears"
ONLY_A = "Only A's MRS equals the price ratio"

CLEARING = "Market clearing: the one price where A's demand for clean air equals B's supply puts both tangencies at one point, on the contract curve"
EQUAL_MRS = "Equal MRSs alone"
LAW_ONLY = "The property right alone"
PLANNER_ONLY = "Only a planner can find it"

AIR_QUESTIONS = [
    Question(
        "q1",
        "A7.2 (A): A enjoys clean air C, B enjoys pollution P = 1 &minus; C. There is no rule "
        "of law, so polluting costs nothing. Why is the competitive equilibrium not Pareto "
        "efficient? (The figure uses illustrative preferences.)",
        choices=[NO_COST, EFF_M, B_ZERO, A_ALL],
        answers=[H("q1.c")],
        mistakes=M({
            "q1.c~" + EFF_M: "Clearing the goods market says nothing about the air. Does C "
                             "appear in B's budget?",
            "q1.c~" + B_ZERO: "Pollution costs B nothing here.",
            "q1.c~" + A_ALL: "A has no instrument: she cannot choose the air.",
        }),
        explain="At M the curves cross, opening a wedge of trades where A pays B in goods for "
                "cleaner air."),
    Question(
        "q2",
        "(B) Country B, the polluter, is given property rights to the air, and quotas of clean "
        "air sell at pC. The two budget constraints?",
        choices=[BUD_OK, BUD_REV, BUD_BOTH, BUD_NONE],
        answers=[H("q2.c")],
        mistakes=M({
            "q2.c~" + BUD_REV: "Who owns the air, and so who sells it?",
            "q2.c~" + BUD_BOTH: "A payment has a payer and a receiver.",
            "q2.c~" + BUD_NONE: "That is part A's world, with no price on the air.",
        }),
        explain="Clean air is now expenditure for A and income for B."),
    Question(
        "q3",
        "Add the two constraints. What happens to the pC&middot;C terms?",
        choices=[TRANSFER, ADD_UP, DOUBLE_C, LEFT_OVER],
        answers=[H("q3.c")],
        mistakes=M({
            "q3.c~" + ADD_UP: "One side pays exactly what the other receives.",
            "q3.c~" + DOUBLE_C: "Write both out and add.",
            "q3.c~" + LEFT_OVER: "There is no government in this economy.",
        }),
        explain="Polluting now costs B: it is forgone quota revenue."),
    Question(
        "q4",
        "(C) At a price pC/p1 that is too low, A wants more clean air than B will sell. Is each "
        "country's MRS equal to the price ratio?",
        choices=[YES_APART, NO_DIFFER, CLEARS_ANY, ONLY_A],
        answers=[H("q4.c")],
        mistakes=M({
            "q4.c~" + NO_DIFFER: "Each one optimizes against the price, so each MRS equals it.",
            "q4.c~" + CLEARS_ANY: "Compare the two points on the line.",
            "q4.c~" + ONLY_A: "B optimizes too.",
        }),
        explain="Equal MRSs hold at every price, so they are not enough for equilibrium."),
    Question(
        "q5",
        "So what selects the efficient point?",
        choices=[CLEARING, EQUAL_MRS, LAW_ONLY, PLANNER_ONLY],
        answers=[H("q5.c")],
        mistakes=M({
            "q5.c~" + EQUAL_MRS: "Step 4 showed they hold even where the market fails to clear.",
            "q5.c~" + LAW_ONLY: "The right creates the market; something else picks the price.",
            "q5.c~" + PLANNER_ONLY: "The market finds it by itself, once the air has a price.",
        }),
        explain="Equal MRS is necessary for efficiency, but any price delivers it; clearing picks "
                "the efficient one."),
]

air = GuidedProblem(
    "Part 7 &middot; Clean air: A7.2",
    "The closest thing in this course to a question that has appeared on the real exam twice. "
    "Good 1 across; pollution up from A's corner, clean air down from B's.",
    AIR_QUESTIONS, draw_air, figsize=(6.6, 4.6),
    outro="About 15&ndash;20% of a full exam paper.",
    sources=[PS("A7.2")],
)


# ======================================================================
# Part 8: problem A7.3, invariance and its limits
# ======================================================================

INV = Smoke("log", 1 / 3, 2 / 3, 5, 15)


def _invariance_layer(ax, stage, zoom):
    # At p = 1 a budget line moves good 1 by at most one unit, a sliver of
    # the 20-wide box, so the inset repeats the picture zoomed in.
    e = INV
    gp.dot(ax, 5, 1, r"$e_A$", 8, -14, colour=MUTE)
    gp.dot(ax, 5, 0, r"$e_B$", 8, 6, colour=MUTE)
    if stage >= 1:
        ax.axhline(1 / 3, color=GREEN, lw=2, label=None if zoom else "contract curve")
    if stage >= 2:
        _s_budget(ax, 5, 0, 1, color=INK, lw=1.6, label=None if zoom else "budget, B owns")
    if stage >= 3:
        gp.dot(ax, 14 / 3, 1 / 3, "B owns" if zoom else "", -8, 8, colour=NEW, ha="right")
        if zoom:
            _s_icA(ax, e, 14 / 3, 1 / 3, color=A_COL, lw=1.1)
            _s_icB(ax, e, 14 / 3, 1 / 3, color=B_COL, lw=1.1)
    if stage >= 4:
        _s_budget(ax, 5, 1, 1, color=INK, lw=1.6, ls="--",
                  label=None if zoom else "budget, A owns")
        gp.dot(ax, 17 / 3, 1 / 3, "A owns" if zoom else "", 8, 8, colour=NEW)


def draw_invariance(ax, stage):
    _sbox(ax, 20)
    _invariance_layer(ax, stage, zoom=False)
    gp.legend(ax, loc="upper right")
    if stage >= 2:
        z = ax.inset_axes([0.4, 0.06, 0.42, 0.6])
        z.set_xlim(3.6, 6.8)
        z.set_ylim(0, 1)
        z.set_xticks([])
        z.set_yticks([])
        for side in z.spines.values():
            side.set_color(MUTE)
        _invariance_layer(z, stage, zoom=True)
        z.set_title("zoomed in", loc="left", color=MUTE, fontsize=8.5)
        ax.indicate_inset_zoom(z, edgecolor=MUTE)


QL_ONLY = "No: it needs quasi-linear utility; with income effects the richer side's willingness to pay rises, so who owns the air moves the efficient level"
COASE_ALL = "Yes: the Coase theorem always gives the same level"
LOG_ONLY = "No: it needs logarithmic utility"
LOW_TC = "Yes, as long as transaction costs are low"

S_FALLS = "It falls: B is richer and buys more clean air"
S_RISES = "It rises"
S_SAME = "It stays the same"
S_ZERO = "It goes to zero"

INVARIANCE_QUESTIONS = [
    Question(
        "r1",
        "A7.3: u<sub>A</sub> = x<sub>A</sub> + (1/3) ln S, u<sub>B</sub> = x<sub>B</sub> + "
        "(2/3) ln(1 &minus; S), &omega;<sub>A</sub> = 5, &omega;<sub>B</sub> = 15. Equate the "
        "two first-order conditions, 1/(3S) = 2/(3(1 &minus; S)). The smoke and the clean air?",
        form=["S* =", BOX, "&nbsp; c* =", BOX],
        answers=[H("r1.0"), H("r1.1")],
        mistakes=M({"r1.0~2/3": "Swapped: 1 &minus; S = 2S."}),
        explain="Where A's marginal benefit meets B's marginal damage."),
    Question(
        "r2",
        "The permit price p (in good 1 per unit of S)?",
        form=["p =", BOX],
        answers=[H("r2.0")],
        mistakes=M({"r2.0~1/3": "That is S*. p = 1/(3S*)."}),
        explain="One price serves both regimes: ownership only decides who pays whom."),
    Question(
        "r3",
        "Case 1, B owns clean air: x<sub>A</sub> = 5 &minus; pS and x<sub>B</sub> = 15 + pS. "
        "Each country's good?",
        form=["x<sub>A</sub> =", BOX, "&nbsp; x<sub>B</sub> =", BOX],
        answers=[H("r3.0"), H("r3.1")],
        mistakes=M({"r3.0~16/3": "A pays for smoke: subtract."}),
        explain="A pays B 1/3 for the right to smoke 1/3."),
    Question(
        "r4",
        "Case 2, A owns the right and sells clean air 1 &minus; S to B. The smoke level and "
        "each country's good?",
        form=["S =", BOX, "&nbsp; x<sub>A</sub> =", BOX, "&nbsp; x<sub>B</sub> =", BOX],
        answers=[H("r4.0"), H("r4.1"), H("r4.2")],
        mistakes=M({"r4.0~1": "B can pay A to cut back.",
                    "r4.1~14/3": "That was case 1. Now B pays A for 2/3 of clean air."}),
        explain="(a) shown: same air quality, different money."),
    Question(
        "r5",
        "(b) Is this a general result?",
        choices=[QL_ONLY, COASE_ALL, LOG_ONLY, LOW_TC],
        answers=[H("r5.c")],
        mistakes=M({
            "r5.c~" + COASE_ALL: "Coase's efficiency claim is general. Is the invariance?",
            "r5.c~" + LOG_ONLY: "A7.3 used logs, the notes' Try it used square roots, and "
                                "both gave invariance. What do they share?",
            "r5.c~" + LOW_TC: "Low transaction costs give efficiency. What gives invariance?",
        }),
        explain="Willingness to pay depends on S alone only when good 1 enters linearly."),
    Question(
        "r6",
        "Without quasi-linearity, suppose B gets the right to clean air and clean air is a "
        "normal good. Compared with A owning the right, the efficient S...",
        choices=[S_FALLS, S_RISES, S_SAME, S_ZERO],
        answers=[H("r6.c")],
        mistakes=M({
            "r6.c~" + S_RISES: "Who got richer, and what does that side want more of?",
            "r6.c~" + S_SAME: "That is the quasi-linear case.",
            "r6.c~" + S_ZERO: "Efficient smoke stays positive: the first puffs are still worth a lot to A.",
        }),
        explain="Varian ch. 35: in general the efficient amount of the externality depends on "
                "who holds the property right."),
]

invariance = GuidedProblem(
    "Part 8 &middot; Is the invariance general? A7.3",
    "Quasi-linear preferences, numbers attached. Good 1 across (20 in all), smoke up from "
    "A's corner.",
    INVARIANCE_QUESTIONS, draw_invariance, figsize=(6.6, 4.6),
    outro="Coase's efficiency claim survives anywhere; the invariance of S needs quasi-linearity. "
          "The sandbox's orange preset shows it breaking.",
    sources=[PS("A7.3")],
)


# ======================================================================
# Where every step comes from (printed pages of s07_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "c1": NOTES("p. 1 &middot; step 1"), "c2": NOTES("p. 2 &middot; step 3"),
    "c3": NOTES("p. 2 &middot; step 4"), "c4": NOTES("p. 2 &middot; step 4"),
    "c5": NOTES("p. 2 &middot; MRS"), "c6": NOTES("p. 2 &middot; contract curve"),
    "c7": NOTES("p. 2 &middot; first welfare theorem"),
    "d1": NOTES("p. 11 &middot; review question 1 (a)"), "d2": NOTES("p. 11 &middot; review question 1 (b)"),
    "d3": NOTES("p. 11 &middot; review question 1 (c)"), "d4": NOTES("p. 4 &middot; Figure 3"),
    "d5": NOTES("p. 4 &middot; Figure 3"),
    "s1": NOTES("p. 6 &middot; Try it"), "s2": NOTES("p. 6 &middot; Try it"),
    "s3": NOTES("p. 6 &middot; Figure 5"), "s4": NOTES("p. 7 &middot; over-pollution"),
    "s5": NOTES("p. 11 &middot; review question 3"), "s6": NOTES("p. 11 &middot; review question 3"),
    "h1": NOTES("p. 10 &middot; worksheet task 1"), "h2": NOTES("p. 10 &middot; worksheet task 1"),
    "h3": NOTES("p. 10 &middot; worksheet task 1"), "h4": NOTES("p. 10 &middot; worksheet task 1"),
    "h5": NOTES("p. 10 &middot; worksheet task 2"), "h6": NOTES("p. 8 &middot; Coase"),
    "v1": NOTES("p. 11 &middot; review question 5"), "v2": NOTES("p. 10 &middot; incentives"),
    "v3": NOTES("p. 10 &middot; incentives"),
    "p1": PS("A7.1"), "p2": PS("A7.1"), "p3": PS("A7.1"), "p4": PS("A7.1"),
    "q1": PS("A7.2 (A)"), "q2": PS("A7.2 (B)"), "q3": PS("A7.2 (B)"), "q4": PS("A7.2 (C)"), "q5": PS("A7.2 (C)"),
    "r1": PS("A7.3 (a)"), "r2": PS("A7.3 (a)"), "r3": PS("A7.3 (a)"), "r4": PS("A7.3 (a)"),
    "r5": PS("A7.3 (b)"), "r6": PS("A7.3 (b)"),
}

for _q in (RECAP_QUESTIONS + DEFINE_QUESTIONS + EFFICIENT_QUESTIONS + PRICING_QUESTIONS
           + SATELLITE_QUESTIONS + TRADE_QUESTIONS + AIR_QUESTIONS + INVARIANCE_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
