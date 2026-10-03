"""
guided_s06.py - session 6 guided page: general equilibrium and exchange.

    Part 1  box        reading the Edgeworth box (review questions 1-2)
    Part 2  economy    the notes' worked exchange economy, end to end
    Part 3  excess     excess demand and Walras' law
    Part 4  worksheet  the notes' worksheet: box and excess demand
    Part 5  same       problem A6.1: identical tastes, a straight contract curve
    Part 6  different  problem A6.2: different tastes, a bent one
    Part 7  theorems   the welfare theorems and the core

Answers are hashes in answers_s06.py, generated from
answer_keys/s06_keys.py in the private repo. The maths is equilibrium.py.
"""

import numpy as np

from equilibrium import Economy
from guided import BOX, GuidedProblem, Question, tag
from guided_s03 import (CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW, _dot, _legend,
                        _start)
from guided_s04 import _arrow

try:
    from answers_s06 import HASHES
except ImportError:
    HASHES = {}

PS = lambda part: tag("problem", "Problem " + part)
NOTES = lambda where: tag("notes", "Notes " + where)
XA, YA, XB, YB = "x<sub>A</sub>", "y<sub>A</sub>", "x<sub>B</sub>", "y<sub>B</sub>"
MA, MB = "m<sub>A</sub>", "m<sub>B</sub>"
ZX, ZY = "z<sub>x</sub>", "z<sub>y</sub>"
A_COL, B_COL = LINE, CURVE          # A blue, B pink, as in the notes' figures


def H(key):
    return HASHES.get(key, "missing:" + key)


def M(messages):
    return {H(k): v for k, v in messages.items()}


# ------------------------------------------------------------------ drawing ---

def _box(ax, X, Y):
    # A's origin bottom left, B's top right, rotated through 180 degrees.
    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    kw = dict(color=INK, fontsize=10)
    # Each axis label sits at the far end of its own axis, arrow pointing away
    # from its owner's corner.
    ax.text(X, -0.025 * Y, r"$x_A$ $\rightarrow$", ha="right", va="top", **kw)
    ax.text(-0.025 * X, Y, r"$y_A$ $\uparrow$", ha="right", va="top", **kw)
    ax.text(0, 1.025 * Y, r"$\leftarrow$ $x_B$", ha="left", va="bottom", **kw)
    ax.text(1.025 * X, 0, r"$y_B$ $\downarrow$", ha="left", va="bottom", **kw)
    ax.text(-0.025 * X, -0.025 * Y, "A", ha="right", va="top", color=A_COL,
            fontsize=12, weight="bold")
    ax.text(1.025 * X, 1.025 * Y, "B", ha="left", va="bottom", color=B_COL,
            fontsize=12, weight="bold")


def _xs(e, n=400):
    return np.linspace(e.X * 0.004, e.X * 0.996, n)


def _icA(ax, e, x, y, **kw):
    level = e.uA(x, y)
    xs = _xs(e)
    ax.plot(xs, np.clip([e.icA(level, v) for v in xs], -1, e.Y + 1), **kw)


def _icB(ax, e, x, y, **kw):
    # Through A's point (x, y): B holds what is left.
    level = e.uB(*e.b_bundle(x, y))
    xs = _xs(e)
    ax.plot(xs, np.clip([e.icB(level, v) for v in xs], -1, e.Y + 1), **kw)


def _lens(ax, e, x, y, label="both better off"):
    xs = _xs(e)
    lo = np.clip([e.icA(e.uA(x, y), v) for v in xs], 0, e.Y)
    hi = np.clip([e.icB(e.uB(*e.b_bundle(x, y)), v) for v in xs], 0, e.Y)
    ax.fill_between(xs, lo, hi, where=lo < hi, color=HALF, alpha=0.16, lw=0, label=label)


def _contract(ax, e, **kw):
    xs = np.linspace(0, e.X, 300)
    ax.plot(xs, [e.contract(v) for v in xs], **kw)


def _pline(ax, e, p, x0, y0, **kw):
    # The price line through (x0, y0), slope -p, across the box.
    xs = np.array([0, e.X])
    ax.plot(xs, y0 - p * (xs - x0), **kw)


def _zframe(ax, pmax, zlo, zhi):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, pmax)
    ax.set_ylim(zlo, zhi)
    ax.set_xlabel(r"$p = p_x/p_y$", color=INK, fontsize=10, loc="right")
    ax.set_ylabel("excess demand", color=INK, fontsize=10, loc="top")


def _zcurves(ax, e, pmax):
    ps = np.linspace(pmax * 0.12, pmax, 200)
    z = np.array([e.excess(p) for p in ps])
    ax.plot(ps, z[:, 0], color=A_COL, lw=2, label=r"$z_x$")
    ax.plot(ps, z[:, 1], color=B_COL, lw=2, label=r"$z_y$")


# ======================================================================
# Part 1: reading the box (review questions 1-2: Astrid and Birk)
# ======================================================================

ASTRID = Economy(2 / 3, 1 / 2, (3, 9), (3, 3))


def draw_box(ax, stage):
    e = ASTRID
    if stage == 0:
        ax.axis("off")
        _start(ax)
        return
    _box(ax, e.X, e.Y)
    if stage >= 2:
        _dot(ax, 3, 9, r"$\omega$", 8, 4, colour=INK)
    if stage >= 3:
        _icA(ax, e, 3, 9, color=A_COL, lw=1.6, label="A through " + r"$\omega$")
        _icB(ax, e, 3, 9, color=B_COL, lw=1.6, label="B through " + r"$\omega$")
    if stage >= 4:
        _lens(ax, e, 3, 9)
    if stage >= 5:
        _dot(ax, 4, 6, "A (4, 6)\nB (2, 6)", 14, -10, colour=GREEN)
    if stage >= 6:
        _icA(ax, e, 4, 6, color=A_COL, lw=1.2, ls="--")
        _icB(ax, e, 4, 6, color=B_COL, lw=1.2, ls="--")
        _pline(ax, e, 3, 4, 6, color=INK, lw=0.8, ls=":")
    _legend(ax, loc="upper right")


DOWNRIGHT = "A gets more x and gives up y: down and to the right of ω"
UPLEFT = "A gets more y and gives up x: up and to the left of ω"
NO_TRADE = "Nowhere: ω is already efficient"
MORE_ALL = "Both get more of everything"

EFF_YES = "Yes: the MRSs are equal, so the curves touch and no trade helps both"
EFF_NO_START = "No: Birk ends up with less x than he started with"
EFF_SAME_Y = "Yes, because both get 6 units of y"
EFF_PRICES = "It cannot be told without prices"

