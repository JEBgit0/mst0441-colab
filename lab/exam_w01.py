"""
exam_w01.py - workshop 1, the first mock exam: sessions 2 to 7.

    Problem 1  sunniva   a budget, a price cut and Cobb-Douglas demand (18)
    Problem 2  trade     two countries in an Edgeworth box (16)
    Problem 3  air       pollution as an externality, and tradable quotas (6)
    Problem 4  concepts  ten multiple-choice questions (10)

The paper is worth 50 points, half a full exam. The page checks final answers
and conclusions only: the derivations, figures and sentences are marked by
hand on the real exam.

Answers are hashes in answers_w01.py, generated from
answer_keys/w01_keys.py in the private repo. The maths is equilibrium.py.
"""

import numpy as np

import edgeworth_plots as ed
import guided_plots as gp
from equilibrium import Economy
from exam import ExamPaper, ExamProblem, Part
from guided import BOX, answers
from style import CURVE, GREEN, HALF, INK, LINE, MUTE, NEW

H, M = answers("w01")

PX, PY = "p<sub>x</sub>", "p<sub>y</sub>"


def _waiting(ax):
    ax.axis("off")
    ax.text(0.5, 0.5, "The figure fills in as parts are marked right.",
            transform=ax.transAxes, ha="center", va="center", color=MUTE, fontsize=11)


# ======================================================================
# Problem 1: Sunniva's trips
# ======================================================================

def draw_sunniva(ax, done):
    if not done & {"1a", "1c1", "1e1", "1e2"}:
        _waiting(ax)
        return
    gp.frame(ax, 480, 960, "trips x", "basket y")
    xt, yt = [], []
    if "1a" in done:
        ax.plot([0, 300], [900, 0], color=LINE, lw=2, label="budget, trips cost 3")
        xt, yt = [300], [900]
    if "1c1" in done:
        ax.plot([0, 450], [900, 0], color=NEW, lw=2, ls="--", label="budget, trips cost 2")
        xt, yt = xt + [450], [900]
    xs = np.linspace(40, 480, 300)
    if "1e1" in done:
        ax.plot(xs, 150 * 450 / xs, color=CURVE, lw=1.5)
        gp.dot(ax, 150, 450, "(150, 450)", -8, 8, colour=CURVE, ha="right")
        yt = yt + [450]
    if "1e2" in done:
        ax.plot(xs, 225 * 450 / xs, color=CURVE, lw=1.5, ls="--")
        gp.dot(ax, 225, 450, "(225, 450)", 8, 8, colour=NEW)
        yt = sorted(set(yt + [450]))
    ax.set_xticks(xt)
    ax.set_yticks(yt)
    ax.tick_params(colors=MUTE, labelsize=8.5)
    gp.legend(ax)


TANGENT = "She picks the point on the budget line where an indifference curve is tangent to it: there MRS = px/py, and no bundle she can afford lies on a higher curve"
CROSS = "She picks a point where an indifference curve crosses the budget line, with MRS above px/py"
MIDDLE = "She picks the midpoint of the budget line, whatever her preferences are"
CORNER = "She buys only the basket, since a trip costs three times as much"

PIVOT = "The budget line pivots out around 900 on the basket axis. She takes more trips, and the basket stays the same, because she spends a fixed share of income on each good"
SHIFT = "The budget line shifts out in parallel, and she buys more of both goods"
PIVOT_LESS = "The budget line pivots out, and she takes more trips and less of the basket"
PIVOT_NONE = "The budget line pivots out, and she takes the same trips and more of the basket"

MRS = "MRS = αy/((1 − α)x) = px/py"
MRS_XY = "MRS = αx/((1 − α)y) = px/py"
MRS_ALPHA = "MRS = (1 − α)y/(αx) = px/py"
MRS_PRICE = "MRS = αy/((1 − α)x) = py/px"

SAME = "Nothing: it stays at 450, because she spends half her income on each good at any price"
FALLS = "It falls, because she buys more trips"
RISES = "It rises, because trips are cheaper"
TO_300 = "It falls to 300"

