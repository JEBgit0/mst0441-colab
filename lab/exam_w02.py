"""
exam_w02.py - workshop 2, the second mock exam: sessions 8 to 11.

    Problem 1  saltdal   which tasks go to AI, and the saving index G (15)
    Problem 2  ricardo   bicycles and grain: comparative advantage (12)
    Problem 3  factors   chemicals and textiles: Stolper-Samuelson (8)
    Problem 4  boards    board games under monopolistic competition (5)
    Problem 5  concepts  ten multiple-choice questions (10)

The paper is worth 50 points, half a full exam. It gives the points of each
problem but, except in Problem 4, not of each part: the split across parts is
this page's own. The page checks final answers and conclusions only: the
derivations, figures and sentences are marked by hand on the real exam.

Answers are hashes in answers_w02.py, generated from
answer_keys/w02_keys.py in the private repo. The maths is firms.py,
ricardo.py and heckscher.py.
"""

import numpy as np

import firms as fm
import guided_plots as gp
from exam import ExamPaper, ExamProblem, Part
from guided import BOX, answers
from heckscher import HO
from style import CURVE, GREEN, GREY, INK, LINE, MUTE, NEW

H, M = answers("w02")

PX, PY = "p<sub>x</sub>", "p<sub>y</sub>"
RH, WH = "r&#770;", "w&#770;"
PYH, PXH = "p&#770;<sub>y</sub>", "p&#770;<sub>x</sub>"


def _waiting(ax):
    ax.axis("off")
    ax.text(0.5, 0.5, "The figure fills in as parts are marked right.",
            transform=ax.transAxes, ha="center", va="center", color=MUTE, fontsize=11)


def _frame(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.set_xticklabels(["%g" % t for t in xticks])
    ax.set_yticklabels(["%g" % t for t in yticks])
    ax.tick_params(colors=MUTE, labelsize=8.5)


# ======================================================================
# Problem 1: Saltdal Freight
# ======================================================================

TASKS = ["customs", "invoicing", "routes", "calls"]
A = (4, 2, 5 / 4, 1 / 2)
CHI = (3 / 10, 1 / 4, 3 / 10, 3 / 20)
W = 400


def draw_saltdal(fig, done):
    if not done & {"1a1", "1b2", "1c3"}:
        _waiting(fig.add_subplot())
        return
    bars, g = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1, 1.1]))
    for side in ("top", "right"):
        bars.spines[side].set_visible(False)
    bars.set_title("AI cost per task-unit, r/A", loc="left", color=INK, fontsize=9.5)
    xs = np.arange(4)
    bars.set_xticks(xs)
    bars.set_xticklabels(TASKS, fontsize=8.5, color=INK)
    bars.set_ylim(0, 1700)
    bars.set_yticks([400])
    bars.tick_params(colors=MUTE, labelsize=8.5)
    bars.axhline(W, color=INK, lw=1.6, ls="--")
    bars.text(3.45, W + 30, "wage 400", color=INK, fontsize=8.5, ha="right")
    if "1a1" in done:
        costs = [800 / a for a in A]
        bars.bar(xs - 0.18, costs, width=0.34, color=[LINE if c < W else GREY for c in costs],
                 label="r = 800")
    if "1c1" in done:
        costs = [600 / a for a in A]
        bars.bar(xs + 0.18, costs, width=0.34, color=NEW, alpha=0.8, label="r = 600")
    gp.legend(bars, loc="upper left")

    _frame(g, 1700, 0.7, "AI rental r", "saving index G", "G(r): kinks at r = wA",
           xticks=[500, 800, 1600], yticks=[0.15, 0.25] if "1c3" in done else
           [0.15] if "1b2" in done else [])
    g.set_yticklabels(["3/20", "1/4"][:len(g.get_yticks())])
    if "1b2" in done:
        rs = np.linspace(200, 1700, 400)
        g.plot(rs, [fm.index(A, CHI, W, r) for r in rs], color=LINE, lw=2)
        gp.dot(g, 800, 3 / 20, "r = 800", 6, 4, colour=LINE)
    if "1c3" in done:
        gp.dot(g, 600, 1 / 4, "r = 600", 6, 4, colour=NEW)
    fig.subplots_adjust(wspace=0.28)