BOX_QUESTIONS = [
    Question(
        "b1",
        "Astrid (A) owns &omega;<sub>A</sub> = (3, 9) and Birk (B) owns &omega;<sub>B</sub> "
        "= (3, 3). How wide and how tall is the Edgeworth box?",
        form=["width", BOX, "&nbsp; height", BOX],
        answers=[H("b1.0"), H("b1.1")],
        mistakes=M({"b1.0~3": "That is Astrid's x alone. The sides measure the economy's "
                              "totals.",
                    "b1.1~9": "That is Astrid's y alone. Add Birk's."}),
        explain="Every point inside is a complete allocation that uses up exactly the totals."),
    Question(
        "b2",
        "Mark &omega;. It sits at (3, 9) from A's corner. Measured from B's corner (top "
        "right), how far is it to the left, and how far down?",
        form=["left", BOX, "&nbsp; down", BOX],
        answers=[H("b2.0"), H("b2.1")],
        mistakes=M({"b2.1~9": "That is Astrid's y. From B's corner you read B's own "
                              "bundle."}),
        explain="One dot, two readings: A's bundle from the bottom left, B's from the top "
                "right."),
    Question(
        "b3",
        "Preferences are u<sub>A</sub> = x<sup>2/3</sup>y<sup>1/3</sup> and u<sub>B</sub> = "
        "x<sup>1/2</sup>y<sup>1/2</sup>. Each one's MRS at &omega;?",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("b3.0"), H("b3.1")],
        mistakes=M({"b3.0~3": "Don't drop the exponent ratio: MRS<sub>A</sub> = "
                              "((2/3)/(1/3))&middot;y/x.",
                    "b3.0~3/2": "Upside down: MRS = (&part;u/&part;x)/(&part;u/&part;y) = "
                                "(a/(1 &minus; a))&middot;y/x.",
                    "b3.1~3": "Use Birk's bundle, (3, 3), not Astrid's."}),
        hints=["For x<sup>a</sup>y<sup>1&minus;a</sup>, MRS = (a/(1 &minus; a))&middot;y/x."],
        explain="Astrid would give 6 units of y for one more x; Birk only 1. The curves "
                "cross at &omega;."),
    Question(
        "b4",
        "So where are the trades that make both better off?",
        choices=[DOWNRIGHT, UPLEFT, NO_TRADE, MORE_ALL],
        answers=[H("b4.c")],
        mistakes=M({
            "b4.c~" + UPLEFT: "Astrid values x at 6 units of y, Birk at 1. Who should end "
                              "up with more x?",
            "b4.c~" + NO_TRADE: "The MRSs differ, so the curves cross at &omega; and leave a "
                                "lens between them.",
            "b4.c~" + MORE_ALL: "The box holds the totals: whatever one gains of a good, "
                                "the other gives up.",
        }),
        explain="The lens between the two curves: A pushes north-east on her map, B "
                "south-west on his."),
    Question(
        "b5",
        "An allocation gives Astrid (4, 6). Read off Birk's bundle.",
        form=["%s =" % XB, BOX, "&nbsp; %s =" % YB, BOX],
        answers=[H("b5.0"), H("b5.1")],
        mistakes=M({"b5.0~3": "That is his endowment. He gets the totals minus Astrid's.",
                    "b5.1~3": "That is his endowment. He gets the totals minus Astrid's."}),
        explain="Totals minus Astrid's bundle."),
    Question(
        "b6",
        "Each one's MRS at that allocation?",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("b6.0"), H("b6.1")],
        mistakes=M({"b6.1~1": "That was at &omega;. Use Birk's new bundle (2, 6).",
                    "b6.0~3/2": "MRS<sub>A</sub> = 2y/x."}),
        explain="Equal."),
    Question(
        "b7",
        "Is that allocation Pareto efficient?",
        choices=[EFF_YES, EFF_NO_START, EFF_SAME_Y, EFF_PRICES],
        answers=[H("b7.c")],
        mistakes=M({
            "b7.c~" + EFF_NO_START: "Efficiency compares with other allocations, not with the "
                                    "starting point.",
            "b7.c~" + EFF_SAME_Y: "Equal amounts are not the test. Compare the MRSs.",
            "b7.c~" + EFF_PRICES: "Efficiency needs no prices, just the two MRSs.",
        }),
        explain="Curves that touch leave no lens, so any move hurts someone."),
]

box = GuidedProblem(
    "Part 1 &middot; Reading the Edgeworth box",
    "Two people, two goods, no production. Astrid and Birk are from the notes' review "
    "questions; their box is twice as tall as it is wide.",
    BOX_QUESTIONS, draw_box, figsize=(5.2, 5.6),
    outro="Hold on to (4, 6): it comes back in review question 4.",
    sources=[NOTES("p. 2&ndash;3"), NOTES("p. 15&ndash;16, review questions 1&ndash;2")],
)


# ======================================================================
# Part 2: the worked exchange economy (notes p. 6-9)
# ======================================================================

WORKED = Economy(0.75, 0.5, (8, 8), (4, 4))


def draw_economy(ax, stage):
    e = WORKED
    _box(ax, e.X, e.Y)
    _dot(ax, 8, 8, r"$\omega$", 8, 4, colour=INK)
    if stage in (1, 2):
        for p in (0.5, 1, 4):
            _pline(ax, e, p, 8, 8, color=GREY, lw=1)
        ax.text(0.3, 0.6, "every price line\npasses through " + r"$\omega$", color=GREY,
                fontsize=9)
    if stage >= 3:
        _pline(ax, e, 2, 8, 8, color=INK, lw=1.6, label="price line, slope " + r"$-p^*$")
    if stage >= 5:
        _dot(ax, 9, 6, "(9, 6)", 8, -14, colour=GREEN)
    if stage >= 6:
        _arrow(ax, (8, 8), (9, 6), GREEN)
    if stage >= 8:
        _icA(ax, e, 9, 6, color=A_COL, lw=1.4, label="A")
        _icB(ax, e, 9, 6, color=B_COL, lw=1.4, label="B")
    if stage >= 9:
        _contract(ax, e, color=GREEN, lw=2, label="contract curve")
    _legend(ax, loc="center left")