SUNNIVA_PARTS = [
    Part("1a", "1(a)", 3,
         "Where does the budget line meet each axis, and what is its slope, with its sign?",
         form=["trips", BOX, "&nbsp; basket", BOX, "&nbsp; slope", BOX],
         answers=[H("1a.0"), H("1a.1"), H("1a.2")],
         mistakes=M({"1a.2~3": "The budget line slopes down.",
                     "1a.2~-1/3": "Upside down: &minus;%s/%s, with trips across." % (PX, PY),
                     "1a.0~900": "All 900 on trips at 3 each."}),
         explain="3x + y = 900: each trip costs three units of the basket."),
    Part("1b", "1(b)", 3,
         "Which sentence describes her optimal choice?",
         choices=[TANGENT, CROSS, MIDDLE, CORNER],
         answers=[H("1b.c")],
         mistakes=M({
             "1b.c~" + CROSS: "Where the curves cross she can still reach a higher one.",
             "1b.c~" + MIDDLE: "That is right only when &alpha; = 1/2. The problem leaves "
                               "&alpha; open.",
             "1b.c~" + CORNER: "With these preferences she always buys some of both goods.",
         }),
         explain="Draw the budget line, one curve tangent to it, and mark the tangency."),
    Part("1c1", "1(c)", 1,
         "The price of a trip falls to 2. Where does the new budget line meet the trips axis?",
         form=["trips", BOX],
         answers=[H("1c1.0")],
         mistakes=M({"1c1.0~300": "That is the old intercept: 900 now buys more trips."}),
         explain="The basket intercept stays at 900: the line pivots."),
    Part("1c2", "1(c)", 3,
         "What happens to the budget line, to trips and to the basket?",
         choices=[PIVOT, SHIFT, PIVOT_LESS, PIVOT_NONE],
         answers=[H("1c2.c")],
         mistakes=M({
             "1c2.c~" + SHIFT: "Only one price changed: 900 still buys 900 units of the basket.",
             "1c2.c~" + PIVOT_LESS: "With these preferences her spending on the basket is "
                                    "(1 &minus; &alpha;) times income, whatever a trip costs.",
             "1c2.c~" + PIVOT_NONE: "Trips got cheaper and her spending on them did not fall.",
         }),
         explain="Dashed new budget line, dashed new curve, and the new optimum straight to the "
                 "right of the old one."),
    Part("1d", "1(d)", 3,
         "Which is the optimality condition for u = x<sup>&alpha;</sup>y<sup>1 &minus; "
         "&alpha;</sup>?",
         choices=[MRS, MRS_XY, MRS_ALPHA, MRS_PRICE],
         answers=[H("1d.c")],
         mistakes=M({
             "1d.c~" + MRS_XY: "u<sub>x</sub> = &alpha;u/x and u<sub>y</sub> = (1 &minus; "
                               "&alpha;)u/y. Divide them again.",
             "1d.c~" + MRS_ALPHA: "MRS = u<sub>x</sub>/u<sub>y</sub>: the &alpha; belongs to x.",
             "1d.c~" + MRS_PRICE: "The slope of the budget line is &minus;%s/%s." % (PX, PY),
         }),
         explain="MRS = u<sub>x</sub>/u<sub>y</sub>. Show both partial derivatives, one step "
                 "per line."),
    Part("1e1", "1(e)", 2,
         "With &alpha; = 1/2 and a trip at 3: her trips and her basket?",
         form=["x =", BOX, "&nbsp; y =", BOX],
         answers=[H("1e1.0"), H("1e1.1")],
         mistakes=M({"1e1.0~450": "450 is what she spends on trips. Divide by the price.",
                     "1e1.0~300": "That is the intercept: all her income on trips."}),
         hints=["The condition gives y = 3x. Put that into 3x + y = 900."],
         explain="Half her income on each good: x = &alpha;m/%s." % PX),
    Part("1e2", "1(e)", 2,
         "And with a trip at 2?",
         form=["x =", BOX, "&nbsp; y =", BOX],
         answers=[H("1e2.0"), H("1e2.1")],
         mistakes=M({"1e2.0~450": "450 is what she spends on trips. Divide by the price."}),
         hints=["Now y = 2x and 2x + y = 900."],
         explain="More trips, the same basket."),
    Part("1e3", "1(e)", 1,
         "What happens to the amount she spends on the basket?",
         choices=[SAME, FALLS, RISES, TO_300],
         answers=[H("1e3.c")],
         mistakes=M({
             "1e3.c~" + FALLS: "Her spending on trips is 3 &times; 150 and then 2 &times; 225.",
             "1e3.c~" + RISES: "Compare y in the two answers above.",
             "1e3.c~" + TO_300: "Compare y in the two answers above.",
         }),
         explain="Cobb&ndash;Douglas spends fixed shares of income."),
]