AUTO_CUSTOMS = "Customs declarations only: invoicing ties at A = 2 and stays with labor"
AUTO_TWO = "Customs and invoicing"
AUTO_THREE = "Every task except customer calls"
AUTO_NONE = "None: AI rents for twice the wage"

NEW_TWO = "Customs and invoicing: the cutoff falls to 3/2"
NEW_ONE = "Customs only, as before"
NEW_THREE = "Customs, invoicing and route planning"
NEW_ALL = "All four tasks"

WORKERS = "The calculation holds wages and the order fixed. It shows which tasks lose labor and how much a fixed order saves, but not whether lower costs raise sales, how demand for the remaining tasks moves, or what happens to wages: that needs product demand and the labor market"
WORK_LOSE = "It proves the workers will lose, since G rose"
WORK_GAIN = "It proves the workers will gain, since costs fell"
WORK_FIRE = "It tells us exactly how many workers will be fired"

SALTDAL_PARTS = [
    Part("1a1", "1(a)", 2,
         "The cost of one task-unit by a worker, and the cutoff &#256; = r/w above which a task "
         "goes to AI?",
         form=["worker", BOX, "&nbsp; cutoff", BOX],
         answers=[H("1a1.0"), H("1a1.1")],
         mistakes=M({"1a1.1~1/2": "Upside down: AI wins when r/A &lt; w, so A &gt; r/w."}),
         hints=["AI costs r/A<sub>i</sub> per task-unit. Compare with the wage."],
         explain="AI wins task i when 800/A<sub>i</sub> &lt; 400."),
    Part("1a2", "1(a)", 1,
         "Which tasks are automated at r = 800?",
         choices=[AUTO_CUSTOMS, AUTO_TWO, AUTO_THREE, AUTO_NONE],
         answers=[H("1a2.c")],
         mistakes=M({
             "1a2.c~" + AUTO_TWO: "Invoicing: 800/2 = 400 = w, a tie, and ties stay with labor.",
             "1a2.c~" + AUTO_THREE: "Route planning: 800/(5/4) = 640 &gt; 400.",
             "1a2.c~" + AUTO_NONE: "Compare per task-unit, r/A, not r.",
         }),
         explain="Only A = 4 is strictly above the cutoff."),
    Part("1b1", "1(b)", 3,
         "The saving &pi;<sub>i</sub> = 1 &minus; c<sub>i</sub>/w on each task, with "
         "c<sub>i</sub> the chosen method's cost?",
         form=["customs", BOX, "invoicing", BOX, "routes", BOX, "calls", BOX],
         answers=[H("1b1.0"), H("1b1.1"), H("1b1.2"), H("1b1.3")],
         mistakes=M({"1b1.2~-3/5": "Use the chosen cost: route planning stays with labor.",
                     "1b1.3~-3": "Use the chosen cost: customer calls stay with labor."}),
         explain="Customs: 1 &minus; 200/400."),
    Part("1b2", "1(b)", 2,
         "The index G = &Sigma;&chi;<sub>i</sub>&pi;<sub>i</sub>, and the kroner saved on an "
         "order that costs 200 000 with workers only?",
         form=["G =", BOX, "&nbsp; saved", BOX],
         answers=[H("1b2.0"), H("1b2.1")],
         mistakes=M({"1b2.1~170000": "That is the new cost. The saving is G &times; 200 000.",
                     "1b2.0~1/2": "Weight the saving by the cost share, 3/10."}),
         explain="G = (3/10)(1/2) = 3/20."),
    Part("1c1", "1(c)", 1,
         "The rental falls to r = 600. The new automated set?",
         choices=[NEW_TWO, NEW_ONE, NEW_THREE, NEW_ALL],
         answers=[H("1c1.c")],
         mistakes=M({
             "1c1.c~" + NEW_ONE: "The cutoff is now 600/400 = 3/2, and invoicing has A = 2.",
             "1c1.c~" + NEW_THREE: "Route planning: 600/(5/4) = 480 &gt; 400.",
             "1c1.c~" + NEW_ALL: "Customer calls: 600/(1/2) = 1200.",
         }),
         explain="Invoicing crosses at r = wA = 800."),
    Part("1c2", "1(c)", 2,
         "The new savings on customs and on invoicing?",
         form=["customs", BOX, "&nbsp; invoicing", BOX],
         answers=[H("1c2.0"), H("1c2.1")],
         mistakes=M({"1c2.0~1/2": "Recompute with r = 600: 1 &minus; 150/400."}),
         explain="Customs saves more than before, invoicing starts saving."),
    Part("1c3", "1(c)", 1,
         "The new G, and the kroner saved on the same order?",
         form=["G =", BOX, "&nbsp; saved", BOX],
         answers=[H("1c3.0"), H("1c3.1")],
         explain="G = (3/10)(5/8) + (1/4)(1/4) = 1/4."),
    Part("1c4", "1(c)", 1,
         "Split the change in G between the task that was already automated and the one that is "
         "newly automated.",
         form=["already", BOX, "&nbsp; new", BOX],
         answers=[H("1c4.0"), H("1c4.1")],
         mistakes=M({"1c4.0~3/16": "Only the extra saving: (3/10)(5/8 &minus; 1/2).",
                     "1c4.0~1/10": "That is the whole change."}),
         explain="3/80 + 5/80 = 1/10."),
    Part("1d", "1(d)", 2,
         "The manager: 'Our costs fell, so our workers will lose.' What can the calculation tell "
         "us about the workers?",
         choices=[WORKERS, WORK_LOSE, WORK_GAIN, WORK_FIRE],
         answers=[H("1d.c")],
         mistakes=M({
             "1d.c~" + WORK_LOSE: "Lower costs can expand sales and demand for the other tasks.",
             "1d.c~" + WORK_GAIN: "Displacement removes labor from automated tasks.",
             "1d.c~" + WORK_FIRE: "The wage and the order are held fixed.",
         }),
         explain="Four sentences on the exam."),
]

