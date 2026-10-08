"""
guided_s09.py - session 9 guided page: comparative advantage, the Ricardian model.

    Part 1  frontiers  the running example: two frontiers, absolute and
                       comparative advantage
    Part 2  autarky    autarky prices, point A and the world relative supply
                       staircase
    Part 3  gains      gains from trade: points B and C, and the price that
                       clears
    Part 4  wages      wages, unit costs and the low-wage fallacy (Try it,
                       review question 1)
    Part 5  worksheet  the notes' worksheet: roles flipped
    Part 6  vinland    review questions 2-5: Vinland and Estland
    Part 7  norway     problem A9.1: Norway and Portugal
    Part 8  tariff     the small-country tariff (context: not examinable)

Answers are hashes in answers_s09.py, generated from
answer_keys/s09_keys.py in the private repo. The maths is ricardo.py: its
self-check reproduces every number asked for here.
"""

import numpy as np

import guided_plots as gp
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW

H, M = answers("s09")

CTX = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
       "context: not examinable</span> ")
AX, AY = "a<sub>x</sub>", "a<sub>y</sub>"
AXF, AYF = "a<sub>x</sub>*", "a<sub>y</sub>*"
SHARE = 0.6                      # the notes' tastes: u = x^0.6 y^0.4


# ------------------------------------------------------------------ drawing ---

def _panel(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    # A bare frame with ticks only where a number has been earned.
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.tick_params(colors=MUTE, labelsize=8.5)


def _ppf(ax, X, Y, **kw):
    kw.setdefault("color", LINE)
    kw.setdefault("lw", 2)
    ax.plot([0, X], [Y, 0], **kw)


def _trade_line(ax, x0, y0, p, **kw):
    # The world price line through (x0, y0), slope -p, from axis to axis.
    kw.setdefault("color", NEW)
    kw.setdefault("lw", 1.6)
    kw.setdefault("ls", "--")
    ax.plot([0, x0 + y0 / p], [y0 + p * x0, 0], **kw)


def _ic(ax, x0, y0, xmax, **kw):
    # The indifference curve of u = x^0.6 y^0.4 through (x0, y0).
    xs = np.linspace(xmax * 0.03, xmax, 300)
    ys = (x0 ** SHARE * y0 ** (1 - SHARE) / xs ** SHARE) ** (1 / (1 - SHARE))
    kw.setdefault("color", CURVE)
    kw.setdefault("lw", 1.4)
    ax.plot(xs, ys, **kw)


def _stairs(ax, lo, hi, corner, qmax, pmax, **kw):
    # World relative supply: flat at each autarky price, vertical in between.
    kw.setdefault("color", LINE)
    kw.setdefault("lw", 2)
    ax.plot([0, 0, corner, corner, qmax], [0, lo, lo, hi, hi], **kw)


def _bars(ax, names, groups, labels, colours, ymax):
    # Grouped bars: one group per name, one bar per entry of groups.
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    xs = np.arange(len(names))
    width = 0.7 / max(len(groups), 1)
    for i, (values, label, colour) in enumerate(zip(groups, labels, colours)):
        ax.bar(xs + (i - (len(groups) - 1) / 2) * width, values, width=width * 0.92,
               color=colour, label=label)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=9, color=INK)
    ax.set_yticks([])
    ax.set_ylim(0, ymax)


# ======================================================================
# Part 1: two frontiers, absolute and comparative advantage
# ======================================================================

def draw_frontiers(fig, stage):
    home, foreign = fig.subplots(1, 2)
    big = stage >= 5
    _panel(home, 215 if big else 112, 110 if big else 66, "cloth", "wine", "Home",
           xticks=[100] + ([200] if big else []) if stage >= 1 else [],
           yticks=[50] + ([100] if big else []) if stage >= 1 else [])
    _panel(foreign, 112, 66, "cloth", "wine", "Foreign",
           xticks=[30] if stage >= 2 else [], yticks=[60] if stage >= 2 else [])
    if stage == 0:
        gp.start(home)
    if stage >= 1:
        _ppf(home, 100, 50)
    if stage >= 2:
        _ppf(foreign, 30, 60, color=CURVE)
    if stage >= 3:
        home.text(52, 28, "slope 1/2", color=LINE, fontsize=9)
        foreign.text(18, 30, "slope 2", color=CURVE, fontsize=9)
    if stage >= 4:
        home.text(0.98, 0.9, "flatter: cheaper cloth", transform=home.transAxes, ha="right",
                  color=LINE, fontsize=9)
    if big:
        _ppf(home, 200, 100, color=NEW, ls="--")
        home.text(105, 52, "twice as productive:\nsame slope", color=NEW, fontsize=9)
    fig.subplots_adjust(wspace=0.3)


ADV = "Home has the absolute advantage in both goods; the comparative advantage is Home's in cloth and Foreign's in wine"
ADV_BOTH = "Home has both the absolute and the comparative advantage in both goods"
ADV_SIZE = "Foreign has the comparative advantage in cloth, because it has more workers"
ADV_NONE = "Nobody has a comparative advantage, since Home is better at everything"

FRONTIER_QUESTIONS = [
    Question(
        "r1",
        "Home needs %s = 1 worker per unit of cloth and %s = 2 per unit of wine, and has "
        "E = 100 workers. Where does its frontier meet each axis?" % (AX, AY),
        form=["cloth", BOX, "&nbsp; wine", BOX],
        answers=[H("r1.0"), H("r1.1")],
        mistakes=M({"r1.1~200": "Divide: each unit of wine takes 2 workers, so E/%s." % AY}),
        explain="Full employment: %s&middot;q<sub>x</sub> + %s&middot;q<sub>y</sub> = E, a straight "
                "line." % (AX, AY)),
    Question(
        "r2",
        "Foreign needs %s = 6 and %s = 3, with E* = 180 workers. Its intercepts?" % (AXF, AYF),
        form=["cloth", BOX, "&nbsp; wine", BOX],
        answers=[H("r2.0"), H("r2.1")],
        mistakes=M({"r2.0~1080": "Divide the labor force by the requirement: 180/6."}),
        explain="Foreign's frontier is the steeper one."),
    Question(
        "r3",
        "The absolute slope of each frontier, %s/%s: the wine given up for one more cloth?"
        % (AX, AY),
        form=["Home", BOX, "&nbsp; Foreign", BOX],
        answers=[H("r3.0"), H("r3.1")],
        mistakes=M({"r3.0~2": "Upside down. One more cloth pulls 1 worker out of wine, where "
                              "she made 1/2 a unit.",
                    "r3.1~1/2": "Upside down: 6 workers leave wine, where each made 1/3."}),
        explain="Slope, marginal rate of transformation, opportunity cost: three names for one "
                "number."),
    Question(
        "r4",
        "Who has the absolute advantage, and who the comparative advantage?",
        choices=[ADV, ADV_BOTH, ADV_SIZE, ADV_NONE],
        answers=[H("r4.c")],
        mistakes=M({
            "r4.c~" + ADV_BOTH: "If Home's ratio is the smaller one in cloth, it has to be the "
                                "larger one in wine.",
            "r4.c~" + ADV_SIZE: "The labor force moves the intercepts, never the slope.",
            "r4.c~" + ADV_NONE: "Compare ratios, not levels: 1/2 against 2.",
        }),
        explain="Absolute advantage compares levels, 1 &lt; 6 and 2 &lt; 3. Comparative advantage "
                "compares opportunity costs, and nobody has it in both goods."),
    Question(
        "r5",
        "Make Home twice as productive at everything: %s = 1/2 and %s = 1. The new cloth "
        "intercept, and the new slope?" % (AX, AY),
        form=["cloth", BOX, "&nbsp; slope", BOX],
        answers=[H("r5.0"), H("r5.1")],
        mistakes=M({"r5.1~1": "Both requirements halved: (1/2)/1.",
                    "r5.1~1/4": "Both requirements halved, not just one."}),
        explain="A uniform gain shifts the frontier without rotating it: a richer country, the "
                "same trade pattern."),
]

