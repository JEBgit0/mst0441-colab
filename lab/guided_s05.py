"""
guided_s05.py - session 5 guided page: assets and choice under uncertainty.

    Part 1  prices     what a stream of payments is worth (context)
    Part 2  attitudes  risk aversion, certainty equivalent, risk premium
    Part 3  worksheet  fair insurance and the lottery premium
    Part 4  ingrid     problem A5.2: fair and loaded insurance
    Part 5  car        problem A5.1: car theft with logarithmic utility
    Part 6  capm       portfolios and the market line (context)

Parts 1 and 6 are marked as context: the notes' exam scope (9 September 2026)
makes asset pricing and portfolios non-examinable.

Answers are hashes in answers_s05.py, generated from
answer_keys/s05_keys.py in the private repo.
"""

import numpy as np

import uncertainty as un
from guided import BOX, GuidedProblem, Question, tag
from guided_s03 import (CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW, _dot, _frame,
                        _legend)
from guided_s04 import _arrow

try:
    from answers_s05 import HASHES
except ImportError:
    HASHES = {}

PS = lambda part: tag("problem", "Problem " + part)
NOTES = lambda where: tag("notes", "Notes " + where)
CTX = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
       "context: not on the session 5 exam rubric</span> ")
CG, CB = "c<sub>good</sub>", "c<sub>bad</sub>"


def H(key):
    return HASHES.get(key, "missing:" + key)


def M(messages):
    return {H(k): v for k, v in messages.items()}


def _certainty(ax, top):
    ax.plot([0, top], [0, top], color=MUTE, lw=1, ls="--", label="certainty line")


def _contingent_frame(ax, top, scale=""):
    _frame(ax, top, top, "c_bad" + scale, "c_good" + scale)


def _ins_line(ax, W, D, q, Kmax, **kw):
    # From the endowment (K = 0) to K = Kmax, in (c_bad, c_good).
    g0, b0 = un.states(W, D, q, 0)
    g1, b1 = un.states(W, D, q, Kmax)
    ax.plot([b0, b1], [g0, g1], **kw)


def _eu_curve(ax, v, pi, level, top, **kw):
    # (1 - pi) v(cg) + pi v(cb) = level, solved for cg along a grid of cb.
    cbs = np.linspace(top * 0.01, top, 300)
    cgs = []
    for cb in cbs:
        rest = (level - pi * v(cb)) / (1 - pi)
        try:
            cgs.append(v.inverse(rest))
        except (ValueError, OverflowError):
            cgs.append(np.nan)
    ax.plot(cbs, cgs, **kw)


def _vcurve(ax, v, top, **kw):
    cs = np.linspace(0.01, top, 300)
    ax.plot(cs, [v(c) for c in cs], **kw)


# ======================================================================
# Part 1: what a stream of payments is worth (context)
# ======================================================================

def draw_prices(fig, stage):
    tl, pc = fig.subplots(1, 2)
    _frame(tl, 11, 470, "year t", "PV of the payment")
    tl.set_title("The bond, payment by payment", loc="left", color=INK, fontsize=10)
    if stage >= 1:
        ts = np.arange(1, 11)
        tl.bar(ts, 100 / 1.1 ** ts, color=LINE, alpha=0.75, label="coupons")
        tl.bar([10], [1000 / 1.1 ** 10], bottom=[100 / 1.1 ** 10], color=HALF, alpha=0.75,
               label="face value")
        _legend(tl)
    if stage >= 2:
        tl.text(0.03, 0.9, "drop the coupons:\nonly the purple bar is left",
                transform=tl.transAxes, color=HALF, fontsize=9)

    _frame(pc, 0.115, 55, "interest rate r", "price per krone a year,  1/r")
    pc.set_title("A perpetuity: PV = x/r", loc="left", color=INK, fontsize=10)
    if stage >= 3:
        rs = np.linspace(0.018, 0.115, 200)
        pc.plot(rs, 1 / rs, color=CURVE, lw=2)
        _dot(pc, 0.10, 10, "bond, 10%", 6, 4)
    if stage >= 4:
        _dot(pc, 0.05, 20, "house, 5%", 6, 4, colour=LINE)
        _dot(pc, 0.025, 40, "house, 2.5%", 6, 4, colour=LINE)
    if stage >= 5:
        _dot(pc, 0.02, 50, "market: rent/price", 6, -2, colour=GREEN)
    if stage >= 7:
        _dot(pc, 0.04, 25, "cabin 4%", 6, 4, colour=NEW)
        _dot(pc, 0.06, 1 / 0.06, "cabin 6%", 6, 4, colour=NEW)
        _arrow(pc, (0.04, 25), (0.06, 1 / 0.06), NEW)
    fig.subplots_adjust(wspace=0.3)