saltdal = ExamProblem(
    "Problem 1 &middot; Saltdal Freight",
    "Four tasks per shipment. A worker-hour makes one task-unit of any task at w = 400 kroner; "
    "an AI-service unit costs r = 800 and makes A<sub>i</sub> task-units: customs declarations "
    "4, invoicing 2, route planning 5/4, customer calls 1/2. Baseline cost shares &chi; = (3/10, "
    "1/4, 3/10, 3/20). Quality is the same, there are no setup costs, and ties stay with labor.",
    SALTDAL_PARTS, draw_saltdal, figsize=(8.0, 3.9), whole_figure=True,
)


# ======================================================================
# Problem 2: bicycles and grain
# ======================================================================

def draw_ricardo(fig, done):
    if not done & {"2a1", "2a2"}:
        _waiting(fig.add_subplot())
        return
    home, foreign = fig.subplots(1, 2)
    _frame(home, 8, 16.5, "bicycles", "grain", "Home", xticks=[6] if "2a1" in done else [],
           yticks=([12] if "2a1" in done else []) + ([15] if "2c2" in done else []))
    _frame(foreign, 8, 16.5, "bicycles", "grain", "Foreign",
           xticks=([5] if "2a2" in done else []) + ([6] if "2c2" in done else []),
           yticks=[15] if "2a2" in done else [])
    if "2a1" in done:
        home.plot([0, 6], [12, 0], color=LINE, lw=2, label="slope 2")
    if "2a2" in done:
        foreign.plot([0, 5], [15, 0], color=CURVE, lw=2, label="slope 3")
    if "2c2" in done:
        home.plot([0, 6], [15, 0], color=NEW, lw=1.6, ls="--", label="p = 5/2")
        foreign.plot([0, 6], [15, 0], color=NEW, lw=1.6, ls="--", label="p = 5/2")
        gp.dot(home, 6, 0, "", colour=NEW)
        gp.dot(foreign, 0, 15, "", colour=NEW)
        gp.dot(home, 3, 7.5, "C", 6, 4, colour=GREEN)
        gp.dot(foreign, 3, 7.5, "C*", 6, 4, colour=GREEN)
    gp.legend(home)
    gp.legend(foreign)
    fig.subplots_adjust(wspace=0.25)


