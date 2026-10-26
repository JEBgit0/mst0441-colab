"""
guided_s10.py - session 10 guided page: Heckscher-Ohlin and factor prices.

    Part 1  prices     zero profits, goods prices to factor prices, and the
                       magnification chain (the first Try it)
    Part 2  outputs    full employment, endowments to outputs, and Rybczynski
                       (the second Try it)
    Part 3  worksheet  the notes' worksheet: the Lerner diagram and the
                       full-employment cross
    Part 4  karelia    review questions 2-4: Karelia, both sides of the model
    Part 5  steel      problem A10.1: steel and apparel, the price side
    Part 6  home       problem A10.3: the quantity side, Heckscher-Ohlin and
                       factor price equalization
    Part 7  record     the empirical record and the short run (review
                       questions 1, 5 and 6, worksheet task 4)
    Part 8  tariff     problem A10.2: Nordheim's bicycle tariff (context: not
                       examinable)

Answers are hashes in answers_s10.py, generated from
answer_keys/s10_keys.py in the private repo. The maths is heckscher.py: its
self-check reproduces every number asked for here.
"""

import numpy as np

import guided_plots as gp
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from heckscher import HO
from style import CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW

H, M = answers("s10")

CTX = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
       "context: not examinable</span> ")
PY, PX = "p<sub>y</sub>", "p<sub>x</sub>"
QY, QX = "q<sub>y</sub>", "q<sub>x</sub>"
RH, WH = "r&#770;", "w&#770;"                      # r-hat and w-hat
PYH, PXH = "p&#770;<sub>y</sub>", "p&#770;<sub>x</sub>"
QYH, QXH = "q&#770;<sub>y</sub>", "q&#770;<sub>x</sub>"


# ------------------------------------------------------------------ drawing ---

def _panel(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    # A bare frame with ticks only where a number has been earned.
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.tick_params(colors=MUTE, labelsize=8.5)


def _prices(ax, ho, good, p, wmax, **kw):
    # One zero-profit line in the factor-price plane: a_K r + a_E w = p, with
    # the wage across and the rental up.
    aK, aE = ho.a[good]
    ws = np.array([0.0, min(p / aE, wmax)])
    ax.plot(ws, (p - aE * ws) / aK, **kw)


def _employment(ax, ho, factor, amount, **kw):
    # One full-employment line in the output plane, q_x across and q_y up.
    i = 0 if factor == "K" else 1
    ay, ax_ = ho.a["y"][i], ho.a["x"][i]
    ax.plot([0, amount / ax_], [amount / ay, 0], **kw)


def _chain(ax, items, ymin, ymax, title):
    # The magnification chain as bars, from the largest change down.
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.axhline(0, color=INK, lw=0.8)
    xs = np.arange(len(items))
    for x, (label, value, colour) in zip(xs, items):
        ax.bar(x, value, width=0.6, color=colour)
        ax.text(x, value + (0.03 if value >= 0 else -0.03) * (ymax - ymin),
                ("%+.1f%%" % value).replace(".0%", "%"), ha="center",
                va="bottom" if value >= 0 else "top", color=INK, fontsize=8.5)
    ax.set_xticks(xs)
    ax.set_xticklabels([label for label, _, _ in items], fontsize=10, color=INK)
    ax.set_yticks([])
    ax.set_ylim(ymin, ymax)


def _empty(ax, title):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)


# ======================================================================
# Part 1: zero profits, from goods prices to factor prices
# ======================================================================

VIN = HO(5, 2, 1, 2)                     # machinery (y) and garments (x)


def draw_prices(fig, stage):
    plane, bars = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.25, 1]))
    _panel(plane, 15, 13, "wage w", "rental r", "Zero profits: one line per good",
           xticks=([5] if stage >= 2 else []) + ([4] if stage >= 4 else []),
           yticks=([2] if stage >= 2 else []) + ([4] if stage >= 3 else []))
    if stage == 0:
        gp.start(plane)
    if stage >= 2:
        _prices(plane, VIN, "y", 20, 15, color=LINE, lw=2, label="machinery: 5r + 2w = 20")
        _prices(plane, VIN, "x", 12, 15, color=CURVE, lw=2, label="garments: r + 2w = 12")
        gp.dot(plane, 5, 2, "(5, 2)", 6, -12, colour=INK)
    if stage >= 3:
        plane.axhline(4, color=GREY, lw=0.8, ls=":")
    if stage >= 4:
        _prices(plane, VIN, "y", 28, 15, color=NEW, lw=1.6, ls="--", label="machinery at 28")
        gp.dot(plane, 4, 4, "(4, 4)", 8, 4, colour=NEW)
        gp.arrow(plane, (5, 2), (4, 4), colour=NEW)
    gp.legend(plane, loc="upper right")

    if stage >= 5:
        _chain(bars, [("$\\hat r$", 100, GREEN), ("$\\hat p_y$", 40, LINE), ("$\\hat p_x$", 0, CURVE),
                      ("$\\hat w$", -20, NEW)], -35, 120, "The magnification chain")
    else:
        _empty(bars, "The magnification chain")
    fig.subplots_adjust(wspace=0.25)


CAPITAL_Y = "Machinery: it uses 5/2 units of capital per worker against garments' 1/2"
CAPITAL_X = "Garments: they use 2 workers per unit, as many as machinery"
CAPITAL_NONE = "Neither: both use 2 units of labor per unit of output"
CAPITAL_BIG = "Machinery, because it is the more valuable good"

GAINS = "Capital owners gain whatever they buy, since r rises faster than both prices; workers lose whatever they buy, since w falls while no price falls"
GAINS_BASKET = "Capital owners gain only if they mostly buy garments, whose price did not move"
GAINS_BOTH = "Both gain: machinery is worth more, so the whole economy is richer"
GAINS_NOMINAL = "Nobody gains in real terms: only nominal prices moved"

AVERAGE = "Each goods price is an average of r and w weighted by cost shares, so each p-hat lies between r-hat and w-hat"
AVG_DEMAND = "Demand for machinery rises by more than its price"
AVG_CAPITAL = "Capital is scarce, so its price always moves most"
AVG_WAGE = "Wages are sticky, so the rental has to do the adjusting"

PRICE_QUESTIONS = [
    Question(
        "p1",
        "The notes' Vinland: machinery (good y) needs 5 units of capital and 2 of labor per "
        "unit; garments (good x) need 1 and 2. Capital per worker, K/E, in each industry?",
        form=["machinery", BOX, "&nbsp; garments", BOX],
        answers=[H("p1.0"), H("p1.1")],
        mistakes=M({"p1.0~2/5": "Capital over labor: 5/2."}),
        explain="Machinery is the capital-intensive industry. Every theorem today is signed by "
                "this ranking."),
    Question(
        "p2",
        "Zero profits: %s = 5r + 2w and %s = r + 2w. At %s = 20 and %s = 12, the rental and the "
        "wage?" % (PY, PX, PY, PX),
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("p2.0"), H("p2.1")],
        mistakes=M({"p2.0~5": "Those are swapped: r first.",
                    "p2.0~8": "Subtract the garment condition from the machinery one: 4r = 8."}),
        hints=["Subtract one condition from the other: the wage drops out."],
        explain="Check both: 10 + 10 = 20 and 2 + 10 = 12. Goods prices alone set factor prices."),
    Question(
        "p3",
        "(b) A machinery boom doubles the rental, and garments still sell for 12. The new wage?",
        form=["w =", BOX],
        answers=[H("p3.0")],
        mistakes=M({"p3.0~5": "The garment condition still has to hold: 4 + 2w = 12.",
                    "p3.0~10": "Double the rental, not the wage: r = 4."}),
        explain="The wage falls from 5 to 4."),
    Question(
        "p4",
        "Now run the machinery condition backward. Which machinery price caused all this?",
        form=["%s =" % PY, BOX],
        answers=[H("p4.0")],
        mistakes=M({"p4.0~40": "Put the new r and w into 5r + 2w: 5(4) + 2(4).",
                    "p4.0~20": "That is the old price. 5(4) + 2(4)?"}),
        explain="A goods price read out of factor prices: the conditions run both ways."),
    Question(
        "p5",
        "(c) The four percentage changes, in percent?",
        form=["%s" % RH, BOX, "&nbsp; %s" % PYH, BOX, "&nbsp; %s" % PXH, BOX, "&nbsp; %s" % WH, BOX],
        answers=[H("p5.0"), H("p5.1"), H("p5.2"), H("p5.3")],
        mistakes=M({"p5.3~20": "The wage fell, from 5 to 4.",
                    "p5.3~-25": "Divide by the old wage, 5: (4 &minus; 5)/5.",
                    "p5.1~8": "In percent: (28 &minus; 20)/20 = 0.4."}),
        explain="%s &gt; %s &gt; %s &gt; %s: 100 &gt; 40 &gt; 0 &gt; &minus;20." % (RH, PYH, PXH, WH)),
    Question(
        "p6",
        "Who gains in real terms, and who loses?",
        choices=[GAINS, GAINS_BASKET, GAINS_BOTH, GAINS_NOMINAL],
        answers=[H("p6.c")],
        mistakes=M({
            "p6.c~" + GAINS_BASKET: "r rose 100%, more than either price. What basket could "
                                    "cost more than that?",
            "p6.c~" + GAINS_BOTH: "The wage fell while no price fell.",
            "p6.c~" + GAINS_NOMINAL: "Compare each factor price with both goods prices.",
        }),
        explain="No preference information needed: that is the power of the theorem."),
    Question(
        "p7",
        "Why must the chain look like this, with the goods prices in the middle?",
        choices=[AVERAGE, AVG_DEMAND, AVG_CAPITAL, AVG_WAGE],
        answers=[H("p7.c")],
        mistakes=M({
            "p7.c~" + AVG_DEMAND: "No demand appears anywhere: zero profits alone.",
            "p7.c~" + AVG_CAPITAL: "Raise the garment price instead and the wage moves most.",
            "p7.c~" + AVG_WAGE: "Both factor prices are flexible here.",
        }),
        explain="Jones's magnification effect: factor prices move more than goods prices."),
]