ECONOMY_QUESTIONS = [
    Question(
        "e1",
        "Income is now the market value of what you own. With p<sub>y</sub> = 1 and p = "
        "p<sub>x</sub>/p<sub>y</sub>, write both incomes.",
        form=["%s =" % MA, BOX, "p +", BOX, "&nbsp; %s =" % MB, BOX, "p +", BOX],
        answers=[H("e1.0"), H("e1.1"), H("e1.2"), H("e1.3")],
        hints=["m = p&middot;&omega;<sup>x</sup> + 1&middot;&omega;<sup>y</sup>."],
        explain="A price change now rotates the budget line around &omega;, because it "
                "changes what you can buy and what you are worth."),
    Question(
        "e2",
        "A spends 3/4 of her income on x, B spends 1/2. Write total demand for x, "
        "%s + %s, as a function of p." % (XA, XB),
        form=["%s + %s =" % (XA, XB), BOX, "+", BOX, "/ p"],
        answers=[H("e2.0"), H("e2.1")],
        mistakes=M({"e2.0~6": "That is A's demand alone, 6 + 6/p. Add B's.",
                    "e2.1~6": "That is A's demand alone, 6 + 6/p. Add B's."}),
        hints=["%s = (3/4)(8p + 8)/p = 6 + 6/p." % XA],
        explain="Everything now hangs on one number, p."),
    Question(
        "e3",
        "Clear the market for x: total demand equals what exists. The price ratio p*?",
        form=["p* =", BOX],
        answers=[H("e3.0")],
        mistakes=M({"e3.0~1/2": "Upside down. 8 + 8/p = 12.",
                    "e3.0~1": "Both totals are 12, but the tastes differ. Solve 8 + 8/p = 12."}),
        explain="Good x is worth twice good y. Only the ratio is pinned down."),
    Question(
        "e4",
        "Incomes at p*?",
        form=["%s =" % MA, BOX, "&nbsp; %s =" % MB, BOX],
        answers=[H("e4.0"), H("e4.1")],
        mistakes=M({"e4.0~16": "Value both goods: 2&middot;8 + 1&middot;8."}),
        explain="A owns more, so she is richer."),
    Question(
        "e5",
        "The allocation: A's bundle, then B's.",
        form=["A: (", BOX, ",", BOX, ") &nbsp; B: (", BOX, ",", BOX, ")"],
        answers=[H("e5.0"), H("e5.1"), H("e5.2"), H("e5.3")],
        mistakes=M({"e5.0~18": "%s = a&middot;%s/p<sub>x</sub>: divide by the price 2." % (XA, MA),
                    "e5.1~18": "%s = (1 &minus; a)&middot;%s/p<sub>y</sub> = 24/4." % (YA, MA)}),
        explain="Check: 9 + 3 = 12 and 6 + 6 = 12. Market y cleared too, and you never "
                "imposed it."),
    Question(
        "e6",
        "A's net trade: how much x does she buy, how much y does she sell, and what is the "
        "value of the trade at p*?",
        form=["buys", BOX, "x, sells", BOX, "y; value", BOX],
        answers=[H("e6.0"), H("e6.1"), H("e6.2")],
        mistakes=M({"e6.2~4": "Value = p&middot;(x bought) &minus; 1&middot;(y sold) = "
                              "2&middot;1 &minus; 2.",
                    "e6.1~6": "Sold = endowment minus what she keeps: 8 &minus; 6."}),
        explain="Zero, as her budget constraint demands: what she buys is paid for by what "
                "she sells."),
    Question(
        "e7",
        "Try it (c): an outsider sees only the prices and A's bundle. Recover A's share a "
        "from them.",
        form=["a = p<sub>x</sub>%s / %s =" % (XA, MA), BOX],
        answers=[H("e7.0")],
        mistakes=M({"e7.0~3/8": "Spending, not quantity: p<sub>x</sub>%s = 2&middot;9." % XA,
                    "e7.0~1/4": "That is the share spent on y."}),
        explain="Preferences recovered from prices and quantities alone: how economists "
                "estimate them from data."),
    Question(
        "e8",
        "Check the tangency: MRS<sub>A</sub> at (9, 6) and MRS<sub>B</sub> at (3, 6).",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("e8.0"), H("e8.1")],
        mistakes=M({"e8.0~2/3": "MRS<sub>A</sub> = (a/(1 &minus; a))&middot;y/x = "
                                "3&middot;y/x.",
                    "e8.1~1/2": "Upside down: y/x for B."}),
        explain="Both equal p*: the market did the planner's work."),
    Question(
        "e9",
        "Setting the MRSs equal with B's bundle (12 &minus; %s, 12 &minus; %s) gives the "
        "contract curve %s = 6%s/(18 &minus; %s). Which %s goes with %s = 6?"
        % (XA, YA, YA, XA, XA, YA, XA),
        form=["%s =" % YA, BOX],
        answers=[H("e9.0")],
        mistakes=M({"e9.0~6": "That is the diagonal. Different tastes bend the curve."}),
        explain="It runs from A's corner to B's and passes through (9, 6)."),
]

economy = GuidedProblem(
    "Part 2 &middot; Solving an exchange economy",
    "The notes' worked example: u<sub>A</sub> = x<sup>3/4</sup>y<sup>1/4</sup>, "
    "u<sub>B</sub> = x<sup>1/2</sup>y<sup>1/2</sup>, &omega;<sub>A</sub> = (8, 8), "
    "&omega;<sub>B</sub> = (4, 4): a 12 &times; 12 box. Prices come from inside the model now.",
    ECONOMY_QUESTIONS, draw_economy, figsize=(6.0, 5.6),
    outro="That is notes Figure 7, built step by step.",
    sources=[NOTES("p. 6&ndash;9")],
)


# ======================================================================
# Part 3: excess demand and Walras' law (same economy)
# ======================================================================

def draw_excess(ax, stage):
    e = WORKED
    _zframe(ax, 3.6, -6, 8.5)
    ps = np.linspace(0.6, 3.6, 200)
    if stage >= 1:
        ax.plot(ps, [e.excess(p)[1] for p in ps], color=B_COL, lw=2, label=r"$z_y$")
    if stage >= 2:
        ax.plot(ps, [e.excess(p)[0] for p in ps], color=A_COL, lw=2, label=r"$z_x$")
        _dot(ax, 1, 4, "+4", 6, 2, colour=A_COL)
        _dot(ax, 1, -4, "-4", 6, -12, colour=B_COL)
    if stage >= 3:
        _arrow(ax, (1, 0.6), (1.9, 0.6), NEW)
        ax.text(1.05, 1.0, "raise p", color=NEW, fontsize=9)
    if stage >= 4:
        _dot(ax, 3, -4 / 3, "-4/3", 6, -12, colour=A_COL)
        _dot(ax, 3, 4, "+4", 6, 2, colour=B_COL)
    if stage >= 5:
        _dot(ax, 2, 0, "p* = 2", 10, -22, colour=GREEN)
    _legend(ax, loc="upper right")


CHEAP = "x is too cheap: excess demand for x, excess supply of y"
DEAR = "x is too dear: excess supply of x, excess demand for y"
CLEAR = "Both markets clear"
ONLY_Y = "Only market y is out of balance"

WALRAS = "Every budget balances, so the value of total excess demand is zero at every price"
LUCK = "A coincidence of these numbers"
SAME_TOTAL = "Both goods have the same total, 12"
CHECKED = "We cleared it by hand as well"

SCALE_NONE = "Nothing: every income doubles too, so no budget set moves"
SCALE_HALF = "Everyone buys half as much"
SCALE_MORE = "Everyone is richer and buys more"
SCALE_EXCESS = "Excess demand appears in both markets"