frontiers = GuidedProblem(
    "Part 1 &middot; Two frontiers",
    "The notes' running example, with cloth as good x and wine as good y. Labor is the only "
    "factor: it moves freely between industries, and not at all between countries.",
    FRONTIER_QUESTIONS, draw_frontiers, figsize=(8.0, 3.8), whole_figure=True,
    outro="The flatter frontier is the comparative advantage in cloth.",
    sources=[NOTES("p. 2&ndash;4")],
)


# ======================================================================
# Part 2: autarky and the world relative supply staircase
# ======================================================================

def draw_autarky(fig, stage):
    home, rs = fig.subplots(1, 2)
    _panel(home, 112, 66, "cloth", "wine", "Home under autarky", xticks=[100], yticks=[50])
    _ppf(home, 100, 50)
    if stage >= 1:
        home.text(22, 48, "slope = p = 1/2", color=LINE, fontsize=9)
    if stage >= 2:
        _ic(home, 60, 20, 112)
        gp.dot(home, 60, 20, "A", 6, 6, colour=CURVE)

    _panel(rs, 3.4, 2.8, "world cloth / world wine", "p", "World relative supply",
           yticks=[0.5, 2] if stage >= 1 else [], xticks=[5 / 3] if stage >= 4 else [])
    rs.set_yticklabels(["1/2", "2"] if stage >= 1 else [])
    rs.set_xticklabels(["5/3"] if stage >= 4 else [])
    if stage >= 1:
        for p in (0.5, 2):
            rs.axhline(p, color=GREY, lw=0.8, ls=":")
    if stage >= 3:
        rs.plot([0, 0], [0, 0.5], color=LINE, lw=3, clip_on=False)
    if stage >= 4:
        rs.plot([5 / 3, 5 / 3], [0.5, 2], color=LINE, lw=2)
    if stage >= 5:
        _stairs(rs, 0.5, 2, 5 / 3, 3.4, 2.8)
        rs.text(0.5, 0.56, "Home: any mix", color=LINE, fontsize=8.5)
        rs.text(2.1, 2.06, "Foreign: any mix", color=LINE, fontsize=8.5)
    if stage >= 6:
        q = np.linspace(0.45, 3.4, 200)
        rs.plot(q, SHARE / (1 - SHARE) / q, color=CURVE, lw=1.6, label="relative demand")
        gp.legend(rs, loc="center right")
    fig.subplots_adjust(wspace=0.3)


BOTH_WINE = "Both make only wine: cloth pays less than wine in both countries"
SPLIT = "Home makes only cloth and Foreign only wine"
BOTH_CLOTH = "Both make only cloth"
HOME_MIX = "Home makes any mix and Foreign only wine"

STEP_HOME = "Home: its two wages are equal there, so any mix earns the same; Foreign still makes only wine"
STEP_FOREIGN = "Foreign: it is the less productive country"
STEP_BOTH = "Both countries make both goods"
STEP_NONE = "Neither: both are fully specialized"

NEITHER = "Neither: relative demand picks the point on the staircase, and the two autarky prices only fence it in"
SET_HOME = "Home, the more productive country"
SET_FOREIGN = "Foreign, the country with more workers"
SET_MEAN = "It is the average of the two autarky prices"

AUTARKY_QUESTIONS = [
    Question(
        "a1",
        "Under autarky both goods are made, so a worker must earn the same in each: "
        "p<sub>x</sub>/%s = p<sub>y</sub>/%s. The autarky relative price of cloth, "
        "p = p<sub>x</sub>/p<sub>y</sub>, in each country?" % (AX, AY),
        form=["Home", BOX, "&nbsp; Foreign", BOX],
        answers=[H("a1.0"), H("a1.1")],
        mistakes=M({"a1.0~2": "Upside down: p = %s/%s." % (AX, AY)}),
        explain="The autarky price equals the slope of the frontier. Technology alone fixes it."),
    Question(
        "a2",
        "Tastes decide the point. Home spends 60% of its income on cloth "
        "(u = x<sup>0.6</sup>y<sup>0.4</sup>), and its income is worth 50 wine. Point A?",
        form=["A = (", BOX, ",", BOX, ")"],
        answers=[H("a2.0"), H("a2.1")],
        mistakes=M({"a2.0~30": "30 wine is what it spends on cloth. Divide by the price, 1/2.",
                    "a2.1~30": "The other 40% goes to wine."}),
        explain="At A the frontier's slope, the autarky price and the MRS are all 1/2. "
                "Consumption is trapped on the frontier."),
    Question(
        "a3",
        "Open the borders and build world relative supply one price at a time. The world "
        "price is below 1/2. Who makes what?",
        choices=[BOTH_WINE, SPLIT, BOTH_CLOTH, HOME_MIX],
        answers=[H("a3.c")],
        mistakes=M({
            "a3.c~" + SPLIT: "Below 1/2 cloth sells for less than it costs even at Home.",
            "a3.c~" + BOTH_CLOTH: "Cloth is cheap here. Compare p/%s with 1/%s." % (AX, AY),
            "a3.c~" + HOME_MIX: "That is at exactly 1/2.",
        }),
        explain="World cloth output is zero, so relative supply is zero."),
    Question(
        "a4",
        "Now any price strictly between 1/2 and 2. Home's output of cloth, Foreign's output "
        "of wine, and the relative supply of cloth?",
        form=["cloth", BOX, "&nbsp; wine", BOX, "&nbsp; ratio", BOX],
        answers=[H("a4.0"), H("a4.1"), H("a4.2")],
        mistakes=M({"a4.2~3/5": "Cloth over wine."}),
        explain="It stays there for every price in the range: the vertical segment."),
    Question(
        "a5",
        "On the lower flat step, at exactly p = 1/2, which country makes both goods?",
        choices=[STEP_HOME, STEP_FOREIGN, STEP_BOTH, STEP_NONE],
        answers=[H("a5.c")],
        mistakes=M({
            "a5.c~" + STEP_FOREIGN: "Foreign's own autarky price, 2, is a long way off.",
            "a5.c~" + STEP_BOTH: "Each country makes both only at its own autarky price.",
            "a5.c~" + STEP_NONE: "At 1/2 Home's workers earn the same in either industry.",
        }),
        explain="A straight frontier gives a corner response: a staircase. The upper step, at "
                "2, is Foreign's."),
    Question(
        "a6",
        "Who sets the world price, Home or Foreign?",
        choices=[NEITHER, SET_HOME, SET_FOREIGN, SET_MEAN],
        answers=[H("a6.c")],
        mistakes=M({
            "a6.c~" + SET_HOME: "Productivity levels set wages, not the price.",
            "a6.c~" + SET_FOREIGN: "Size moves the corner of the staircase, but demand still "
                                   "picks the point.",
            "a6.c~" + SET_MEAN: "Nothing forces the midpoint. What does the world want to buy?",
        }),
        explain="If the world wants a lot of cloth the price lands near 2 and Home does well."),
]

autarky = GuidedProblem(
    "Part 2 &middot; Autarky and the world price",
    "The same two countries. First closed, then open: one world relative price of cloth, "
    "found where world relative supply meets world relative demand.",
    AUTARKY_QUESTIONS, draw_autarky, figsize=(8.0, 3.8), whole_figure=True,
    outro="Trade happens only between the two autarky prices: the bargaining range.",
    sources=[NOTES("p. 4&ndash;8")],
)


# ======================================================================
# Part 3: gains from trade
# ======================================================================