prices = GuidedProblem(
    "Part 1 &middot; Zero profits: goods prices to factor prices",
    "Two goods, two factors, fixed input requirements, perfect competition. Price equals unit "
    "cost in each good, so each good gives one line in the plane of the wage w and the rental "
    "r: factor prices sit where the lines cross.",
    PRICE_QUESTIONS, draw_prices, figsize=(8.0, 3.9), whole_figure=True,
    outro="Stolper&ndash;Samuelson: the factor used intensively in the good whose price rises "
          "gains in real terms, and the other factor loses.",
    sources=[NOTES("p. 6&ndash;8")],
)


# ======================================================================
# Part 2: full employment, from endowments to outputs
# ======================================================================

def draw_outputs(fig, stage):
    cross, bars = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.25, 1]))
    big = stage >= 2
    _panel(cross, 130 if big else 95, 34, "garments q$_x$", "machinery q$_y$",
           "Full employment: one line per factor",
           xticks=([15] if stage >= 1 else []) + ([6] if stage >= 2 else []),
           yticks=([15] if stage >= 1 else []) + ([24] if stage >= 2 else []))
    if stage == 0:
        gp.start(cross)
    if stage >= 1:
        _employment(cross, VIN, "E", 60, color=CURVE, lw=2, label="labor: 2q$_y$ + 2q$_x$ = 60")
        _employment(cross, VIN, "K", 90, color=LINE, lw=2, label="capital: 5q$_y$ + q$_x$ = 90")
        gp.dot(cross, 15, 15, "", colour=INK)
    if stage >= 3:
        _employment(cross, VIN, "K", 126, color=NEW, lw=1.6, ls="--", label="capital: 126")
        gp.dot(cross, 6, 24, "", colour=NEW)
        gp.arrow(cross, (15, 15), (6, 24), colour=NEW)
    gp.legend(cross, loc="upper right")

    if stage >= 4:
        _chain(bars, [("$\\hat q_y$", 60, LINE), ("$\\hat K$", 40, GREEN), ("$\\hat E$", 0, CURVE),
                      ("$\\hat q_x$", -60, NEW)], -80, 85, "Rybczynski's chain")
    else:
        _empty(bars, "Rybczynski's chain")
    fig.subplots_adjust(wspace=0.25)


RYB = "Rybczynski: at fixed goods prices the input ratios are fixed, so machinery can absorb the new capital only by taking labor from garments, which shrink"
RYB_SS = "Stolper-Samuelson: the rental fell, so garments became more expensive to make"
RYB_PRICE = "Garments shrink because their price fell"
RYB_BOTH = "Both outputs grow: the economy has more capital"

OUTPUT_QUESTIONS = [
    Question(
        "o1",
        "Same technology. Full employment: 5%s + %s = K and 2%s + 2%s = E. At K = 90 and E = 60, "
        "both outputs?" % (QY, QX, QY, QX),
        form=["machinery", BOX, "&nbsp; garments", BOX],
        answers=[H("o1.0"), H("o1.1")],
        hints=["The labor line says %s + %s = 30. Subtract it from the capital line." % (QY, QX)],
        explain="Check: 75 + 15 = 90 and 30 + 30 = 60."),
    Question(
        "o2",
        "(b) The detective version. A decade later, at unchanged prices, machinery output is 24 "
        "and the labor force is still 60. How much labor is left for garments, and how much do "
        "they make?",
        form=["labor", BOX, "&nbsp; garments", BOX],
        answers=[H("o2.0"), H("o2.1")],
        mistakes=M({"o2.1~12": "Each unit of garments needs 2 workers.",
                    "o2.0~36": "Machinery takes 2 &times; 24 = 48 workers."}),
        hints=["Start from labor: it is the factor you know did not move."],
        explain="Garments fall from 15 to 6."),
    Question(
        "o3",
        "Read the capital line: how much capital is there now, and how much arrived?",
        form=["K =", BOX, "&nbsp; arrived", BOX],
        answers=[H("o3.0"), H("o3.1")],
        mistakes=M({"o3.0~120": "Garments still use some: 5 &times; 24 + 6.",
                    "o3.1~30": "126 &minus; 90."}),
        explain="Recovered from outputs alone: what empirical work does with real data."),
    Question(
        "o4",
        "(c) The percentage changes in machinery output, capital and garment output?",
        form=["%s" % QYH, BOX, "&nbsp; K&#770;", BOX, "&nbsp; %s" % QXH, BOX],
        answers=[H("o4.0"), H("o4.1"), H("o4.2")],
        mistakes=M({"o4.2~60": "Garments fell, from 15 to 6.",
                    "o4.0~9": "In percent: (24 &minus; 15)/15."}),
        explain="60 &gt; 40 &gt; 0 &gt; &minus;60: magnification on the quantity side."),
    Question(
        "o5",
        "Which theorem is this, and why do garments shrink although nothing was taken from them?",
        choices=[RYB, RYB_SS, RYB_PRICE, RYB_BOTH],
        answers=[H("o5.c")],
        mistakes=M({
            "o5.c~" + RYB_SS: "Prices are held fixed, so factor prices are too.",
            "o5.c~" + RYB_PRICE: "Goods prices did not move at all.",
            "o5.c~" + RYB_BOTH: "Read your chain: one output fell.",
        }),
        explain="Stolper&ndash;Samuelson moves prices holding endowments; Rybczynski moves "
                "endowments holding prices. Duals."),
    Question(
        "o6",
        "Both outputs are non-negative only for some endowments. Between which two values of "
        "K/E?",
        form=["", BOX, "&le; K/E &le;", BOX],
        answers=[H("o6.0"), H("o6.1")],
        mistakes=M({"o6.0~2": "Capital per worker in garments: 1/2."}),
        hints=["The bounds are the two industries' own capital-labor ratios."],
        explain="The cone of diversification. Outside it the country specializes."),
]

outputs = GuidedProblem(
    "Part 2 &middot; Full employment: endowments to outputs",
    "The same Vinland, now on the quantity side. Each factor gives one line in the plane of "
    "the two outputs, and the economy produces where they cross.",
    OUTPUT_QUESTIONS, draw_outputs, figsize=(8.0, 3.9), whole_figure=True,
    outro="Rybczynski: the growing factor's good expands more than in proportion, and the other "
          "good contracts.",
    sources=[NOTES("p. 9&ndash;10")],
)


# ======================================================================
# Part 3: the worksheet, the Lerner diagram and the full-employment cross
# ======================================================================

SHEET = HO(2, 1, 1, 3)                   # electronics (y) and textiles (x)