PRICES_QUESTIONS = [
    Question(
        "w1",
        "A bond: maturity 10 years, coupon 100 a year, face value 1000, interest rate "
        "10%. What is its present value? (Round to the krone.)",
        form=["PV =", BOX],
        answers=[H("w1.0")],
        mistakes=M({"w1.0~2000": "Every payment must be discounted, once per year it is away.",
                    "w1.0~1100": "Discount the coupons and the face value."}),
        hints=["Sum x/(1 + r)<sup>t</sup> over the ten years, plus F/(1 + r)<sup>10</sup>."],
        explain="The coupon rate equals the yield, so the bond trades at par."),
    Question(
        "w2",
        "Now drop the coupons. What is the bond worth?",
        form=["PV =", BOX],
        answers=[H("w2.0")],
        mistakes=M({"w2.0~1000": "The face value arrives in ten years. Discount it."}),
        explain="About 386: the coupons were worth the other 614."),
    Question(
        "w3",
        "A third bond pays 100 a year forever and never repays. At 10%, what is it worth?",
        form=["PV =", BOX],
        answers=[H("w3.0")],
        mistakes=M({"w3.0~10": "Upside down: PV = x/r.",
                    "w3.0~1100": "No face value ever arrives."}),
        hints=["Pull one factor of 1 + r out of the sum: PV = (x + PV)/(1 + r)."],
        explain="PV = x/r. Giving up the face value buys the coupons from year 11 on: "
                "at 10% they are worth exactly the same."),
    Question(
        "w4",
        "A house rents for NOK 200,000 a year forever, with no repairs. Value it at 5% "
        "and at 2.5%, in NOK million.",
        form=["at 5%:", BOX, "&nbsp; at 2.5%:", BOX],
        answers=[H("w4.0"), H("w4.1")],
        mistakes=M({"w4.0~4000000": "In NOK million: 4,000,000 is 4.",
                    "w4.1~2": "Halving the rate doubles the price."}),
        explain="Housing markets hang on every central bank meeting."),
    Question(
        "w5",
        "An identical house just sold for NOK 10 million. What discount rate is the "
        "market using, in percent?",
        form=["r =", BOX, "%"],
        answers=[H("w5.0")],
        mistakes=M({"w5.0~50": "Upside down: r = rent/price.",
                    "w5.0~5": "Run the formula backwards: r = x/PV."}),
        explain="Rent over price reads the discount rate out of housing data."),
    Question(
        "w6",
        "Repairs actually cost NOK 50,000 a year. At 2.5%, what is the house worth "
        "(NOK million)?",
        form=["PV =", BOX],
        answers=[H("w6.0")],
        mistakes=M({"w6.0~8": "Costs come off the stream before you capitalize it.",
                    "w6.0~2": "That values the repairs. Value what is left after them."}),
        explain="Only the net stream is yours."),
    Question(
        "w7",
        "Worksheet task 1: a cabin rents for a fixed 120 a year forever. Value it at 4% "
        "and at 6%, and give the owner's capital loss.",
        form=["at 4%:", BOX, "&nbsp; at 6%:", BOX, "&nbsp; loss:", BOX],
        answers=[H("w7.0"), H("w7.1"), H("w7.2")],
        mistakes=M({"w7.2~-1000": "Give the loss as a positive number."}),
        explain="Rate up, price down: long payment streams are very sensitive to r."),
]

prices = GuidedProblem(
    "Part 1 &middot; What a stream of payments is worth",
    CTX + "Bonds, perpetuities and a house: session 4's discounting, payment by "
    "payment. The worksheet's first task is here too.",
    PRICES_QUESTIONS, draw_prices, figsize=(7.6, 4.0), whole_figure=True,
    outro="Price down means yield up: an arithmetic fact about fixed streams.",
    sources=[NOTES("p. 2&ndash;4"), NOTES("p. 18, worksheet")],
)


# ======================================================================
# Part 2: risk attitudes (Try it: 100 or 400, fifty-fifty)
# ======================================================================

