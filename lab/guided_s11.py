"""
guided_s11.py - session 11 guided page: monopolistic competition, gravity and
trade policy.

    Part 1  iit       intra-industry trade: the puzzle and the index (review
                      question 1)
    Part 2  markup    markup pricing and free entry (the first Try it)
    Part 3  ces       constant elasticity: price, markup and firm scale
                      (worksheet task 2, review question 2)
    Part 4  ppzz      the worksheet's PP-ZZ panel: what trade does to the
                      equilibrium
    Part 5  nordia    problem A11.1: Nordia and Sudia
    Part 6  gravity   the gravity equation (the second Try it, A11.2, review
                      question 4, the worksheet's gravity panel)
    Part 7  border    border effects and multilateral resistance (review
                      question 5)
    Part 8  hme       the home-market effect, Helpman's index and Melitz
    Part 9  tariff    the large country, the optimum tariff and who paid in
                      2018 (context: not examinable)

Answers are hashes in answers_s11.py, generated from
answer_keys/s11_keys.py in the private repo. The maths is monopolistic.py:
its self-check reproduces every number asked for here.
"""

import numpy as np

import guided_plots as gp
import monopolistic as mc
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW

H, M = answers("s11")

CTX = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
       "context: not examinable</span> ")
SIG = "&sigma;"
ETA = "&eta;"


# ------------------------------------------------------------------ drawing ---