def draw_gains(fig, stage):
    home, foreign = fig.subplots(1, 2)
    _panel(home, 112, 110, "cloth", "wine", "Home", xticks=[100],
           yticks=[50] + ([100] if stage >= 2 else []))
    _panel(foreign, 70, 110, "cloth", "wine", "Foreign", xticks=[30], yticks=[60])
    _ppf(home, 100, 50)
    _ic(home, 60, 20, 112, lw=1.1)
    gp.dot(home, 60, 20, "A", -12, -12, colour=CURVE)
    _ppf(foreign, 30, 60, color=LINE)
    _ic(foreign, 18, 24, 70, lw=1.1)
    gp.dot(foreign, 18, 24, "A*", -18, -12, colour=CURVE)
    if stage >= 1:
        gp.dot(home, 100, 0, "B", 6, 6, colour=NEW)
    if stage >= 2:
        _trade_line(home, 100, 0, 1)
    if stage >= 3:
        _ic(home, 60, 40, 112)
        gp.dot(home, 60, 40, "C", 8, 4, colour=GREEN)
        home.plot([60, 60, 100], [40, 0, 0], color=GREY, lw=0.8, ls=":")
        home.text(0.98, 0.95, "sell 40 cloth,\nbuy 40 wine", transform=home.transAxes,
                  ha="right", va="top", color=MUTE, fontsize=8.5)
    if stage >= 4:
        gp.dot(foreign, 0, 60, "B*", 8, 2, colour=NEW)
        _trade_line(foreign, 0, 60, 1)
        _ic(foreign, 36, 24, 70)
        gp.dot(foreign, 36, 24, "C*", 8, 4, colour=GREEN)
    if stage >= 6:
        _trade_line(home, 60, 20, 1, color=HALF, lw=1.1, ls=":")
        home.text(4, 84, "through A:\nexchange gain", color=HALF, fontsize=8.5)
    fig.subplots_adjust(wspace=0.3)


EX_SPEC = "Exchange: trading from A at the world price already reaches bundles above the frontier. Specialization: moving production to B pushes the budget line out further"
ONE_GAIN = "There is one gain only: Home sells cloth at a higher price"
SPEC_FIRST = "Without specialization, trade cannot help at all"
ZERO_SUM = "Home gains only what Foreign loses"

BIG_HOME = "The world price equals Home's autarky price: Home still makes both goods and gains nothing, and the small country takes the gain"
BIG_WINS = "Home gains most, because it trades the most"
BIG_SPLIT = "The gains are split in proportion to the labor forces"
BIG_NONE = "Neither country gains"

GAINS_QUESTIONS = [
    Question(
        "g1",
        "The world price settles at p = 1. A cloth now buys one wine and costs Home only half "
        "a wine to make. Where does Home produce?",
        form=["B = (", BOX, ",", BOX, ")"],
        answers=[H("g1.0"), H("g1.1")],
        mistakes=M({"g1.0~60": "That is the autarky point. Above its autarky price every Home "
                               "worker earns more in cloth."}),
        explain="Production moves to the corner of the frontier."),
    Question(
        "g2",
        "From B, Home can sell cloth one for one. Where does that line meet the wine axis, and "
        "what is its absolute slope?",
        form=["wine", BOX, "&nbsp; slope", BOX],
        answers=[H("g2.0"), H("g2.1")],
        mistakes=M({"g2.0~50": "That is the frontier. Sell all 100 cloth at one wine each.",
                    "g2.1~1/2": "That is the frontier's slope. The line through B has slope p."}),
        explain="Home's new budget line: steeper than the frontier, and above it everywhere "
                "except at B."),
    Question(
        "g3",
        "Home still wants 60 cloth. How much cloth does it ship abroad, and what does it "
        "consume?",
        form=["ships", BOX, "&nbsp; C = (", BOX, ",", BOX, ")"],
        answers=[H("g3.0"), H("g3.1"), H("g3.2")],
        mistakes=M({"g3.2~20": "It brings home one wine for each of the 40 cloth it ships."}),
        explain="The same cloth and twice the wine: C lies above the frontier, which was "
                "impossible before."),
    Question(
        "g4",
        "Foreign is the mirror image. With the same tastes it consumed A* = (18, 24) under "
        "autarky; now it specializes at B* = (0, 60). Its bundle C* at p = 1?",
        form=["C* = (", BOX, ",", BOX, ")"],
        answers=[H("g4.0"), H("g4.1")],
        mistakes=M({"g4.0~18": "Its income is 60 wine, 60% of it goes to cloth, and cloth now "
                               "costs 1, not 2."}),
        explain="The same wine and twice the cloth. Both countries consume above their "
                "frontiers."),
    Question(
        "g5",
        "Check the market: Home wants to sell 40 cloth and Foreign wants to buy 36. With these "
        "tastes Home buys 60 cloth at any price in the range and Foreign buys 36/p. Which price "
        "clears the cloth market?",
        form=["p =", BOX],
        answers=[H("g5.0")],
        mistakes=M({"g5.0~1": "At p = 1 forty are offered and thirty-six wanted."}),
        hints=["Demand equals supply: 60 + 36/p = 100."],
        explain="Relative demand selects the price inside the range. The notes keep p = 1 for "
                "the cleaner arithmetic."),
    Question(
        "g6",
        "Two gains hide in Home's move from A to C. Which two?",
        choices=[EX_SPEC, ONE_GAIN, SPEC_FIRST, ZERO_SUM],
        answers=[H("g6.c")],
        mistakes=M({
            "g6.c~" + ONE_GAIN: "Compare the line through A with the line through B.",
            "g6.c~" + SPEC_FIRST: "Stay at A and swap at the world price: already above the "
                                  "frontier.",
            "g6.c~" + ZERO_SUM: "Foreign moved above its frontier too.",
        }),
        explain="The exchange gain alone improves welfare; specialization makes it larger."),
    Question(
        "g7",
        "Worksheet task 3: let Home be very large, so that relative demand cuts the lower flat "
        "step. What happens?",
        choices=[BIG_HOME, BIG_WINS, BIG_SPLIT, BIG_NONE],
        answers=[H("g7.c")],
        mistakes=M({
            "g7.c~" + BIG_WINS: "Whose price moved? A country gains only when its price does.",
            "g7.c~" + BIG_SPLIT: "The gain goes to the country whose price moves most.",
            "g7.c~" + BIG_NONE: "Foreign trades at 1/2 instead of its own 2.",
        }),
        explain="The small partner cannot absorb enough cloth to move the big country off its "
                "own step."),
]

gains = GuidedProblem(
    "Part 3 &middot; Gains from trade",
    "Under autarky one point did two jobs. Under trade they come apart: production at B, "
    "consumption at C. Each panel starts with the frontier and the autarky point.",
    GAINS_QUESTIONS, draw_gains, figsize=(8.0, 4.2), whole_figure=True,
    outro="Bring this diagram, with A, B and C marked, to the in-person session.",
    sources=[NOTES("p. 8&ndash;10"), NOTES("p. 18, worksheet task 3")],
)


# ======================================================================
# Part 4: wages, unit costs and the low-wage fallacy
# ======================================================================

def draw_wages(fig, stage):
    costs, gaps = fig.subplots(1, 2)
    costs.set_title("Unit cost = wage × labor", loc="left", color=INK, fontsize=9.5)
    if stage >= 2:
        _bars(costs, ["cloth", "wine"], [[1, 2], [2, 1]], ["Home", "Foreign"],
              [LINE, CURVE], 2.6)
        gp.legend(costs, loc="upper center")
    else:
        _bars(costs, ["cloth", "wine"], [], [], [], 2.6)

    gaps.set_title("Productivity gap a*/a", loc="left", color=INK, fontsize=9.5)
    if stage >= 3:
        _bars(gaps, ["wine", "cloth"], [[1.5, 6]], [None], [[CURVE, LINE]], 7)
        gaps.axhline(3, color=INK, lw=1.6, ls="--")
        gaps.text(-0.36, 3.12, "w/w* = 3", color=INK, fontsize=9)
    else:
        _bars(gaps, ["wine", "cloth"], [], [], [], 7)
    if stage >= 5:
        gaps.axhline(4.5, color=NEW, lw=1.6, ls="--")
        gaps.text(-0.36, 4.62, "at p = 3/2: 9/2", color=NEW, fontsize=9)
    fig.subplots_adjust(wspace=0.25)