EXCESS_QUESTIONS = [
    Question(
        "x1",
        "Total demand for y is (1 &minus; a)%s + (1 &minus; b)%s. Write it as a function of p."
        % (MA, MB),
        form=["%s + %s =" % (YA, YB), BOX, "p +", BOX],
        answers=[H("x1.0"), H("x1.1")],
        mistakes=M({"x1.0~2": "That is A's alone: (1/4)(8p + 8). Add B's (1/2)(4p + 4)."}),
        explain="So z<sub>y</sub>(p) = 4p + 4 &minus; 12 = 4p &minus; 8: it rises with p."),
    Question(
        "x2",
        "With %s(p) = 8/p &minus; 4 and %s(p) = 4p &minus; 8, evaluate both at p = 1." % (ZX, ZY),
        form=["%s(1) =" % ZX, BOX, "&nbsp; %s(1) =" % ZY, BOX],
        answers=[H("x2.0"), H("x2.1")],
        mistakes=M({"x2.0~-4": "8/1 &minus; 4.",
                    "x2.1~4": "4&middot;1 &minus; 8."}),
        explain="Excess demand for one good is mirrored by excess supply of the other."),
    Question(
        "x3",
        "What does that say at p = 1?",
        choices=[CHEAP, DEAR, CLEAR, ONLY_Y],
        answers=[H("x3.c")],
        mistakes=M({
            "x3.c~" + DEAR: "%s &gt; 0 means people want more x than exists." % ZX,
            "x3.c~" + CLEAR: "Clearing means both are zero.",
            "x3.c~" + ONLY_Y: "%s is not zero either." % ZX,
        }),
        explain="An auctioneer would raise the price of x until both curves sit on the axis."),
    Question(
        "x4",
        "Walras' law says p&middot;%s + %s = 0 at every price. Check it at p = 3." % (ZX, ZY),
        form=["%s(3) =" % ZX, BOX, "&nbsp; %s(3) =" % ZY, BOX, "&nbsp; p&middot;%s + %s ="
              % (ZX, ZY), BOX],
        answers=[H("x4.0"), H("x4.1"), H("x4.2")],
        mistakes=M({"x4.0~-4": "8/3 &minus; 4.", "x4.2~8/3": "Multiply %s by p = 3." % ZX}),
        explain="Zero away from equilibrium too."),
    Question(
        "x5",
        "So why did market y clear for free in Part 2?",
        choices=[WALRAS, LUCK, SAME_TOTAL, CHECKED],
        answers=[H("x5.c")],
        mistakes=M({
            "x5.c~" + LUCK: "It holds for every economy like this one: try p = 1 and p = 3.",
            "x5.c~" + SAME_TOTAL: "The totals do not matter. What links the two markets?",
            "x5.c~" + CHECKED: "We only checked it afterwards. Why did the check have to pass?",
        }),
        explain="With %s = 0, Walras' law leaves p<sub>y</sub>%s = 0. With n goods, clear "
                "n &minus; 1 markets and the last clears itself." % (ZX, ZY)),
    Question(
        "x6",
        "Double every price: p<sub>x</sub> = 4, p<sub>y</sub> = 2. What changes?",
        choices=[SCALE_NONE, SCALE_HALF, SCALE_MORE, SCALE_EXCESS],
        answers=[H("x6.c")],
        mistakes=M({
            "x6.c~" + SCALE_HALF: "Incomes are the value of endowments. What happens to them?",
            "x6.c~" + SCALE_MORE: "Prices doubled as well.",
            "x6.c~" + SCALE_EXCESS: "Every budget line is the same line as before.",
        }),
        explain="Only relative prices are determined, which is why we could set p<sub>y</sub> "
                "= 1, the numeraire."),
]

excess = GuidedProblem(
    "Part 3 &middot; Excess demand and Walras' law",
    "The same economy, read off one axis: what everyone wants minus what exists, at "
    "each price ratio.",
    EXCESS_QUESTIONS, draw_excess, figsize=(6.0, 4.6),
    outro="Counting equations is not proving existence: that needs convex preferences.",
    sources=[NOTES("p. 9&ndash;11")],
)


# ======================================================================
# Part 4: the worksheet (u_A = x^3/4 y^1/4, u_B = x^1/4 y^3/4)
# ======================================================================

SHEET = Economy(0.75, 0.25, (2, 6), (6, 2))


def draw_worksheet(fig, stage):
    bx, zx = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1, 1.15]))
    e = SHEET
    _box(bx, e.X, e.Y)
    _dot(bx, 2, 6, r"$\omega$", -8, -14, colour=INK, ha="right")
    if stage >= 1:
        bx.annotate("A: (2, 6)\nB: (6, 2)", (2, 6), textcoords="offset points",
                    xytext=(10, 10), color=MUTE, fontsize=8.5)
    if stage >= 2:
        _icA(bx, e, 2, 6, color=A_COL, lw=1.4)
        _icB(bx, e, 2, 6, color=B_COL, lw=1.4)
        _lens(bx, e, 2, 6, label=None)
    if stage >= 4:
        _pline(bx, e, 1, 2, 6, color=INK, lw=1.6)
    if stage >= 5:
        _dot(bx, 6, 2, "(6, 2)", 8, -16, colour=GREEN)
    if stage >= 6:
        _arrow(bx, (2, 6), (6, 2), GREEN)
    if stage >= 9:
        _contract(bx, e, color=GREEN, lw=2)
        _icA(bx, e, 6, 2, color=A_COL, lw=1, ls="--")
        _icB(bx, e, 6, 2, color=B_COL, lw=1, ls="--")

    _zframe(zx, 2.4, -3.5, 6.5)
    zx.set_title("Excess demand", loc="left", color=INK, fontsize=10)
    if stage >= 7:
        _dot(zx, 0.5, 5, "", colour=A_COL)
        _dot(zx, 0.5, -2.5, "", colour=B_COL)
    if stage >= 8:
        _zcurves(zx, e, 2.4)
        _dot(zx, 2, -2.5, "", colour=A_COL)
        _dot(zx, 2, 5, "", colour=B_COL)
        _dot(zx, 1, 0, "both cross here", 6, 6, colour=GREEN)
    _legend(zx, loc="upper right")
    fig.subplots_adjust(wspace=0.3)


SHEET_QUESTIONS = [
    Question(
        "k1",
        "Worksheet task 1: &omega;<sub>A</sub> = (2, 6) and &omega;<sub>B</sub> = (6, 2). "
        "Give the box's dimensions, and &omega; read from B's corner.",
        form=["width", BOX, "height", BOX, "&nbsp; B's corner: (", BOX, ",", BOX, ")"],
        answers=[H("k1.0"), H("k1.1"), H("k1.2"), H("k1.3")],
        mistakes=M({"k1.2~2": "That is A's x. From B's corner you read B's bundle."}),
        explain="An 8 &times; 8 box."),
    Question(
        "k2",
        "u<sub>A</sub> = x<sup>3/4</sup>y<sup>1/4</sup> and u<sub>B</sub> = "
        "x<sup>1/4</sup>y<sup>3/4</sup>. Where do the mutually improving trades lie?",
        choices=[DOWNRIGHT, UPLEFT, NO_TRADE, MORE_ALL],
        answers=[H("k2.c")],
        mistakes=M({
            "k2.c~" + UPLEFT: "At &omega;, MRS<sub>A</sub> = 3&middot;6/2 = 9 and "
                              "MRS<sub>B</sub> = (1/3)&middot;2/6 = 1/9. Who values x more?",
            "k2.c~" + NO_TRADE: "Compare the two MRSs at &omega;.",
            "k2.c~" + MORE_ALL: "The box holds the totals.",
        }),
        hints=["Compute each MRS at &omega;: (a/(1 &minus; a))&middot;y/x."],
        explain="A loves x and holds little of it; B the reverse. A wide lens."),
    Question(
        "k3",
        "Task 2: the endogenous incomes, with p<sub>y</sub> = 1.",
        form=["%s =" % MA, BOX, "p +", BOX, "&nbsp; %s =" % MB, BOX, "p +", BOX],
        answers=[H("k3.0"), H("k3.1"), H("k3.2"), H("k3.3")],
        explain="Each line through &omega; is a candidate budget line."),
    Question(
        "k4",
        "Clear the market for x. The price ratio?",
        form=["p* =", BOX],
        answers=[H("k4.0")],
        hints=["%s = (3/4)(2p + 6)/p and %s = (1/4)(6p + 2)/p; set the sum equal to 8." % (XA, XB)],
        explain="The budget line has slope &minus;1, as the worksheet promises."),
    Question(
        "k5",
        "The allocation: A's bundle, then B's.",
        form=["A: (", BOX, ",", BOX, ") &nbsp; B: (", BOX, ",", BOX, ")"],
        answers=[H("k5.0"), H("k5.1"), H("k5.2"), H("k5.3")],
        mistakes=M({"k5.0~2": "That is her endowment. Use the demand (3/4)%s/p." % MA}),
        explain="The two swap places: each ends up holding the good they like."),
    Question(
        "k6",
        "Net trades: how much x does A buy, and how much y does she sell?",
        form=["buys", BOX, "x, sells", BOX, "y"],
        answers=[H("k6.0"), H("k6.1")],
        explain="Four for four at p = 1: the value of her trade is zero."),
    Question(
        "k7",
        "Task 3: %s(p) = 5/p &minus; 5 and %s(p) = 5p &minus; 5. Plot them at p = 1/2: "
        "the values?" % (ZX, ZY),
        form=["%s(1/2) =" % ZX, BOX, "&nbsp; %s(1/2) =" % ZY, BOX],
        answers=[H("k7.0"), H("k7.1")],
        mistakes=M({"k7.0~-5/2": "5/(1/2) = 10."}),
        explain="x is too cheap at p = 1/2."),
    Question(
        "k8",
        "And at p = 2, with Walras' law as a check?",
        form=["%s(2) =" % ZX, BOX, "&nbsp; %s(2) =" % ZY, BOX, "&nbsp; 2%s + %s =" % (ZX, ZY), BOX],
        answers=[H("k8.0"), H("k8.1"), H("k8.2")],
        explain="Both cross zero at p = 1, together."),
    Question(
        "k9",
        "Sketch the contract curve. First check that the equilibrium is on it: each MRS at "
        "the allocation.",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("k9.0"), H("k9.1")],
        mistakes=M({"k9.0~9": "That was at &omega;. Use A's new bundle (6, 2).",
                    "k9.0~1/3": "MRS<sub>A</sub> = 3&middot;y/x."}),
        explain="Both equal p* = 1. The contract curve here is %s = %s/(9 &minus; %s), "
                "bowed below the diagonal." % (YA, XA, XA)),
]