def draw_attitudes(ax, stage):
    A = un.V("sqrt")
    _frame(ax, 520, 24, "wealth c", "v(c)")
    _vcurve(ax, A, 520, color=CURVE, lw=2, label=r"$v(c) = \sqrt{c}$")
    if stage >= 1:
        ax.plot([100, 400], [10, 20], color=LINE, lw=1.4, label="gamble one")
        _dot(ax, 100, 10, "100", -8, 6, colour=LINE, ha="right")
        _dot(ax, 400, 20, "400", -8, 6, colour=LINE, ha="right")
        ax.axvline(250, color=MUTE, lw=0.8, ls=":")
        ax.text(255, 1, "EV", color=MUTE, fontsize=9)
    if stage >= 2:
        _dot(ax, 250, 15, "EU", 6, -14, colour=LINE)
        _dot(ax, 250, 250 ** 0.5, "v(EV)", -6, 6, colour=CURVE, ha="right")
    if stage >= 4:
        ax.plot([0, 225], [15, 15], color=GREEN, lw=1, ls="--")
        _dot(ax, 225, 15, "CE", -6, 6, colour=GREEN, ha="right")
        ax.annotate("", xy=(225, 13.2), xytext=(250, 13.2),
                    arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2))
        ax.text(237, 11.6, "premium", color=GREEN, fontsize=8.5, ha="center")
    if stage >= 5:
        ax.plot([16, 484], [4, 22], color=NEW, lw=1.4, ls="--", label="gamble two")
        _dot(ax, 16, 4, "", colour=NEW)
        _dot(ax, 484, 22, "", colour=NEW)
        _dot(ax, 169, 13, "CE two", -6, 6, colour=NEW, ha="right")
    _legend(ax, loc="lower right")


A_PAYS = "Only A, with v = sqrt(c)"
B_PAYS = "Only B, with v = c"
C_PAYS = "Only C, with v = c^2"
ALL_PAY = "All three"
C_ONLY = "Only C"
A_ONLY = "Only A"
B_ONLY = "Only B"
NONE_TWO = "Nobody: the mean is the same"

ATTITUDE_QUESTIONS = [
    Question(
        "x1",
        "Gamble one pays a wealth of 100 or 400 (thousand kroner), each with probability "
        "1/2. What is its expected value?",
        form=["EV =", BOX],
        answers=[H("x1.0")],
        mistakes=M({"x1.0~500": "Weight each outcome by its probability."}),
        explain="The average outcome."),
    Question(
        "x2",
        "Person A has v(c) = &radic;c. What is A's expected utility of the gamble?",
        form=["EU =", BOX],
        answers=[H("x2.0")],
        mistakes=M({"x2.0~15.81": "That is the utility of the average, v(EV). Average the "
                                  "utilities instead."}),
        hints=["EU = &frac12;v(100) + &frac12;v(400)."],
        explain="The average of the utilities, which lies on the chord."),
    Question(
        "x3",
        "B has v(c) = c and C has v(c) = c&sup2;. Who would pay to avoid the gamble?",
        choices=[A_PAYS, B_PAYS, C_PAYS, ALL_PAY],
        answers=[H("x3.c")],
        mistakes=M({
            "x3.c~" + B_PAYS: "For B, EU is just the EV: is B better or worse off?",
            "x3.c~" + C_PAYS: "C's EU is 85,000 against v(250) = 62,500. Does C want "
                              "the gamble or the sure mean?",
            "x3.c~" + ALL_PAY: "Compare EU with v(EV) for each one.",
        }),
        explain="Risk aversion is concavity: v'' &lt; 0. A positive v' only says more "
                "is better."),
    Question(
        "x4",
        "For A, find the certainty equivalent (the sure wealth with the same utility) and "
        "the risk premium.",
        form=["CE =", BOX, "&nbsp; premium =", BOX],
        answers=[H("x4.0"), H("x4.1")],
        mistakes=M({"x4.0~15": "That is a utility. Which wealth gives a utility of 15?",
                    "x4.1~225": "The premium is EV &minus; CE."}),
        explain="A would hand over 25,000 kroner just to make the risk go away."),
    Question(
        "x5",
        "Gamble two pays 16 or 484, fifty-fifty: the same mean, a wider spread. A's "
        "certainty equivalent and risk premium?",
        form=["CE =", BOX, "&nbsp; premium =", BOX],
        answers=[H("x5.0"), H("x5.1")],
        mistakes=M({"x5.0~13": "That is A's expected utility. Turn it into wealth.",
                    "x5.1~25": "That is gamble one's premium."}),
        explain="Same average, much scarier gamble."),
    Question(
        "x6",
        "Who prefers gamble two to gamble one?",
        choices=[C_ONLY, A_ONLY, B_ONLY, NONE_TWO],
        answers=[H("x6.c")],
        mistakes=M({
            "x6.c~" + A_ONLY: "A's certainty equivalent fell from 225 to 169.",
            "x6.c~" + B_ONLY: "B only cares about the mean, which did not change.",
            "x6.c~" + NONE_TWO: "The mean is the same, but one of them likes spread.",
        }),
        explain="A mean-preserving spread sorts people purely by curvature."),
]