sunniva = ExamProblem(
    "Problem 1 &middot; Sunniva's trips",
    "Sunniva has 900 a month to spend on train trips x and a basket of other goods y. The "
    "basket costs %s = 1 and a trip costs %s = 3. Her preferences are "
    "u(x, y) = x<sup>&alpha;</sup>y<sup>1 &minus; &alpha;</sup>, with &alpha; between 0 and 1. "
    "Trips are on the horizontal axis." % (PY, PX),
    SUNNIVA_PARTS, draw_sunniva, figsize=(5.8, 4.6),
)


# ======================================================================
# Problem 2: Home and Foreign in an Edgeworth box
# ======================================================================

TRADE = Economy(1 / 2, 1 / 3, (10, 60), (30, 60))       # Home is A, Foreign is B


def _box(ax, e):
    # Like ed.box, with the paper's names on the corners. This box is three
    # times as tall as it is wide, so it is not drawn to scale.
    ax.set_xlim(0, e.X)
    ax.set_ylim(0, e.Y)
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    kw = dict(color=INK, fontsize=10)
    ax.text(e.X, -0.025 * e.Y, r"trips $\rightarrow$", ha="right", va="top", **kw)
    ax.text(-0.025 * e.X, e.Y, r"basket $\uparrow$", ha="right", va="top", **kw)
    ax.text(-0.025 * e.X, -0.025 * e.Y, "Home", ha="right", va="top", color=LINE,
            fontsize=11, weight="bold")
    ax.text(1.025 * e.X, 1.025 * e.Y, "Foreign", ha="left", va="bottom", color=CURVE,
            fontsize=11, weight="bold")


def draw_trade(ax, done):
    e = TRADE
    if "2b1" not in done:
        _waiting(ax)
        return
    _box(ax, e)
    gp.dot(ax, 10, 60, r"$\omega$", 8, 6, colour=INK)
    if "2b2" in done:
        ed.ic_a(ax, e, 10, 60, color=LINE, lw=1.6, label="Home through " + r"$\omega$")
        ed.ic_b(ax, e, 10, 60, color=CURVE, lw=1.6, label="Foreign through " + r"$\omega$")
        ed.lens(ax, e, 10, 60, color=HALF, alpha=0.16, label="both better off")
    if "2c1" in done:
        ed.price_line(ax, e, 2, 10, 60, color=INK, lw=1.2, ls=":", label="price line, slope −2")
    if {"2c2", "2c3"} <= done:
        ed.ic_a(ax, e, 20, 40, color=LINE, lw=1.2, ls="--")
        ed.ic_b(ax, e, 20, 40, color=CURVE, lw=1.2, ls="--")
        gp.dot(ax, 20, 40, "E", 10, 2, colour=GREEN)
    if "2d1" in done:
        ed.contract(ax, e, color=GREEN, lw=1.2, label="contract curve")
    # Below the box: inside it, a legend would sit on top of the curves.
    if ax.get_legend_handles_labels()[0]:
        leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=8.5,
                        frameon=False)
        for text in leg.get_texts():
            text.set_color(INK)


DEMAND = "x = α(px·ωx + ωy)/px, with each country's own α and endowment"
D_NO_VALUE = "x = α(ωx + ωy)/px"
D_OTHER = "x = (1 − α)(px·ωx + ωy)/px"
D_NO_PRICE = "x = α(px·ωx + ωy)"

HOME_BUYS = "Home would give up 6 units of the basket for a trip and Foreign only 1, so Home buys trips from Foreign and pays in baskets; every allocation in the lens is better for both"
FOREIGN_BUYS = "Foreign buys trips from Home, because Foreign has more trips"
NO_TRADE = "There is nothing to trade, because both own 60 units of the basket"
ONE_GAINS = "Home gains from trade and Foreign loses the same amount"