worksheet = GuidedProblem(
    "Part 4 &middot; The worksheet",
    "The notes' worksheet: the box on the left, excess demand on the right.",
    SHEET_QUESTIONS, draw_worksheet, figsize=(8.2, 4.4), whole_figure=True,
    outro="Task 4, the theorems, is Part 7. Bring the sheet: we go through it in class.",
    sources=[NOTES("p. 14&ndash;15, worksheet")],
)


# ======================================================================
# Part 5: problem A6.1, identical tastes
# ======================================================================

SAME = Economy(0.5, 0.5, (3, 9), (9, 3))


def draw_same(ax, stage):
    e = SAME
    _box(ax, e.X, e.Y)
    _dot(ax, 3, 9, r"$\omega$", 8, 4, colour=INK)
    if stage >= 1:
        for x in (4, 8):
            _icA(ax, e, x, x, color=A_COL, lw=1)
            _icB(ax, e, x, x, color=B_COL, lw=1)
            _dot(ax, x, x, "", colour=GREEN)
    if stage >= 2:
        _contract(ax, e, color=GREEN, lw=2, label="contract curve")
    if stage >= 3:
        _pline(ax, e, 1, 3, 9, color=INK, lw=1.6, label="price line")
    if stage >= 4:
        _dot(ax, 6, 6, "CE", 8, -14, colour=NEW)
        _arrow(ax, (3, 9), (6, 6), NEW)
    _legend(ax, loc="lower right")


EQ_RATIO = "A's y/x equals B's y/x: equal MRS"
EQ_X = "A and B consume the same amount of x"
EQ_U = "A and B get the same utility"
EQ_ONE = "A's MRS equals 1"

DIAG = "A's y/x equals total y / total x: the box's diagonal"
ANTI = "A's y = total y − (total y / total x)·A's x: the other diagonal"
CURVED = "A curve bending below the diagonal"
POINT = "Only the equal split"

P_RATIO = "Total y / total x: services are dear when they are scarce"
P_INV = "Total x / total y"
P_ONE = "Always 1"
P_WHO = "It depends on who owns what"

ON_CC = "At the CE, A's y/x equals the price ratio, which equals total y / total x: the contract curve's equation"
CLEARS = "Because the markets clear"
IDENT = "Because the countries are identical"
ANY_BUDGET = "Every point on the budget line is efficient"

SAME_QUESTIONS = [
    Question(
        "i1",
        "Both countries have u = x<sup>1/2</sup>y<sup>1/2</sup>. Divide the planner's "
        "first-order conditions pairwise. What condition comes out?",
        choices=[EQ_RATIO, EQ_X, EQ_U, EQ_ONE],
        answers=[H("i1.c")],
        mistakes=M({
            "i1.c~" + EQ_X: "The planner equalizes rates of substitution, not quantities.",
            "i1.c~" + EQ_U: "B's utility is held at a level &#363;, not set equal to A's.",
            "i1.c~" + EQ_ONE: "The MRS equals &mu;<sub>x</sub>/&mu;<sub>y</sub>, which "
                              "need not be 1.",
        }),
        explain="MRS<sub>A</sub> = MRS<sub>B</sub>; &lambda; drops out of the ratio."),
    Question(
        "i2",
        "Substitute %s = &omega;<sup>x</sup> &minus; %s and %s = &omega;<sup>y</sup> &minus; "
        "%s and simplify. The contract curve is:" % (XB, XA, YB, YA),
        choices=[DIAG, ANTI, CURVED, POINT],
        answers=[H("i2.c")],
        mistakes=M({
            "i2.c~" + ANTI: "That line runs from top left to bottom right. Does it pass "
                            "through both origins?",
            "i2.c~" + CURVED: "Cross-multiply and expand: the %s%s terms cancel, leaving "
                              "no curvature." % (XB, YB),
            "i2.c~" + POINT: "Vary the planner's &#363; and you get a whole set.",
        }),
        explain="A straight line from origin to origin: every efficient point has the "
                "totals' own mix."),
    Question(
        "i3",
        "Part 3: solve the competitive equilibrium. The price ratio p<sub>x</sub>/p<sub>y</sub>?",
        choices=[P_RATIO, P_INV, P_ONE, P_WHO],
        answers=[H("i3.c")],
        mistakes=M({
            "i3.c~" + P_INV: "Upside down. Clear market x: (1/2)(p&omega;<sup>x</sup> + "
                             "&omega;<sup>y</sup>)/p = &omega;<sup>x</sup>.",
            "i3.c~" + P_ONE: "Only when the totals are equal.",
            "i3.c~" + P_WHO: "Total income is p&omega;<sup>x</sup> + &omega;<sup>y</sup> "
                             "whoever owns it; with identical shares only the totals matter.",
        }),
        explain="Services are expensive exactly when they are scarce relative to goods."),
    Question(
        "i4",
        "With numbers: &omega;<sub>A</sub> = (3, 9) and &omega;<sub>B</sub> = (9, 3), the "
        "endowments of A6.2. The price ratio and A's bundle?",
        form=["p* =", BOX, "&nbsp; A: (", BOX, ",", BOX, ")"],
        answers=[H("i4.0"), H("i4.1"), H("i4.2")],
        mistakes=M({"i4.1~3": "That is A's endowment. Spend half of %s = 12 on each good." % MA}),
        explain="The equal split, on the diagonal."),
    Question(
        "i5",
        "Part 4: why is the competitive allocation Pareto efficient?",
        choices=[ON_CC, CLEARS, IDENT, ANY_BUDGET],
        answers=[H("i5.c")],
        mistakes=M({
            "i5.c~" + CLEARS: "Clearing alone is feasibility. What does the price do to "
                              "the two MRSs?",
            "i5.c~" + IDENT: "Part 6 has different countries and the CE is still efficient.",
            "i5.c~" + ANY_BUDGET: "The budget line crosses the contract curve only once.",
        }),
        explain="Both MRSs equal the same price, so they equal each other: the first "
                "welfare theorem, by hand."),
]