attitudes = GuidedProblem(
    "Part 2 &middot; Risk attitudes",
    "The notes' Try it, which carries the whole theory of risk attitudes. Three people "
    "face the same gamble: (A) v = &radic;c, (B) v = c, (C) v = c&sup2;. The figure "
    "follows A.",
    ATTITUDE_QUESTIONS, draw_attitudes, figsize=(6.4, 4.6),
    outro="Compare v(EV) with EU: that one inequality decides the attitude to risk.",
    sources=[NOTES("p. 8&ndash;9")],
)


# ======================================================================
# Part 3: the worksheet (W = 100, D = 50, pi = q = 1/5; lottery 4 or 16)
# ======================================================================

def draw_worksheet(fig, stage):
    ins, lot = fig.subplots(1, 2)
    _contingent_frame(ins, 115)
    ins.set_title("Insurance", loc="left", color=INK, fontsize=10)
    _certainty(ins, 115)
    if stage >= 1:
        _dot(ins, 50, 100, "e = (50, 100)", 6, 4, colour=LINE)
    if stage >= 2:
        _ins_line(ins, 100, 50, 0.2, 60, color=LINE, lw=2, label="budget, fair q")
    if stage >= 3:
        _dot(ins, 90, 90, "(90, 90)", 6, -14, colour=CURVE)
        _arrow(ins, (50, 100), (90, 90), CURVE)
        v = un.V("sqrt")
        _eu_curve(ins, v, 0.2, v(90), 115, color=CURVE, lw=1.4)
    _legend(ins, loc="lower right")

    v = un.V("sqrt")
    _frame(lot, 18, 4.6, "wealth c", "v(c)")
    lot.set_title(r"Risk premium, $v = \sqrt{c}$", loc="left", color=INK, fontsize=10)
    _vcurve(lot, v, 18, color=CURVE, lw=2)
    _dot(lot, 4, 2, "4", -6, 6, colour=LINE, ha="right")
    _dot(lot, 16, 4, "16", -6, 6, colour=LINE, ha="right")
    if stage >= 5:
        lot.plot([4, 16], [2, 4], color=LINE, lw=1.4)
        _dot(lot, 10, 3, "EU at c = 10", 6, -14, colour=LINE)
    if stage >= 6:
        lot.plot([0, 9], [3, 3], color=GREEN, lw=1, ls="--")
        _dot(lot, 9, 3, "CE", -6, 6, colour=GREEN, ha="right")
        lot.annotate("", xy=(9, 2.6), xytext=(10, 2.6),
                     arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2))
        lot.text(9.5, 2.3, "premium", color=GREEN, fontsize=8.5, ha="center")
    fig.subplots_adjust(wspace=0.28)


CERT = "Certainty: 90 in both states, the gamble's own mean"
PROFIT = "A profit for the insurer"
MOREW = "More expected wealth"
NOTHING = "Nothing: she pays 10 for an expected payout of 10"