EFFICIENT = "Both MRSs equal the price ratio, so the two indifference curves are tangent: no trade can make one country better off without hurting the other"
EFF_SAME = "Both countries end up with the same number of trips"
EFF_CLEAR = "Both markets clear"
EFF_BETTER = "Both countries are better off than at their endowments"

TRADE_PARTS = [
    Part("2a", "2(a)", 3,
         "Each country's demand for trips, as a function of %s and the value of its "
         "endowment?" % PX,
         choices=[DEMAND, D_NO_VALUE, D_OTHER, D_NO_PRICE],
         answers=[H("2a.c")],
         mistakes=M({
             "2a.c~" + D_NO_VALUE: "Income is the value of the endowment: trips are worth %s "
                                   "each." % PX,
             "2a.c~" + D_OTHER: "&alpha; is the share spent on x.",
             "2a.c~" + D_NO_PRICE: "That is spending on trips. Divide by the price.",
         }),
         explain="From 1(d): spend the share &alpha; of income on trips. Home: (10%s + 60)/(2%s). "
                 "Foreign: (30%s + 60)/(3%s)." % (PX, PX, PX, PX)),
    Part("2b1", "2(b)", 1,
         "How wide and how tall is the Edgeworth box?",
         form=["width", BOX, "&nbsp; height", BOX],
         answers=[H("2b1.0"), H("2b1.1")],
         mistakes=M({"2b1.0~10": "That is Home's trips alone. Add Foreign's.",
                     "2b1.1~60": "Add the two countries' baskets."}),
         explain="The sides are the world's totals. The figure is not drawn to scale."),
    Part("2b2", "2(b)", 2,
         "Each country's MRS at its endowment?",
         form=["Home", BOX, "&nbsp; Foreign", BOX],
         answers=[H("2b2.0"), H("2b2.1")],
         mistakes=M({"2b2.0~1/6": "Upside down: y/x, with &alpha;/(1 &minus; &alpha;) = 1.",
                     "2b2.1~2": "Foreign has &alpha;/(1 &minus; &alpha;) = 1/2."}),
         hints=["MRS = &alpha;y/((1 &minus; &alpha;)x), at (10, 60) and at (30, 60)."],
         explain="The two curves through &omega; cross, so there is a lens between them."),
    Part("2b3", "2(b)", 1,
         "Who gains by trading, and in which direction?",
         choices=[HOME_BUYS, FOREIGN_BUYS, NO_TRADE, ONE_GAINS],
         answers=[H("2b3.c")],
         mistakes=M({
             "2b3.c~" + FOREIGN_BUYS: "Compare the MRSs: who values a trip more?",
             "2b3.c~" + NO_TRADE: "The MRSs differ at &omega;.",
             "2b3.c~" + ONE_GAINS: "Inside the lens both are on higher curves.",
         }),
         explain="Different MRSs at the endowment are the gains from trade."),
    Part("2c1", "2(c)", 2,
         "The relative price of a trip that clears the market for trips?",
         form=["%s =" % PX, BOX],
         answers=[H("2c1.0")],
         mistakes=M({"2c1.0~1/2": "Upside down. Solve 15 + 50/%s = 40." % PX}),
         hints=["Add the two demands from 2(a) and set them equal to the 40 trips there are."],
         explain="5 + 30/%s + 10 + 20/%s = 40." % (PX, PX)),
    Part("2c2", "2(c)", 2,
         "Home's bundle at that price?",
         form=["trips", BOX, "&nbsp; basket", BOX],
         answers=[H("2c2.0"), H("2c2.1")],
         mistakes=M({"2c2.0~40": "Half of its income of 80, divided by the price of a trip."}),
         hints=["Home's income is 10%s + 60." % PX],
         explain="Home buys 10 trips and pays 20 units of the basket: point E in the figure."),
    Part("2c3", "2(c)", 2,
         "Foreign's bundle?",
         form=["trips", BOX, "&nbsp; basket", BOX],
         answers=[H("2c3.0"), H("2c3.1")],
         mistakes=M({"2c3.1~40": "Foreign spends two thirds of its income of 120 on the "
                                 "basket."}),
         hints=["Foreign's income is 30%s + 60." % PX],
         explain="The baskets add to 120: the other market clears too, by Walras' law."),
    Part("2d1", "2(d)", 2,
         "Each country's MRS at its equilibrium bundle?",
         form=["Home", BOX, "&nbsp; Foreign", BOX],
         answers=[H("2d1.0"), H("2d1.1")],
         mistakes=M({"2d1.1~4": "Foreign has &alpha;/(1 &minus; &alpha;) = 1/2."}),
         explain="Both equal the price ratio."),
    Part("2d2", "2(d)", 1,
         "Why is the allocation Pareto efficient?",
         choices=[EFFICIENT, EFF_SAME, EFF_CLEAR, EFF_BETTER],
         answers=[H("2d2.c")],
         mistakes=M({
             "2d2.c~" + EFF_SAME: "A coincidence of these numbers, not the reason.",
             "2d2.c~" + EFF_CLEAR: "That makes it feasible. What makes it efficient?",
             "2d2.c~" + EFF_BETTER: "Every point in the lens does that; only some are "
                                    "efficient.",
         }),
         explain="The first welfare theorem, shown directly."),
]