same = GuidedProblem(
    "Part 5 &middot; Identical tastes: A6.1",
    "Two countries with u = x<sup>1/2</sup>y<sup>1/2</sup>, services x and goods y. "
    "Symbolic first, then A6.2's numbers. The figure uses those numbers.",
    SAME_QUESTIONS, draw_same, figsize=(6.0, 5.6),
    outro="Mock exam 5 and the 2025 exam both open with this problem.",
    sources=[PS("A6.1")],
)


# ======================================================================
# Part 6: problem A6.2, different tastes
# ======================================================================

DIFF = Economy(2 / 3, 1 / 3, (3, 9), (9, 3))


def draw_different(ax, stage):
    e = DIFF
    _box(ax, e.X, e.Y)
    _dot(ax, 3, 9, r"$\omega$", 8, 4, colour=INK)
    if stage in (1, 2):
        for p in (0.5, 2):
            _pline(ax, e, p, 3, 9, color=GREY, lw=1)
    if stage >= 3:
        _pline(ax, e, 1, 3, 9, color=INK, lw=1.6, label="price line")
    if stage >= 5:
        _dot(ax, 8, 4, "CE (8, 4)", 14, -4, colour=NEW)
    if stage >= 6:
        _arrow(ax, (3, 9), (8, 4), NEW)
    if stage >= 7:
        _contract(ax, e, color=GREEN, lw=2, label="contract curve")
        ax.plot([0, 12], [0, 12], color=GREY, lw=1, ls="--", label="A6.1: the diagonal")
    if stage >= 8:
        _icA(ax, e, 8, 4, color=A_COL, lw=1.2)
        _icB(ax, e, 8, 4, color=B_COL, lw=1.2)
    if stage >= 10:
        _dot(ax, 6, 6, "(6, 6)", -8, 6, colour=HALF, ha="right")
        _icA(ax, e, 6, 6, color=A_COL, lw=1, ls=":")
        _icB(ax, e, 6, 6, color=B_COL, lw=1, ls=":")
    if stage >= 11:
        _lens(ax, e, 6, 6, label=None)
    if stage >= 12:
        _dot(ax, 6, 2.4, "(6, 2.4)", -8, -14, colour=GREEN, ha="right")
    _legend(ax, loc="upper left")


A_BUYS = "A buys 5 services from B and pays with 5 goods"
B_BUYS = "B buys 5 services from A and pays with 5 goods"
A_PAYS_MORE = "A buys 5 services and pays with 10 goods"
NOBODY = "No trade: both incomes are 12"

BENDS = "Different tastes leave one cross term standing: the services-lover A holds relatively more services at every efficient point"
SCARCE = "Services are scarcer than goods"
UNEQUAL = "The endowments are unequal"
PRICE_NOT_ONE = "The price ratio is no longer 1"

TRADE_OK = "No: B gives A one service for one good, and both are better off"
WRONG_WAY = "No: A gives B one service for one good, and both are better off"
TOO_DEAR = "No: B gives A one service for three goods, and both are better off"
ON_BUDGET = "Yes: it lies on the budget line at p* = 1"