RULES = "Comparative advantage decides what a country exports; absolute advantage decides how high its wages are"
RULES_REV = "Absolute advantage decides the trade pattern; comparative advantage decides wages"
RULES_ABS = "Absolute advantage decides both"
RULES_COMP = "Comparative advantage decides both"

LOW_WAGE = "Their wages are low because their productivity is low; costs are wages times labor requirements, and the wage ratio adjusts until each country is cheapest in some good"
LW_TRUE = "It is true: a country with lower wages undersells in every good"
LW_ABS = "A low-wage country can only export if it also has an absolute advantage"
LW_NONE = "Wages play no role in costs in this model"

WAGE_QUESTIONS = [
    Question(
        "w1",
        "Free trade at p = 1, with wine the numeraire. Home exports cloth, so a worker earns "
        "w = p/%s. Foreign exports wine, so w* = 1/%s. The two wages?" % (AX, AYF),
        form=["w =", BOX, "&nbsp; w* =", BOX],
        answers=[H("w1.0"), H("w1.1")],
        mistakes=M({"w1.1~1/6": "Foreign makes wine: divide by %s = 3." % AYF}),
        explain="Home wages are three times Foreign wages: the model's whole account of why "
                "incomes differ."),
    Question(
        "w2",
        "Costs are wages times labor requirements. The unit cost of each good in each country?",
        form=["Home: cloth", BOX, "wine", BOX, "&nbsp; Foreign: cloth", BOX, "wine", BOX],
        answers=[H("w2.0"), H("w2.1"), H("w2.2"), H("w2.3")],
        mistakes=M({"w2.2~6": "That is the labor requirement. Multiply by Foreign's wage, 1/3.",
                    "w2.3~3": "That is the labor requirement. Multiply by Foreign's wage, 1/3."}),
        explain="Each country is cheapest in exactly one good, and Foreign's low wage is what "
                "makes it competitive in wine."),
    Question(
        "w3",
        "In general Foreign undersells Home in a good when a*/a &lt; w/w*. The wage ratio, and "
        "the productivity gap a*/a in cloth and in wine?",
        form=["w/w* =", BOX, "&nbsp; cloth", BOX, "&nbsp; wine", BOX],
        answers=[H("w3.0"), H("w3.1"), H("w3.2")],
        mistakes=M({"w3.0~1/3": "Home's wage over Foreign's.",
                    "w3.2~2/3": "Foreign's requirement on top: 3/2."}),
        explain="The wage ratio is the cutoff, the same for every good: session 8's automation "
                "cutoff with a country in place of the machine."),
    Question(
        "w4",
        "Try it (a): world demand shifts toward cloth and the price rises to p = 3/2, still "
        "inside the range. Both wages?",
        form=["w =", BOX, "&nbsp; w* =", BOX],
        answers=[H("w4.0"), H("w4.1")],
        mistakes=M({"w4.1~1/2": "Foreign exports wine, the numeraire: the cloth boom never "
                                "touches its wage."}),
        explain="Only the wage of the country that exports cloth moves."),
    Question(
        "w5",
        "(b) The new cutoff w/w*, and the level Foreign's cloth requirement would have to fall "
        "below before Foreign takes cloth as well?",
        form=["w/w* =", BOX, "&nbsp; %s below" % AXF, BOX],
        answers=[H("w5.0"), H("w5.1")],
        mistakes=M({"w5.1~6": "That is today's requirement. Foreign takes cloth when %s/%s "
                              "falls below the cutoff." % (AXF, AX)}),
        explain="Wine's gap 3/2 is below 9/2 and cloth's gap 6 is above it: still one good each."),
    Question(
        "w6",
        "(c) Home still ships 40 cloth abroad. What does it consume now?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("w6.0"), H("w6.1")],
        mistakes=M({"w6.1~40": "Forty cloth now buy 40 &times; 3/2 wine."}),
        explain="Same goods shipped, 20 more wine received: a terms-of-trade improvement."),
    Question(
        "w7",
        "Review question 1: which concept decides the pattern of trade, and which the level of "
        "wages?",
        choices=[RULES, RULES_REV, RULES_ABS, RULES_COMP],
        answers=[H("w7.c")],
        mistakes=M({
            "w7.c~" + RULES_REV: "The other way round: exports follow the ratio of labor "
                                 "requirements.",
            "w7.c~" + RULES_ABS: "The trade prediction never mentions the levels.",
            "w7.c~" + RULES_COMP: "w = p/%s: the level of the requirement sets the wage." % AX,
        }),
        explain="What does a country export? Look at the ratio. How rich are its workers? Look "
                "at the levels."),
    Question(
        "w8",
        "Rebut the claim \"we cannot compete with low-wage countries\".",
        choices=[LOW_WAGE, LW_TRUE, LW_ABS, LW_NONE],
        answers=[H("w8.c")],
        mistakes=M({
            "w8.c~" + LW_TRUE: "Then that country would export everything and import nothing. "
                               "Trade must balance.",
            "w8.c~" + LW_ABS: "Foreign exports wine with a disadvantage in both goods.",
            "w8.c~" + LW_NONE: "Costs are w&middot;a.",
        }),
        explain="Low wages and low productivity are the same fact stated twice."),
]

wages = GuidedProblem(
    "Part 4 &middot; Wages, unit costs and the low-wage fallacy",
    "Home needs less labor per unit in both goods. So why does it not undersell Foreign "
    "everywhere?",
    WAGE_QUESTIONS, draw_wages, figsize=(8.0, 3.8), whole_figure=True,
    outro="Trade patterns follow comparative advantage, wage levels follow absolute advantage.",
    sources=[NOTES("p. 10&ndash;12"), NOTES("p. 19, review question 1")],
)


# ======================================================================
# Part 5: the worksheet, with the roles flipped
# ======================================================================

def draw_worksheet(fig, stage):
    home, foreign = fig.subplots(1, 2)
    _panel(home, 6.6, 5.6, "cloth", "wine", "Home: 4, 5 and 20 workers",
           xticks=range(1, 7), yticks=range(1, 6))
    _panel(foreign, 11, 5.6, "cloth", "wine", "Foreign: 1, 2 and 10 workers",
           xticks=range(2, 11, 2), yticks=range(1, 6))
    for ax in (home, foreign):
        ax.grid(True, color="#e5e7eb", lw=0.6)
        ax.set_axisbelow(True)
    gp.dot(home, 0, 4, "20/5", 8, 2, colour=MUTE)
    if stage >= 1:
        _ppf(home, 5, 4)
        home.text(1.2, 1.7, "slope 4/5", color=LINE, fontsize=9)
    if stage >= 2:
        _ppf(foreign, 10, 5, color=CURVE)
        foreign.text(2.4, 2.4, "slope 1/2", color=CURVE, fontsize=9)
    if stage >= 3:
        foreign.text(0.98, 0.9, "flatter: comparative\nadvantage in cloth",
                     transform=foreign.transAxes, ha="right", va="top", color=CURVE, fontsize=9)
    if stage >= 4:
        _trade_line(home, 0, 4, 2 / 3)
        _trade_line(foreign, 10, 0, 2 / 3)
    fig.subplots_adjust(wspace=0.25)


SHEET_FOREIGN = "Foreign: its frontier is the flatter one, 1/2 against 4/5. It also holds the absolute advantage in both goods"
SHEET_HOME = "Home: it has twice as many workers"
SHEET_HOME_SLOPE = "Home: 4/5 is larger than 1/2"
SHEET_BOTH = "Foreign has the comparative advantage in both goods"

FAIR = "Home's wage is low because it needs more labor in both goods; the low wage is what lets it sell the good where its disadvantage is smallest"
FAIR_DUMP = "It is unfair: Home sells wine below its cost"
FAIR_SIZE = "Home is the larger country, so it can afford lower wages"
FAIR_SAME = "Wages are the same in both countries under free trade"