def _panel(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    # A bare frame with ticks only where a number has been earned.
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.tick_params(colors=MUTE, labelsize=8.5)


def _costs(ax, mcost, F, qmax, **kw):
    # Average cost MC + F/q, falling toward the flat marginal cost.
    qs = np.linspace(qmax * 0.04, qmax, 300)
    kw.setdefault("color", LINE)
    kw.setdefault("lw", 2)
    ax.plot(qs, mcost + F / qs, **kw)


def _bars(ax, names, values, colours, ymax, title, fmt="%s"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    xs = np.arange(len(names))
    ax.bar(xs, values, color=colours, width=0.6)
    for x, v in zip(xs, values):
        if v:
            ax.text(x, v + ymax * 0.02, fmt % v, ha="center", color=INK, fontsize=8.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=8.5, color=INK)
    ax.set_yticks([])
    ax.set_ylim(0, ymax)


# ======================================================================
# Part 1: the intra-industry trade puzzle
# ======================================================================

def draw_iit(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title("Nordmark's trade, by industry", loc="left", color=INK, fontsize=9.5)
    xs = np.arange(2)
    ax.bar(xs - 0.18, [80, 50], width=0.34, color=LINE, label="exports")
    ax.bar(xs + 0.18, [40, 0], width=0.34, color=CURVE, label="imports")
    ax.set_xticks(xs)
    ax.set_xticklabels(["vehicles", "wheat"], fontsize=10, color=INK)
    ax.set_yticks([])
    ax.set_ylim(0, 105)
    if stage >= 1:
        ax.text(0, 92, "IIT = 2/3: two-way", ha="center", color=GREEN, fontsize=10)
        ax.text(1, 62, "IIT = 0: one-way", ha="center", color=MUTE, fontsize=10)
    gp.legend(ax, loc="upper right")


DIFFERENCE = "Both are difference models with constant returns and perfect competition: in each industry a country either exports or imports. This session allows increasing returns internal to the firm"
DIFF_TASTES = "Both assume identical tastes; this session lets tastes differ across countries"
DIFF_FACTORS = "Both have too few factors; this session adds a third one"
DIFF_COSTS = "Both ignore transport costs; this session adds them"

CHAIN = "Increasing returns force imperfect competition, imperfect competition needs differentiated varieties, and varieties generate two-way trade"
CHAIN_REV = "Two-way trade causes differentiation, which causes increasing returns"
CHAIN_PC = "Increasing returns are compatible with perfect competition, so firms price at marginal cost"
CHAIN_GOV = "Trade agreements create varieties, and varieties create scale"

WHERE = "High for machinery, chemicals and vehicles among OECD partners; low for commodity trade between rich and poor countries"
WHERE_POOR = "High for commodity trade between rich and poor countries"
WHERE_ALL = "About the same in every industry"
WHERE_NONE = "Close to zero almost everywhere, as Ricardo predicts"

IIT_QUESTIONS = [
    Question(
        "i1",
        "Review question 1: Nordmark exports vehicles worth 80 and imports vehicles worth 40; it "
        "exports wheat worth 50 and imports none. The index IIT = 1 &minus; |X &minus; M|/(X + M) "
        "for each industry?",
        form=["vehicles", BOX, "&nbsp; wheat", BOX],
        answers=[H("i1.0"), H("i1.1")],
        mistakes=M({"i1.0~1/3": "That is |X &minus; M|/(X + M). The index is one minus it.",
                    "i1.1~1": "Wheat flows one way only."}),
        explain="0 is pure one-way trade, 1 pure two-way trade."),
    Question(
        "i2",
        "Why do Ricardo and Heckscher&ndash;Ohlin both predict IIT = 0 in every industry, and "
        "which assumption does this session break?",
        choices=[DIFFERENCE, DIFF_TASTES, DIFF_FACTORS, DIFF_COSTS],
        answers=[H("i2.c")],
        mistakes=M({
            "i2.c~" + DIFF_TASTES: "Tastes stay identical and homothetic here too.",
            "i2.c~" + DIFF_FACTORS: "The model of this session has one factor, labor.",
            "i2.c~" + DIFF_COSTS: "Trade costs come later, for gravity. They are not the fix.",
        }),
        explain="Two identical countries trade nothing in either model."),
    Question(
        "i3",
        "The session's whole argument in one chain?",
        choices=[CHAIN, CHAIN_REV, CHAIN_PC, CHAIN_GOV],
        answers=[H("i3.c")],
        mistakes=M({
            "i3.c~" + CHAIN_REV: "Start from the technology: falling average cost.",
            "i3.c~" + CHAIN_PC: "Pricing at marginal cost loses the fixed cost.",
            "i3.c~" + CHAIN_GOV: "Varieties come from firms, one each.",
        }),
        explain="One new ingredient, increasing returns, forces the other two."),
    Question(
        "i4",
        "Where is the index high in the data?",
        choices=[WHERE, WHERE_POOR, WHERE_ALL, WHERE_NONE],
        answers=[H("i4.c")],
        mistakes=M({
            "i4.c~" + WHERE_POOR: "That is one-way trade: different countries, different goods.",
            "i4.c~" + WHERE_ALL: "It splits by industry and by partner.",
            "i4.c~" + WHERE_NONE: "Germany sells cars to France and France to Germany.",
        }),
        explain="The split comes back later as a test: gravity works where the index is high."),
]

iit = GuidedProblem(
    "Part 1 &middot; The intra-industry trade puzzle",
    "Most world trade flows between similar countries, in similar goods, in both directions "
    "at once. Ricardo and Heckscher&ndash;Ohlin predict none of it.",
    IIT_QUESTIONS, draw_iit, figsize=(6.0, 4.0),
    outro="Rich, similar countries trade because of variety and scale, not because of "
          "difference.",
    sources=[NOTES("p. 1&ndash;2"), NOTES("p. 26, review question 1")],
)


# ======================================================================
# Part 2: markup pricing and free entry
# ======================================================================

def draw_markup(ax, stage):
    _panel(ax, 420, 16, "output per firm", "price, cost", "One firm's costs",
           xticks=[200] if stage >= 3 else [],
           yticks=[8] + ([10] if stage >= 1 else []) + ([12] if stage >= 2 else []))
    ax.axhline(8, color=CURVE, lw=1.6, label="MC = 8")
    if stage >= 1:
        ax.axhline(10, color=NEW, lw=1.2, ls="--", label="Fjordline's price, 10")
    if stage >= 2:
        ax.axhline(12, color=HALF, lw=1.2, ls=":", label="Nordvik's price, 12")
    if stage >= 3:
        _costs(ax, 8, 400, 420, label="AC = 8 + 400/q")
        gp.dot(ax, 200, 10, "p = AC", 6, 6, colour=GREEN)
    if stage >= 4:
        ax.fill_between([0, 200], 8, 10, color=GREEN, alpha=0.15, lw=0)
        ax.text(100, 8.6, "markup earnings = F", ha="center", color=GREEN, fontsize=9)
    gp.legend(ax, loc="upper right")


AC_ABOVE = "Average cost is above marginal cost at every output, so pricing at marginal cost would lose the fixed cost every period"
AC_DEMAND = "Demand is inelastic, so firms can charge what they like"
AC_COLLUDE = "Firms collude to keep the price up"
AC_TAX = "The government sets a minimum price"

RECONCILE = "Markup revenue exactly covers the fixed cost: entry shifts each firm's demand in until it is tangent to average cost"
REC_SHORT = "They contradict each other, so one of them holds only in the short run"
REC_MONOP = "Only the largest firm has market power; the others earn zero"
REC_COST = "Zero profit means price equals marginal cost, so the market power is not used"

MARKUP_QUESTIONS = [
    Question(
        "m1",
        "Try it: Fjordline sells a kitchenware variety at marginal cost 8 and faces demand "
        "elasticity %s = 5. The markup factor %s/(%s &minus; 1), and the price?" % (ETA, ETA, ETA),
        form=["markup", BOX, "&nbsp; p =", BOX],
        answers=[H("m1.0"), H("m1.1")],
        mistakes=M({"m1.0~4/5": "Upside down: &eta;/(&eta; &minus; 1) = 5/4.",
                    "m1.1~40": "Multiply marginal cost by the markup factor, not by &eta;."}),
        explain="MR = MC: p(1 &minus; 1/&eta;) = MC."),
    Question(
        "m2",
        "(b) Nordvik sells a furniture variety, also at marginal cost 8, and charges 12. Which "
        "elasticity does its variety face?",
        form=["%s =" % ETA, BOX],
        answers=[H("m2.0")],
        mistakes=M({"m2.0~3/2": "That is the markup factor. Solve &eta;/(&eta; &minus; 1) = 3/2."}),
        hints=["The markup factor is 12/8 = 3/2."],
        explain="A higher price over the same cost: less elastic demand, read off a price tag."),
    Question(
        "m3",
        "(c) Free entry: Fjordline's profit is zero at 200 units. The fixed cost?",
        form=["F =", BOX],
        answers=[H("m3.0")],
        mistakes=M({"m3.0~2000": "Only the markup earns money: (p &minus; MC) q.",
                    "m3.0~1600": "Only the markup earns money: (p &minus; MC) q."}),
        explain="F = (10 &minus; 8) &times; 200. Every number here runs both ways."),
    Question(
        "m4",
        "Why must the price be above marginal cost for anyone to produce at all?",
        choices=[AC_ABOVE, AC_DEMAND, AC_COLLUDE, AC_TAX],
        answers=[H("m4.c")],
        mistakes=M({
            "m4.c~" + AC_DEMAND: "Demand is downward sloping, and entry keeps profits at zero.",
            "m4.c~" + AC_COLLUDE: "Each firm prices on its own: MR = MC.",
            "m4.c~" + AC_TAX: "No government in this model.",
        }),
        explain="Increasing returns: one fixed cost, spread over more output."),
    Question(
        "m5",
        "Review question 2(d): every firm has market power, yet every firm earns zero profit. "
        "How?",
        choices=[RECONCILE, REC_SHORT, REC_MONOP, REC_COST],
        answers=[H("m5.c")],
        mistakes=M({
            "m5.c~" + REC_SHORT: "Both hold in the long-run equilibrium at once.",
            "m5.c~" + REC_MONOP: "Symmetric firms: every one has the same market power.",
            "m5.c~" + REC_COST: "Zero profit means price equals average cost.",
        }),
        explain="One sentence on the exam."),
]

markup = GuidedProblem(
    "Part 2 &middot; Markup pricing and free entry",
    "Many firms, each making its own variety, with a fixed cost, a flat marginal cost and free "
    "entry. Two conditions: MR = MC, and p = AC.",
    MARKUP_QUESTIONS, draw_markup, figsize=(6.4, 4.4),
    outro="Monopoly pricing firm by firm, plus a zero-profit entry condition.",
    sources=[NOTES("p. 3&ndash;5")],
)


# ======================================================================
# Part 3: constant elasticity, price, markup and scale
# ======================================================================

def draw_ces(fig, stage):
    mk, ac = fig.subplots(1, 2)
    _panel(mk, 8.4, 3.3, "elasticity " + r"$\sigma$", "markup p/MC", "The markup factor",
           xticks=[2, 3, 5, 6], yticks=[1, 2])
    s = np.linspace(1.4, 8.4, 200)
    mk.plot(s, s / (s - 1), color=LINE, lw=2)
    mk.axhline(1, color=GREY, lw=0.8, ls=":")
    for need, sig in ((1, 6), (2, 2), (4, 3), (5, 5)):
        if stage >= need:
            gp.dot(mk, sig, sig / (sig - 1), "", colour=NEW if sig in (6, 2) else GREEN)

    _panel(ac, 175, 16, "output per firm", "price, cost", "Zero profit: p = AC",
           xticks=([150] if stage >= 1 else []) + ([30] if stage >= 2 else [])
           + ([50] if stage >= 4 else []) + ([100] if stage >= 5 else []))
    if stage >= 1:
        _costs(ac, 5, 150, 175, label="MC 5, F 150")
        ac.axhline(5, color=GREY, lw=0.8, ls=":")
        gp.dot(ac, 150, 6, "", colour=NEW)
    if stage >= 2:
        gp.dot(ac, 30, 10, "", colour=NEW)
    if stage >= 4:
        _costs(ac, 4, 100, 175, color=CURVE, label="MC 4, F 100")
        gp.dot(ac, 50, 6, "", colour=GREEN)
    if stage >= 5:
        gp.dot(ac, 100, 5, "", colour=GREEN)
    gp.legend(ac, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


STANDARDS = "Less elastic demand allows a bigger markup, so fewer units are needed to cover the same fixed cost: higher prices, smaller firms"
STD_SAME = "The price rises but firm output is unchanged"
STD_BIG = "A bigger markup makes firms grow"
STD_MC = "Marginal cost rises with the standard"

CES_QUESTIONS = [
    Question(
        "c1",
        "Worksheet task 2: a variety with %s = 6, MC = 5 and F = 150. The price, the markup "
        "p/MC, and the zero-profit output?" % SIG,
        form=["p =", BOX, "&nbsp; p/MC =", BOX, "&nbsp; q =", BOX],
        answers=[H("c1.0"), H("c1.1"), H("c1.2")],
        mistakes=M({"c1.2~30": "That is the output for &sigma; = 2. Here p &minus; MC = 1."}),
        hints=["p = MC &sigma;/(&sigma; &minus; 1); then p = AC gives q = F/(p &minus; MC)."],
        explain="With many firms the elasticity of substitution is each firm's demand "
                "elasticity."),
    Question(
        "c2",
        "Product standards cut the elasticity to %s = 2. Redo the price and the output." % SIG,
        form=["p =", BOX, "&nbsp; q =", BOX],
        answers=[H("c2.0"), H("c2.1")],
        mistakes=M({"c2.1~150": "The markup is now 5 per unit: 150/5."}),
        explain="The markup doubles the price; the firm needs only 30 units."),
    Question(
        "c3",
        "What did the standards do?",
        choices=[STANDARDS, STD_SAME, STD_BIG, STD_MC],
        answers=[H("c3.c")],
        mistakes=M({
            "c3.c~" + STD_SAME: "q = F/(p &minus; MC): the markup is in the denominator.",
            "c3.c~" + STD_BIG: "150 against 30.",
            "c3.c~" + STD_MC: "Marginal cost stayed at 5.",
        }),
        explain="Closer substitutes do the opposite: lower markups, bigger firms."),
    Question(
        "c4",
        "Review question 2: a firm in Arland with %s = 3, MC = 4 and F = 100. Price, markup and "
        "zero-profit output?" % SIG,
        form=["p =", BOX, "&nbsp; p/MC =", BOX, "&nbsp; q =", BOX],
        answers=[H("c4.0"), H("c4.1"), H("c4.2")],
        mistakes=M({"c4.2~25": "q = F/(p &minus; MC) = 100/2."}),
        explain="Show both derivations on the exam."),
    Question(
        "c5",
        "(c) Deeper integration makes varieties closer substitutes: %s = 5." % SIG,
        form=["p =", BOX, "&nbsp; q =", BOX],
        answers=[H("c5.0"), H("c5.1")],
        explain="A smaller markup, so each firm must sell twice as much to cover F."),
]

ces = GuidedProblem(
    "Part 3 &middot; Constant elasticity: price, markup and scale",
    "With CES preferences the markup is constant, &sigma;/(&sigma; &minus; 1), whatever happens "
    "in the market, and zero profit then pins down firm size.",
    CES_QUESTIONS, draw_ces, figsize=(8.0, 3.9), whole_figure=True,
    outro="Under CES, firm scale responds to &sigma; and the costs, not to market size.",
    sources=[NOTES("p. 7&ndash;8"), NOTES("p. 25, worksheet task 2"),
             NOTES("p. 26, review question 2")],
)


# ======================================================================
# Part 4: the worksheet's PP-ZZ panel
# ======================================================================

def draw_ppzz(ax, stage):
    _panel(ax, 0.56, 3.4, "consumption per variety c", "p/w", "Markup meets entry",
           xticks=[1 / 16, 1 / 8, 1 / 4, 1 / 2], yticks=[1, 2, 3])
    ax.set_xticklabels(["1/16", "1/8", "1/4", "1/2"])
    cs = np.linspace(0.04, 0.56, 300)
    if stage >= 1:
        ax.axhline(2, color=LINE, lw=2, label="PP: p/w = 2")
    if stage >= 2:
        ax.plot(cs, mc.zz(cs, 32, 4, 1), color=CURVE, lw=2, label="ZZ, E = 32")
        for c in (1 / 16, 1 / 8, 1 / 4, 1 / 2):
            ax.plot([c], [mc.zz(c, 32, 4, 1)], "o", color=CURVE, ms=5)
    if stage >= 3:
        gp.dot(ax, 1 / 8, 2, "N = 4", 6, 6, colour=INK)
    if stage >= 4:
        ax.plot(cs, mc.zz(cs, 64, 4, 1), color=NEW, lw=1.6, ls="--", label="ZZ', E = 64")
        gp.dot(ax, 1 / 16, 2, "N = 8", -10, 8, colour=NEW, ha="right")
        gp.arrow(ax, (1 / 8, 2), (1 / 16, 2), colour=NEW)
    gp.legend(ax, loc="upper right")


VARIETY = "Only the variety gain: with a constant markup PP is flat, so the price-wage ratio and firm scale do not move, but consumers buy from twice as many firms"
VAR_PRO = "Only the pro-competitive gain: the markup falls"
VAR_SCALE = "Only the scale gain: each firm grows"
VAR_NONE = "None: each country still has 4 firms"

GENERAL = "PP slopes up: as c falls, demand gets more elastic, the markup and p/w fall, firms move down their AC curves and grow, and with E fixed each country has fewer firms while consumers have more varieties"
GEN_SAME = "Nothing changes from the flat case"
GEN_MORE = "Each country gains firms, since the market is bigger"
GEN_PRICE = "The markup rises, since firms sell abroad"

PPZZ_QUESTIONS = [
    Question(
        "z1",
        "The worksheet's economy: square-root utility, so %s = 2, with fixed labor &alpha; = 4, "
        "marginal labor &beta; = 1 and E = 32. PP is the markup condition p/w = &beta;%s/(%s "
        "&minus; 1). Its height?" % (SIG, SIG, SIG),
        form=["p/w =", BOX],
        answers=[H("z1.0")],
        explain="With a constant markup PP is flat."),
    Question(
        "z2",
        "ZZ is zero profit: p/w = 1 + 4/(Ec) = 1 + 1/(8c). Its height at c = 1/16, 1/8, 1/4 and "
        "1/2?",
        form=["", BOX, ",", BOX, ",", BOX, ",", BOX],
        answers=[H("z2.0"), H("z2.1"), H("z2.2"), H("z2.3")],
        mistakes=M({"z2.0~2": "1 + 1/(8 &times; 1/16) = 1 + 2."}),
        explain="ZZ is the average cost curve, falling toward &beta; = 1."),
    Question(
        "z3",
        "Mark the equilibrium. Its c, and the number of firms N = 1/((&alpha;/E) + &beta;c)?",
        form=["c =", BOX, "&nbsp; N =", BOX],
        answers=[H("z3.0"), H("z3.1")],
        mistakes=M({"z3.1~8": "&alpha;/E = 4/32 = 1/8, plus &beta;c = 1/8: N = 1/(1/4)."}),
        explain="Each firm sells y = Ec = 4 units."),
    Question(
        "z4",
        "Trade with an identical country doubles E to 64. The new c and N?",
        form=["c =", BOX, "&nbsp; N =", BOX],
        answers=[H("z4.0"), H("z4.1")],
        mistakes=M({"z4.1~4": "N counts the integrated market's varieties: 1/(4/64 + 1/16)."}),
        explain="ZZ shifts down and the crossing slides left."),
    Question(
        "z5",
        "How many firms does each country have now, and how much does each firm make?",
        form=["firms per country", BOX, "&nbsp; y =", BOX],
        answers=[H("z5.0"), H("z5.1")],
        mistakes=M({"z5.0~8": "8 varieties in the integrated market, made in two countries."}),
        explain="The same 4 firms each, the same scale: y = Ec = 64/16."),
    Question(
        "z6",
        "Which gain from trade survives in this economy?",
        choices=[VARIETY, VAR_PRO, VAR_SCALE, VAR_NONE],
        answers=[H("z6.c")],
        mistakes=M({
            "z6.c~" + VAR_PRO: "PP is flat at 2 before and after.",
            "z6.c~" + VAR_SCALE: "y = 4 before and after.",
            "z6.c~" + VAR_NONE: "Consumers now buy from 8 firms, not 4.",
        }),
        explain="CES isolates the gain from variety: nothing else moves."),
    Question(
        "z7",
        "In Feenstra's general case PP slopes up. What does trade do there?",
        choices=[GENERAL, GEN_SAME, GEN_MORE, GEN_PRICE],
        answers=[H("z7.c")],
        mistakes=M({
            "z7.c~" + GEN_SAME: "With an upward PP, a lower c means a lower p/w.",
            "z7.c~" + GEN_MORE: "Bigger firms and the same labor force: fewer firms per country.",
            "z7.c~" + GEN_PRICE: "More competitors: more elastic demand, a smaller markup.",
        }),
        explain="Two gains, pro-competitive and variety, and the Canadian puzzle resolved: some "
                "firms exit, the survivors grow."),
]

ppzz = GuidedProblem(
    "Part 4 &middot; The worksheet: markup meets entry",
    "The left panel of the worksheet. Consumption per variety c across, the price-wage ratio "
    "up: PP is markup pricing, ZZ is zero profit.",
    PPZZ_QUESTIONS, draw_ppzz, figsize=(6.4, 4.5),
    outro="Two identical trading countries are one economy with twice the labor force.",
    sources=[NOTES("p. 5&ndash;7"), NOTES("p. 25&ndash;26, worksheet")],
)


# ======================================================================
# Part 5: problem A11.1, Nordia and Sudia
# ======================================================================

def draw_nordia(fig, stage):
    ac, n = fig.subplots(1, 2)
    _panel(ac, 420, 16, "output per firm q", "price, cost", "A representative firm",
           xticks=[100] if stage >= 2 else [], yticks=[6] + ([8] if stage >= 1 else []))
    ac.axhline(6, color=CURVE, lw=1.6, label="MC = 6")
    if stage >= 1:
        ac.axhline(8, color=NEW, lw=1.2, ls="--", label="p = 8")
    if stage >= 2:
        _costs(ac, 6, 200, 420, label="AC = 6 + 200/q")
        gp.dot(ac, 100, 8, "p = AC", 6, 6, colour=GREEN)
    gp.legend(ac, loc="upper right")

    if stage >= 4:
        _bars(n, ["Nordia\nautarky", "integrated\nmarket"], [20, 40], [LINE, GREEN], 50,
              "Varieties a consumer can buy")
        n.bar([1], [20], color=LINE, width=0.6)
        n.text(1, 9, "Nordia's 20", ha="center", color="white", fontsize=8.5)
        n.text(1, 29, "Sudia's 20", ha="center", color="white", fontsize=8.5)
    elif stage >= 3:
        _bars(n, ["Nordia\nautarky", "integrated\nmarket"], [20, 0], [LINE, GREEN], 50,
              "Varieties a consumer can buy")
    else:
        _bars(n, ["Nordia\nautarky", "integrated\nmarket"], [0, 0], [LINE, GREEN], 50,
              "Varieties a consumer can buy")
    fig.subplots_adjust(wspace=0.25)


CONTRAST = "Here the gain is more varieties for each consumer, with no specialization by comparative advantage. Ricardo needs different technologies and Heckscher-Ohlin different endowments, and identical countries have neither, so those models predict no trade"
CON_SAME = "The gain is the same as in Ricardo: each country specializes where it is most productive"
CON_HO = "Heckscher-Ohlin predicts trade here, since factor prices differ"
CON_PRICE = "The gain is a lower price, as in both earlier models"

NORDIA_QUESTIONS = [
    Question(
        "n1",
        "A11.1 (a): %s = 4, MC = 6 and F = 200 in both countries. The price, and the markup "
        "ratio p/MC?" % SIG,
        form=["p =", BOX, "&nbsp; p/MC =", BOX],
        answers=[H("n1.0"), H("n1.1")],
        mistakes=M({"n1.1~3/4": "Upside down: &sigma;/(&sigma; &minus; 1)."}),
        explain="p = 6 &times; 4/3."),
    Question(
        "n2",
        "(b) The output q of a representative firm under free entry?",
        form=["q =", BOX],
        answers=[H("n2.0")],
        mistakes=M({"n2.0~25": "Only the markup, 8 &minus; 6, covers the fixed cost.",
                    "n2.0~33.3": "p = AC means 8 = 6 + 200/q."}),
        explain="8 = 6 + 200/q."),
    Question(
        "n3",
        "(c) Autarky: Nordia's consumers spend 16,000 on the industry. Units bought, and "
        "varieties produced?",
        form=["Q =", BOX, "&nbsp; n =", BOX],
        answers=[H("n3.0"), H("n3.1")],
        mistakes=M({"n3.1~160": "Divide units by output per firm: 2000/100."}),
        explain="One firm per variety."),
    Question(
        "n4",
        "(d) Integration doubles spending to 32,000. The new price, firm scale and number of "
        "varieties?",
        form=["p =", BOX, "&nbsp; q =", BOX, "&nbsp; n =", BOX],
        answers=[H("n4.0"), H("n4.1"), H("n4.2")],
        mistakes=M({"n4.0~4": "The markup is constant: the price stays at 8.",
                    "n4.1~200": "Firm scale is pinned by zero profit, not by the market."}),
        explain="Same price, same scale, twice the varieties for every consumer."),
    Question(
        "n5",
        "(e) Contrast this gain with Ricardo's and Heckscher&ndash;Ohlin's.",
        choices=[CONTRAST, CON_SAME, CON_HO, CON_PRICE],
        answers=[H("n5.c")],
        mistakes=M({
            "n5.c~" + CON_SAME: "Nordia and Sudia are identical: nobody is relatively better.",
            "n5.c~" + CON_HO: "Identical endowments, identical factor prices.",
            "n5.c~" + CON_PRICE: "The price stayed at 8.",
        }),
        explain="Five sentences on the exam."),
]

nordia = GuidedProblem(
    "Part 5 &middot; Nordia and Sudia: A11.1",
    "Two identical countries, one differentiated industry under monopolistic competition, as in "
    "the session.",
    NORDIA_QUESTIONS, draw_nordia, figsize=(8.0, 3.9), whole_figure=True,
    outro="About 20% of an exam paper. Draw the figure if it makes the argument more precise.",
    sources=[PS("A11.1")],
)


# ======================================================================
# Part 6: the gravity equation
# ======================================================================

def draw_gravity(fig, stage):
    line, fac = fig.subplots(1, 2)
    for side in ("top", "right"):
        line.spines[side].set_visible(False)
    line.set_xscale("log", base=2)
    line.set_yscale("log", base=2)
    line.set_xlim(140, 2300)
    line.set_ylim(0.6, 14)
    line.set_xticks([200, 400, 800, 1600])
    line.set_xticklabels(["200", "400", "800", "1600"])
    line.set_yticks([1, 2, 4, 8])
    line.set_yticklabels(["1", "2", "4", "8"])
    line.minorticks_off()
    line.tick_params(colors=MUTE, labelsize=8.5)
    line.set_xlabel("partner GDP (log scale)", color=INK, fontsize=9, loc="right")
    line.set_ylabel("Vestland's exports", color=INK, fontsize=9, loc="top")
    line.set_title("Gravity: draw the line", loc="left", color=INK, fontsize=9.5)
    if stage >= 6:
        g = np.array([150, 2200])
        line.plot(g, g / 200, color=LINE, lw=2, label="exports = GDP/200")
        line.plot([200, 400, 800, 1600], [1, 2, 4, 8], "o", color=LINE, ms=6)
    if stage >= 7:
        gp.dot(line, 400, 8, "Naboria", 6, -4, colour=NEW)
        line.plot([400, 400], [2, 8], color=NEW, lw=1, ls=":")
    gp.legend(line, loc="upper left")

    names, values, colours = [], [], []
    if stage >= 1:
        names, values, colours = ["(a)"], [40], [LINE]
    if stage >= 2:
        names, values, colours = ["(a)", "(b)"], [40, 80], [LINE, LINE]
    if stage >= 3:
        names, values, colours = names + ["actual"], values + [10], colours + [NEW]
    _bars(fac, names, values, colours, 95, "Vinland's exports to Estland")
    fig.subplots_adjust(wspace=0.25)


OFF_LINE = "Something gravity leaves out: Naboria is close, or shares a language or a border, so its trade costs are low relative to everyone else's. GDP enters with a coefficient near 1 because every country spends a fixed share of its income on each variety"
OFF_GDP = "Naboria's GDP must be measured wrongly"
OFF_DIST = "Naboria is far away"
OFF_SIZE = "Gravity only holds for large partners"

GRAVITY_QUESTIONS = [
    Question(
        "g1",
        "Try it: Vinland's GDP is 1,000, Estland's 600 and world GDP 15,000. Frictionless "
        "gravity, X = Y<sub>i</sub>Y<sub>j</sub>/Y<sub>w</sub>: Vinland's exports to Estland?",
        form=["X =", BOX],
        answers=[H("g1.0")],
        mistakes=M({"g1.0~600000": "Divide by world GDP."}),
        explain="Estland buys the share 600/15,000 of everything Vinland makes."),
    Question(
        "g2",
        "(b) A decade on, all three GDPs have doubled. The prediction?",
        form=["X =", BOX],
        answers=[H("g2.0")],
        mistakes=M({"g2.0~160": "World GDP doubles too: the numerator quadruples, the "
                                "denominator doubles."}),
        explain="Gravity is about shares: growing with the world doubles your trade."),
    Question(
        "g3",
        "(c) Actual exports are only 10. Take %s = 3, so trade scales with T<sup>1 &minus; "
        "%s</sup> = T<sup>&minus;2</sup>. The iceberg factor T, and the share of each shipment "
        "that melts?" % (SIG, SIG),
        form=["T =", BOX, "&nbsp; melts", BOX],
        answers=[H("g3.0"), H("g3.1")],
        mistakes=M({"g3.0~4": "T<sup>&minus;2</sup> = 1/4, so T<sup>2</sup> = 4.",
                    "g3.1~2": "A share: ship 2, 1 arrives."}),
        explain="A trade cost read off a trade shortfall: how the border literature works."),
    Question(
        "g4",
        "A11.2: ln X<sub>ij</sub> = k + ln Y<sub>i</sub> + ln Y<sub>j</sub> &minus; ln "
        "d<sub>ij</sub>. By what factor does trade change if (a) j's GDP doubles, or (b) the "
        "distance triples?",
        form=["(a)", BOX, "&nbsp; (b)", BOX],
        answers=[H("g4.0"), H("g4.1")],
        mistakes=M({"g4.1~3": "Distance enters with a minus sign: trade falls.",
                    "g4.1~-3": "A factor: trade becomes 1/3 of what it was."}),
        explain="Unit elasticities: 1% more GDP, 1% more trade."),
    Question(
        "g5",
        "Review question 4: exporter GDP grows by half, importer GDP by a third, and effective "
        "distance doubles. The factor from GDP growth alone, and from all three?",
        form=["GDP alone", BOX, "&nbsp; all three", BOX],
        answers=[H("g5.0"), H("g5.1")],
        mistakes=M({"g5.0~11/6": "Multiply, do not add: (3/2)(4/3).",
                    "g5.1~4": "Divide by the distance factor."}),
        explain="Workshop 2's question 5.7 is the same arithmetic."),
    Question(
        "g6",
        "The worksheet's right panel: Vestland spends the share 500/100,000 = 1/200 of world "
        "spending, so it predicts exports = partner GDP/200. Exports to partners with GDP 200, "
        "400, 800 and 1600?",
        form=["", BOX, ",", BOX, ",", BOX, ",", BOX],
        answers=[H("g6.0"), H("g6.1"), H("g6.2"), H("g6.3")],
        explain="On doubling axes, a slope of one: a straight line."),
    Question(
        "g7",
        "Naboria has GDP 400 and takes exports of 8. The prediction, and how many times the "
        "prediction Naboria actually trades?",
        form=["predicted", BOX, "&nbsp; times", BOX],
        answers=[H("g7.0"), H("g7.1")],
        explain="Well above the line."),
    Question(
        "g8",
        "What pulls a partner off the line, and why is the GDP coefficient near 1?",
        choices=[OFF_LINE, OFF_GDP, OFF_DIST, OFF_SIZE],
        answers=[H("g8.c")],
        mistakes=M({
            "g8.c~" + OFF_GDP: "The other partners sit exactly on the line.",
            "g8.c~" + OFF_DIST: "Far away would pull it below the line.",
            "g8.c~" + OFF_SIZE: "The line holds for every size: shares.",
        }),
        explain="Nearby countries trade too much for their GDP, distant giants too little."),
]

gravity = GuidedProblem(
    "Part 6 &middot; The gravity equation",
    "Each country makes its own varieties and everyone has the same homothetic tastes, so "
    "country j buys the share s<sub>j</sub> of everything country i makes: X<sub>ij</sub> = "
    "Y<sub>i</sub>Y<sub>j</sub>/Y<sub>w</sub>.",
    GRAVITY_QUESTIONS, draw_gravity, figsize=(8.0, 3.9), whole_figure=True,
    outro="Gravity: trade is about size and friction, not comparative advantage.",
    sources=[NOTES("p. 8&ndash;9"), NOTES("p. 11&ndash;13"), PS("A11.2"),
             NOTES("p. 25&ndash;26, worksheet")],
)


# ======================================================================
# Part 7: border effects and multilateral resistance
# ======================================================================

def draw_border(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title("Sales at home (grey) and abroad (purple), % of GDP", loc="left", color=INK,
                 fontsize=9.5)
    names = ["Canada,\nno border", "Canada,\nborder", "U.S.,\nno border", "U.S.,\nborder"]
    home = [10, 55, 90, 95]
    xs = np.arange(4)
    show = [True, stage >= 2, True, stage >= 2]
    ax.bar(xs, [h if s else 0 for h, s in zip(home, show)], color=GREY, width=0.6)
    ax.bar(xs, [100 - h if s else 0 for h, s in zip(home, show)],
           bottom=[h if s else 0 for h, s in zip(home, show)], color=HALF, alpha=0.7, width=0.6)
    for x, h, s in zip(xs, home, show):
        if s:
            ax.text(x, h / 2, "%d" % h, ha="center", va="center", color="white", fontsize=9)
            ax.text(x, h + (100 - h) / 2, "%d" % (100 - h), ha="center", va="center",
                    color="white", fontsize=9)
    if stage >= 3:
        ax.text(0.5, 106, "×11", ha="center", color=NEW, fontsize=12, weight="bold")
        ax.text(2.5, 106, "×19/9", ha="center", color=NEW, fontsize=12, weight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=8.5, color=INK)
    ax.set_yticks([])
    ax.set_ylim(0, 115)


SIZE = "Canada is small: when its exports halve, most of its sales must turn inward, so its home/abroad ratio jumps. The fix is to include exporter and importer fixed effects, which stand in for multilateral resistance"
SIZE_TASTE = "Canadians prefer Canadian goods much more than Americans prefer American ones"
SIZE_TARIFF = "Canada's tariffs are higher than America's"
SIZE_DIST = "Distance matters more in Canada"

RESIST = "What matters is a pair's trade cost relative to both countries' costs with everyone else: the multilateral resistance terms. Leaving them out makes the small country's border look far too large"
RES_DIST = "Distance should enter squared, as in Newton's law"
RES_TARIFF = "Low tariffs prove the border effect is a data error"
RES_GDP = "The GDP coefficients should be larger than 1"

BORDER_QUESTIONS = [
    Question(
        "b1",
        "McCallum's border indicator for province-to-province trade came out at &gamma; = 3.09 "
        "in 1988. Trade between two provinces is how many times that of a comparable "
        "province-state pair? To the nearest whole number.",
        form=["e<sup>3.09</sup> &asymp;", BOX],
        answers=[H("b1.0")],
        mistakes=M({"b1.0~3": "The indicator is in logs: take e to the power 3.09."}),
        explain="Feenstra: nearly unbelievable. By 1993 the number was 15.7."),
    Question(
        "b2",
        "Review question 5: frictionless, Canada sells 10% of its GDP at home and 90% to the U.S.; "
        "the U.S. sells 90% at home and 10% to Canada. The border halves cross-border trade, and "
        "displaced exports are sold at home. The new shares, in percent?",
        form=["Canada home", BOX, "abroad", BOX, "&nbsp; U.S. home", BOX, "abroad", BOX],
        answers=[H("b2.0"), H("b2.1"), H("b2.2"), H("b2.3")],
        mistakes=M({"b2.0~5": "What Canada no longer exports, it sells at home: 10 + 45."}),
        explain="Same friction, very different moves."),
    Question(
        "b3",
        "The measured border effect, (home/abroad) after over (home/abroad) before, for each?",
        form=["Canada", BOX, "&nbsp; U.S.", BOX],
        answers=[H("b3.0"), H("b3.1")],
        mistakes=M({"b3.0~55/45": "Divide by the frictionless ratio, 10/90."}),
        hints=["Canada: (55/45)/(10/90)."],
        explain="11 against about 2: the size asymmetry is in the measurement, not the border."),
    Question(
        "b4",
        "Why does the same true friction produce such different measured effects, and what is the "
        "practical fix?",
        choices=[SIZE, SIZE_TASTE, SIZE_TARIFF, SIZE_DIST],
        answers=[H("b4.c")],
        mistakes=M({
            "b4.c~" + SIZE_TASTE: "The arithmetic used one friction, the same for both.",
            "b4.c~" + SIZE_TARIFF: "The friction halves trade in both directions.",
            "b4.c~" + SIZE_DIST: "No distance appears in the arithmetic.",
        }),
        explain="Fixed effects give a border factor of 4.7; the structural method 5.2 on average."),
    Question(
        "b5",
        "A11.2 (c): trade inside a country is 20 times trade across a low-tariff border. What "
        "does multilateral resistance add to the equation?",
        choices=[RESIST, RES_DIST, RES_TARIFF, RES_GDP],
        answers=[H("b5.c")],
        mistakes=M({
            "b5.c~" + RES_DIST: "The puzzle is about borders, not about distance.",
            "b5.c~" + RES_TARIFF: "Borders matter beyond tariffs: everything T stands for.",
            "b5.c~" + RES_GDP: "They come out close to 1, as theory says.",
        }),
        explain="New Zealand and Australia trade heavily because everywhere else is far from both."),
]

border = GuidedProblem(
    "Part 7 &middot; Borders and multilateral resistance",
    "McCallum's border puzzle, and Anderson and van Wincoop's resolution: borders hit small "
    "countries harder, purely mechanically.",
    BORDER_QUESTIONS, draw_border, figsize=(6.4, 4.4),
    outro="Always include exporter and importer fixed effects in a gravity regression.",
    sources=[NOTES("p. 11&ndash;14"), NOTES("p. 26, review question 5")],
)


# ======================================================================
# Part 8: the home-market effect, Helpman's index and Melitz
# ======================================================================

def draw_hme(ax, stage):
    _panel(ax, 1, 0.56, "country A's share of the region's GDP", "1 − Σ s²",
           "Helpman's size dispersion index",
           xticks=[0.5, 0.9] if stage >= 2 else [], yticks=[0.18, 0.5] if stage >= 2 else [])
    s = np.linspace(0, 1, 200)
    if stage >= 2:
        ax.plot(s, 1 - s ** 2 - (1 - s) ** 2, color=LINE, lw=2)
        gp.dot(ax, 0.5, 0.5, "equal size", 6, 6, colour=GREEN)
        gp.dot(ax, 0.9, 0.18, "9 to 1", 6, 6, colour=NEW)
    else:
        ax.text(0.5, 0.5, "Step 2 draws the index.", transform=ax.transAxes, ha="center",
                va="center", color=MUTE, fontsize=11)


HME = "The larger market attracts more than its share of firms and becomes a net exporter of the differentiated good: N1 grows faster than E1, and N2 falls"
HME_IMPORT = "The larger market becomes a net importer, since its demand is high"
HME_PROP = "Each country gets firms in proportion to its size"
HME_NONE = "Size does not matter for where firms locate"

SIGN = "The rival fixed-variety view predicts the opposite sign, so the test can tell the models apart; gravity fits whenever countries specialize, whatever the reason"
SIGN_FIT = "Gravity fits so well that no further test is needed"
SIGN_SIZE = "The two views predict the same sign but different sizes"
SIGN_DATA = "Only the home-market effect can be measured in trade data"

MELITZ = "Only the most productive firms export, and opening trade shifts market share to them and pushes the least productive out: average productivity rises without any firm changing its technology"
MEL_LEARN = "Firms become more productive by exporting"
MEL_ALL = "Every firm exports once trade opens"
MEL_SAME = "All firms are identical, as in Krugman"

HME_QUESTIONS = [
    Question(
        "h1",
        "Krugman's home-market effect: grow country 1's labor force a little from two identical "
        "countries. What happens?",
        choices=[HME, HME_IMPORT, HME_PROP, HME_NONE],
        answers=[H("h1.c")],
        mistakes=M({
            "h1.c~" + HME_IMPORT: "That is the fixed-variety intuition. With free entry, firms "
                                  "follow the market.",
            "h1.c~" + HME_PROP: "Magnification: more than proportional.",
            "h1.c~" + HME_NONE: "Entry responds to market size.",
        }),
        explain="N&#770;<sub>1</sub> &gt; &Ecirc;<sub>1</sub> &gt; 0 &gt; N&#770;<sub>2</sub>."),
    Question(
        "h2",
        "Helpman: trade relative to GDP is proportional to 1 &minus; &Sigma;s<sub>i</sub>&sup2;. "
        "The index for two equal countries, and for shares 9/10 and 1/10?",
        form=["equal", BOX, "&nbsp; 9 to 1", BOX],
        answers=[H("h2.0"), H("h2.1")],
        mistakes=M({"h2.1~19/100": "1 &minus; 0.81 &minus; 0.01."}),
        explain="Similar-sized countries trade more with each other, holding total size fixed."),
    Question(
        "h3",
        "Davis and Weinstein: where home demand is 10% higher, production is 16% higher. The "
        "implied elasticity of production with respect to demand?",
        form=["", BOX],
        answers=[H("h3.0")],
        mistakes=M({"h3.0~6": "A ratio: 16/10."}),
        explain="Above 1, so net exports rise with home demand: a home-market effect."),
    Question(
        "h4",
        "Why is the home-market effect a better test of the model than gravity's good fit?",
        choices=[SIGN, SIGN_FIT, SIGN_SIZE, SIGN_DATA],
        answers=[H("h4.c")],
        mistakes=M({
            "h4.c~" + SIGN_FIT: "Gravity also holds in Ricardian and Heckscher&ndash;Ohlin "
                                "models with many goods.",
            "h4.c~" + SIGN_SIZE: "They disagree about the sign.",
            "h4.c~" + SIGN_DATA: "Gravity is measured in trade data too.",
        }),
        explain="A good test is one where rival models disagree about the sign, not the size."),
    Question(
        "h5",
        "Background: Melitz. What changes once firms differ in productivity?",
        choices=[MELITZ, MEL_LEARN, MEL_ALL, MEL_SAME],
        answers=[H("h5.c")],
        mistakes=M({
            "h5.c~" + MEL_LEARN: "The causality runs the other way: they export because they "
                                 "are better.",
            "h5.c~" + MEL_ALL: "Exporting has an extra fixed cost: a second, higher cutoff.",
            "h5.c~" + MEL_SAME: "That is the assumption Melitz drops.",
        }),
        explain="About half of Trefler's 17% productivity gain in Canada came from plant "
                "turnover."),
]

hme = GuidedProblem(
    "Part 8 &middot; Testing the model",
    "Gravity fits, but it fits for any model where countries make different goods. Which "
    "predictions belong to this model alone?",
    HME_QUESTIONS, draw_hme, figsize=(6.4, 4.2),
    outro="Melitz is background for your general education, not assessed material.",
    sources=[NOTES("p. 10"), NOTES("p. 14&ndash;16")],
)


# ======================================================================
# Part 9: the large country and the optimum tariff (context)
# ======================================================================

def draw_tariff(ax, stage):
    gp.frame(ax, 105, 105, "imports M", "price")
    ms = np.array([0, 100])
    ax.plot(ms, 100 - ms, color=CURVE, lw=2, label="import demand M(p)")
    ax.plot(ms, ms, color=LINE, lw=2, label="foreign export supply X*(p*)")
    gp.dot(ax, 50, 50, "free trade", 6, -14, colour=INK)
    T = mc.large_tariff(100, 1, 100 / 3)
    if stage >= 1:
        m1, p, ps = T["M1"], T["p"], T["pstar"]
        ax.plot([0, m1], [p, p], color=NEW, lw=1.2, ls="--")
        ax.plot([0, m1], [ps, ps], color=NEW, lw=1.2, ls="--")
        ax.fill([0, m1, m1, 0], [50, 50, p, p], color=NEW, alpha=0.25, lw=0)
        ax.fill([0, m1, m1, 0], [ps, ps, 50, 50], color=GREEN, alpha=0.3, lw=0)
        ax.fill([m1, 50, m1], [p, 50, 50], color="#dc2626", alpha=0.3, lw=0)
        ax.text(m1 / 2, (50 + p) / 2, "paid at home", ha="center", va="center", fontsize=8.5,
                color=INK)
        ax.text(m1 / 2, (ps + 50) / 2, "e: paid abroad", ha="center", va="center", fontsize=8.5,
                color=INK)
        ax.text(m1 + 3, 54, "b + d", color="#dc2626", fontsize=8.5)
    gp.legend(ax, loc="upper center")


SIGN_W = "Whether the terms-of-trade gain e outweighs the deadweight loss b + d: e is first-order and b + d second-order near free trade, so a small tariff helps a large country"
SIGN_REV = "The revenue always outweighs the triangles"
SIGN_TRI = "The triangles always outweigh the revenue, whatever the country's size"
SIGN_DEM = "Only the size of foreign demand"

PASS = "Foreign export prices barely fell, so tariffs passed through almost completely: e was close to zero and the welfare change was just -(b + d)"
PASS_E = "Foreign exporters cut their prices by the tariff: e was the whole revenue"
PASS_GAIN = "The terms of trade improved, as theory predicts for a large country"
PASS_NONE = "Domestic prices did not rise"

DILEMMA = "Each country gains from a tariff whatever the other does, but if both impose one the terms-of-trade effects cancel and both bear the distortions: a Prisoners' Dilemma, which agreements and MFN exist to escape"
DIL_COORD = "A coordination game: both want to match the other's tariff"
DIL_ZERO = "A zero-sum game: one country's gain is the other's loss, so agreements cannot help"
DIL_SMALL = "Small countries gain most from a trade war"

TARIFF_QUESTIONS = [
    Question(
        "t1",
        "Johnson's optimum tariff is t = 1/&epsilon;*, the inverse elasticity of foreign export "
        "supply. Broda, Lim&atilde;o and Weinstein put the inverse at about 2.4 for "
        "differentiated products and 0.5 for homogeneous ones. The optimum ad valorem tariffs, "
        "in percent, and a small country's?",
        form=["differentiated", BOX, "&nbsp; homogeneous", BOX, "&nbsp; small", BOX],
        answers=[H("t1.0"), H("t1.1"), H("t1.2")],
        mistakes=M({"t1.0~2.4": "In percent: 2.4 is 240%.",
                    "t1.2~100": "A small country faces perfectly elastic supply: 1/&infin;."}),
        explain="Assuming, and this carries a lot of weight, that nobody retaliates."),
    Question(
        "t2",
        "The figure: import demand M = 100 &minus; p, foreign supply X* = p*. The tariff splits "
        "the revenue into what home consumers pay and e, what foreigners pay through a lower "
        "world price. Against those, Home loses the triangle b + d. What decides the sign of "
        "&Delta;W = e &minus; (b + d)?",
        choices=[SIGN_W, SIGN_REV, SIGN_TRI, SIGN_DEM],
        answers=[H("t2.c")],
        mistakes=M({
            "t2.c~" + SIGN_REV: "Only part of the revenue, e, comes from abroad.",
            "t2.c~" + SIGN_TRI: "That is the small country, where e = 0.",
            "t2.c~" + SIGN_DEM: "It is foreign supply that matters.",
        }),
        explain="The losses grow with the square of the tariff, so there is an interior optimum."),
    Question(
        "t3",
        "2018: importers paid $23.8bn in duties and the government kept $15.6bn. How much simply "
        "vanished, in $bn?",
        form=["", BOX],
        answers=[H("t3.0")],
        explain="The deadweight loss. Note what is not in the table: a terms-of-trade gain."),
    Question(
        "t4",
        "What did the 2018 passthrough evidence find?",
        choices=[PASS, PASS_E, PASS_GAIN, PASS_NONE],
        answers=[H("t4.c")],
        mistakes=M({
            "t4.c~" + PASS_E: "Unit values, measured before the duty, barely moved.",
            "t4.c~" + PASS_GAIN: "The survey calls the absence of a gain puzzling.",
            "t4.c~" + PASS_NONE: "Treated prices rose by roughly the tariff.",
        }),
        explain="The large country behaved like a small one."),
    Question(
        "t5",
        "Why do trade agreements exist?",
        choices=[DILEMMA, DIL_COORD, DIL_ZERO, DIL_SMALL],
        answers=[H("t5.c")],
        mistakes=M({
            "t5.c~" + DIL_COORD: "Each country wants a tariff whatever the other does.",
            "t5.c~" + DIL_ZERO: "Mutual tariffs destroy world welfare: negative-sum.",
            "t5.c~" + DIL_SMALL: "Small countries trade larger shares of income and lose most.",
        }),
        explain="Session 12 writes this game down as a matrix."),
]

tariff = GuidedProblem(
    "Part 9 &middot; The large country and the optimum tariff",
    CTX + "Tariffs are not on the exam, here or in sessions 9 and 10. The import market of a "
    "country big enough to move the world price.",
    TARIFF_QUESTIONS, draw_tariff, figsize=(6.4, 4.6),
    outro="A tariff is a tax on the technology of market exchange: necessarily welfare-reducing "
          "for a country too small to move world prices.",
    sources=[NOTES("p. 17&ndash;24"), NOTES("p. 26&ndash;27, review question 6")],
)


# ======================================================================
# Where every step comes from (printed pages of s11_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "i1": NOTES("p. 26 &middot; review question 1"), "i2": NOTES("p. 26 &middot; review question 1"),
    "i3": NOTES("p. 2 &middot; the chain"), "i4": NOTES("p. 2 &middot; the index"),
    "m1": NOTES("p. 5 &middot; Try it (a)"), "m2": NOTES("p. 5 &middot; Try it (b)"),
    "m3": NOTES("p. 5 &middot; Try it (c)"), "m4": NOTES("p. 4 &middot; cost curves"),
    "m5": NOTES("p. 26 &middot; review question 2(d)"),
    "c1": NOTES("p. 25 &middot; worksheet task 2"), "c2": NOTES("p. 25 &middot; worksheet task 2"),
    "c3": NOTES("p. 25 &middot; worksheet task 2"), "c4": NOTES("p. 26 &middot; review question 2"),
    "c5": NOTES("p. 26 &middot; review question 2(c)"),
    "z1": NOTES("p. 26 &middot; worksheet panel"), "z2": NOTES("p. 26 &middot; worksheet panel"),
    "z3": NOTES("p. 26 &middot; worksheet panel"), "z4": NOTES("p. 26 &middot; worksheet panel"),
    "z5": NOTES("p. 26 &middot; worksheet panel"), "z6": NOTES("p. 8 &middot; CES"),
    "z7": NOTES("p. 6 &middot; what trade does"),
    "n1": PS("A11.1 (a)"), "n2": PS("A11.1 (b)"), "n3": PS("A11.1 (c)"), "n4": PS("A11.1 (d)"),
    "n5": PS("A11.1 (e)"),
    "g1": NOTES("p. 13 &middot; Try it (a)"), "g2": NOTES("p. 13 &middot; Try it (b)"),
    "g3": NOTES("p. 13 &middot; Try it (c)"), "g4": PS("A11.2 (a)&ndash;(b)"),
    "g5": NOTES("p. 26 &middot; review question 4"), "g6": NOTES("p. 26 &middot; worksheet panel"),
    "g7": NOTES("p. 26 &middot; worksheet panel"), "g8": NOTES("p. 9 &middot; reading the line"),
    "b1": NOTES("p. 12 &middot; McCallum"), "b2": NOTES("p. 26 &middot; review question 5"),
    "b3": NOTES("p. 26 &middot; review question 5"), "b4": NOTES("p. 26 &middot; review question 5"),
    "b5": PS("A11.2 (c)"),
    "h1": NOTES("p. 15 &middot; home-market effect"), "h2": NOTES("p. 10 &middot; Helpman"),
    "h3": NOTES("p. 15 &middot; Davis and Weinstein"), "h4": NOTES("p. 15 &middot; the test"),
    "h5": NOTES("p. 15&ndash;16 &middot; Melitz"),
    "t1": NOTES("p. 19 &middot; Johnson's formula"), "t2": NOTES("p. 18 &middot; the import market"),
    "t3": NOTES("p. 24 &middot; who paid"), "t4": NOTES("p. 23 &middot; passthrough"),
    "t5": NOTES("p. 19&ndash;20 &middot; Prisoners' Dilemma"),
}

for _q in (IIT_QUESTIONS + MARKUP_QUESTIONS + CES_QUESTIONS + PPZZ_QUESTIONS + NORDIA_QUESTIONS
           + GRAVITY_QUESTIONS + BORDER_QUESTIONS + HME_QUESTIONS + TARIFF_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