DIFF_QUESTIONS = [
    Question(
        "j1",
        "(a) u<sub>A</sub> = x<sup>2/3</sup>y<sup>1/3</sup>, u<sub>B</sub> = "
        "x<sup>1/3</sup>y<sup>2/3</sup>, &omega;<sub>A</sub> = (3, 9), &omega;<sub>B</sub> = "
        "(9, 3), p<sub>y</sub> = 1. Each country's income?",
        form=["M<sub>A</sub> =", BOX, "p +", BOX, "&nbsp; M<sub>B</sub> =", BOX, "p +", BOX],
        answers=[H("j1.0"), H("j1.1"), H("j1.2"), H("j1.3")],
        mistakes=M({"j1.0~9": "Services first: &omega;<sub>A</sub> = (3, 9) means 3 services."}),
        explain="The value of the endowment at the prices being solved for."),
    Question(
        "j2",
        "(b) The demands, by the Cobb&ndash;Douglas share rule. Fill in the shares.",
        form=["%s =" % XA, BOX, "M<sub>A</sub>/p, &nbsp;%s =" % YA, BOX, "M<sub>A</sub>, &nbsp;%s ="
              % XB, BOX, "M<sub>B</sub>/p, &nbsp;%s =" % YB, BOX, "M<sub>B</sub>"],
        answers=[H("j2.0"), H("j2.1"), H("j2.2"), H("j2.3")],
        mistakes=M({"j2.2~2/3": "B's exponent on services is 1/3."}),
        explain="The exponent is the budget share."),
    Question(
        "j3",
        "(c) Clear the services market. Total demand is (__p + __)/p; set it equal to 12.",
        form=["%s + %s = (" % (XA, XB), BOX, "p +", BOX, ")/p; &nbsp; p* =", BOX],
        answers=[H("j3.0"), H("j3.1"), H("j3.2")],
        mistakes=M({"j3.0~3": "A's part is (2/3)(3p + 9) = 2p + 6; add B's (1/3)(9p + 3)."}),
        explain="One service trades for one good."),
    Question(
        "j4",
        "(c) In one sentence: why does the market for y then clear automatically?",
        choices=[WALRAS, LUCK, SAME_TOTAL, CHECKED],
        answers=[H("j4.c")],
        mistakes=M({
            "j4.c~" + LUCK: "It is guaranteed. By what?",
            "j4.c~" + SAME_TOTAL: "The totals do not matter. What links the two markets?",
            "j4.c~" + CHECKED: "Checking is not a reason. Why must the check pass?",
        }),
        explain="Walras' law."),
    Question(
        "j5",
        "(d) The equilibrium allocation.",
        form=["A: (", BOX, ",", BOX, ") &nbsp; B: (", BOX, ",", BOX, ")"],
        answers=[H("j5.0"), H("j5.1"), H("j5.2"), H("j5.3")],
        mistakes=M({"j5.0~4": "A spends 2/3 of 12 on services: (2/3)&middot;12/1."}),
        explain="8 + 4 = 12 in each market."),
    Question(
        "j6",
        "(d) Who sells what to whom?",
        choices=[A_BUYS, B_BUYS, A_PAYS_MORE, NOBODY],
        answers=[H("j6.c")],
        mistakes=M({
            "j6.c~" + B_BUYS: "A starts with 3 services and ends with 8.",
            "j6.c~" + A_PAYS_MORE: "At p* = 1, one service costs one good.",
            "j6.c~" + NOBODY: "Equal incomes do not mean equal bundles: compare (3, 9) with "
                              "(8, 4).",
        }),
        explain="Five goods buy exactly five services: each country's trade balances."),
    Question(
        "j7",
        "(e) Set MRS<sub>A</sub> = 2%s/%s equal to MRS<sub>B</sub> = (12 &minus; %s)/(2(12 "
        "&minus; %s)) and cross-multiply. Collect the terms in %s:" % (YA, XA, YA, XA, YA),
        form=["%s(48 &minus;" % YA, BOX, "%s) =" % XA, BOX, XA],
        answers=[H("j7.0"), H("j7.1")],
        mistakes=M({"j7.0~4": "Only part of the cross term cancels: 4%s%s on the left, "
                              "%s%s on the right." % (XA, YA, XA, YA),
                    "j7.0~5": "Subtract, don't add: 4%s%s &minus; %s%s." % (XA, YA, XA, YA)}),
        hints=["4%s(12 &minus; %s) = %s(12 &minus; %s)." % (YA, XA, XA, YA)],
        explain="So %s = 4%s/(16 &minus; %s)." % (YA, XA, XA)),
    Question(
        "j8",
        "Verify the CE is on it: each MRS at (8, 4) and (4, 8).",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("j8.0"), H("j8.1")],
        mistakes=M({"j8.0~1/2": "MRS<sub>A</sub> = 2&middot;y/x = 2&middot;4/8."}),
        explain="Both equal p* = 1."),
    Question(
        "j9",
        "(e) Why is the contract curve no longer a straight line?",
        choices=[BENDS, SCARCE, UNEQUAL, PRICE_NOT_ONE],
        answers=[H("j9.c")],
        mistakes=M({
            "j9.c~" + SCARCE: "The totals are 12 and 12.",
            "j9.c~" + UNEQUAL: "The contract curve does not depend on the endowments at all.",
            "j9.c~" + PRICE_NOT_ONE: "p* = 1 here, and the curve has no price in it.",
        }),
        explain="It bends below the diagonal, toward the services-lover."),
    Question(
        "j10",
        "(f) The equal split: (6, 6) for each. Each MRS there?",
        form=["MRS<sub>A</sub> =", BOX, "&nbsp; MRS<sub>B</sub> =", BOX],
        answers=[H("j10.0"), H("j10.1")],
        mistakes=M({"j10.0~1": "Don't drop the exponent ratio: 2&middot;y/x.",
                    "j10.1~2": "B's ratio is (1/3)/(2/3) = 1/2."}),
        explain="A would give 2 goods for a service; B asks only 1/2."),
    Question(
        "j11",
        "Is the equal split Pareto efficient?",
        choices=[TRADE_OK, WRONG_WAY, TOO_DEAR, ON_BUDGET],
        answers=[H("j11.c")],
        mistakes=M({
            "j11.c~" + WRONG_WAY: "Who values services more?",
            "j11.c~" + TOO_DEAR: "A pays at most 2 goods for a service.",
            "j11.c~" + ON_BUDGET: "Affordable is not the same as efficient: compare the MRSs.",
        }),
        explain="Any rate between 1/2 and 2 goods per service works: (6, 6) is fair and "
                "still inefficient."),
    Question(
        "j12",
        "On the contract curve, which %s goes with %s = 6?" % (YA, XA),
        form=["%s =" % YA, BOX],
        answers=[H("j12.0")],
        mistakes=M({"j12.0~6": "That is the equal split, which is not efficient.",
                    "j12.0~3": "That is the worked economy's curve. Use 4%s/(16 &minus; %s)."
                               % (XA, XA)}),
        explain="Efficiency and fairness are different axes."),
]

different = GuidedProblem(
    "Part 6 &middot; Different tastes: A6.2",
    "The same market as A6.1, but A loves services and B loves goods. Services x across, "
    "goods y up.",
    DIFF_QUESTIONS, draw_different, figsize=(6.0, 5.6),
    outro="Mock exam 5 and the 2025 exam both open with a version of this problem.",
    sources=[PS("A6.2")],
)


# ======================================================================
# Part 7: the welfare theorems and the core (worked economy)
# ======================================================================

def draw_theorems(ax, stage):
    e = WORKED
    _box(ax, e.X, e.Y)
    _contract(ax, e, color=GREEN, lw=2, label="contract curve")
    _dot(ax, 8, 8, r"$\omega$", 8, 4, colour=INK)
    _dot(ax, 9, 6, "CE", 8, -12, colour=GREEN)
    if stage >= 2:
        _dot(ax, 6, 3, "F", -8, 4, colour=HALF, ha="right")
        _icA(ax, e, 6, 3, color=A_COL, lw=1.2)
        _icB(ax, e, 6, 3, color=B_COL, lw=1.2)
        _pline(ax, e, 1.5, 6, 3, color=INK, lw=1.6, label="supporting line")
    if stage >= 3:
        _dot(ax, 8, 0.02, r"$\tilde\omega$", 8, 6, colour=NEW)
        _arrow(ax, (8, 8), (8, 0.3), NEW)
        ax.text(8.2, 4.2, "transfer", color=NEW, fontsize=9)
    if stage >= 5:
        _lens(ax, e, 8, 8, label="lens through " + r"$\omega$")
        lo, hi = e.core()
        xs = np.linspace(lo, hi, 50)
        ax.plot(xs, [e.contract(v) for v in xs], color=NEW, lw=5, alpha=0.8,
                solid_capstyle="round", label="core")
    _legend(ax, loc="upper left")


FIRST_OK = "Competitive equilibrium ⇒ Pareto efficient, with no externalities and no market power"
FIRST_REV = "Pareto efficient ⇒ competitive equilibrium"
FIRST_FAIR = "Competitive equilibrium ⇒ fair"
FIRST_CONV = "Competitive equilibrium ⇒ Pareto efficient, but only with convex preferences"

CONVEX = "Convex preferences: otherwise an agent's best point on the supporting line need not be F"
NO_EXT = "No externalities"
EQUAL_END = "Equal endowments"
COBB = "Cobb–Douglas preferences"

F_NOT_CORE = "No: A is worse off at F than at ω, so she would never trade there voluntarily"
F_CORE = "Yes: every point on the contract curve is in the core"
F_B_WORSE = "No: B is worse off at F than at ω"
F_CORE_P = "Yes: F is supported by prices"

CE_IN = "Inside it: efficient by the first theorem, and individually rational because ω is always affordable"
CE_END = "At its end, where A does best"
CE_OUT = "Outside it: the market ignores what people start with"
CE_DEP = "It depends on the price"