ADVANTAGE = "Foreign has the absolute advantage in both goods; Home has the comparative advantage in bicycles and Foreign in grain"
ADV_HOME = "Home has the absolute and the comparative advantage in bicycles"
ADV_BOTH = "Foreign has the comparative advantage in both goods"
ADV_REV = "Home has the comparative advantage in grain and Foreign in bicycles"

PATTERN = "Home makes only bicycles and Foreign only grain"
PAT_REV = "Home makes only grain and Foreign only bicycles"
PAT_BOTH = "Both make both goods"
PAT_F = "Foreign makes both goods, since it is more productive in both"

WHY = "Comparative advantage, not hours, decides: a bicycle costs Home 2 grain and Foreign 3. Home's wage is lower, 5/8 against 1, because its productivity is lower, so its unit cost of bicycles is lower: 5/2 against 3"
WHY_ABS = "Home is more productive at making bicycles"
WHY_SUB = "Home subsidizes its bicycle industry"
WHY_SIZE = "Home has more workers"

RICARDO_PARTS = [
    Part("2a1", "2(a)", 1,
         "Home's frontier: where does it meet each axis, and its absolute slope?",
         form=["bicycles", BOX, "&nbsp; grain", BOX, "&nbsp; slope", BOX],
         answers=[H("2a1.0"), H("2a1.1"), H("2a1.2")],
         mistakes=M({"2a1.2~1/2": "The grain given up per bicycle: a<sub>x</sub>/a<sub>y</sub>."}),
         explain="24/4 and 24/2."),
    Part("2a2", "2(a)", 1,
         "And Foreign's?",
         form=["bicycles", BOX, "&nbsp; grain", BOX, "&nbsp; slope", BOX],
         answers=[H("2a2.0"), H("2a2.1"), H("2a2.2")],
         mistakes=M({"2a2.2~1/3": "a*<sub>x</sub>/a*<sub>y</sub> = 3/1."}),
         explain="15/3 and 15/1."),
    Part("2b1", "2(b)", 2,
         "The autarky relative price of bicycles in each country?",
         form=["Home", BOX, "&nbsp; Foreign", BOX],
         answers=[H("2b1.0"), H("2b1.1")],
         mistakes=M({"2b1.0~1/2": "Upside down: p = a<sub>x</sub>/a<sub>y</sub>."}),
         explain="The slope of each frontier."),
    Part("2b2", "2(b)", 2,
         "Who has the absolute and who the comparative advantage in each good?",
         choices=[ADVANTAGE, ADV_HOME, ADV_BOTH, ADV_REV],
         answers=[H("2b2.c")],
         mistakes=M({
             "2b2.c~" + ADV_HOME: "Foreign needs 3 hours per bicycle against Home's 4.",
             "2b2.c~" + ADV_BOTH: "Nobody has a comparative advantage in both goods.",
             "2b2.c~" + ADV_REV: "A bicycle costs 2 grain at Home and 3 in Foreign.",
         }),
         explain="Absolute compares hours, comparative compares autarky prices."),
    Part("2c1", "2(c)", 1,
         "Under free trade, which good does each country produce?",
         choices=[PATTERN, PAT_REV, PAT_BOTH, PAT_F],
         answers=[H("2c1.c")],
         mistakes=M({
             "2c1.c~" + PAT_REV: "Each exports where its autarky price is lower.",
             "2c1.c~" + PAT_BOTH: "Strictly between the autarky prices both specialize.",
             "2c1.c~" + PAT_F: "Trade follows comparative, not absolute, advantage.",
         }),
         explain="Home 6 bicycles, Foreign 15 grain."),
    Part("2c2", "2(c)", 2,
         "The world price that clears the market for bicycles?",
         form=["p =", BOX],
         answers=[H("2c2.0")],
         mistakes=M({"2c2.0~2": "That is Home's autarky price. Demand: (6p + 15)/(2p) = 6.",
                     "2c2.0~3": "That is Foreign's autarky price. Demand: (6p + 15)/(2p) = 6."}),
         hints=["Each country spends half its income on bicycles. Home's income is 6p, Foreign's 15."],
         explain="2 &lt; 5/2 &lt; 3: inside the range."),
    Part("2d1", "2(d)", 1,
         "The wage in each country, in grain?",
         form=["Home w", BOX, "&nbsp; Foreign w*", BOX],
         answers=[H("2d1.0"), H("2d1.1")],
         mistakes=M({"2d1.0~1/2": "Home makes bicycles: w = p/a<sub>x</sub> = (5/2)/4."}),
         explain="Home's wage is 5/8 of Foreign's."),
    Part("2d2", "2(d)", 1,
         "The unit cost of each good in each country?",
         form=["Home: bicycles", BOX, "grain", BOX, "&nbsp; Foreign: bicycles", BOX, "grain", BOX],
         answers=[H("2d2.0"), H("2d2.1"), H("2d2.2"), H("2d2.3")],
         mistakes=M({"2d2.0~4": "Multiply the hours by Home's wage, 5/8."}),
         explain="Home is cheaper in bicycles, Foreign in grain."),
    Part("2d3", "2(d)", 1,
         "Why does Home export bicycles although Foreign needs fewer hours to make one?",
         choices=[WHY, WHY_ABS, WHY_SUB, WHY_SIZE],
         answers=[H("2d3.c")],
         mistakes=M({
             "2d3.c~" + WHY_ABS: "4 hours against 3.",
             "2d3.c~" + WHY_SUB: "No policy in the model.",
             "2d3.c~" + WHY_SIZE: "The labor force moves the intercepts, not the costs.",
         }),
         explain="Three sentences on the exam."),
]