def draw_worksheet(fig, stage):
    lerner, cross = fig.subplots(1, 2)
    wide = stage >= 5
    _panel(lerner, 1.05 if wide else 0.55, 0.3, "labor per krone", "capital per krone",
           "Lerner: inputs per krone of output",
           xticks=([0.1, 0.3] if stage >= 2 else []) + ([0.5] if stage >= 3 else [])
           + ([1.0] if wide else []),
           yticks=([0.1, 0.2] if stage >= 2 else []) + ([0.25] if stage >= 3 else []))
    lerner.text(0.1, 0.205, "electronics", color=LINE, fontsize=8.5)
    lerner.text(0.3, 0.107, "textiles", color=CURVE, fontsize=8.5)
    gp.dot(lerner, 0.1, 0.2, "", colour=LINE)
    gp.dot(lerner, 0.3, 0.1, "", colour=CURVE)
    if stage >= 3:
        lerner.plot([0, 0.5], [0.25, 0], color=INK, lw=1.6, label="isocost 2E + 4K = 1")
    if stage >= 4:
        lerner.fill([0, 0.15, 0.6], [0, 0.3, 0.2], color=GREEN, alpha=0.12, lw=0)
        lerner.plot([0, 0.15], [0, 0.3], color=LINE, lw=1, ls=":")
        lerner.plot([0, 0.6], [0, 0.2], color=CURVE, lw=1, ls=":")
        lerner.text(0.33, 0.22, "cone", color=GREEN, fontsize=9)
    if wide:
        gp.dot(lerner, 1 / 15, 2 / 15, "", colour=NEW)
        lerner.plot([0, 1], [1 / 7, 0], color=NEW, lw=1.6, ls="--", label="at %s = 15: E + 7K = 1" % "p$_y$")
    gp.legend(lerner, loc="upper right")

    _panel(cross, 21, 26, "textiles q$_x$", "electronics q$_y$", "Full employment",
           xticks=range(5, 21, 5), yticks=range(5, 26, 5))
    cross.grid(True, color="#e5e7eb", lw=0.6)
    cross.set_axisbelow(True)
    _employment(cross, SHEET, "K", 50, color=LINE, lw=2, label="capital: 2q$_y$ + q$_x$ = 50")
    if stage >= 8:
        _employment(cross, SHEET, "E", 50, color=CURVE, lw=2, label="labor: E = 50")
        gp.dot(cross, 10, 20, "", colour=INK)
    if stage >= 9:
        _employment(cross, SHEET, "E", 60, color=NEW, lw=1.6, ls="--", label="labor: E = 60")
        gp.dot(cross, 14, 18, "", colour=NEW)
    gp.legend(cross, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


CONE = "Those with K/E between 1/3 and 2: they can be split between the two rays with both industries active, and inside that cone factor prices do not depend on the endowment"
CONE_ANY = "Every endowment: goods prices always fix factor prices"
CONE_ABOVE = "Those with K/E above 2, where capital is plentiful"
CONE_LINE = "Only endowments on the isocost line"

SHEET_GAINS = "Capital owners gain and workers lose, in terms of either good"
SHEET_TEXT = "Workers gain if they buy textiles, whose price did not move"
SHEET_BOTH = "Both lose: electronics got dearer"
SHEET_NONE = "Nobody: the economy is diversified, so factor prices are fixed"

SHEET_QUESTIONS = [
    Question(
        "w1",
        "Task 1: electronics (good y) needs 2 units of capital and 1 of labor; textiles (good x) "
        "1 and 3. Capital per worker in each?",
        form=["electronics", BOX, "&nbsp; textiles", BOX],
        answers=[H("w1.0"), H("w1.1")],
        mistakes=M({"w1.1~3": "Capital over labor: 1/3."}),
        explain="Electronics is capital intensive."),
    Question(
        "w2",
        "Zero profits: %s = 2r + w and %s = r + 3w. Solve at %s = %s = 10." % (PY, PX, PY, PX),
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("w2.0"), H("w2.1")],
        mistakes=M({"w2.0~2": "Swapped: r first."}),
        hints=["Set the two conditions equal: 2r + w = r + 3w, so r = 2w."],
        explain="Inputs per krone: electronics (1/10, 2/10), textiles (3/10, 1/10), the two dots."),
    Question(
        "w3",
        "Task 3, left panel: the isocost line wE + rK = 1 passes through both dots. Where does it "
        "meet each axis?",
        form=["labor 1/w =", BOX, "&nbsp; capital 1/r =", BOX],
        answers=[H("w3.0"), H("w3.1")],
        mistakes=M({"w3.0~2": "The intercept is 1/w, not w."}),
        explain="Read factor prices off the axes: the whole Lerner diagram in one line."),
    Question(
        "w4",
        "The rays through the two dots bound a cone. Which endowments lie in it?",
        choices=[CONE, CONE_ANY, CONE_ABOVE, CONE_LINE],
        answers=[H("w4.c")],
        mistakes=M({
            "w4.c~" + CONE_ANY: "Outside the cone one good is not made, and the tangency logic "
                                "breaks.",
            "w4.c~" + CONE_ABOVE: "Above the steeper ray the economy makes electronics only.",
            "w4.c~" + CONE_LINE: "The line is about prices, the cone about endowments.",
        }),
        explain="Factor price insensitivity: inside the cone, endowments do not move w and r."),
    Question(
        "w5",
        "Re-solve at %s = 15, with %s still 10." % (PY, PX),
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("w5.0"), H("w5.1")],
        hints=["From the textile condition r = 10 &minus; 3w. Put that into 2r + w = 15."],
        explain="The electronics dot moves in to (1/15, 2/15), and the isocost line pivots."),
    Question(
        "w6",
        "The four changes, in percent?",
        form=["%s" % RH, BOX, "&nbsp; %s" % PYH, BOX, "&nbsp; %s" % PXH, BOX, "&nbsp; %s" % WH, BOX],
        answers=[H("w6.0"), H("w6.1"), H("w6.2"), H("w6.3")],
        mistakes=M({"w6.0~3": "In percent: (7 &minus; 4)/4.", "w6.3~50": "The wage halved."}),
        explain="75 &gt; 50 &gt; 0 &gt; &minus;50."),
    Question(
        "w7",
        "Who gains and who loses in real terms?",
        choices=[SHEET_GAINS, SHEET_TEXT, SHEET_BOTH, SHEET_NONE],
        answers=[H("w7.c")],
        mistakes=M({
            "w7.c~" + SHEET_TEXT: "The wage fell 50% and textiles cost the same: fewer textiles.",
            "w7.c~" + SHEET_BOTH: "The rental rose 75%, more than electronics' 50%.",
            "w7.c~" + SHEET_NONE: "Fixed for given goods prices, but the price moved.",
        }),
        explain="The capital-intensive good's price rose, so capital wins outright."),
    Question(
        "w8",
        "Task 2: full employment is 2%s + %s = K = 50 and %s + 3%s = E = 50. Both outputs?"
        % (QY, QX, QY, QX),
        form=["%s =" % QY, BOX, "&nbsp; %s =" % QX, BOX],
        answers=[H("w8.0"), H("w8.1")],
        hints=["%s = 50 &minus; 2%s from the capital line." % (QX, QY)],
        explain="The crossing in the right panel."),
    Question(
        "w9",
        "Let E rise to 60 at unchanged prices. The new outputs?",
        form=["%s =" % QY, BOX, "&nbsp; %s =" % QX, BOX],
        answers=[H("w9.0"), H("w9.1")],
        mistakes=M({"w9.0~24": "Electronics falls: the new labor goes to textiles."}),
        explain="The economy slides down the fixed capital line."),
    Question(
        "w10",
        "Chain %s, &Ecirc; and %s, in percent." % (QXH, QYH),
        form=["%s" % QXH, BOX, "&nbsp; &Ecirc;", BOX, "&nbsp; %s" % QYH, BOX],
        answers=[H("w10.0"), H("w10.1"), H("w10.2")],
        mistakes=M({"w10.2~10": "Electronics fell, from 20 to 18."}),
        explain="40 &gt; 20 &gt; 0 &gt; &minus;10: Rybczynski, the labor version."),
]

worksheet = GuidedProblem(
    "Part 3 &middot; The worksheet: Lerner and the full-employment cross",
    "Tasks 1 to 3, the two panels to finish before the in-person session. With fixed "
    "coefficients each unit-value isoquant collapses to a single dot.",
    SHEET_QUESTIONS, draw_worksheet, figsize=(8.0, 3.9), whole_figure=True,
    outro="Bring the sheet: we go through it together in class.",
    sources=[NOTES("p. 20&ndash;21, worksheet")],
)


# ======================================================================
# Part 4: review questions 2-4, Karelia
# ======================================================================

KAR = HO(3, 1, 1, 2)                     # robotics (y) and footwear (x)