WORKSHEET_QUESTIONS = [
    Question(
        "s1",
        "Home needs 4 workers per unit of cloth and 5 per unit of wine, and has 20 workers. One "
        "intercept is done: 20/5 = 4 wine. The cloth intercept, and the absolute slope?",
        form=["cloth", BOX, "&nbsp; slope", BOX],
        answers=[H("s1.0"), H("s1.1")],
        mistakes=M({"s1.1~5/4": "Upside down: %s/%s." % (AX, AY)}),
        explain="The slope is Home's autarky price of cloth."),
    Question(
        "s2",
        "Foreign: 1 worker per cloth, 2 per wine, 10 workers, and no helpers this time. Both "
        "intercepts and the slope?",
        form=["cloth", BOX, "&nbsp; wine", BOX, "&nbsp; slope", BOX],
        answers=[H("s2.0"), H("s2.1"), H("s2.2")],
        mistakes=M({"s2.1~20": "Divide: 10 workers, 2 per unit of wine."}),
        explain="Foreign's autarky price of cloth is 1/2."),
    Question(
        "s3",
        "Circle the country with the comparative advantage in cloth.",
        choices=[SHEET_FOREIGN, SHEET_HOME, SHEET_HOME_SLOPE, SHEET_BOTH],
        answers=[H("s3.c")],
        mistakes=M({
            "s3.c~" + SHEET_HOME: "Workers move the intercepts, not the slope.",
            "s3.c~" + SHEET_HOME_SLOPE: "The slope is the cost of cloth: the lower one wins.",
            "s3.c~" + SHEET_BOTH: "Nobody has a comparative advantage in both goods.",
        }),
        explain="The roles have flipped: Foreign is better at everything, and Home is the "
                "low-wage country."),
    Question(
        "s4",
        "Task 2: take the world price p = 2/3, between the two autarky prices. Home now exports "
        "wine, the numeraire, and Foreign exports cloth. Both wages?",
        form=["w =", BOX, "&nbsp; w* =", BOX],
        answers=[H("s4.0"), H("s4.1")],
        mistakes=M({"s4.0~1/6": "Home makes wine this time: w = 1/%s." % AY,
                    "s4.1~1/2": "Foreign makes cloth: w* = p/%s." % AXF}),
        explain="Foreign's wage is more than three times Home's."),
    Question(
        "s5",
        "Check with unit costs, wage times labor requirement.",
        form=["Home: cloth", BOX, "wine", BOX, "&nbsp; Foreign: cloth", BOX, "wine", BOX],
        answers=[H("s5.0"), H("s5.1"), H("s5.2"), H("s5.3")],
        mistakes=M({"s5.0~4": "Multiply the requirement by Home's wage, 1/5."}),
        explain="Foreign wins cloth, 2/3 against 4/5. Home wins wine, 1 against 4/3."),
    Question(
        "s6",
        "Why is Home's low wage not unfair competition?",
        choices=[FAIR, FAIR_DUMP, FAIR_SIZE, FAIR_SAME],
        answers=[H("s6.c")],
        mistakes=M({
            "s6.c~" + FAIR_DUMP: "Home's wine costs exactly its price, 1.",
            "s6.c~" + FAIR_SIZE: "The wage is 1/%s: size does not enter." % AY,
            "s6.c~" + FAIR_SAME: "1/5 against 2/3.",
        }),
        explain="The wage reflects productivity. Without it Home could sell nothing and buy "
                "nothing."),
    Question(
        "s7",
        "Task 3: let Home be very large. At which world price does trade settle?",
        form=["p =", BOX],
        answers=[H("s7.0")],
        mistakes=M({"s7.0~1/2": "That is Foreign's autarky price. A very large Home cannot be "
                                "moved off its own step."}),
        explain="Home's own autarky price: Home keeps making both goods and gains nothing."),
]

worksheet = GuidedProblem(
    "Part 5 &middot; The worksheet: roles flipped",
    "The two frontiers to finish before the in-person session, then the four tasks. This "
    "time Foreign holds the absolute advantage in everything.",
    WORKSHEET_QUESTIONS, draw_worksheet, figsize=(8.0, 3.8), whole_figure=True,
    outro="Close task 2 with one written sentence of your own.",
    sources=[NOTES("p. 18&ndash;19, worksheet")],
)


# ======================================================================
# Part 6: review questions 2-5, Vinland and Estland
# ======================================================================

def draw_vinland(fig, stage):
    ppf, rs = fig.subplots(1, 2)
    _panel(ppf, 330, 110, "timber", "glass", "Frontiers",
           xticks=([300] if stage >= 1 else []) + ([40] if stage >= 2 else []),
           yticks=([100] if stage >= 1 else []) + ([60] if stage >= 2 else []))
    if stage == 0:
        gp.start(ppf)
    if stage >= 1:
        _ppf(ppf, 300, 100, label="Vinland")
    if stage >= 2:
        _ppf(ppf, 40, 60, color=CURVE, label="Estland")
    if stage >= 4:
        gp.dot(ppf, 300, 0, "", colour=NEW)
        gp.dot(ppf, 0, 60, "", colour=NEW)
        _trade_line(ppf, 300, 0, 1, lw=1.1)
        _trade_line(ppf, 0, 60, 1, lw=1.1)
    if stage >= 5:
        gp.dot(ppf, 260, 40, "(260, 40)", -8, 8, colour=GREEN, ha="right")
        gp.dot(ppf, 40, 20, "(40, 20)", 8, 2, colour=GREEN)
    gp.legend(ppf, loc="upper right")

    _panel(rs, 8, 2.2, "world timber / world glass", "p", "World relative supply",
           yticks=[1 / 3, 1.5] if stage >= 10 else [], xticks=[5] if stage >= 10 else [])
    rs.set_yticklabels(["1/3", "3/2"] if stage >= 10 else [])
    if stage >= 10:
        _stairs(rs, 1 / 3, 1.5, 5, 8, 2.2)
        q = np.linspace(1.6, 8, 200)
        rs.plot(q, 5 / q, color=CURVE, lw=1.6, label="demand cuts the vertical")
    if stage >= 11:
        q = np.linspace(0.3, 8, 200)
        rs.plot(q, 2 / 3 / q, color=NEW, lw=1.6, ls="--", label="demand cuts the lower step")
    gp.legend(rs, loc="upper right")
    fig.subplots_adjust(wspace=0.3)


VIN = "Vinland has the absolute advantage in both goods; the comparative advantage is Vinland's in timber and Estland's in glass"
VIN_REV = "Vinland has the absolute advantage in both; the comparative advantage is Estland's in timber and Vinland's in glass"
VIN_BOTH = "Vinland has the absolute and the comparative advantage in both goods"
VIN_SPLIT = "Vinland has the absolute advantage in timber and Estland in glass"

LOWER = "The world price equals Vinland's autarky price, 1/3: Vinland still makes both goods and gains nothing, and Estland takes the gain"
LOWER_EST = "The world price equals Estland's autarky price, and Estland gains nothing"
LOWER_BOTH = "Both countries make both goods, and nobody gains"
LOWER_SAME = "Nothing changes: both still specialize completely"