ricardo = ExamProblem(
    "Problem 2 &middot; Bicycles and grain",
    "Labor only. Home needs a<sub>x</sub> = 4 hours per bicycle and a<sub>y</sub> = 2 per unit "
    "of grain, with L = 24; Foreign needs a*<sub>x</sub> = 3 and a*<sub>y</sub> = 1, with "
    "L* = 15. Both have u = x<sup>1/2</sup>y<sup>1/2</sup>. Grain is the numeraire and p = "
    "%s/%s." % (PX, PY),
    RICARDO_PARTS, draw_ricardo, figsize=(8.0, 3.8), whole_figure=True,
)


# ======================================================================
# Problem 3: chemicals and textiles
# ======================================================================

CHEM = HO(3, 1, 1, 3)                    # chemicals (y) and textiles (x)


def draw_factors(ax, done):
    if "3a2" not in done:
        _waiting(ax)
        return
    _frame(ax, 4.2, 4.2, "wage w", "rental r", "Zero profits",
           xticks=[2] + ([2.75] if "3b1" in done else []),
           yticks=[2] + ([1.75] if "3b1" in done else []))
    w = np.array([0, 4.2])
    ax.plot(w, (8 - w) / 3, color=LINE, lw=2, label="chemicals: 3r + w = 8")
    ax.plot(w, 8 - 3 * w, color=CURVE, lw=2, label="textiles: r + 3w = 8")
    gp.dot(ax, 2, 2, "", colour=INK)
    if "3b1" in done:
        ax.plot(w, 10 - 3 * w, color=NEW, lw=1.6, ls="--", label="textiles at 10")
        gp.dot(ax, 2.75, 1.75, "", colour=NEW)
        gp.arrow(ax, (2, 2), (2.75, 1.75), colour=NEW)
    gp.legend(ax, loc="upper right")


RANKING = "Chemicals use 3 units of capital per worker and textiles 1/3: chemicals are capital intensive, textiles labor intensive"
RANK_REV = "Textiles are capital intensive"
RANK_SAME = "Both use 4 units of input per unit, so there is no ranking"
RANK_PRICE = "Chemicals, because they are dearer"