trade = ExamProblem(
    "Problem 2 &middot; Home and Foreign",
    "Home owns 10 trips and 60 units of the basket, and has &alpha;<sub>H</sub> = 1/2. "
    "Foreign owns 30 trips and 60 units of the basket, and has &alpha;<sub>F</sub> = 1/3. "
    "Both have u = x<sup>&alpha;</sup>y<sup>1 &minus; &alpha;</sup>. The basket is the "
    "numeraire, %s = 1. Home is in the south-west corner of the box." % PY,
    TRADE_PARTS, draw_trade, figsize=(5.4, 5.6),
)


# ======================================================================
# Problem 3: pollution and clean air
# ======================================================================

def draw_air(ax, done):
    # The paper gives no utility functions, so this is one example: each
    # country owns one unit of x and values air as x + sqrt(its share of it).
    if "3a1" not in done:
        _waiting(ax)
        return
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    kw = dict(color=INK, fontsize=10)
    ax.text(2, -0.03, r"$x_A$ $\rightarrow$", ha="right", va="top", **kw)
    ax.text(-0.03, 1, r"pollution $\uparrow$", ha="right", va="top", rotation=90, **kw)
    ax.text(2.03, 0, r"clean air $\downarrow$", ha="left", va="bottom", rotation=90, **kw)
    ax.text(-0.03, -0.03, "A", ha="right", va="top", color=LINE, fontsize=12, weight="bold")
    ax.text(2.03, 1.03, "B", ha="left", va="bottom", color=CURVE, fontsize=12, weight="bold")
    P = np.linspace(0, 1, 200)
    gp.dot(ax, 1, 1, "no rule of law", -8, -14, colour=INK, ha="right")
    if "3a2" in done:
        ax.plot(2 - np.sqrt(P), P, color=LINE, lw=1.6, label="A's curve")
        ax.plot(1 + np.sqrt(1 - P), P, color=CURVE, lw=1.6, label="B's curve")
        ax.fill_betweenx(P, 2 - np.sqrt(P), 1 + np.sqrt(1 - P), color=HALF, alpha=0.16, lw=0,
                         label="both better off")
    if "3b2" in done:
        p = 0.5 / np.sqrt(0.5)
        ax.plot([1, 1 + p], [1, 0], color=INK, lw=1.2, ls=":", label="quota price line")
        ax.axhline(0.5, color=GREEN, lw=1.2, label="efficient")
        gp.dot(ax, 1 + p / 2, 0.5, "quota market", 8, 6, colour=GREEN)
    ax.set_title("One example, drawn from A's corner", loc="left", color=MUTE, fontsize=9)
    gp.legend(ax, loc="lower left")


FAIL = "Clean air has no price, so A pollutes until its own marginal benefit is zero and ignores B's loss. At that corner the two MRSs differ: B would pay A to pollute less, and both would gain"
FAIL_RICH = "A ends up richer than B, and that is unfair"
FAIL_X = "The total amount of good x falls when A pollutes"
FAIL_NOT = "It is Pareto efficient: no trade can help B without hurting A"