VINLAND_QUESTIONS = [
    Question(
        "v1",
        "Review question 2: Vinland makes timber (x) and glass (y) with %s = 1 and %s = 3, and "
        "has E = 300 workers. Both intercepts and the absolute slope of its frontier?" % (AX, AY),
        form=["timber", BOX, "&nbsp; glass", BOX, "&nbsp; slope", BOX],
        answers=[H("v1.0"), H("v1.1"), H("v1.2")],
        mistakes=M({"v1.2~3": "Upside down: %s/%s." % (AX, AY)}),
        explain="Vinland's autarky price of timber is 1/3."),
    Question(
        "v2",
        "Estland: %s = 6, %s = 4 and E* = 240." % (AXF, AYF),
        form=["timber", BOX, "&nbsp; glass", BOX, "&nbsp; slope", BOX],
        answers=[H("v2.0"), H("v2.1"), H("v2.2")],
        mistakes=M({"v2.2~2/3": "Upside down: 6/4."}),
        explain="Estland's autarky price of timber is 3/2."),
    Question(
        "v3",
        "Absolute and comparative advantage?",
        choices=[VIN, VIN_REV, VIN_BOTH, VIN_SPLIT],
        answers=[H("v3.c")],
        mistakes=M({
            "v3.c~" + VIN_REV: "Timber costs 1/3 glass in Vinland and 3/2 in Estland.",
            "v3.c~" + VIN_BOTH: "Nobody has a comparative advantage in both goods.",
            "v3.c~" + VIN_SPLIT: "Compare levels: 1 &lt; 6 and 3 &lt; 4.",
        }),
        explain="Vinland's autarky price is the lower one: it exports timber."),
    Question(
        "v4",
        "Review question 3: the world price settles at p = 1, between 1/3 and 3/2, so both "
        "want to trade. What does each country produce?",
        form=["Vinland: timber", BOX, "&nbsp; Estland: glass", BOX],
        answers=[H("v4.0"), H("v4.1")],
        mistakes=M({"v4.1~40": "Estland makes glass: 240/4."}),
        explain="Complete specialization, each at a corner of its frontier."),
    Question(
        "v5",
        "Vinland consumes (260, 40). How much timber does it export, and how much glass does "
        "Estland keep after paying for it at p = 1?",
        form=["exports", BOX, "&nbsp; Estland keeps", BOX],
        answers=[H("v5.0"), H("v5.1")],
        mistakes=M({"v5.1~60": "Estland pays 40 glass for the 40 timber."}),
        explain="Estland ends at (40, 20). Forty timber against forty glass: the trade balances."),
    Question(
        "v6",
        "How many workers would each country need to make its bundle at home: (260, 40) in "
        "Vinland and (40, 20) in Estland?",
        form=["Vinland", BOX, "&nbsp; Estland", BOX],
        answers=[H("v6.0"), H("v6.1")],
        mistakes=M({"v6.0~300": "%s&middot;260 + %s&middot;40, with %s = 3." % (AX, AY, AY)}),
        explain="More than the 300 and 240 they have: both bundles lie strictly outside the "
                "frontiers."),
    Question(
        "v7",
        "Review question 4: glass is the numeraire, so p<sub>x</sub> = p<sub>y</sub> = 1. The "
        "wage in each country?",
        form=["Vinland", BOX, "&nbsp; Estland", BOX],
        answers=[H("v7.0"), H("v7.1")],
        mistakes=M({"v7.1~1/6": "Estland makes glass: 1/%s." % AYF}),
        explain="Each worker earns the value of what she makes in the export industry."),
    Question(
        "v8",
        "The unit cost w&middot;a of each good in each country?",
        form=["Vinland: timber", BOX, "glass", BOX, "&nbsp; Estland: timber", BOX, "glass", BOX],
        answers=[H("v8.0"), H("v8.1"), H("v8.2"), H("v8.3")],
        mistakes=M({"v8.2~6": "Multiply by Estland's wage, 1/4."}),
        explain="Vinland is cheaper in timber, Estland in glass."),
    Question(
        "v9",
        "Estland undersells Vinland in good i when a<sub>i</sub>*/a<sub>i</sub> &lt; w/w*. The "
        "wage ratio, and the two productivity gaps?",
        form=["w/w* =", BOX, "&nbsp; timber", BOX, "&nbsp; glass", BOX],
        answers=[H("v9.0"), H("v9.1"), H("v9.2")],
        mistakes=M({"v9.0~1/4": "Vinland's wage over Estland's.",
                    "v9.2~3/4": "Estland's requirement on top: 4/3."}),
        explain="4/3 &lt; 4 &lt; 6: the wage ratio falls strictly between the gaps, so each "
                "country is competitive in exactly one good."),
    Question(
        "v10",
        "Review question 5: the world relative supply of timber. The price of each flat "
        "segment, and the quantity at the vertical one?",
        form=["lower", BOX, "&nbsp; upper", BOX, "&nbsp; quantity", BOX],
        answers=[H("v10.0"), H("v10.1"), H("v10.2")],
        mistakes=M({"v10.2~1/5": "Timber over glass: 300/60."}),
        explain="Flat at each autarky price, vertical where both are fully specialized."),
    Question(
        "v11",
        "What changes if relative demand cuts the lower flat segment instead?",
        choices=[LOWER, LOWER_EST, LOWER_BOTH, LOWER_SAME],
        answers=[H("v11.c")],
        mistakes=M({
            "v11.c~" + LOWER_EST: "The lower step sits at Vinland's price, 1/3.",
            "v11.c~" + LOWER_BOTH: "Estland now buys timber at 1/3 instead of 3/2.",
            "v11.c~" + LOWER_SAME: "On a flat step one country makes both goods.",
        }),
        explain="A country whose price does not move gains nothing from trade."),
]

vinland = GuidedProblem(
    "Part 6 &middot; Vinland and Estland",
    "Review questions 2&ndash;5: one economy from frontiers to wages to the staircase.",
    VINLAND_QUESTIONS, draw_vinland, figsize=(8.0, 3.8), whole_figure=True,
    outro="Draw the staircase yourself, with both flat segments and the vertical one labelled.",
    sources=[NOTES("p. 19, review questions 2&ndash;5")],
)


# ======================================================================
# Part 7: problem A9.1, Norway and Portugal
# ======================================================================

def draw_norway(fig, stage):
    no, pt = fig.subplots(1, 2)
    _panel(no, 660, 660, "salmon", "textiles", "Norway",
           xticks=[600] if stage >= 1 else [],
           yticks=([300] if stage >= 1 else []) + ([600] if stage >= 6 else []))
    _panel(pt, 230, 230, "salmon", "textiles", "Portugal",
           xticks=([100] if stage >= 2 else []) + ([200] if stage >= 6 else []),
           yticks=[200] if stage >= 2 else [])
    if stage == 0:
        gp.start(no)
    if stage >= 1:
        _ppf(no, 600, 300)
        no.text(110, 120, "slope −1/2", color=LINE, fontsize=9)
    if stage >= 2:
        _ppf(pt, 100, 200, color=CURVE)
        pt.text(8, 60, "slope −2", color=CURVE, fontsize=9)
    if stage >= 5:
        gp.dot(no, 600, 0, "", colour=NEW)
        gp.dot(pt, 0, 200, "", colour=NEW)
    if stage >= 6:
        _trade_line(no, 600, 0, 1)
        _trade_line(pt, 0, 200, 1)
        gp.dot(no, 500, 100, "(500, 100)", 8, 4, colour=GREEN)
        gp.dot(pt, 100, 100, "(100, 100)", 8, 4, colour=GREEN)
    fig.subplots_adjust(wspace=0.3)


NOR = "Norway has the absolute advantage in both goods; the comparative advantage is Norway's in salmon and Portugal's in textiles"
NOR_REV = "Norway has the absolute advantage in both; the comparative advantage is Portugal's in salmon and Norway's in textiles"
NOR_BOTH = "Norway has the absolute and the comparative advantage in both goods"
NOR_SPLIT = "Norway has the absolute advantage in salmon and Portugal in textiles"

UNDERCUT = "Costs are wages times labor requirements. Norway's wage is three times Portugal's but it is only 1.5 times as productive in textiles, so its textiles cost 2 against Portugal's 1"
UC_CHOICE = "Norway could undercut Portugal in textiles, but chooses not to"
UC_SAME = "Wages are the same in both countries, so labor requirements decide"
UC_LABOR = "Portugal needs less labor per unit of textiles"