SS = "ŵ > p̂x > p̂y > r̂: 37.5 > 25 > 0 > -12.5, the Stolper-Samuelson theorem"
SS_RYB = "The same chain, and it is the Rybczynski theorem"
SS_ORDER = "p̂x > ŵ > p̂y > r̂: Stolper-Samuelson"
SS_FPE = "The same chain, and it is factor price equalization"

REAL = "Workers gain and capital owners lose in real terms. The wage rises more than either price and the rental falls while no price falls, so the answer does not depend on what anyone buys"
REAL_BASKET = "Workers gain only if they spend most on chemicals"
REAL_BOTH = "Both gain, since textiles are worth more"
REAL_NONE = "Neither: only nominal prices changed"

FACTOR_PARTS = [
    Part("3a1", "3(a)", 1,
         "Rank the two industries by factor intensity.",
         choices=[RANKING, RANK_REV, RANK_SAME, RANK_PRICE],
         answers=[H("3a1.c")],
         mistakes=M({
             "3a1.c~" + RANK_REV: "Textiles use 1 unit of capital and 3 of labor.",
             "3a1.c~" + RANK_SAME: "Intensity is the ratio K/L.",
             "3a1.c~" + RANK_PRICE: "Prices do not enter the ranking.",
         }),
         explain="Every result is signed by this ranking."),
    Part("3a2", "3(a)", 2,
         "Zero profits: %s = 3r + w and %s = r + 3w. Find r and w at %s = %s = 8."
         % (PY, PX, PY, PX),
         form=["r =", BOX, "&nbsp; w =", BOX],
         answers=[H("3a2.0"), H("3a2.1")],
         hints=["Set the two conditions equal: 3r + w = r + 3w."],
         explain="r = w = 2."),
    Part("3b1", "3(b)", 2,
         "The price of textiles rises to %s = 10. The new r and w?" % PX,
         form=["r =", BOX, "&nbsp; w =", BOX],
         answers=[H("3b1.0"), H("3b1.1")],
         mistakes=M({"3b1.0~11/4": "Swapped: the rental falls."}),
         hints=["From the chemicals condition w = 8 &minus; 3r."],
         explain="Check: 21/4 + 11/4 = 8 and 7/4 + 33/4 = 10."),
    Part("3b2", "3(b)", 1,
         "The four percentage changes, in percent?",
         form=["%s" % WH, BOX, "%s" % PXH, BOX, "%s" % PYH, BOX, "%s" % RH, BOX],
         answers=[H("3b2.0"), H("3b2.1"), H("3b2.2"), H("3b2.3")],
         mistakes=M({"3b2.3~12.5": "The rental fell, from 2 to 7/4."}),
         explain="37.5, 25, 0 and &minus;12.5."),
    Part("3b3", "3(b)", 1,
         "Arrange them in one chain and name the theorem.",
         choices=[SS, SS_RYB, SS_ORDER, SS_FPE],
         answers=[H("3b3.c")],
         mistakes=M({
             "3b3.c~" + SS_RYB: "Rybczynski moves endowments; here a price moved.",
             "3b3.c~" + SS_ORDER: "37.5 against 25.",
             "3b3.c~" + SS_FPE: "Factor price equalization is about two countries.",
         }),
         explain="Magnification: factor prices move more than goods prices."),
    Part("3c", "3(c)", 1,
         "Do workers and capital owners gain or lose in real terms?",
         choices=[REAL, REAL_BASKET, REAL_BOTH, REAL_NONE],
         answers=[H("3c.c")],
         mistakes=M({
             "3c.c~" + REAL_BASKET: "w rose 37.5%, more than either price.",
             "3c.c~" + REAL_BOTH: "The rental fell while no price fell.",
             "3c.c~" + REAL_NONE: "Compare each factor price with both goods prices.",
         }),
         explain="Three sentences on the exam."),
]

factors = ExamProblem(
    "Problem 3 &middot; Chemicals and textiles",
    "Chemicals (good y) need 3 units of capital and 1 of labor per unit; textiles (good x) 1 "
    "of capital and 3 of labor. Both industries are competitive and the economy is small.",
    FACTOR_PARTS, draw_factors, figsize=(5.8, 4.4),
)


# ======================================================================
# Problem 4: board games
# ======================================================================