THEOREM_QUESTIONS = [
    Question(
        "t1",
        "The first welfare theorem. Which direction, under which assumptions?",
        choices=[FIRST_OK, FIRST_REV, FIRST_FAIR, FIRST_CONV],
        answers=[H("t1.c")],
        mistakes=M({
            "t1.c~" + FIRST_REV: "That direction is the second theorem, and it needs more.",
            "t1.c~" + FIRST_FAIR: "One agent owning everything is efficient. Efficiency is "
                                  "not fairness.",
            "t1.c~" + FIRST_CONV: "Convexity is what the second theorem needs. The first "
                                  "does without it.",
        }),
        explain="The market exhausts the gains from trade. It says nothing about fairness."),
    Question(
        "t2",
        "A planner prefers F = (6, 3) for A, on the contract curve. What price ratio "
        "supports F?",
        form=["p =", BOX],
        answers=[H("t2.0")],
        mistakes=M({"t2.0~1/2": "That is y/x. MRS<sub>A</sub> = 3&middot;y/x.",
                    "t2.0~2": "That is the old p*. F's own tangent gives its price."}),
        explain="The common tangent at F: the efficient point tells you its prices."),
    Question(
        "t3",
        "At that price, what is A's endowment (8, 8) worth, what is F worth, and how much "
        "(in units of y) must A hand to B as a lump sum?",
        form=["&omega;<sub>A</sub>:", BOX, "&nbsp; F:", BOX, "&nbsp; transfer:", BOX],
        answers=[H("t3.0"), H("t3.1"), H("t3.2")],
        mistakes=M({"t3.0~24": "That is at the old price 2. Use 3/2.",
                    "t3.2~-8": "Give it as a positive amount from A to B."}),
        explain="Move &omega; onto the line, here straight down to (8, 0), and both choose F. "
                "The market allocates; the transfer distributes."),
    Question(
        "t4",
        "Which assumption does the second theorem need that the first does not?",
        choices=[CONVEX, NO_EXT, EQUAL_END, COBB],
        answers=[H("t4.c")],
        mistakes=M({
            "t4.c~" + NO_EXT: "Both theorems need that one.",
            "t4.c~" + EQUAL_END: "The transfer moves the endowment anyway.",
            "t4.c~" + COBB: "Cobb&ndash;Douglas is one convex example, not the requirement.",
        }),
        explain="With a non-convex curve, A walks off along the line to a point G she likes "
                "better (notes Figure 10)."),
    Question(
        "t5",
        "Without the transfer, is F in the core of this economy?",
        choices=[F_NOT_CORE, F_CORE, F_B_WORSE, F_CORE_P],
        answers=[H("t5.c")],
        mistakes=M({
            "t5.c~" + F_CORE: "The core adds a second test: both must prefer it to &omega;.",
            "t5.c~" + F_B_WORSE: "B holds (6, 9) at F against (4, 4) at &omega;.",
            "t5.c~" + F_CORE_P: "Prices support it only after the transfer.",
        }),
        hints=["u<sub>A</sub> = x<sup>3/4</sup>y<sup>1/4</sup>: compare (6, 3) with (8, 8)."],
        explain="The core is the stretch of the contract curve inside the lens through "
                "&omega;. Move &omega; and the core moves; the contract curve does not."),
    Question(
        "t6",
        "Where does the competitive equilibrium (9, 6) sit relative to the core?",
        choices=[CE_IN, CE_END, CE_OUT, CE_DEP],
        answers=[H("t6.c")],
        mistakes=M({
            "t6.c~" + CE_END: "Look at the figure: the core runs on both sides of it.",
            "t6.c~" + CE_OUT: "Could anyone be worse off than at &omega;, when &omega; is "
                              "on their budget line?",
            "t6.c~" + CE_DEP: "At the equilibrium price it is a fixed point.",
        }),
        explain="The market picks a point the two would have agreed on anyway."),
]

theorems = GuidedProblem(
    "Part 7 &middot; The welfare theorems and the core",
    "Back to the worked economy of Part 2, with its contract curve and equilibrium. "
    "Task 4 of the worksheet.",
    THEOREM_QUESTIONS, draw_theorems, figsize=(6.0, 5.6),
    outro="If you want to redistribute income, redistribute income: don't hand selected "
          "groups a lower price.",
    sources=[NOTES("p. 11&ndash;14"), NOTES("p. 15, worksheet task 4")],
)


# ======================================================================
# Where every step comes from (printed pages of s06_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "b1": NOTES("p. 15 &middot; review question 1"), "b2": NOTES("p. 15 &middot; review question 1"),
    "b3": NOTES("p. 16 &middot; review question 2"), "b4": NOTES("p. 15 &middot; review question 1"),
    "b5": NOTES("p. 15 &middot; review question 1"), "b6": NOTES("p. 16 &middot; review question 2"),
    "b7": NOTES("p. 16 &middot; review question 2"),
    "e1": NOTES("p. 7 &middot; incomes"), "e2": NOTES("p. 7 &middot; demands"),
    "e3": NOTES("p. 7 &middot; Try it (a)"), "e4": NOTES("p. 8 &middot; Try it (b)"),
    "e5": NOTES("p. 8 &middot; Try it (b)"), "e6": NOTES("p. 8 &middot; Try it (b)"),
    "e7": NOTES("p. 8 &middot; Try it (c)"), "e8": NOTES("p. 8 &middot; tangency"),
    "e9": NOTES("p. 8 &middot; contract curve"),
    "x1": NOTES("p. 9 &middot; excess demand"), "x2": NOTES("p. 10 &middot; excess demand"),
    "x3": NOTES("p. 10 &middot; excess demand"), "x4": NOTES("p. 10 &middot; Walras' law"),
    "x5": NOTES("p. 10 &middot; Walras' law"), "x6": NOTES("p. 11 &middot; numeraire"),
    "k1": NOTES("p. 14 &middot; worksheet task 1"), "k2": NOTES("p. 14 &middot; worksheet task 1"),
    "k3": NOTES("p. 15 &middot; worksheet task 2"), "k4": NOTES("p. 15 &middot; worksheet task 2"),
    "k5": NOTES("p. 15 &middot; worksheet task 2"), "k6": NOTES("p. 15 &middot; worksheet task 2"),
    "k7": NOTES("p. 15 &middot; worksheet task 3"), "k8": NOTES("p. 15 &middot; worksheet task 3"),
    "k9": NOTES("p. 15 &middot; worksheet task 1"),
    "i1": PS("A6.1 (1)"), "i2": PS("A6.1 (1)&ndash;(2)"), "i3": PS("A6.1 (3)"),
    "i4": PS("A6.1 (3), A6.2's numbers"), "i5": PS("A6.1 (4)"),
    "j1": PS("A6.2 (a)"), "j2": PS("A6.2 (b)"), "j3": PS("A6.2 (c)"), "j4": PS("A6.2 (c)"),
    "j5": PS("A6.2 (d)"), "j6": PS("A6.2 (d)"), "j7": PS("A6.2 (e)"), "j8": PS("A6.2 (e)"),
    "j9": PS("A6.2 (e)"), "j10": PS("A6.2 (f)"), "j11": PS("A6.2 (f)"), "j12": PS("A6.2 (f)"),
    "t1": NOTES("p. 11 &middot; first theorem"), "t2": NOTES("p. 11 &middot; second theorem"),
    "t3": NOTES("p. 11 &middot; second theorem"), "t4": NOTES("p. 12 &middot; convexity"),
    "t5": NOTES("p. 13 &middot; the core"), "t6": NOTES("p. 14 &middot; the core"),
}

for _q in (BOX_QUESTIONS + ECONOMY_QUESTIONS + EXCESS_QUESTIONS + SHEET_QUESTIONS
           + SAME_QUESTIONS + DIFF_QUESTIONS + THEOREM_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