NORWAY_QUESTIONS = [
    Question(
        "n1",
        "A9.1 (a): Norway needs %s = 2 hours per unit of salmon and %s = 4 per unit of textiles, "
        "with E = 1200 hours. Both intercepts and the slope of its frontier, with its sign?"
        % (AX, AY),
        form=["salmon", BOX, "&nbsp; textiles", BOX, "&nbsp; slope", BOX],
        answers=[H("n1.0"), H("n1.1"), H("n1.2")],
        mistakes=M({"n1.2~1/2": "The frontier slopes down.",
                    "n1.2~-2": "Upside down: &minus;%s/%s." % (AX, AY)}),
        hints=["Full employment: 2q<sub>x</sub> + 4q<sub>y</sub> = 1200. Solve for q<sub>y</sub>."],
        explain="q<sub>y</sub> = 300 &minus; q<sub>x</sub>/2. On the exam, show that derivation."),
    Question(
        "n2",
        "Portugal: %s = 12, %s = 6 and E* = 1200." % (AXF, AYF),
        form=["salmon", BOX, "&nbsp; textiles", BOX, "&nbsp; slope", BOX],
        answers=[H("n2.0"), H("n2.1"), H("n2.2")],
        mistakes=M({"n2.2~2": "The frontier slopes down.",
                    "n2.2~-1/2": "Upside down: &minus;12/6."}),
        explain="q<sub>y</sub> = 200 &minus; 2q<sub>x</sub>."),
    Question(
        "n3",
        "(b) The autarky relative price of salmon, p<sup>a</sup>, in each country?",
        form=["Norway", BOX, "&nbsp; Portugal", BOX],
        answers=[H("n3.0"), H("n3.1")],
        mistakes=M({"n3.0~2": "Upside down: p<sup>a</sup> = %s/%s." % (AX, AY)}),
        hints=["Both goods are made, so wages are equal across industries: "
               "p<sub>x</sub>/%s = p<sub>y</sub>/%s." % (AX, AY)],
        explain="The autarky price is the absolute slope of the frontier."),
    Question(
        "n4",
        "(c) Absolute and comparative advantage?",
        choices=[NOR, NOR_REV, NOR_BOTH, NOR_SPLIT],
        answers=[H("n4.c")],
        mistakes=M({
            "n4.c~" + NOR_REV: "Salmon costs 1/2 textiles in Norway and 2 in Portugal.",
            "n4.c~" + NOR_BOTH: "Nobody has a comparative advantage in both goods.",
            "n4.c~" + NOR_SPLIT: "Compare levels: 2 &lt; 12 and 4 &lt; 6.",
        }),
        explain="The two answers differ because one compares productivity levels and the other "
                "compares opportunity costs."),
    Question(
        "n5",
        "(d) The range of world prices at which both want to trade, and each country's output "
        "strictly inside it?",
        form=["", BOX, "&lt; p &lt;", BOX, "&nbsp; Norway: salmon", BOX,
              "&nbsp; Portugal: textiles", BOX],
        answers=[H("n5.0"), H("n5.1"), H("n5.2"), H("n5.3")],
        mistakes=M({"n5.3~100": "Portugal makes textiles: 1200/6."}),
        explain="Norway sells salmon for more than its own opportunity cost, and Portugal buys "
                "it for less than its own."),
    Question(
        "n6",
        "(e) The world price settles at p = 1 and Norway ships 100 salmon to Portugal. Each "
        "country's bundle?",
        form=["Norway (", BOX, ",", BOX, ")", "&nbsp; Portugal (", BOX, ",", BOX, ")"],
        answers=[H("n6.0"), H("n6.1"), H("n6.2"), H("n6.3")],
        mistakes=M({"n6.3~200": "Portugal pays 100 textiles for the salmon."}),
        explain="One such bundle each, on the price line through the production corner."),
    Question(
        "n7",
        "How many hours would each need to make that bundle at home?",
        form=["Norway", BOX, "&nbsp; Portugal", BOX],
        answers=[H("n7.0"), H("n7.1")],
        mistakes=M({"n7.0~1200": "2&middot;500 + 4&middot;100."}),
        explain="Both exceed 1200: the bundles lie outside the frontiers."),
    Question(
        "n8",
        "(f) Normalize p<sub>y</sub> = 1, so p<sub>x</sub> = 1. The wage in each country?",
        form=["Norway", BOX, "&nbsp; Portugal", BOX],
        answers=[H("n8.0"), H("n8.1")],
        mistakes=M({"n8.0~1/4": "Norway makes salmon: p<sub>x</sub>/%s." % AX,
                    "n8.1~1/12": "Portugal makes textiles: p<sub>y</sub>/%s." % AYF}),
        hints=["A worker earns the value of what she makes in the industry her country "
               "specializes in."],
        explain="Norway's wage is three times Portugal's."),
    Question(
        "n9",
        "The unit cost of each good in each country?",
        form=["Norway: salmon", BOX, "textiles", BOX, "&nbsp; Portugal: salmon", BOX,
              "textiles", BOX],
        answers=[H("n9.0"), H("n9.1"), H("n9.2"), H("n9.3")],
        mistakes=M({"n9.1~4": "Multiply by Norway's wage, 1/2.",
                    "n9.3~6": "Multiply by Portugal's wage, 1/6."}),
        explain="Each country is cheapest in exactly one good."),
    Question(
        "n10",
        "Norway is more productive in both goods. Why does it not undercut Portugal in "
        "textiles as well?",
        choices=[UNDERCUT, UC_CHOICE, UC_SAME, UC_LABOR],
        answers=[H("n10.c")],
        mistakes=M({
            "n10.c~" + UC_CHOICE: "At these prices it cannot: 2 against 1.",
            "n10.c~" + UC_SAME: "1/2 against 1/6.",
            "n10.c~" + UC_LABOR: "6 against Norway's 4.",
        }),
        explain="The wage ratio, 3, lies between the productivity gaps 3/2 and 6."),
]

norway = GuidedProblem(
    "Part 7 &middot; Norway and Portugal: A9.1",
    "Salmon is good x, textiles good y, and p = p<sub>x</sub>/p<sub>y</sub>. Each country has "
    "1200 labor hours.",
    NORWAY_QUESTIONS, draw_norway, figsize=(8.0, 4.2), whole_figure=True,
    outro="30% of an exam paper. The figures and the sentences are yours to write.",
    sources=[PS("A9.1")],
)


# ======================================================================
# Part 8: the small-country tariff (context)
# ======================================================================

def draw_tariff(ax, stage):
    gp.frame(ax, 85, 78, "quantity of wheat", "price")
    ax.plot([0, 58], [20, 78], color=LINE, lw=2, label="supply")
    ax.plot([22, 85], [78, 15], color=CURVE, lw=2, label="demand")
    ax.axhline(40, color=GREY, lw=1.2, ls="--")
    ax.text(84, 41, "world price 40", color=MUTE, fontsize=8.5, ha="right")
    ticks_x, ticks_y = [], [40]
    if stage >= 1:
        ticks_x += [20, 60]
    if stage >= 2:
        ax.axhline(50, color=NEW, lw=1.2, ls="--")
        ax.text(84, 51, "with the tariff", color=NEW, fontsize=8.5, ha="right")
        ticks_x += [30, 50]
        ticks_y += [50]
        for x in (30, 50):
            ax.plot([x, x], [0, 50], color=GREY, lw=0.8, ls=":")
    if stage >= 1:
        for x in (20, 60):
            ax.plot([x, x], [0, 40], color=GREY, lw=0.8, ls=":")
    if stage >= 3:
        ax.fill([0, 20, 30, 0], [40, 40, 50, 50], color=LINE, alpha=0.18, lw=0)
        ax.fill([20, 30, 30], [40, 40, 50], color=NEW, alpha=0.45, lw=0)
        ax.fill([30, 50, 50, 30], [40, 40, 50, 50], color=GREEN, alpha=0.22, lw=0)
        ax.fill([50, 60, 50], [40, 40, 50], color=NEW, alpha=0.45, lw=0)
        for x, name in ((11, "a"), (27, "b"), (40, "c"), (53, "d")):
            ax.text(x, 44.5, name, color=INK, fontsize=10, ha="center", va="center")
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.tick_params(colors=MUTE, labelsize=8.5)
    gp.legend(ax, loc="upper center")


WRONG_TOOL = "A tariff is a consumption tax plus a production subsidy: a production subsidy alone raises output at the cost of triangle b, without the consumption distortion d"
TOOL_REV = "A tariff is the cheapest way to raise output, because it also brings in revenue"
TOOL_FOREIGN = "A small country's tariff is paid by foreigners"
TOOL_SAME = "A tariff and a production subsidy cost the country the same"