BOARD = "The price and each firm's output stay the same, since a constant elasticity fixes the markup and zero profit then fixes firm size. Nordøy keeps its number of firms, but a consumer can now buy from both countries' firms: twice the varieties. The gain is the gain from variety"
BOARD_PRICE = "The price falls and each firm grows, so Nordøy has fewer firms; the gain is a lower markup"
BOARD_SPEC = "Nordøy specializes in the games it makes best, as in Ricardo; the gain is specialization"
BOARD_NONE = "Nothing changes: identical countries have nothing to trade"

NO_TRADE = "Both models need the countries to differ, in technology or in endowments. Identical countries have identical autarky prices, so there is no comparative advantage"
NT_COST = "Both models assume trade costs are prohibitive"
NT_GOODS = "Both models only allow one good"
NT_SIZE = "Both models need one country to be larger"

BOARD_PARTS = [
    Part("4a", "4(a)", 3,
         "Nordøy and Sørøy open to trade with each other, and the elasticity of demand is "
         "constant. What happens to the price, to each firm's output, to the number of firms in "
         "Nordøy and to the varieties a consumer there can buy? Where does the gain come from?",
         choices=[BOARD, BOARD_PRICE, BOARD_SPEC, BOARD_NONE],
         answers=[H("4a.c")],
         mistakes=M({
             "4a.c~" + BOARD_PRICE: "That is the general case. With a constant elasticity the "
                                    "markup cannot fall.",
             "4a.c~" + BOARD_SPEC: "Nobody has a comparative advantage between identical "
                                   "countries.",
             "4a.c~" + BOARD_NONE: "Each firm makes its own variety, and consumers love variety.",
         }),
         explain="Five sentences on the exam."),
    Part("4b", "4(b)", 2,
         "Why can neither the Ricardian nor the Heckscher&ndash;Ohlin model produce trade "
         "between Nordøy and Sørøy?",
         choices=[NO_TRADE, NT_COST, NT_GOODS, NT_SIZE],
         answers=[H("4b.c")],
         mistakes=M({
             "4b.c~" + NT_COST: "Both models assume free trade.",
             "4b.c~" + NT_GOODS: "Both have two goods.",
             "4b.c~" + NT_SIZE: "Size moves neither model's prediction.",
         }),
         explain="Two sentences on the exam."),
]

boards = ExamProblem(
    "Problem 4 &middot; Board games",
    "Nordøy and Sørøy are identical. In each, board games are made under monopolistic "
    "competition: many firms, one variety each, a fixed cost and a constant marginal cost, free "
    "entry, and consumers who love variety. No calculation is needed.",
    BOARD_PARTS,
)


# ======================================================================
# Problem 5: ten multiple-choice questions
# ======================================================================

def _mc(n, prompt, options, hint, explain):
    # One point each. options are the paper's (a) to (d), in the paper's order.
    return Part("m%d" % n, "5.%d" % n, 1, prompt,
                choices=["(%s) %s" % (letter, text) for letter, text in zip("abcd", options)],
                answers=[H("m%d.c" % n)], hints=[hint], explain=explain)