def draw_karelia(fig, stage):
    plane, cross = fig.subplots(1, 2)
    _panel(plane, 9, 16, "wage w", "rental r", "Factor prices",
           xticks=([4] if stage >= 2 else []) + ([3] if stage >= 3 else []),
           yticks=([2] if stage >= 2 else []) + ([4] if stage >= 3 else []))
    if stage == 0:
        gp.start(plane)
    if stage >= 2:
        _prices(plane, KAR, "y", 10, 9, color=LINE, lw=2, label="robotics at 10")
        _prices(plane, KAR, "x", 10, 9, color=CURVE, lw=2, label="footwear at 10")
        gp.dot(plane, 4, 2, "", colour=INK)
    if stage >= 3:
        _prices(plane, KAR, "y", 15, 9, color=NEW, lw=1.6, ls="--", label="robotics at 15")
        gp.dot(plane, 3, 4, "", colour=NEW)
    gp.legend(plane, loc="upper right")

    _panel(cross, 75, 26, "footwear q$_x$", "robotics q$_y$", "Outputs")
    if stage >= 5:
        _employment(cross, KAR, "E", 40, color=CURVE, lw=2, label="labor 40")
        _employment(cross, KAR, "K", 60, color=LINE, lw=2, label="capital 60")
        gp.dot(cross, 12, 16, "(12, 16)", 8, -12, colour=INK)
    if stage >= 6:
        _employment(cross, KAR, "K", 70, color=NEW, lw=1.6, ls="--", label="capital 70")
        gp.dot(cross, 10, 20, "(10, 20)", 8, 4, colour=NEW)
    gp.legend(cross, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


ABSORB = "At fixed prices both industries keep their input ratios; robotics needs labor to absorb the new capital, and the only place it can come from is footwear"
ABSORB_PRICE = "The price of footwear fell"
ABSORB_RENT = "The rental rose, so footwear became too expensive to make"
ABSORB_DEMAND = "Consumers want fewer shoes when they are richer"

REVERSAL = "The two isoquants would cross twice: two common tangents and two cones, so goods prices no longer pin down factor prices without knowing which cone the endowment is in"
REV_NONE = "Nothing: the diagram has one tangent line whatever the technology"
REV_SAME = "Both industries would use the same ratio, so the cone would vanish"
REV_FPE = "Factor prices would be equalized everywhere, even outside the cone"

KARELIA_QUESTIONS = [
    Question(
        "k1",
        "Review question 2: robotics (y) uses 3 units of capital and 1 of labor; footwear (x) 1 "
        "and 2. (a) Capital per worker in each?",
        form=["robotics", BOX, "&nbsp; footwear", BOX],
        answers=[H("k1.0"), H("k1.1")],
        mistakes=M({"k1.1~2": "Capital over labor: 1/2."}),
        explain="Robotics is capital intensive."),
    Question(
        "k2",
        "(b) %s = 3r + w and %s = r + 2w. Solve at %s = %s = 10." % (PY, PX, PY, PX),
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("k2.0"), H("k2.1")],
        mistakes=M({"k2.0~4": "Swapped: r first."}),
        explain="Check: 6 + 4 = 10 and 2 + 8 = 10."),
    Question(
        "k3",
        "(c) The robotics price rises to 15.",
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("k3.0"), H("k3.1")],
        explain="Check: 12 + 3 = 15 and 4 + 6 = 10."),
    Question(
        "k4",
        "(d) The four changes, in percent?",
        form=["%s" % RH, BOX, "&nbsp; %s" % PYH, BOX, "&nbsp; %s" % PXH, BOX, "&nbsp; %s" % WH, BOX],
        answers=[H("k4.0"), H("k4.1"), H("k4.2"), H("k4.3")],
        mistakes=M({"k4.3~-33.3": "Divide by the old wage, 4: (3 &minus; 4)/4.",
                    "k4.3~-100/3": "Divide by the old wage, 4: (3 &minus; 4)/4.",
                    "k4.3~25": "The wage fell."}),
        explain="100 &gt; 50 &gt; 0 &gt; &minus;25: Stolper&ndash;Samuelson. Capital gains, labor "
                "loses, in real terms."),
    Question(
        "k5",
        "Review question 3: 3%s + %s = K and %s + 2%s = E. At K = 60 and E = 40?"
        % (QY, QX, QY, QX),
        form=["%s =" % QY, BOX, "&nbsp; %s =" % QX, BOX],
        answers=[H("k5.0"), H("k5.1")],
        explain="Check: 48 + 12 = 60 and 16 + 24 = 40."),
    Question(
        "k6",
        "Capital grows to K = 70 at unchanged prices.",
        form=["%s =" % QY, BOX, "&nbsp; %s =" % QX, BOX],
        answers=[H("k6.0"), H("k6.1")],
        explain="Robotics up, footwear down."),
    Question(
        "k7",
        "The chain %s, K&#770;, %s, in percent?" % (QYH, QXH),
        form=["%s" % QYH, BOX, "&nbsp; K&#770;", BOX, "&nbsp; %s" % QXH, BOX],
        answers=[H("k7.0"), H("k7.1"), H("k7.2")],
        mistakes=M({"k7.1~10": "In percent of the old stock: 10/60."}),
        explain="25 &gt; 16.7 &gt; 0 &gt; &minus;16.7: Rybczynski."),
    Question(
        "k8",
        "Why does footwear contract absolutely, although nothing was taken away from it?",
        choices=[ABSORB, ABSORB_PRICE, ABSORB_RENT, ABSORB_DEMAND],
        answers=[H("k8.c")],
        mistakes=M({
            "k8.c~" + ABSORB_PRICE: "Prices are held fixed.",
            "k8.c~" + ABSORB_RENT: "With fixed prices the rental cannot move.",
            "k8.c~" + ABSORB_DEMAND: "Demand plays no role in the full-employment conditions.",
        }),
        explain="Three sentences on the exam: fixed ratios, labor needed, footwear releases it."),
    Question(
        "k9",
        "Review question 4: what would a factor intensity reversal do to the Lerner diagram?",
        choices=[REVERSAL, REV_NONE, REV_SAME, REV_FPE],
        answers=[H("k9.c")],
        mistakes=M({
            "k9.c~" + REV_NONE: "With a reversal the isoquants intersect twice.",
            "k9.c~" + REV_SAME: "That is a tie at one wage, not a reversal.",
            "k9.c~" + REV_FPE: "Countries in different cones get different factor prices.",
        }),
        explain="Without the no-reversal assumption no theorem is unconditional."),
]

karelia = GuidedProblem(
    "Part 4 &middot; Karelia: review questions 2&ndash;4",
    "One economy, both sides: goods prices to factor prices, then endowments to outputs.",
    KARELIA_QUESTIONS, draw_karelia, figsize=(8.0, 3.8), whole_figure=True,
    outro="Draw the Lerner diagram of review question 4 yourself, with 1/w and 1/r labelled.",
    sources=[NOTES("p. 21&ndash;22, review questions 2&ndash;4")],
)


# ======================================================================
# Part 5: problem A10.1, steel and apparel (the price side)
# ======================================================================

STEEL = HO(2, 1, 1, 1)                   # steel (y) and apparel (x)


def draw_steel(fig, stage):
    plane, real = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.1, 1]))
    _panel(plane, 13, 13, "wage w", "rental r", "Steel and apparel",
           xticks=([6] if stage >= 3 else []) + ([4] if stage >= 4 else []),
           yticks=([2] if stage >= 3 else []) + ([4] if stage >= 4 else []))
    if stage < 3:
        gp.start(plane)
    if stage >= 3:
        _prices(plane, STEEL, "y", 10, 13, color=LINE, lw=2, label="steel: 2r + w = 10")
        _prices(plane, STEEL, "x", 8, 13, color=CURVE, lw=2, label="apparel: r + w = 8")
        gp.dot(plane, 6, 2, "(6, 2)", 6, -12, colour=INK)
    if stage >= 4:
        _prices(plane, STEEL, "y", 12, 13, color=NEW, lw=1.6, ls="--", label="steel at 12")
        gp.dot(plane, 4, 4, "(4, 4)", 8, 2, colour=NEW)
    gp.legend(plane, loc="upper right")

    for side in ("top", "right"):
        real.spines[side].set_visible(False)
    real.set_title("Real returns, before and after", loc="left", color=INK, fontsize=9.5)
    names = ["r/p$_y$", "r/p$_x$", "w/p$_y$", "w/p$_x$"]
    xs = np.arange(4)
    real.set_xticks(xs)
    real.set_xticklabels(names, fontsize=9, color=INK)
    real.set_yticks([])
    real.set_ylim(0, 0.9)
    if stage >= 7:
        real.bar(xs[:2] - 0.18, [0.2, 0.25], width=0.34, color=GREY, label="before")
        real.bar(xs[:2] + 0.18, [1 / 3, 0.5], width=0.34, color=GREEN, label="after")
    if stage >= 8:
        real.bar(xs[2:] - 0.18, [0.6, 0.75], width=0.34, color=GREY)
        real.bar(xs[2:] + 0.18, [1 / 3, 0.5], width=0.34, color=NEW)
    gp.legend(real, loc="upper left")
    fig.subplots_adjust(wspace=0.25)


RANK = "Steel uses 2 units of capital per worker and apparel 1, so steel is capital intensive: the theorem says which factor gains from a price rise only once you know which good uses it intensively"
RANK_ABS = "Steel uses more capital in absolute terms, which is all the theorem needs"
RANK_PRICE = "Steel is dearer, so it is the capital-intensive good"
RANK_NONE = "Both use one unit of labor, so there is no ranking"

SS = "r̂ = 100 > p̂y = 20 > p̂x = 0 > ŵ = -33: Stolper-Samuelson"
SS_RYB = "The same chain, and it is Rybczynski"
SS_ORDER = "p̂y > r̂ > p̂x > ŵ: Stolper-Samuelson"
SS_FPE = "The same chain, and it is factor price equalization"