TARIFF_QUESTIONS = [
    Question(
        "t1",
        "Try it: a small country imports wheat at a world price of 40, with demand "
        "D(p) = 100 &minus; p and supply S(p) = p &minus; 20. Under free trade: supply, demand "
        "and imports?",
        form=["S<sub>0</sub> =", BOX, "&nbsp; D<sub>0</sub> =", BOX, "&nbsp; imports", BOX],
        answers=[H("t1.0"), H("t1.1"), H("t1.2")],
        hints=["Put the world price into both: S(40) and D(40)."],
        explain="Imports are demand minus supply."),
    Question(
        "t2",
        "(a) After a specific tariff, imports fall to 20. Recover the domestic price and the "
        "tariff.",
        form=["price", BOX, "&nbsp; t =", BOX],
        answers=[H("t2.0"), H("t2.1")],
        mistakes=M({"t2.0~40": "That is the world price. Which price gives imports of 20?"}),
        hints=["Imports are D &minus; S = 120 &minus; 2p."],
        explain="The inversion an analyst runs: you observe quantities, rarely the tariff."),
    Question(
        "t3",
        "(b) At 50, firms supply 30 and consumers buy 50. The four areas between the price "
        "lines?",
        form=["a", BOX, "&nbsp; b", BOX, "&nbsp; c", BOX, "&nbsp; d", BOX],
        answers=[H("t3.0"), H("t3.1"), H("t3.2"), H("t3.3")],
        mistakes=M({"t3.0~200": "a is a trapezoid: 10 &times; (20 + 30)/2.",
                    "t3.0~300": "a is a trapezoid: 10 &times; (20 + 30)/2.",
                    "t3.2~400": "Revenue is the tariff times the imports that remain, 20."}),
        explain="a is the producers' gain and c the revenue. Consumers lose a + b + c + d."),
    Question(
        "t4",
        "a and c are transfers. The national loss?",
        form=["loss", BOX],
        answers=[H("t4.0")],
        mistakes=M({"t4.0~550": "That is what consumers lose. Producers and the government get "
                                "a and c back."}),
        explain="b is the production distortion and d the consumption distortion: nobody gets "
                "them."),
    Question(
        "t5",
        "(c) Halve the tariff. The deadweight loss, and the revenue?",
        form=["loss", BOX, "&nbsp; revenue", BOX],
        answers=[H("t5.0"), H("t5.1")],
        mistakes=M({"t5.0~50": "Both the height and the base of each triangle halve.",
                    "t5.1~100": "Imports rise to 30 at a price of 45."}),
        explain="A quarter of the loss and three quarters of the revenue: the loss goes with "
                "the square of the tariff."),
    Question(
        "t6",
        "Review question 6: why is a tariff the wrong instrument if the goal is more domestic "
        "production?",
        choices=[WRONG_TOOL, TOOL_REV, TOOL_FOREIGN, TOOL_SAME],
        answers=[H("t6.c")],
        mistakes=M({
            "t6.c~" + TOOL_REV: "Revenue is a transfer from consumers; triangle d is pure "
                                "waste.",
            "t6.c~" + TOOL_FOREIGN: "A small country takes the world price as given.",
            "t6.c~" + TOOL_SAME: "The tariff also costs triangle d.",
        }),
        explain="Session 7's targeting principle: intervene at the margin where the problem is."),
]

tariff = GuidedProblem(
    "Part 8 &middot; The small-country tariff",
    CTX + "Background for the policy debate. One tax diagram, redrawn for an open economy: "
    "the tariff lifts the domestic price to the world price plus t.",
    TARIFF_QUESTIONS, draw_tariff, figsize=(6.4, 4.6),
    outro="The last increment of a tariff raises the least revenue and does the most damage.",
    sources=[NOTES("p. 14&ndash;18"), NOTES("p. 20, review question 6")],
)


# ======================================================================
# Where every step comes from (printed pages of s09_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "r1": NOTES("p. 3 &middot; frontiers"), "r2": NOTES("p. 3 &middot; frontiers"),
    "r3": NOTES("p. 4 &middot; opportunity cost"), "r4": NOTES("p. 3 &middot; running example"),
    "r5": NOTES("p. 4 &middot; uniform gain"),
    "a1": NOTES("p. 5 &middot; autarky price"), "a2": NOTES("p. 5 &middot; point A"),
    "a3": NOTES("p. 6 &middot; relative supply"), "a4": NOTES("p. 6 &middot; relative supply"),
    "a5": NOTES("p. 6 &middot; the staircase"), "a6": NOTES("p. 8 &middot; bargaining range"),
    "g1": NOTES("p. 8 &middot; step 3"), "g2": NOTES("p. 9 &middot; step 4"),
    "g3": NOTES("p. 9 &middot; steps 5&ndash;6"), "g4": NOTES("p. 9 &middot; Foreign"),
    "g5": NOTES("p. 9 &middot; clearing price"), "g6": NOTES("p. 9 &middot; two gains"),
    "g7": NOTES("p. 18 &middot; worksheet task 3"),
    "w1": NOTES("p. 10 &middot; wages"), "w2": NOTES("p. 10 &middot; unit costs"),
    "w3": NOTES("p. 11 &middot; the cutoff"), "w4": NOTES("p. 11 &middot; Try it (a)"),
    "w5": NOTES("p. 11 &middot; Try it (b)"), "w6": NOTES("p. 11 &middot; Try it (c)"),
    "w7": NOTES("p. 19 &middot; review question 1"), "w8": NOTES("p. 19 &middot; review question 1"),
    "s1": NOTES("p. 18 &middot; worksheet task 1"), "s2": NOTES("p. 18 &middot; worksheet task 1"),
    "s3": NOTES("p. 18 &middot; worksheet task 1"), "s4": NOTES("p. 18 &middot; worksheet task 2"),
    "s5": NOTES("p. 18 &middot; worksheet task 2"), "s6": NOTES("p. 18 &middot; worksheet task 2"),
    "s7": NOTES("p. 18 &middot; worksheet task 3"),
    "v1": NOTES("p. 19 &middot; review question 2"), "v2": NOTES("p. 19 &middot; review question 2"),
    "v3": NOTES("p. 19 &middot; review question 2"), "v4": NOTES("p. 19 &middot; review question 3"),
    "v5": NOTES("p. 19 &middot; review question 3"), "v6": NOTES("p. 19 &middot; review question 3"),
    "v7": NOTES("p. 19 &middot; review question 4"), "v8": NOTES("p. 19 &middot; review question 4"),
    "v9": NOTES("p. 19 &middot; review question 4"), "v10": NOTES("p. 19 &middot; review question 5"),
    "v11": NOTES("p. 19 &middot; review question 5"),
    "n1": PS("A9.1 (a)"), "n2": PS("A9.1 (a)"), "n3": PS("A9.1 (b)"), "n4": PS("A9.1 (c)"),
    "n5": PS("A9.1 (d)"), "n6": PS("A9.1 (e)"), "n7": PS("A9.1 (e)"), "n8": PS("A9.1 (f)"),
    "n9": PS("A9.1 (f)"), "n10": PS("A9.1 (f)"),
    "t1": NOTES("p. 17 &middot; Try it"), "t2": NOTES("p. 17 &middot; Try it (a)"),
    "t3": NOTES("p. 17 &middot; Try it (b)"), "t4": NOTES("p. 17 &middot; Try it (b)"),
    "t5": NOTES("p. 17 &middot; Try it (c)"), "t6": NOTES("p. 20 &middot; review question 6"),
}

for _q in (FRONTIER_QUESTIONS + AUTARKY_QUESTIONS + GAINS_QUESTIONS + WAGE_QUESTIONS
           + WORKSHEET_QUESTIONS + VINLAND_QUESTIONS + NORWAY_QUESTIONS + TARIFF_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