CONCEPT_PARTS = [
    _mc(1, "The elasticity of substitution between AI and labor is &sigma; = 2. AI becomes "
           "cheaper relative to labor. Labor's share of the firm's costs",
        ["rises", "falls", "stays the same, since only prices changed",
         "cannot be signed without the firm's output"],
        "With &sigma; &gt; 1 the quantity of AI rises by more than its price falls.",
        "&sigma; &gt; 1: the cheaper input's share rises, so labor's falls."),
    _mc(2, "A study finds that AI could technically perform most of the tasks in an occupation. "
           "This tells you that",
        ["wages in the occupation will fall", "firms will automate those tasks",
         "the occupation is exposed, while adoption depends on unit costs, quality and adoption "
         "costs",
         "workers in the occupation will be displaced"],
        "Technically possible is not the same as cheaper.",
        "Exposure is not adoption, and adoption is not displacement."),
    _mc(3, "In the Ricardian model, a country that needs more hours than its trading partner to "
           "make every good",
        ["cannot export anything",
         "exports the good in which its disadvantage is smallest, and has the lower wage",
         "gains nothing from trade", "must protect its industries to trade"],
        "Problem 2 is this case.",
        "Comparative advantage, paid for with a lower wage."),
    _mc(4, "In the Ricardian model, the pattern of trade follows comparative advantage. The "
           "level of each country's wage follows",
        ["absolute advantage", "comparative advantage", "the size of the labor force",
         "the world price only"],
        "w = p/a<sub>x</sub>: what sets the level of a?",
        "Ratios for the pattern, levels for the wages."),
    _mc(5, "In the Heckscher&ndash;Ohlin model, the economy's capital stock rises while goods "
           "prices stay fixed. Then",
        ["both outputs rise in proportion", "the rental rate of capital falls",
         "the output of the capital-intensive good rises by more than in proportion, and the "
         "output of the labor-intensive good falls",
         "the wage rises"],
        "Fixed prices mean fixed factor prices.",
        "Rybczynski, with magnification on the quantity side."),
    _mc(6, "Leontief found that U.S. imports used more capital per worker than U.S. exports. "
           "Leamer (1980) showed that",
        ["Leontief's data were wrong",
         "Leontief compared the wrong two ratios, and the right comparison, capital per worker "
         "in production against consumption, showed the U.S. to be capital abundant",
         "Heckscher&ndash;Ohlin is refuted", "the U.S. was labor abundant"],
        "Leamer kept the data and changed the test.",
        "$6,949 against $6,737 per person in 1947."),
    _mc(7, "Gravity with unit elasticities, ln X<sub>ij</sub> = k + ln Y<sub>i</sub> + ln "
           "Y<sub>j</sub> &minus; ln d<sub>ij</sub>. The exporter's GDP triples, the importer's "
           "doubles, and the distance between them triples. Predicted trade changes by a factor "
           "of",
        ["18", "2", "6", "1/2"],
        "Multiply the GDP factors and divide by the distance factor.",
        "3 &times; 2 / 3 = 2."),
    _mc(8, "McCallum found that Canadian provinces trade far more with each other than with "
           "U.S. states at the same distance. The measured border effect is large mainly because",
        ["tariffs between Canada and the U.S. are high",
         "Canada is small, and leaving out multilateral resistance makes the border effect look "
         "larger",
         "distance matters more in Canada", "Canadians prefer Canadian goods"],
        "Remember the 10/90 arithmetic.",
        "Anderson and van Wincoop: size inflates the measured number."),
    _mc(9, "In the gravity equation that comes out of the monopolistic competition model, "
           "bilateral trade is proportional to the importer's GDP because",
        ["bigger countries face lower trade costs",
         "every country spends a fixed share of its income on each variety, so a bigger importer "
         "spends more on each of the exporter's varieties",
         "bigger countries make more varieties and therefore import less",
         "GDP is measured in the same currency in both countries"],
        "Identical homothetic tastes: what share does j spend on i's goods?",
        "X<sub>ij</sub> = s<sub>j</sub>Y<sub>i</sub>."),
    _mc(10, "The gravity equation fits trade data well across countries and years. This good "
            "fit shows that",
        ["the monopolistic competition model is the right model of trade",
         "countries specialize in different goods, whatever the reason, since gravity holds "
         "whenever they do",
         "tariffs are low everywhere", "GDP and distance are measured without error"],
        "Which other models also give gravity?",
        "A good fit proves specialization, not monopolistic competition."),
]

concepts = ExamProblem(
    "Problem 5 &middot; Key concepts",
    "Ten multiple-choice questions, one point each. Exactly one answer is correct. On paper, "
    "write the question number and the letter, one line per question, as 5.1 (b).",
    CONCEPT_PARTS,
)


paper = ExamPaper(
    "Workshop 2 &middot; your score",
    [saltdal, ricardo, factors, boards, concepts],
    note="The paper gives each problem's points; except in Problem 4, the split across parts is "
         "this page's. On the exam the derivation, the figure and the sentences carry the marks, "
         "so compare those with the solutions.",
)