BASKET = "No: the rental rose more than either price and the wage fell while no price fell, so the answer holds for any basket"
BASKET_YES = "Yes: a worker who buys only apparel is better off"
BASKET_STEEL = "Yes: a capital owner who buys only steel loses"
BASKET_NOM = "It depends on whether incomes are measured in kroner"

OPEN = "Capital owners gain and workers lose in real terms, for any consumption pattern, by magnification. So the losers are identifiable, and whether to compensate them is a policy choice, not a matter of accounting"
OPEN_ALL = "Everybody gains, since trade raises national income"
OPEN_TASTE = "Who gains depends on what each group consumes"
OPEN_AUTO = "The losers are compensated automatically through lower prices"

LEONTIEF = "U.S. imports were more capital intensive than exports, $18,200 against $13,700 per person, odd for the most capital-abundant country. HOV tests factor content instead of goods, and its sign and rank tests pass in 61% and 49% of cases: about a coin flip"
LEON_EXPORTS = "U.S. exports were more capital intensive than imports, as the theory predicts"
LEON_HOV = "The modern tests confirm the theory in about 90% of cases"
LEON_DATA = "Leontief's data were wrong, and the paradox disappeared once corrected"

STEEL_QUESTIONS = [
    Question(
        "a1",
        "A10.1 (a): steel (good y) needs 2 units of capital and 1 of labor per unit; apparel "
        "(good x) 1 of each. Capital per worker in each?",
        form=["steel", BOX, "&nbsp; apparel", BOX],
        answers=[H("a1.0"), H("a1.1")],
        mistakes=M({"a1.0~1/2": "Capital over labor: 2/1."}),
        explain="Steel is capital intensive, apparel labor intensive."),
    Question(
        "a2",
        "Why is that ranking the object the Stolper&ndash;Samuelson theorem needs?",
        choices=[RANK, RANK_ABS, RANK_PRICE, RANK_NONE],
        answers=[H("a2.c")],
        mistakes=M({
            "a2.c~" + RANK_ABS: "Intensity is a ratio: capital per worker.",
            "a2.c~" + RANK_PRICE: "Prices do not enter the ranking.",
            "a2.c~" + RANK_NONE: "Compare capital per worker: 2 against 1.",
        }),
        explain="Two sentences on the exam."),
    Question(
        "a3",
        "(b) %s = 2r + w and %s = r + w give r = %s &minus; %s and w = 2%s &minus; %s. Evaluate at "
        "%s = 10 and %s = 8." % (PY, PX, PY, PX, PX, PY, PY, PX),
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("a3.0"), H("a3.1")],
        mistakes=M({"a3.0~6": "Swapped: r = 10 &minus; 8."}),
        explain="Verify: 2(2) + 6 = 10 and 2 + 6 = 8. On the exam, show both substitutions."),
    Question(
        "a4",
        "(c) Steel rises 20%, to 12; apparel stays at 8.",
        form=["r =", BOX, "&nbsp; w =", BOX],
        answers=[H("a4.0"), H("a4.1")],
        explain="Verify: 8 + 4 = 12 and 4 + 4 = 8."),
    Question(
        "a5",
        "(d) The percentage changes, in percent?",
        form=["%s" % PYH, BOX, "&nbsp; %s" % PXH, BOX, "&nbsp; %s" % RH, BOX, "&nbsp; %s" % WH, BOX],
        answers=[H("a5.0"), H("a5.1"), H("a5.2"), H("a5.3")],
        mistakes=M({"a5.3~-50": "Divide by the old wage, 6: (4 &minus; 6)/6.",
                    "a5.3~33.3": "The wage fell.", "a5.3~100/3": "The wage fell."}),
        explain="Sensible rounding is fine: &minus;33.3."),
    Question(
        "a6",
        "Arrange them in one chain, and name the theorem.",
        choices=[SS, SS_RYB, SS_ORDER, SS_FPE],
        answers=[H("a6.c")],
        mistakes=M({
            "a6.c~" + SS_RYB: "Rybczynski moves endowments; here prices moved.",
            "a6.c~" + SS_ORDER: "100 against 20.",
            "a6.c~" + SS_FPE: "Factor price equalization is about two countries.",
        }),
        explain="The magnification effect, with the paper's numbers."),
    Question(
        "a7",
        "(e) The rental in terms of each good, r/%s and r/%s, before and after?" % (PY, PX),
        form=["r/%s:" % PY, BOX, "&rarr;", BOX, "&nbsp; r/%s:" % PX, BOX, "&rarr;", BOX],
        answers=[H("a7.0"), H("a7.1"), H("a7.2"), H("a7.3")],
        mistakes=M({"a7.1~2/5": "After: 4/12."}),
        explain="Up in terms of both goods."),
    Question(
        "a8",
        "And the wage, w/%s and w/%s?" % (PY, PX),
        form=["w/%s:" % PY, BOX, "&rarr;", BOX, "&nbsp; w/%s:" % PX, BOX, "&rarr;", BOX],
        answers=[H("a8.0"), H("a8.1"), H("a8.2"), H("a8.3")],
        explain="Down in terms of both goods."),
    Question(
        "a9",
        "Does the answer depend on the basket the factor owner consumes?",
        choices=[BASKET, BASKET_YES, BASKET_STEEL, BASKET_NOM],
        answers=[H("a9.c")],
        mistakes=M({
            "a9.c~" + BASKET_YES: "w/%s fell from 3/4 to 1/2." % PX,
            "a9.c~" + BASKET_STEEL: "r/%s rose from 1/5 to 1/3." % PY,
            "a9.c~" + BASKET_NOM: "Real returns are measured in goods.",
        }),
        explain="Five sentences on the exam, with the derivation."),
    Question(
        "a10",
        "(f) A country opens to trade in a way that raises the relative price of its "
        "capital-intensive good.",
        choices=[OPEN, OPEN_ALL, OPEN_TASTE, OPEN_AUTO],
        answers=[H("a10.c")],
        mistakes=M({
            "a10.c~" + OPEN_ALL: "Aggregate gains hide a factor that loses outright.",
            "a10.c~" + OPEN_TASTE: "Magnification makes tastes irrelevant.",
            "a10.c~" + OPEN_AUTO: "Compensation is theoretically available and politically rare.",
        }),
        explain="The gap between possible and actual compensation is where the politics live."),
    Question(
        "a11",
        "(g) The empirical record.",
        choices=[LEONTIEF, LEON_EXPORTS, LEON_HOV, LEON_DATA],
        answers=[H("a11.c")],
        mistakes=M({
            "a11.c~" + LEON_EXPORTS: "That is what the theory predicted. Why a paradox?",
            "a11.c~" + LEON_HOV: "Set the scores against the coin-flip benchmark of 50%.",
            "a11.c~" + LEON_DATA: "Leamer said he ran the wrong test, not that the data were "
                                  "wrong.",
        }),
        explain="Use only the findings in the session 10 notes."),
]

steel = GuidedProblem(
    "Part 5 &middot; Steel and apparel: A10.1",
    "The price side, in the exam's format. Steel is good y, apparel good x, and both "
    "industries are perfectly competitive.",
    STEEL_QUESTIONS, draw_steel, figsize=(8.0, 3.9), whole_figure=True,
    outro="About 30% of an exam paper. The derivations and the sentences are yours to write.",
    sources=[PS("A10.1")],
)


# ======================================================================
# Part 6: problem A10.3, the quantity side
# ======================================================================