WORKSHEET_QUESTIONS = [
    Question(
        "y1",
        "Worksheet task 2: wealth W = 100, damage D = 50 with probability &pi; = 1/5. "
        "Where is the endowment (no insurance) in the (%s, %s) diagram?" % (CB, CG),
        form=["%s =" % CB, BOX, "&nbsp; %s =" % CG, BOX],
        answers=[H("y1.0"), H("y1.1")],
        mistakes=M({"y1.0~100": "%s goes across: wealth in the bad state." % CB}),
        explain="High up and to the left: plenty if all goes well, little if not."),
    Question(
        "y2",
        "Coverage K costs qK in both states and pays K in the bad one. With the fair "
        "premium q = &pi;, what is the slope of the budget line, d%s/d%s?" % (CG, CB),
        form=["slope =", BOX],
        answers=[H("y2.0")],
        mistakes=M({"y2.0~-1/5": "That is &minus;q. Write both states in K and eliminate K.",
                    "y2.0~1/4": "Right size, wrong sign.",
                    "y2.0~-4": "Upside down."}),
        hints=["%s = W &minus; qK and %s = W &minus; D + (1 &minus; q)K." % (CG, CB)],
        explain="&minus;q/(1 &minus; q): insurance is a price for wealth in the state "
                "where you are poor."),
    Question(
        "y3",
        "Task 3: with strictly concave utility and q = &pi;, what coverage does she "
        "choose, and what is her wealth then?",
        form=["K* =", BOX, "&nbsp; wealth =", BOX],
        answers=[H("y3.0"), H("y3.1")],
        mistakes=M({"y3.0~40": "Fair pricing gives equal marginal utilities, so equal "
                               "wealth in both states.",
                    "y3.1~100": "She pays the premium in the good state too."}),
        hints=["The FOC at q = &pi; gives v'(%s) = v'(%s)." % (CG, CB)],
        explain="Full insurance, on the certainty line."),
    Question(
        "y4",
        "What does the premium of 10 actually buy?",
        choices=[CERT, PROFIT, MOREW, NOTHING],
        answers=[H("y4.c")],
        mistakes=M({
            "y4.c~" + PROFIT: "At a fair price the insurer's expected profit is zero.",
            "y4.c~" + MOREW: "Expected wealth is 90 with or without insurance.",
            "y4.c~" + NOTHING: "Same expected wealth, but compare the risk.",
        }),
        explain="Fair insurance turns a gamble into its own mean."),
    Question(
        "y5",
        "Task 4: a lottery pays 4 or 16 with equal probability, v(c) = &radic;c. "
        "Expected value and expected utility?",
        form=["EV =", BOX, "&nbsp; EU =", BOX],
        answers=[H("y5.0"), H("y5.1")],
        mistakes=M({"y5.1~10": "That is the expected value. Average the utilities.",
                    "y5.1~3.16": "That is v(EV). Average the utilities instead."}),
        explain="The chord's height at c = 10."),
    Question(
        "y6",
        "Certainty equivalent and risk premium?",
        form=["CE =", BOX, "&nbsp; premium =", BOX],
        answers=[H("y6.0"), H("y6.1")],
        mistakes=M({"y6.0~3": "That is utility. Which wealth gives v = 3?"}),
        explain="She would give up 1 to get rid of the risk."),
]

worksheet = GuidedProblem(
    "Part 3 &middot; The worksheet",
    "The notes' worksheet: an insurance problem on the left, a risk premium on the right.",
    WORKSHEET_QUESTIONS, draw_worksheet, figsize=(7.6, 4.0), whole_figure=True,
    outro="Bring the sheet: we go through it in class.",
    sources=[NOTES("p. 18&ndash;19, worksheet")],
)


# ======================================================================
# Part 4: problem A5.2, Ingrid insures a boat
# ======================================================================

def draw_ingrid(ax, stage):
    v = un.V("sqrt")
    _contingent_frame(ax, 125)
    _certainty(ax, 125)
    if stage >= 1:
        _dot(ax, 36, 100, "e", 6, 4, colour=LINE)
    if stage >= 2:
        _ins_line(ax, 100, 64, 0.25, 64, color=LINE, lw=2, label="fair, q = 1/4",
                  alpha=1 if stage < 5 else 0.45)
    if stage >= 3:
        _dot(ax, 84, 84, "(84, 84)", 6, -14, colour=CURVE)
        _eu_curve(ax, v, 0.25, v(84), 125, color=CURVE, lw=1.4)
    if stage >= 4:
        _eu_curve(ax, v, 0.25, 9, 125, color=GREY, lw=1.2, ls=":")
        ax.text(103, 64, "EU = 9:\nthe curve\nthrough e", color=GREY, fontsize=9)
    if stage >= 5:
        _ins_line(ax, 100, 64, 1 / 3, 64, color=NEW, lw=2, ls="--", label="loaded, q = 1/3")
    if stage >= 7:
        k = un.optimal_coverage(v, 100, 64, 0.25, 1 / 3)
        g, b = un.states(100, 64, 1 / 3, k)
        _dot(ax, b, g, "partial cover", 6, 6, colour=NEW)
    _legend(ax, loc="lower right")


ABOVE = "Above the certainty line: she keeps some risk"
ON = "On the certainty line: full cover"
BELOW = "Below: she over-insures"
AT_E = "At the endowment: no cover at all"
K0 = "K = 0: no cover"
KD = "K = D: full cover"
KANY = "Any K: she is indifferent"
KHALF = "Half cover"