BUDGETS = "A: px·xA = px·ωA + pC·C;   B: px·xB + pC·C = px·ωB"
B_REVERSED = "A: px·xA + pC·C = px·ωA;   B: px·xB = px·ωB + pC·C"
B_UNCHANGED = "A: px·xA = px·ωA;   B: px·xB = px·ωB"
B_LUMP = "A: px·xA = px·ωA + pC;   B: px·xB = px·ωB − pC"

CLEARS = "pC/px equals both countries' MRS between clean air and x: the clean air A wants to sell equals what B wants to buy. Facing one price, their indifference curves are tangent, so no trade can help one without hurting the other"
C_FREE = "pC/px = 0: clean air has to be free for the market to clear"
C_ONE = "pC/px = 1, because there is one unit of air"
C_ANY = "Any positive pC/px clears the market"

AIR_PARTS = [
    Part("3a1", "3(a)", 1,
         "With no rule of law, how much does A pollute, and how much clean air is left for B?",
         form=["P =", BOX, "&nbsp; C =", BOX],
         answers=[H("3a1.0"), H("3a1.1")],
         mistakes=M({"3a1.0~0": "Pollution costs A nothing, and A enjoys it."}),
         explain="A corner of the box: A pays nothing, so A takes all the air."),
    Part("3a2", "3(a)", 2,
         "Why is that outcome not Pareto efficient?",
         choices=[FAIL, FAIL_RICH, FAIL_X, FAIL_NOT],
         answers=[H("3a2.c")],
         mistakes=M({
             "3a2.c~" + FAIL_RICH: "Efficiency is not about who is richer.",
             "3a2.c~" + FAIL_X: "The resource constraints leave total x unchanged.",
             "3a2.c~" + FAIL_NOT: "B would give up some x for cleaner air, and the last unit "
                                  "of pollution is worth almost nothing to A.",
         }),
         explain="In the box: the two curves through that corner cross, and the lens between "
                 "them is what a missing market leaves on the table."),
    Part("3b1", "3(b)", 2,
         "A now holds the rights to the air and sells quotas of clean air at a price "
         "p<sub>C</sub>. The two budget constraints?",
         choices=[BUDGETS, B_REVERSED, B_UNCHANGED, B_LUMP],
         answers=[H("3b1.c")],
         mistakes=M({
             "3b1.c~" + B_REVERSED: "A owns the air: A is paid for the clean air it leaves.",
             "3b1.c~" + B_UNCHANGED: "Those are the constraints without a market.",
             "3b1.c~" + B_LUMP: "B pays for the clean air it buys, C units, not a fixed sum.",
         }),
         explain="The same thing with pollution: p<sub>x</sub>x<sub>A</sub> + p<sub>C</sub>P = "
                 "p<sub>x</sub>&omega;<sub>A</sub> + p<sub>C</sub>, since A owns one unit and "
                 "C = 1 &minus; P."),
    Part("3b2", "3(b)", 1,
         "When does the quota market clear, and why is that allocation Pareto efficient?",
         choices=[CLEARS, C_FREE, C_ONE, C_ANY],
         answers=[H("3b2.c")],
         mistakes=M({
             "3b2.c~" + C_FREE: "At a price of zero A sells no clean air at all.",
             "3b2.c~" + C_ONE: "The price depends on how much each side values the air.",
             "3b2.c~" + C_ANY: "At most prices one side wants to trade more than the other.",
         }),
         explain="Once clean air has a price the first welfare theorem applies again."),
]

air = ExamProblem(
    "Problem 3 &middot; Pollution",
    "Two countries share one unit of air. Country B enjoys clean air C, and country A enjoys "
    "the opposite, pollution P = 1 &minus; C. Each also consumes good x and owns "
    "&omega;<sub>A</sub> or &omega;<sub>B</sub> of it.",
    AIR_PARTS, draw_air, figsize=(5.8, 4.4),
)


# ======================================================================
# Problem 4: ten multiple-choice questions
# ======================================================================

def _mc(n, prompt, options, hint, explain):
    # One point each. options are the paper's (a) to (d), in the paper's order.
    return Part("m%d" % n, "4.%d" % n, 1, prompt,
                choices=["(%s) %s" % (letter, text) for letter, text in zip("abcd", options)],
                answers=[H("m%d.c" % n)], hints=[hint], explain=explain)