def draw_home(fig, stage):
    cone, cross = fig.subplots(1, 2)
    _panel(cone, 125, 165, "labor E", "capital K", "Endowments and the cone",
           xticks=[100] if stage >= 2 else [],
           yticks=([110, 120] if stage >= 7 else [120] if stage >= 2 else []) + ([140] if stage >= 4 else []))
    if stage == 0:
        gp.start(cone)
    if stage >= 2:
        cone.fill([0, 82.5, 125], [0, 165, 125], color=GREEN, alpha=0.12, lw=0)
        cone.plot([0, 82.5], [0, 165], color=LINE, lw=1.2, ls=":", label="steel ray, K/E = 2")
        cone.plot([0, 125], [0, 125], color=CURVE, lw=1.2, ls=":", label="apparel ray, K/E = 1")
        gp.dot(cone, 100, 120, "Home", 6, 2, colour=LINE)
    if stage >= 4:
        gp.dot(cone, 100, 140, "Home later", 6, 2, colour=NEW)
    if stage >= 7:
        gp.dot(cone, 100, 110, "Foreign", 6, -12, colour=CURVE)
    gp.legend(cone, loc="upper left")

    _panel(cross, 150, 75, "apparel q$_x$", "steel q$_y$", "Home's outputs",
           xticks=([80] if stage >= 1 else []) + ([60] if stage >= 4 else []),
           yticks=([20] if stage >= 1 else []) + ([40] if stage >= 4 else []))
    if stage >= 1:
        _employment(cross, STEEL, "E", 100, color=CURVE, lw=2, label="labor 100")
        _employment(cross, STEEL, "K", 120, color=LINE, lw=2, label="capital 120")
        gp.dot(cross, 80, 20, "", colour=INK)
    if stage >= 4:
        _employment(cross, STEEL, "K", 140, color=NEW, lw=1.6, ls="--", label="capital 140")
        gp.dot(cross, 60, 40, "", colour=NEW)
    gp.legend(cross, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


CONE_NAME = "The cone of diversification: outside it one output would be negative, so the country specializes in one good"
CONE_NAME_FPE = "The trade triangle: outside it the country stops trading"
CONE_NAME_PPF = "The production possibility frontier: outside it output is infeasible"
CONE_NAME_NONE = "It has no name: outside it both goods are still produced"

FIXED = "Goods prices, and with them factor prices and both industries' input ratios. Steel must expand to absorb the capital, it needs labor to do so, and labor can only come from apparel"
FIXED_E = "Only the labor force; the price of steel rises with the capital"
FIXED_TASTE = "Tastes, so that demand for apparel falls"
FIXED_NONE = "Nothing is held fixed: apparel falls because it is less profitable"

PATTERN = "Home, since K/E = 1.2 against 1.1. Home exports steel and Foreign apparel, by Heckscher-Ohlin, given identical technologies and identical homothetic tastes"
PATTERN_SIZE = "Home, since it has more capital in total; Home exports apparel"
PATTERN_F = "Foreign, since it makes more apparel; Foreign exports steel"
PATTERN_NONE = "Neither: same labor, same technology, so there is no trade"

MOVING = "Goods trade does the moving: exporting steel exports the capital embodied in it, so trade in goods substitutes for trade in factors. Same technology and same prices give the same tangent line, so the same w and r"
MOVING_MIGR = "Workers migrate until wages are equal"
MOVING_CAP = "Capital flows to where its return is highest"
MOVING_GOV = "Governments set wages equal through trade agreements"

DUALS = "Stolper-Samuelson takes endowments as given and signs factor prices after a price change; Rybczynski takes prices as given and signs outputs after an endowment change. Different technologies would break both, and then the answers to (d) and (e) would change"
DUALS_SAME = "They are the same theorem stated twice"
DUALS_TASTES = "Both take tastes as given and sign welfare"
DUALS_ONLY = "Only factor price equalization depends on assumptions"

HOME_QUESTIONS = [
    Question(
        "h1",
        "A10.3 (a)-(b): the same technology, so 2%s + %s = K and %s + %s = E, which give "
        "%s = K &minus; E and %s = 2E &minus; K. Home has K = 120 and E = 100. Its outputs?"
        % (QY, QX, QY, QX, QY, QX),
        form=["steel", BOX, "&nbsp; apparel", BOX],
        answers=[H("h1.0"), H("h1.1")],
        explain="Verify: 40 + 80 = 120 and 20 + 80 = 100."),
    Question(
        "h2",
        "For which K/E are both outputs non-negative?",
        form=["", BOX, "&le; K/E &le;", BOX],
        answers=[H("h2.0"), H("h2.1")],
        hints=["%s &ge; 0 needs K &ge; E, and %s &ge; 0 needs K &le; 2E." % (QY, QX)],
        explain="Between apparel's ratio and steel's."),
    Question(
        "h3",
        "What is that range called, and what happens outside it?",
        choices=[CONE_NAME, CONE_NAME_FPE, CONE_NAME_PPF, CONE_NAME_NONE],
        answers=[H("h3.c")],
        mistakes=M({
            "h3.c~" + CONE_NAME_FPE: "The range is about which goods are made.",
            "h3.c~" + CONE_NAME_PPF: "It is a range of endowment ratios, not of outputs.",
            "h3.c~" + CONE_NAME_NONE: "At K/E = 2.5, apparel output would be negative.",
        }),
        explain="One sentence on the exam."),
    Question(
        "h4",
        "(c) K rises to 140 with E unchanged. The new outputs?",
        form=["steel", BOX, "&nbsp; apparel", BOX],
        answers=[H("h4.0"), H("h4.1")],
        mistakes=M({"h4.1~80": "Apparel falls: 2(100) &minus; 140."}),
        explain="Verify both constraints again."),
    Question(
        "h5",
        "The four percentage changes, in percent?",
        form=["K&#770;", BOX, "&nbsp; &Ecirc;", BOX, "&nbsp; %s" % QYH, BOX, "&nbsp; %s" % QXH, BOX],
        answers=[H("h5.0"), H("h5.1"), H("h5.2"), H("h5.3")],
        mistakes=M({"h5.0~20": "Divide by the old stock, 120: 20/120."}),
        explain="100 &gt; 16.7 &gt; 0 &gt; &minus;25: Rybczynski."),
    Question(
        "h6",
        "What is held fixed for the result, and why must one output fall?",
        choices=[FIXED, FIXED_E, FIXED_TASTE, FIXED_NONE],
        answers=[H("h6.c")],
        mistakes=M({
            "h6.c~" + FIXED_E: "Rybczynski holds goods prices fixed.",
            "h6.c~" + FIXED_TASTE: "Demand never enters the full-employment conditions.",
            "h6.c~" + FIXED_NONE: "At fixed prices both industries are equally profitable: zero.",
        }),
        explain="Three sentences on the exam."),
    Question(
        "h7",
        "(d) Foreign has the same technology, K* = 110 and E* = 100. Its outputs?",
        form=["steel", BOX, "&nbsp; apparel", BOX],
        answers=[H("h7.0"), H("h7.1")],
        explain="Foreign makes relatively more apparel at the same prices."),
    Question(
        "h8",
        "Which country is capital abundant, and who exports what?",
        choices=[PATTERN, PATTERN_SIZE, PATTERN_F, PATTERN_NONE],
        answers=[H("h8.c")],
        mistakes=M({
            "h8.c~" + PATTERN_SIZE: "Abundance compares ratios, K/E, and the abundant factor's "
                                    "good is exported.",
            "h8.c~" + PATTERN_F: "Compare K/E: 1.1 against 1.2.",
            "h8.c~" + PATTERN_NONE: "Different capital stocks: different autarky prices.",
        }),
        explain="State the ceteris paribus clause explicitly on the exam."),
    Question(
        "h9",
        "(e) Free trade sets %s = 10 and %s = 8 in both countries. The wage and rental in each?"
        % (PY, PX),
        form=["Home w", BOX, "r", BOX, "&nbsp; Foreign w*", BOX, "r*", BOX],
        answers=[H("h9.0"), H("h9.1"), H("h9.2"), H("h9.3")],
        mistakes=M({"h9.2~5": "Foreign has the same technology and faces the same prices."}),
        explain="Factor price equalization: the endowments never entered."),
    Question(
        "h10",
        "How can factor prices be equal when factors cannot cross the border?",
        choices=[MOVING, MOVING_MIGR, MOVING_CAP, MOVING_GOV],
        answers=[H("h10.c")],
        mistakes=M({
            "h10.c~" + MOVING_MIGR: "The model rules factor movements out.",
            "h10.c~" + MOVING_CAP: "Capital stays home too.",
            "h10.c~" + MOVING_GOV: "Nothing but zero profits at common prices.",
        }),
        explain="Four sentences on the exam, saying what does the moving."),
    Question(
        "h11",
        "(f) Duals, and an assumption that would break them.",
        choices=[DUALS, DUALS_SAME, DUALS_TASTES, DUALS_ONLY],
        answers=[H("h11.c")],
        mistakes=M({
            "h11.c~" + DUALS_SAME: "One moves prices, the other endowments.",
            "h11.c~" + DUALS_TASTES: "Neither needs tastes at all.",
            "h11.c~" + DUALS_ONLY: "Heckscher&ndash;Ohlin also needs identical technologies.",
        }),
        explain="Endowments outside the cone or a factor intensity reversal would do it too."),
]

home = GuidedProblem(
    "Part 6 &middot; Home and Foreign: A10.3",
    "The same technology as A10.1, now on the quantity side. Every answer is an integer or a "
    "simple fraction.",
    HOME_QUESTIONS, draw_home, figsize=(8.0, 3.9), whole_figure=True,
    outro="About 25&ndash;30% of an exam paper.",
    sources=[PS("A10.3")],
)


# ======================================================================
# Part 7: the empirical record and the short run
# ======================================================================

def draw_record(fig, stage):
    data, sf = fig.subplots(1, 2)
    for side in ("top", "right"):
        data.spines[side].set_visible(False)
    data.set_title("Capital per person, 1947 ($)", loc="left", color=INK, fontsize=9.5)
    data.set_yticks([])
    data.set_ylim(0, 21000)
    names, values, colours = [], [], []
    if stage >= 1:
        names += ["exports", "imports"]
        values += [13700, 18200]
        colours += [LINE, CURVE]
    if stage >= 2:
        names += ["production", "consumption"]
        values += [6949, 6737]
        colours += [GREEN, GREY]
    xs = np.arange(len(names))
    data.bar(xs, values, color=colours, width=0.6)
    for x, v in zip(xs, values):
        data.text(x, v + 300, "{:,}".format(v), ha="center", color=INK, fontsize=8.5)
    data.set_xticks(xs)
    data.set_xticklabels(names, fontsize=8.5, color=INK)
    if stage >= 2:
        data.axvline(1.5, color=MUTE, lw=0.8, ls=":")
        data.text(0.5, 20000, "Leontief", ha="center", color=MUTE, fontsize=8.5)
        data.text(2.5, 20000, "Leamer", ha="center", color=MUTE, fontsize=8.5)

    _panel(sf, 10, 10, "labor in x  →     ← labor in y", "w", "Specific factors (short run)")
    xs = np.linspace(0.5, 9.5, 100)
    # Calibrated so that a 25% rise in p_x lifts the wage from 5 to 5.625: 12.5%.
    if stage >= 4:
        sf.plot(xs, 8 - 0.6 * xs, color=CURVE, lw=2, label="p$_x$ VMP, industry x")
        sf.plot(xs, 1.25 + 0.75 * xs, color=LINE, lw=2, label="p$_y$ VMP, industry y")
        gp.dot(sf, 5, 5, "A", 6, -12, colour=INK)
    if stage >= 5:
        sf.plot(xs, 1.25 * (8 - 0.6 * xs), color=CURVE, lw=1.4, ls="--", label="p$_x$ up 25%")
        gp.dot(sf, 35 / 6, 5.625, "B", 6, 2, colour=NEW)
    gp.legend(sf, loc="upper center")
    fig.subplots_adjust(wspace=0.25)


PARADOX = "Imports were more capital intensive than exports, though the U.S. was the most capital-abundant country"
PARA_LABOR = "The U.S. turned out to be labor abundant"
PARA_SAME = "Exports and imports used the same capital per worker"
PARA_LAND = "The U.S. imported more land than it exported"

LEAMER = "Production against consumption: production carried $6,949 of capital per person and consumption $6,737, so the U.S. behaves as capital abundant, and unbalanced trade does not upset this comparison"
LEAMER_EX = "Exports against imports again, with better data"
LEAMER_SKILL = "Skilled against unskilled labor"
LEAMER_LAND = "Land against capital"

COIN = "A coin flip would pass half the time, so 61% is barely better than chance; the measured factor content is also far too small (the missing trade)"
COIN_GOOD = "61% is a clear success, since most tests fail more often than that"
COIN_BIG = "The trade it measures is too large, not too small"
COIN_DATA = "The sign test cannot be passed with real data"

FPE_EXTRA = "FPE also needs both countries inside the cone, so both produce both goods; the data most clearly reject identical technologies across countries"
FPE_EXTRA_TASTE = "FPE needs different tastes; the data reject free trade"
FPE_EXTRA_NONE = "FPE needs nothing extra; the data reject constant returns"
FPE_EXTRA_SIZE = "FPE needs equal country size; the data reject homothetic tastes"

SPECIFIC = "The wage rises less than the price that rose, so the worker's real wage falls in one good and rises in the other: it depends on her basket. The specific factor in the rising industry gains and the other loses, so the cleavage is sector against sector, not factor against factor"
SPEC_SS = "Exactly as in Stolper-Samuelson: workers lose in terms of both goods"
SPEC_ALL = "All specific factors gain from any price rise"
SPEC_FPE = "Wages are equalized across countries even in the short run"

RECORD_QUESTIONS = [
    Question(
        "e1",
        "Leontief, 1947: a million dollars of exports used $2.5m of capital and 182 person-years, "
        "imports $3.1m and 170. Why was the result called a paradox?",
        choices=[PARADOX, PARA_LABOR, PARA_SAME, PARA_LAND],
        answers=[H("e1.c")],
        mistakes=M({
            "e1.c~" + PARA_LABOR: "That would have been the conclusion, if the test were right.",
            "e1.c~" + PARA_SAME: "Divide: about 13,700 against 18,200.",
            "e1.c~" + PARA_LAND: "Land was one of the defenses, not the finding.",
        }),
        explain="Be able to reproduce the table from memory."),
    Question(
        "e2",
        "Review question 5: which two ratios did Leamer (1980) say should have been compared?",
        choices=[LEAMER, LEAMER_EX, LEAMER_SKILL, LEAMER_LAND],
        answers=[H("e2.c")],
        mistakes=M({
            "e2.c~" + LEAMER_EX: "Leamer's point was that this comparison is the wrong test.",
            "e2.c~" + LEAMER_SKILL: "That was one of the earlier defenses.",
            "e2.c~" + LEAMER_LAND: "Leamer kept Leontief's two factors.",
        }),
        explain="Four sentences on the exam, numbers included."),
    Question(
        "e3",
        "Worksheet task 4: the HOV sign test passes 61% of the time. Why is that unimpressive?",
        choices=[COIN, COIN_GOOD, COIN_BIG, COIN_DATA],
        answers=[H("e3.c")],
        mistakes=M({
            "e3.c~" + COIN_GOOD: "What would flipping a coin score?",
            "e3.c~" + COIN_BIG: "Trefler: countries trade far less factor content than predicted.",
            "e3.c~" + COIN_DATA: "It can, and does, about half the time by chance.",
        }),
        explain="One productivity parameter per country lifts R&sup2; to 0.486."),
    Question(
        "e4",
        "Review question 1: which extra condition does factor price equalization need, and which "
        "assumption do the data most clearly reject?",
        choices=[FPE_EXTRA, FPE_EXTRA_TASTE, FPE_EXTRA_NONE, FPE_EXTRA_SIZE],
        answers=[H("e4.c")],
        mistakes=M({
            "e4.c~" + FPE_EXTRA_TASTE: "Tastes are identical and homothetic in the model.",
            "e4.c~" + FPE_EXTRA_NONE: "A specialized country breaks the tangency logic.",
            "e4.c~" + FPE_EXTRA_SIZE: "Constant returns make size irrelevant.",
        }),
        explain="Feenstra: HOV performs poorly unless technologies may differ."),
    Question(
        "e5",
        "The short run: capital is stuck in each industry and only labor moves. In the notes' "
        "figure %s rises 25%% and the wage 12.5%%. By how much does the real wage change in terms "
        "of x, and in terms of y, whose price is flat? In percent." % PX,
        form=["w/%s" % PX, BOX, "&nbsp; w/%s" % PY, BOX],
        answers=[H("e5.0"), H("e5.1")],
        mistakes=M({"e5.0~-12.5": "Divide, do not subtract: 1.125/1.25 = 0.9."}),
        hints=["The real wage in x is w/%s: it moves by 1.125/1.25 &minus; 1." % PX],
        explain="%s &gt; %s &gt; %s = 0: no magnification for the mobile factor." % (PXH, WH, PYH)),
    Question(
        "e6",
        "Review question 6: what does the specific-factors model say?",
        choices=[SPECIFIC, SPEC_SS, SPEC_ALL, SPEC_FPE],
        answers=[H("e6.c")],
        mistakes=M({
            "e6.c~" + SPEC_SS: "With more factors than goods the theorem fails: Jones and "
                               "Scheinkman.",
            "e6.c~" + SPEC_ALL: "The specific factor in the other industry loses its workers.",
            "e6.c~" + SPEC_FPE: "Here factor prices depend on endowments.",
        }),
        explain="The same economy at two horizons: capital is specific today and mobile in a "
                "decade."),
]

record = GuidedProblem(
    "Part 7 &middot; The record and the short run",
    "Review questions 1, 5 and 6, and worksheet task 4: what the data say, and what changes "
    "when capital cannot move.",
    RECORD_QUESTIONS, draw_record, figsize=(8.0, 3.8), whole_figure=True,
    outro="Leontief ran the wrong test; the right tests still fail until technologies may differ.",
    sources=[NOTES("p. 13&ndash;17"), NOTES("p. 21&ndash;22, review questions 1, 5, 6")],
)


# ======================================================================
# Part 8: problem A10.2, Nordheim's bicycle tariff (context)
# ======================================================================

def draw_tariff(ax, stage):
    gp.frame(ax, 85, 62, "bicycles", "price")
    ax.plot([0, 60], [0, 60], color=LINE, lw=2, label="supply S = p")
    ps = np.array([2, 60])
    ax.plot(120 - 2 * ps, ps, color=CURVE, lw=2, label="demand D = 120 − 2p")
    ax.axhline(20, color=GREY, lw=1.2, ls="--")
    ax.text(84, 21, "world price 20", color=MUTE, fontsize=8.5, ha="right")
    ticks_x, ticks_y = [], [20]
    if stage >= 1:
        ticks_x += [20, 80]
        for x in (20, 80):
            ax.plot([x, x], [0, 20], color=GREY, lw=0.8, ls=":")
    if stage >= 2:
        ax.axhline(30, color=NEW, lw=1.2, ls="--")
        ax.text(84, 31, "with the tariff", color=NEW, fontsize=8.5, ha="right")
        ticks_x += [30, 60]
        ticks_y += [30]
        for x in (30, 60):
            ax.plot([x, x], [0, 30], color=GREY, lw=0.8, ls=":")
    if stage >= 3:
        ax.fill([0, 20, 30, 0], [20, 20, 30, 30], color=LINE, alpha=0.18, lw=0)
        ax.fill([20, 30, 30], [20, 20, 30], color=NEW, alpha=0.45, lw=0)
        ax.fill([30, 60, 60, 30], [20, 20, 30, 30], color=GREEN, alpha=0.22, lw=0)
        ax.fill([60, 80, 60], [20, 20, 30], color=NEW, alpha=0.45, lw=0)
        for x, name in ((12, "a"), (27, "b"), (45, "c"), (66, "d")):
            ax.text(x, 24.5, name, color=INK, fontsize=10, ha="center", va="center")
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.tick_params(colors=MUTE, labelsize=8.5)
    gp.legend(ax, loc="upper center")


LARGE = "A small country takes the world price as given, so all of the tariff lands on its own consumers. A large country's tariff also lowers the world price, a terms-of-trade gain that can outweigh the triangles"
LARGE_SAME = "Nothing changes: a tariff costs b + d whatever the country's size"
LARGE_FOREIGN = "A small country's tariff is paid by foreign exporters"
LARGE_REVENUE = "A large country collects no revenue"

DWL = "b + d are lost to everybody: producers and the government get a and c back, but nobody gets the two triangles"
DWL_NONE = "There is no loss: the government's revenue covers it"
DWL_C = "The loss is c, the revenue, since consumers pay it"
DWL_ALL = "The loss is a + b + c + d"

TARIFF_QUESTIONS = [
    Question(
        "t1",
        "A10.2 (a): demand D = 120 &minus; 2p and supply S = p, world price 20. Under free trade: "
        "demand, supply and imports?",
        form=["D =", BOX, "&nbsp; S =", BOX, "&nbsp; imports", BOX],
        answers=[H("t1.0"), H("t1.1"), H("t1.2")],
        explain="Imports are demand minus supply."),
    Question(
        "t2",
        "With a tariff of 10 the price is 30. Demand, supply and imports now?",
        form=["D =", BOX, "&nbsp; S =", BOX, "&nbsp; imports", BOX],
        answers=[H("t2.0"), H("t2.1"), H("t2.2")],
        explain="Imports halve."),
    Question(
        "t3",
        "(c) The four areas between the price lines?",
        form=["a", BOX, "&nbsp; b", BOX, "&nbsp; c", BOX, "&nbsp; d", BOX],
        answers=[H("t3.0"), H("t3.1"), H("t3.2"), H("t3.3")],
        mistakes=M({"t3.0~200": "a is a trapezoid: 10 &times; (20 + 30)/2.",
                    "t3.2~600": "Revenue is the tariff times the imports that remain, 30."}),
        explain="They add to 700, the consumers' loss: 10 &times; (80 + 60)/2."),
    Question(
        "t4",
        "(d) The deadweight loss?",
        form=["loss", BOX],
        answers=[H("t4.0")],
        mistakes=M({"t4.0~700": "That is what consumers lose. Producers and the government get "
                                "a and c back."}),
        explain="b + d."),
    Question(
        "t5",
        "Why is it a loss for the country, even though the government and producers gain?",
        choices=[DWL, DWL_NONE, DWL_C, DWL_ALL],
        answers=[H("t5.c")],
        mistakes=M({
            "t5.c~" + DWL_NONE: "Revenue is c only.",
            "t5.c~" + DWL_C: "c is a transfer to the government.",
            "t5.c~" + DWL_ALL: "a and c are transfers.",
        }),
        explain="Production distortion b, consumption distortion d."),
    Question(
        "t6",
        "(e) Why does the small-country assumption matter?",
        choices=[LARGE, LARGE_SAME, LARGE_FOREIGN, LARGE_REVENUE],
        answers=[H("t6.c")],
        mistakes=M({
            "t6.c~" + LARGE_SAME: "A large country moves the world price.",
            "t6.c~" + LARGE_FOREIGN: "Only a large country can push part of it abroad.",
            "t6.c~" + LARGE_REVENUE: "It collects revenue, partly paid by foreigners.",
        }),
        explain="Session 11 takes up the large country."),
]

tariff = GuidedProblem(
    "Part 8 &middot; Nordheim's bicycle tariff: A10.2",
    CTX + "Optional practice, not graded. The small-country tariff diagram from session 9, with "
    "new numbers.",
    TARIFF_QUESTIONS, draw_tariff, figsize=(6.4, 4.6),
    outro="Tariffs are background in this course: no exam question asks for them.",
    sources=[PS("A10.2")],
)


# ======================================================================
# Where every step comes from (printed pages of s10_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "p1": NOTES("p. 8 &middot; Try it (a)"), "p2": NOTES("p. 8 &middot; Try it (a)"),
    "p3": NOTES("p. 8 &middot; Try it (b)"), "p4": NOTES("p. 8 &middot; Try it (b)"),
    "p5": NOTES("p. 8 &middot; Try it (c)"), "p6": NOTES("p. 8 &middot; Try it (c)"),
    "p7": NOTES("p. 7 &middot; magnification"),
    "o1": NOTES("p. 10 &middot; Try it (a)"), "o2": NOTES("p. 10 &middot; Try it (b)"),
    "o3": NOTES("p. 10 &middot; Try it (b)"), "o4": NOTES("p. 10 &middot; Try it (c)"),
    "o5": NOTES("p. 9 &middot; Rybczynski"), "o6": NOTES("p. 11&ndash;12 &middot; the cone"),
    "w1": NOTES("p. 20 &middot; worksheet task 1"), "w2": NOTES("p. 20 &middot; worksheet task 1"),
    "w3": NOTES("p. 21 &middot; worksheet panel"), "w4": NOTES("p. 4 &middot; the cone"),
    "w5": NOTES("p. 20 &middot; worksheet task 1"), "w6": NOTES("p. 20 &middot; worksheet task 1"),
    "w7": NOTES("p. 20 &middot; worksheet task 1"), "w8": NOTES("p. 20 &middot; worksheet task 2"),
    "w9": NOTES("p. 20 &middot; worksheet task 2"), "w10": NOTES("p. 20 &middot; worksheet task 2"),
    "k1": NOTES("p. 21 &middot; review question 2"), "k2": NOTES("p. 21 &middot; review question 2"),
    "k3": NOTES("p. 22 &middot; review question 2"), "k4": NOTES("p. 22 &middot; review question 2"),
    "k5": NOTES("p. 22 &middot; review question 3"), "k6": NOTES("p. 22 &middot; review question 3"),
    "k7": NOTES("p. 22 &middot; review question 3"), "k8": NOTES("p. 22 &middot; review question 3"),
    "k9": NOTES("p. 22 &middot; review question 4"),
    "a1": PS("A10.1 (a)"), "a2": PS("A10.1 (a)"), "a3": PS("A10.1 (b)"), "a4": PS("A10.1 (c)"),
    "a5": PS("A10.1 (d)"), "a6": PS("A10.1 (d)"), "a7": PS("A10.1 (e)"), "a8": PS("A10.1 (e)"),
    "a9": PS("A10.1 (e)"), "a10": PS("A10.1 (f)"), "a11": PS("A10.1 (g)"),
    "h1": PS("A10.3 (a)&ndash;(b)"), "h2": PS("A10.3 (a)"), "h3": PS("A10.3 (a)"),
    "h4": PS("A10.3 (c)"), "h5": PS("A10.3 (c)"), "h6": PS("A10.3 (c)"), "h7": PS("A10.3 (d)"),
    "h8": PS("A10.3 (d)"), "h9": PS("A10.3 (e)"), "h10": PS("A10.3 (e)"), "h11": PS("A10.3 (f)"),
    "e1": NOTES("p. 13 &middot; Leontief"), "e2": NOTES("p. 22 &middot; review question 5"),
    "e3": NOTES("p. 21 &middot; worksheet task 4"), "e4": NOTES("p. 21 &middot; review question 1"),
    "e5": NOTES("p. 16&ndash;17 &middot; specific factors"),
    "e6": NOTES("p. 22 &middot; review question 6"),
    "t1": PS("A10.2 (a)"), "t2": PS("A10.2 (a)"), "t3": PS("A10.2 (c)"), "t4": PS("A10.2 (d)"),
    "t5": PS("A10.2 (d)"), "t6": PS("A10.2 (e)"),
}

for _q in (PRICE_QUESTIONS + OUTPUT_QUESTIONS + SHEET_QUESTIONS + KARELIA_QUESTIONS
           + STEEL_QUESTIONS + HOME_QUESTIONS + RECORD_QUESTIONS + TARIFF_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