INGRID_QUESTIONS = [
    Question(
        "z1",
        "Ingrid has W = 100 (thousand kroner). With probability 1/4 her boat is damaged "
        "and she loses 64. Where is her endowment?",
        form=["%s =" % CB, BOX, "&nbsp; %s =" % CG, BOX],
        answers=[H("z1.0"), H("z1.1")],
        mistakes=M({"z1.0~64": "That is the loss. What is left after it?"}),
        explain="A point on the certainty line means the same wealth whatever happens."),
    Question(
        "z2",
        "Insurance is actuarially fair, q = &pi;. What is the slope of her budget line?",
        form=["slope =", BOX],
        answers=[H("z2.0")],
        mistakes=M({"z2.0~-1/4": "That is &minus;&pi;. The slope is &minus;&pi;/(1 &minus; &pi;)."}),
        explain="The line through (36, 100): %s = 112 &minus; %s/3." % (CG, CB)),
    Question(
        "z3",
        "Her optimal coverage, and her wealth there?",
        form=["K* =", BOX, "&nbsp; wealth =", BOX],
        answers=[H("z3.0"), H("z3.1")],
        mistakes=M({"z3.1~100": "She pays the premium qK in the good state too.",
                    "z3.1~36": "With full cover the bad state is topped up."}),
        explain="84 is exactly her expected wealth: fair insurance converts the gamble "
                "into its mean."),
    Question(
        "z4",
        "At the endowment: her expected utility, its certainty equivalent, and the risk "
        "premium?",
        form=["EU =", BOX, "&nbsp; CE =", BOX, "&nbsp; premium =", BOX],
        answers=[H("z4.0"), H("z4.1"), H("z4.2")],
        mistakes=M({"z4.0~84": "That is expected wealth. Average &radic; of wealth.",
                    "z4.2~19": "The premium is E[c] &minus; CE, with E[c] = 84."}),
        explain="Full insurance gives 84 for sure, more than the 81 the endowment is "
                "worth to her."),
    Question(
        "z5",
        "(e) The insurer charges q = 1/3 &gt; &pi;. What is the new slope?",
        form=["slope =", BOX],
        answers=[H("z5.0")],
        mistakes=M({"z5.0~-1/3": "That is the fair slope. Use &minus;q/(1 &minus; q)."}),
        explain="Steeper, and still through the endowment: buying nothing costs nothing."),
    Question(
        "z6",
        "From the first-order condition, v'(%s)/v'(%s) = q(1 &minus; &pi;)/((1 &minus; q)&pi;). "
        "Evaluate it." % (CB, CG),
        form=["ratio =", BOX],
        answers=[H("z6.0")],
        mistakes=M({"z6.0~2/3": "Upside down: q(1 &minus; &pi;) on top.",
                    "z6.0~1": "That is the fair case."}),
        explain="Above one."),
    Question(
        "z7",
        "So where is her optimum now?",
        choices=[ABOVE, ON, BELOW, AT_E],
        answers=[H("z7.c")],
        mistakes=M({
            "z7.c~" + ON: "On the line the two marginal utilities are equal. Is the "
                          "ratio 1?",
            "z7.c~" + BELOW: "v' is decreasing: a bigger v'(%s) means a smaller %s." % (CB, CB),
            "z7.c~" + AT_E: "At the endowment the ratio would be far above 3/2. She buys "
                            "some.",
        }),
        explain="The loading makes the bad state's wealth expensive: partial cover."),
    Question(
        "z8",
        "(f) Suppose instead her utility were linear and the premium loaded, q &gt; &pi;. "
        "How much cover?",
        choices=[K0, KD, KANY, KHALF],
        answers=[H("z8.c")],
        mistakes=M({
            "z8.c~" + KD: "EU = W &minus; &pi;D + K(&pi; &minus; q). What is the sign "
                          "of &pi; &minus; q?",
            "z8.c~" + KANY: "That is the fair case, q = &pi;.",
            "z8.c~" + KHALF: "EU is a straight line in K: no interior optimum.",
        }),
        explain="Only risk aversion makes anyone pay a loading. That is the insurance "
                "industry."),
]

ingrid = GuidedProblem(
    "Part 4 &middot; Ingrid insures a boat: A5.2",
    "The in-person problem the mock exams ask for. W = 100, a loss of 64 with "
    "probability 1/4, v(c) = &radic;c. %s across, %s up." % (CB, CG),
    INGRID_QUESTIONS, draw_ingrid, figsize=(6.4, 4.8),
    outro="Fair: full cover. Loaded: partial. Risk neutral: a corner.",
    sources=[PS("A5.2")],
)


# ======================================================================
# Part 5: problem A5.1, car theft (in thousands for the figure)
# ======================================================================

def draw_car(ax, stage):
    _contingent_frame(ax, 56, " (thousands)")
    _certainty(ax, 56)
    _dot(ax, 0, 50, "e: car not stolen", 6, 4, colour=LINE)
    if stage >= 1:
        _ins_line(ax, 50, 50, 0.05, 50, color=LINE, lw=2, label="q = 0.05")
    if stage >= 2:
        _dot(ax, 9.5, 49.5, "K* = 10", 6, -14, colour=CURVE)
    if stage >= 4:
        _ins_line(ax, 50, 50, 0.01, 50, color=GREEN, lw=1.8, ls="--", label="fair, q = 0.01")
    if stage >= 5:
        _dot(ax, 49.5, 49.5, "full cover", -8, 10, colour=GREEN, ha="right")
    _legend(ax, loc="lower right")