CONCEPT_PARTS = [
    _mc(1, "The slope of the budget line, &minus;%s/%s, tells you" % (PX, PY),
        ["how much utility one more unit of x gives",
         "how many units of y must be given up to afford one more unit of x",
         "the share of income spent on x",
         "the income elasticity of x"],
        "The budget line is about what the market lets you swap, not about tastes.",
        "The market's rate of exchange between the two goods."),
    _mc(2, "At a bundle where MRS = u<sub>x</sub>/u<sub>y</sub> is larger than %s/%s, a "
           "consumer with smooth preferences should" % (PX, PY),
        ["buy more x and less y", "buy less x and more y",
         "stay put, since the bundle is optimal", "spend less than the whole budget"],
        "She values one more x at more y than the market charges for it.",
        "She keeps swapping y for x until the MRS has fallen to the price ratio."),
    _mc(3, "A good is a Giffen good if",
        ["its demand rises when income rises", "it is a luxury",
         "it is inferior and the income effect of a price change outweighs the substitution "
         "effect",
         "it is a perfect substitute for another good"],
        "Demand must rise when the price rises. Which effect can push that way?",
        "Inferior, and strongly enough to beat the substitution effect."),
    _mc(4, "When the price of good x rises, the substitution effect on its own",
        ["always reduces the quantity of x demanded", "always raises the quantity of x demanded",
         "reduces the quantity of x only if x is a normal good",
         "has no sign without more information"],
        "Normal or inferior decides the sign of the income effect. And the other one?",
        "The substitution effect never goes with the price."),
    _mc(5, "A good's income elasticity is 1.6. As income rises, the share of the budget spent "
           "on it",
        ["falls", "stays constant", "rises", "depends on the price of the good"],
        "Demand grows by 1.6% when income grows by 1%.",
        "Above one: spending on the good grows faster than income. A luxury."),
    _mc(6, "In the two-period model the interest rate rises. Which consumer is unambiguously "
           "better off?",
        ["a borrower in period 1", "a lender in period 1", "both", "neither"],
        "The budget line pivots around the endowment. Whose old bundle is still affordable?",
        "A lender can still afford her old bundle and stays a lender: revealed preference."),
    _mc(7, "A risk-averse person faces a lottery paying 4 or 16 with equal probability. "
           "Compared with receiving 10 for certain, she",
        ["prefers the lottery", "prefers the certain 10",
         "is indifferent, since the expected values are equal",
         "cannot rank the two without knowing prices"],
        "The expected value of the lottery is 10 as well. What does risk aversion mean?",
        "Concave utility: u(10) is above the average of u(4) and u(16)."),
    _mc(8, "In a two-good exchange economy you have found the price at which the market for x "
           "clears. The market for y",
        ["must be checked separately", "clears at the same price, by Walras's law",
         "clears only if both consumers have the same preferences",
         "clears only if the endowments are equal"],
        "Every budget balances, so the value of total excess demand is zero.",
        "p&middot;z<sub>x</sub> + z<sub>y</sub> = 0 at every price."),
    _mc(9, "The First Welfare Theorem says that a competitive equilibrium is",
        ["fair, since everyone faces the same prices",
         "Pareto efficient, given no externalities and price-taking",
         "the allocation that maximizes total utility", "unique"],
        "The theorem is about efficiency, and it needs conditions.",
        "It says nothing about fairness, and Problem 3 shows what an externality does to it."),
    _mc(10, "Pollution is an externality because",
        ["it is produced by firms rather than consumers", "it harms many people at once",
         "its effect on others carries no price, so the polluter's choice ignores their loss",
         "it cannot be measured"],
        "What is missing in Problem 3(a) and present in 3(b)?",
        "A missing market: the effect on others has no price."),
]

concepts = ExamProblem(
    "Problem 4 &middot; Key concepts",
    "Ten multiple-choice questions, one point each. Exactly one answer is correct. On paper, "
    "write the question number and the letter, one line per question.",
    CONCEPT_PARTS,
)


paper = ExamPaper(
    "Workshop 1 &middot; your score",
    [sunniva, trade, air, concepts],
    note="The page checks final answers and conclusions. On the exam the derivation, the "
         "figure and the sentences carry the marks, so compare those with the solutions.",
)