CAR_QUESTIONS = [
    Question(
        "n1",
        "A5.1: your car is worth 50,000, stolen with probability 1%, and you have nothing "
        "else. Cover costs 0.05 per krone. If you buy K = 20,000, what is your wealth in "
        "each state?",
        form=["%s =" % CG, BOX, "&nbsp; %s =" % CB, BOX],
        answers=[H("n1.0"), H("n1.1")],
        mistakes=M({"n1.1~20000": "The premium is paid in the bad state too.",
                    "n1.0~50000": "The premium is paid in the good state."}),
        explain="Expected utility is 0.99 ln(50,000 &minus; 0.05K) + 0.01 ln(0.95K)."),
    Question(
        "n2",
        "With v = ln, what is your demand for insurance K*?",
        form=["K* =", BOX],
        answers=[H("n2.0")],
        mistakes=M({"n2.0~50000": "Full cover needs a fair price. Here q = 0.05 &gt; 0.01."}),
        hints=["Differentiate: 0.99(&minus;0.05)/(50,000 &minus; 0.05K) + 0.01(0.95)/(0.95K) = 0."],
        explain="Partial insurance: 10,000 of a 50,000 loss."),
    Question(
        "n3",
        "What is the insurer's expected profit?",
        form=["profit =", BOX],
        answers=[H("n3.0")],
        mistakes=M({"n3.0~500": "That is the good state only. In the bad state it pays out.",
                    "n3.0~-9500": "That is the bad state only. Weight the two states."}),
        explain="K(q &minus; &pi;): the loading is the insurer's margin."),
    Question(
        "n4",
        "Competition drives expected profit to zero. What premium q per krone?",
        form=["q =", BOX],
        answers=[H("n4.0")],
        mistakes=M({"n4.0~0.05": "That is the old premium. Set K(q &minus; &pi;) = 0."}),
        explain="The actuarially fair premium: q = &pi;."),
    Question(
        "n5",
        "Your demand for insurance at that price?",
        form=["K* =", BOX],
        answers=[H("n5.0")],
        mistakes=M({"n5.0~10000": "That was at the loaded price."}),
        explain="Full cover: 49,500 in both states."),
]

car = GuidedProblem(
    "Part 5 &middot; Car theft: A5.1",
    "The in-person insurance problem with logarithmic utility. In kroner; the figure "
    "is in thousands.",
    CAR_QUESTIONS, draw_car, figsize=(6.4, 4.6),
    outro="A loading by a factor of five, and demand answers accordingly.",
    sources=[PS("A5.1")],
)


# ======================================================================
# Part 6: portfolios and the market line (context, review question 6)
# ======================================================================

def draw_capm(ax, stage):
    _frame(ax, 2.4, 17, "beta", "expected return (%)")
    bs = np.array([0, 2.4])
    ax.plot(bs, 3 + bs * 5, color=LINE, lw=2, label="market line")
    _dot(ax, 0, 3, r"$r_f$ = 3", 6, 4, colour=LINE)
    _dot(ax, 1, 8, "market (1, 8)", 6, -14, colour=LINE)
    if stage >= 1:
        _dot(ax, 2, 13, "beta 2", 6, -14, colour=CURVE)
    if stage >= 2:
        _dot(ax, 0.4, 5, "", colour=CURVE)
    if stage >= 3:
        _dot(ax, 0.4, 6, "a good deal", 6, 4, colour=NEW)
        _arrow(ax, (0.4, 6), (0.4, 5.15), NEW)
    _legend(ax, loc="lower right")


GOOD_DEAL = "Above the line: buyers push its price up and its expected return down"
BAD_DEAL = "Below the line: its price falls"
ON_LINE = "On the line: nothing happens"
ARB = "A riskless arbitrage profit"
DIVERS = "Diversifiable risk can be removed for free, so it earns no premium"
SMALL_VAR = "Its variance is too small to matter"
EQ_BETA = "Variance and beta are the same thing"
IGNORE = "Investors do not care about risk"

CAPM_QUESTIONS = [
    Question(
        "o1",
        "Review question 6: the risk-free rate is 3% and the market's expected return is 8%. "
        "What expected return does the CAPM assign to a stock with &beta; = 2?",
        form=["&mu; =", BOX, "%"],
        answers=[H("o1.0")],
        mistakes=M({"o1.0~16": "&beta; multiplies the market's excess return, &mu;<sub>m</sub> "
                               "&minus; r<sub>f</sub>, not &mu;<sub>m</sub>.",
                    "o1.0~10": "Add r<sub>f</sub>."}),
        explain="r<sub>f</sub> + &beta;(&mu;<sub>m</sub> &minus; r<sub>f</sub>)."),
    Question(
        "o2",
        "An analyst pitches a stock with &beta; = 0.4. What does the market line say its "
        "expected return should be?",
        form=["&mu; =", BOX, "%"],
        answers=[H("o2.0")],
        mistakes=M({"o2.0~3.2": "Add the risk-free rate."}),
        explain="The CAPM's price list."),
    Question(
        "o3",
        "The pitch says 6%. What happens?",
        choices=[GOOD_DEAL, BAD_DEAL, ON_LINE, ARB],
        answers=[H("o3.c")],
        mistakes=M({
            "o3.c~" + BAD_DEAL: "Compare 6% with the line's value.",
            "o3.c~" + ON_LINE: "Compare 6% with the line's value.",
            "o3.c~" + ARB: "A higher expected return is not a certain profit.",
        }),
        explain="Prices adjust expected returns until the asset sits on the line."),
    Question(
        "o4",
        "Why does the stock's own variance appear nowhere in these answers?",
        choices=[DIVERS, SMALL_VAR, EQ_BETA, IGNORE],
        answers=[H("o4.c")],
        mistakes=M({
            "o4.c~" + SMALL_VAR: "It would not matter however large it was.",
            "o4.c~" + EQ_BETA: "Beta is a covariance slope, not a variance.",
            "o4.c~" + IGNORE: "They are risk averse: they care about the risk they cannot "
                              "diversify.",
        }),
        explain="Only beta is priced: the market will not pay for risk you did not have "
                "to bear."),
]

capm = GuidedProblem(
    "Part 6 &middot; Portfolios and the market line",
    CTX + "Review question 6, on the CAPM.",
    CAPM_QUESTIONS, draw_capm, figsize=(6.4, 4.4),
    outro="That is session 5. Risk aversion means requiring compensation for risk, not "
          "refusing it.",
    sources=[NOTES("p. 13&ndash;18"), NOTES("p. 20, review question 6")],
)


# ======================================================================
# Where every step comes from (printed pages of s05_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "w1": NOTES("p. 3 &middot; Try it (a)"), "w2": NOTES("p. 3 &middot; Try it (b)"),
    "w3": NOTES("p. 3 &middot; Try it (c)"), "w4": NOTES("p. 4 &middot; Try it (a)"),
    "w5": NOTES("p. 4 &middot; Try it (b)"), "w6": NOTES("p. 4 &middot; Try it (c)"),
    "w7": NOTES("p. 18 &middot; worksheet task 1"),
    "x1": NOTES("p. 9 &middot; Try it (a)"), "x2": NOTES("p. 9 &middot; Try it (a)"),
    "x3": NOTES("p. 9 &middot; Try it (a)"), "x4": NOTES("p. 9 &middot; Try it (b)"),
    "x5": NOTES("p. 9 &middot; Try it (c)"), "x6": NOTES("p. 9 &middot; Try it (c)"),
    "y1": NOTES("p. 18 &middot; worksheet task 2"), "y2": NOTES("p. 18 &middot; worksheet task 2"),
    "y3": NOTES("p. 18 &middot; worksheet task 3"), "y4": NOTES("p. 18 &middot; worksheet task 3"),
    "y5": NOTES("p. 18 &middot; worksheet task 4"), "y6": NOTES("p. 18 &middot; worksheet task 4"),
    "z1": PS("A5.2 (a)"), "z2": PS("A5.2 (b)"), "z3": PS("A5.2 (c)"), "z4": PS("A5.2 (d)"),
    "z5": PS("A5.2 (e)"), "z6": PS("A5.2 (e)"), "z7": PS("A5.2 (e)"), "z8": PS("A5.2 (f)"),
    "n1": PS("A5.1 (1)"), "n2": PS("A5.1 (2)"), "n3": PS("A5.1 (3)"),
    "n4": PS("A5.1 (4)"), "n5": PS("A5.1 (4)"),
    "o1": NOTES("p. 20 &middot; review question 6"), "o2": NOTES("p. 20 &middot; review question 6"),
    "o3": NOTES("p. 20 &middot; review question 6"), "o4": NOTES("p. 20 &middot; review question 6"),
}

for _q in (PRICES_QUESTIONS + ATTITUDE_QUESTIONS + WORKSHEET_QUESTIONS + INGRID_QUESTIONS
           + CAR_QUESTIONS + CAPM_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
