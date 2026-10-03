"""
guided_s04.py - session 4 guided page: intertemporal choice.

    Part 1  budget     the two-period budget line (worksheet numbers)
    Part 2  kari       the log case and the bond (the notes' Try it)
    Part 3  worksheet  patience, the endowment and a rate rise
    Part 4  rates      the real rate and who gains from monetary policy
    Part 5  taxes      problems A4.1 and A4.2 (session 3 revisited)
    Part 6  lifetime   problem A4.3: assets, windfalls and a credit limit

Answers are hashes in answers_s04.py, generated from
answer_keys/s04_keys.py in the private repo (see guided_s03.py for the scheme).
"""

import numpy as np

from guided import BOX, GuidedProblem, Question, tag
from guided_s03 import (CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW, _dot, _frame,
                        _legend, _start)

try:
    from answers_s04 import HASHES
except ImportError:
    HASHES = {}

PS = lambda part: tag("problem", "Problem " + part)
NOTES = lambda where: tag("notes", "Notes " + where)
C1, C2, M1, M2 = "c<sub>1</sub>", "c<sub>2</sub>", "m<sub>1</sub>", "m<sub>2</sub>"
X1, X2 = "x<sub>1</sub>", "x<sub>2</sub>"


def H(key):
    return HASHES.get(key, "missing:" + key)


def M(messages):
    return {H(k): v for k, v in messages.items()}


def _iline(ax, r, m1, m2, **kw):
    # The NPV budget line from (NPV, 0) to (0, FV).
    ax.plot([0, m1 + m2 / (1 + r)], [(1 + r) * m1 + m2, 0], **kw)


def _log_curve(ax, beta, c1, c2, xmax, **kw):
    # ln c1 + beta ln c2 = level, through (c1, c2).
    level = np.log(c1) + beta * np.log(c2)
    xs = np.linspace(xmax * 0.02, xmax, 300)
    ax.plot(xs, np.exp((level - np.log(xs)) / beta), **kw)


def _endowment(ax, m1, m2, label="e", colour=LINE, dx=8, dy=4):
    ax.plot([m1], [m2], "s", color=colour, ms=7, zorder=6)
    ax.annotate(label, (m1, m2), textcoords="offset points", xytext=(dx, dy),
                color=colour, fontsize=10.5)


def _arrow(ax, start, end, colour=INK):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.3, shrinkA=6, shrinkB=6))


UPLEFT = "Only the part up and to the left of e: saving still works"
DOWNRIGHT = "Only the part down and to the right of e"
ONLY_E = "Only e itself"
ALL_LINE = "All of it: lenders do not matter"

SHIFT_PAR = "It shifts out, parallel: no price changed"
PIV_E = "It pivots around e"
PIV_C2 = "It pivots around the c2-intercept"
NO_MOVE = "It does not move"

STEEPER = "It pivots around e and gets steeper"
FLATTER = "It pivots around e and gets flatter"
SHIFT_IN = "It shifts in, parallel"
PIV_C1 = "It pivots around the c1-intercept"

GROW = "beta(1 + r) > 1"
BETA1 = "beta > 1"
RPOS = "r > 0"
LATE = "m2 > m1"

HALF_NPV = "Half of her NPV, 120/2, happens to equal her income today"
NEVER_B = "Patient people never borrow"
LOW_R = "The interest rate is too low to bother saving"
EQ_C = "beta = 1 makes c1 = c2"

PIVOT_E = "The endowment e"
PIVOT_C1 = "The c1-intercept"
PIVOT_C2 = "The c2-intercept"
PIVOT_OPT = "Her optimum"

LENDERS = "Lenders: anyone choosing left of e, with c1 < m1"
BORROWERS = "Borrowers: anyone choosing right of e"
EVERYONE = "Everyone: waiting pays more"
NOBODY = "Nobody: e stays affordable either way"

DIVIDE = "rho = (r - pi)/(1 + pi): the shortcut forgets to divide by 1 + pi"
R_RISES = "Inflation also pushes up r"
NO_GAP = "It doesn't: the two are equal"
TAXES = "Interest is taxed"

LENDER_UP = "A lender: the rotation adds bundles on her side of e"
BORROWER_UP = "A borrower: borrowing is cheaper"
BOTH_UP = "Both: higher rates mean more income"
NEITHER_UP = "Neither: e is unchanged"

AMBIG = "Substitution says save more, but being richer says consume more today"
ALWAYS_DOWN = "It doesn't: c1 always falls"
INCOME_ONLY = "Only the income effect matters for a lender"
NO_EFFECT = "Lenders' c1 never responds to r"

INC_TAX = "The income tax"
AD_VAL = "The ad valorem tax"
SAME_TAX = "Indifferent: same revenue"
DEP_TAX = "It depends on the prices"


# ======================================================================
# Part 1: the two-period budget line (worksheet: m = (60, 63), r = 5%)
# ======================================================================

def draw_budget(ax, stage):
    _frame(ax, 150, 165, "c1   (today)", "c2   (tomorrow)")
    _endowment(ax, 60, 63, r"$e = (m_1, m_2)$")
    if stage >= 1:
        _dot(ax, 120, 0, r"$m_1 + \frac{m_2}{1+r}$", 6, 10, colour=LINE)
    if stage >= 2:
        _dot(ax, 0, 126, r"$(1+r)m_1 + m_2$", 8, -4, colour=LINE)
    if stage < 3:
        return
    style = dict(color=LINE, lw=2.2, zorder=4, label=r"budget, slope $-(1+r)$")
    if stage >= 4:
        # No credit: only the saving half survives.
        ax.plot([0, 60], [126, 63], **style)
        ax.plot([60, 120], [63, 0], color=LINE, lw=1.4, ls=":", alpha=0.45)
        ax.axvline(60, color=MUTE, lw=0.9, ls="--")
        ax.text(64, 100, "no one lends:\nnothing right of e", color=MUTE, fontsize=9)
    else:
        ax.plot([0, 120], [126, 0], **style)
    if stage >= 5:
        _iline(ax, 0.05, 80, 63, color=HALF, lw=1.8, ls="--", alpha=1 if stage == 5 else 0.4,
               label=r"$m_1 \uparrow$: parallel shift")
        _endowment(ax, 80, 63, "e'", colour=HALF, dx=6, dy=-14)
    if stage >= 6:
        _iline(ax, 0.25, 60, 63, color=NEW, lw=1.8, ls="--", label=r"$r \uparrow$: pivot around e")
    _legend(ax)


BUDGET_QUESTIONS = [
    Question(
        "i1",
        "Worksheet task 1: income %s = 60 today and %s = 63 tomorrow, r = 5%%. "
        "Spend everything today, borrowing against tomorrow. How much is that? "
        "(The %s-intercept, the NPV of income.)" % (M1, M2, C1),
        form=["%s =" % C1, BOX],
        answers=[H("i1.0")],
        mistakes=M({"i1.0~123": "Tomorrow's 63 is worth less today: discount it by 1 + r.",
                    "i1.0~126": "That is the future value: waiting for everything."}),
        hints=["Eliminate the bond: %s + %s/(1 + r) = %s + %s/(1 + r)." % (C1, C2, M1, M2)],
        explain="The present value of lifetime income."),
    Question(
        "i2",
        "Now wait for everything: save all of today's income. How much can you "
        "consume tomorrow? (The %s-intercept, the future value.)" % C2,
        form=["%s =" % C2, BOX],
        answers=[H("i2.0")],
        mistakes=M({"i2.0~123": "Today's 60 earns interest before tomorrow.",
                    "i2.0~120": "That is the present value."}),
        explain="(1 + r)%s + %s." % (M1, M2)),
    Question(
        "i3",
        "What is the slope of the budget line, d%s/d%s?" % (C2, C1),
        form=["slope =", BOX],
        answers=[H("i3.0")],
        mistakes=M({"i3.0~1.05": "Right size, wrong sign.",
                    "i3.0~-20/21": "Upside down: one more krone today costs 1 + r tomorrow."}),
        explain="&minus;(1 + r): consuming a krone today costs 1 + r kroner tomorrow."),
    Question(
        "i4",
        "Suppose no one will lend to you. Which part of the budget line can you "
        "still reach?",
        choices=[UPLEFT, DOWNRIGHT, ONLY_E, ALL_LINE],
        answers=[H("i4.c")],
        mistakes=M({
            "i4.c~" + DOWNRIGHT: "Right of e means %s &gt; %s. How would you pay for "
                                 "that without a loan?" % (C1, M1),
            "i4.c~" + ONLY_E: "Can you still save without anyone lending to you?",
            "i4.c~" + ALL_LINE: "Consuming more than %s today needs someone to lend." % M1,
        }),
        explain="A credit constraint cuts off exactly the region where students and "
                "young households want to be."),
    Question(
        "i5",
        "Back to normal credit. Income today rises. What happens to the line?",
        choices=[SHIFT_PAR, PIV_E, PIV_C2, NO_MOVE],
        answers=[H("i5.c")],
        mistakes=M({
            "i5.c~" + PIV_E: "A pivot changes the slope &minus;(1 + r). Did r change?",
            "i5.c~" + PIV_C2: "Does the %s-intercept (1 + r)%s + %s contain %s?" % (C2, M1, M2, M1),
            "i5.c~" + NO_MOVE: "Both intercepts contain %s." % M1,
        }),
        explain="Income changes shift the line; the interest rate pivots it."),
    Question(
        "i6",
        "The interest rate rises. What happens to the line?",
        choices=[STEEPER, FLATTER, SHIFT_IN, PIV_C1],
        answers=[H("i6.c")],
        mistakes=M({
            "i6.c~" + FLATTER: "The slope is &minus;(1 + r). Bigger r means...?",
            "i6.c~" + SHIFT_IN: "r is a price, so the slope changes.",
            "i6.c~" + PIV_C1: "Which point needs no market at all, whatever r is?",
        }),
        explain="Consuming your income in each period needs no bonds, so no rate can "
                "take e away."),
]

budget = GuidedProblem(
    "Part 1 &middot; The two-period budget",
    "Consumption today on the horizontal axis, tomorrow on the vertical. A bond "
    "carries kroner across at the interest rate r. The endowment e (consume your "
    "income each period) is marked.",
    BUDGET_QUESTIONS, draw_budget, figsize=(6.4, 4.6),
    outro="Every fact in this session is a movement of this line.",
    sources=[NOTES("p. 2&ndash;6"), NOTES("p. 12, worksheet")],
)


# ======================================================================
# Part 2: the log case and the bond (Try it: Kari, m = (50, 60), r = 20%)
# ======================================================================

def draw_kari(ax, stage):
    _frame(ax, 118, 140, "c1", "c2")
    _endowment(ax, 50, 60, "e = (50, 60)", dx=-62, dy=6)
    if stage >= 1:
        _iline(ax, 0.2, 50, 60, color=LINE, lw=2.2, zorder=4, label="Kari's budget")
        ax.fill_between([0, 100], [120, 0], 0, color=LINE, alpha=0.06, lw=0)
    if stage >= 2:
        _log_curve(ax, 2 / 3, 60, 48, 118, color=CURVE, lw=2, zorder=4)
        _dot(ax, 60, 48, "", colour=CURVE)
    if stage >= 3:
        _arrow(ax, (50, 60), (60, 48), CURVE)
        ax.text(14, 22, "e -> optimum: borrow today,\nrepay with interest tomorrow",
                color=CURVE, fontsize=9)
    if stage >= 4:
        _log_curve(ax, 0.25, 80, 24, 118, color=HALF, lw=1.4, ls="--", alpha=0.7)
        _dot(ax, 80, 24, "Sondre", 6, 6, colour=HALF)
    if stage >= 5:
        _iline(ax, 0.2, 50, 72, color=GREEN, lw=1.8, ls="--", label="bonus next year")
        _dot(ax, 66, 52.8, "", colour=GREEN)
    if stage >= 6:
        xs = np.array([0, 100])
        ax.plot(xs, 0.8 * xs, color=MUTE, lw=1, ls=":",
                label=r"$c_2 = \beta(1+r)\,c_1$")
    _legend(ax)


KARI_QUESTIONS = [
    Question(
        "j1",
        "Kari earns 50 this year and 60 next year, and can save or borrow at r = 20%. "
        "What are the NPV and the future value of her income?",
        form=["NPV =", BOX, "&nbsp; FV =", BOX],
        answers=[H("j1.0"), H("j1.1")],
        mistakes=M({"j1.0~110": "Discount next year's 60 by 1.2.",
                    "j1.1~110": "This year's 50 earns 20% before next year."}),
        explain="Her budget line runs from the NPV on the %s axis to the FV on the %s "
                "axis, slope &minus;1.2." % (C1, C2)),
    Question(
        "j2",
        "Her utility is ln %s + &beta; ln %s with &beta; = 2/3. What does she "
        "consume in each period?" % (C1, C2),
        form=["%s* =" % C1, BOX, "&nbsp; %s* =" % C2, BOX],
        answers=[H("j2.0"), H("j2.1")],
        mistakes=M({"j2.0~50": "That is her income, not her choice.",
                    "j2.0~40": "%s* = NPV/(1 + &beta;), not NPV&middot;&beta;/(1 + &beta;)." % C1,
                    "j2.1~60": "Use the Euler equation: %s = &beta;(1 + r)%s." % (C2, C1)}),
        hints=["Log utility splits the NPV: a share 1/(1 + &beta;) is spent today.",
               "Then the Euler equation: %s = &beta;(1 + r)%s." % (C2, C1)],
        explain="The tangency: her willingness to trade across time equals 1 + r."),
    Question(
        "j3",
        "Does she borrow or lend? Give her bond b<sub>1</sub> = %s &minus; %s and "
        "what is repaid next year." % (M1, C1),
        form=["b<sub>1</sub> =", BOX, "&nbsp; repaid =", BOX],
        answers=[H("j3.0"), H("j3.1")],
        mistakes=M({"j3.0~10": "She consumes more than she earns, so b<sub>1</sub> is negative.",
                    "j3.1~10": "The loan is repaid with 20% interest."}),
        explain="She borrows, and 60 &minus; 12 leaves exactly her %s*." % C2),
    Question(
        "j4",
        "Her neighbour Sondre has the same income and rate and log utility too, but "
        "chooses %s = 80. What is his &beta;?" % C1,
        form=["&beta; =", BOX],
        answers=[H("j4.0")],
        mistakes=M({"j4.0~5/4": "That is 1 + &beta;.",
                    "j4.0~4/5": "%s = NPV/(1 + &beta;). Solve for &beta;." % C1}),
        explain="The bigger spender today is the less patient one: impatience read "
                "off a single choice."),
    Question(
        "j5",
        "Kari is promised a bonus of 12, paid next year. By how much does her "
        "consumption today rise?",
        form=["&Delta;%s =" % C1, BOX],
        answers=[H("j5.0")],
        mistakes=M({"j5.0~10": "That is the bonus in today's money. She spends only her "
                               "share of it today.",
                    "j5.0~12": "Discount it, then take her share.",
                    "j5.0~36/5": "Discount the bonus first: it arrives next year."}),
        explain="She borrows against a bonus she has not received: permanent income "
                "at work."),
    Question(
        "j6",
        "Look at the Euler equation %s = &beta;(1 + r)%s. When does consumption grow "
        "over time?" % (C2, C1),
        choices=[GROW, BETA1, RPOS, LATE],
        answers=[H("j6.c")],
        mistakes=M({
            "j6.c~" + BETA1: "&beta; is below 1. What multiplies %s?" % C1,
            "j6.c~" + RPOS: "Kari faces r = 20% but her consumption falls. Why?",
            "j6.c~" + LATE: "Income timing only enters through the NPV.",
        }),
        explain="Patience times the reward for waiting, against the pull of the present."),
]

kari = GuidedProblem(
    "Part 2 &middot; The log case and the bond",
    "The notes' Try it. Kari earns 50 this year and 60 next year, and can save or "
    "borrow at r = 20%.",
    KARI_QUESTIONS, draw_kari, figsize=(6.4, 4.6),
    outro="Incomes enter only through their NPV: when you earn matters only through "
          "what it is worth today.",
    sources=[NOTES("p. 7&ndash;9")],
)


# ======================================================================
# Part 3: the worksheet (m = (60, 63), r = 5%)
# ======================================================================

def draw_worksheet(fig, stage):
    ax, rx = fig.subplots(1, 2)
    _frame(ax, 140, 150, "c1", "c2")
    ax.set_title("The budget line", loc="left", color=INK, fontsize=10)
    _iline(ax, 0.05, 60, 63, color=LINE, lw=2.2, zorder=4)
    _endowment(ax, 60, 63, "e", dx=8, dy=4)
    if stage >= 1:
        _log_curve(ax, 0.5, 80, 42, 140, color=CURVE, lw=1.8)
        _dot(ax, 80, 42, r"$\beta = 1/2$", 6, 6)
    if stage >= 2:
        _arrow(ax, (60, 63), (80, 42), CURVE)
    if stage >= 3:
        _log_curve(ax, 1.0, 60, 63, 140, color=HALF, lw=1.6, ls="--")
        ax.annotate(r"$\beta = 1$: at e", (60, 63), textcoords="offset points",
                    xytext=(-10, -18), ha="right", color=HALF, fontsize=10)

    _frame(rx, 140, 150, "c1", "c2")
    rx.set_title("The rate rise", loc="left", color=INK, fontsize=10)
    _iline(rx, 0.05, 60, 63, color=GREY, lw=1.8, label="r = 5%")
    _endowment(rx, 60, 63, "e", dx=8, dy=4)
    if stage >= 5:
        _iline(rx, 0.25, 60, 63, color=NEW, lw=2, ls="--", label="r = 25%")
    if stage >= 6:
        rx.fill_between([0, 60], [126, 63], [138, 63], color=GREEN, alpha=0.2, lw=0)
        rx.text(4, 140, "gained: lenders", color=GREEN, fontsize=9.5)
        xs = np.linspace(60, 120, 50)
        old = 63 - 1.05 * (xs - 60)
        new = np.maximum(0, 63 - 1.25 * (xs - 60))
        rx.fill_between(xs, new, old, color=NEW, alpha=0.15, lw=0)
        rx.text(84, 30, "lost:\nborrowers", color=NEW, fontsize=9.5)
    _legend(rx)
    fig.subplots_adjust(wspace=0.25)


WORKSHEET_QUESTIONS = [
    Question(
        "k1",
        "Worksheet task 2: log utility with &beta; = 1/2, income (60, 63), r = 5%. "
        "Find the bundle.",
        form=["%s* =" % C1, BOX, "&nbsp; %s* =" % C2, BOX],
        answers=[H("k1.0"), H("k1.1")],
        mistakes=M({"k1.0~60": "That is the endowment. Compute NPV/(1 + &beta;).",
                    "k1.0~40": "%s* = NPV/(1 + &beta;)." % C1,
                    "k1.1~63": "That is the endowment."}),
        hints=["The NPV is 120 (Part 1). A share 1/(1 + &beta;) is consumed today."],
        explain="The tangency sits right of e."),
    Question(
        "k2",
        "Does this person borrow or lend? Give b<sub>1</sub> and what is repaid in "
        "period 2.",
        form=["b<sub>1</sub> =", BOX, "&nbsp; repaid =", BOX],
        answers=[H("k2.0"), H("k2.1")],
        mistakes=M({"k2.0~20": "Consuming more than %s today means b<sub>1</sub> &lt; 0." % M1,
                    "k2.1~20": "Repaid with 5% interest."}),
        explain="A borrower: the impatient one sits right of e."),
    Question(
        "k3",
        "Task 3: redo it with &beta; = 1.",
        form=["%s* =" % C1, BOX, "&nbsp; %s* =" % C2, BOX],
        answers=[H("k3.0"), H("k3.1")],
        mistakes=M({"k3.0~80": "That is the &beta; = 1/2 answer. With &beta; = 1 the "
                               "share today is 1/2."}),
        explain="Exactly the endowment."),
    Question(
        "k4",
        "Why does the patient person sit exactly at the endowment here?",
        choices=[HALF_NPV, NEVER_B, LOW_R, EQ_C],
        answers=[H("k4.c")],
        mistakes=M({
            "k4.c~" + NEVER_B: "Patience is relative to the income path. With income "
                               "early, a patient person can still borrow? Or save?",
            "k4.c~" + LOW_R: "Any r shifts the bundle unless something else lines up.",
            "k4.c~" + EQ_C: "Check your answer: is %s* = %s*?" % (C1, C2),
        }),
        explain="A coincidence of these numbers, not a law: change %s and the bond "
                "appears again." % M2),
    Question(
        "k5",
        "Task 4: the rate jumps to 25%. Which point of the line cannot move?",
        choices=[PIVOT_E, PIVOT_C1, PIVOT_C2, PIVOT_OPT],
        answers=[H("k5.c")],
        mistakes=M({
            "k5.c~" + PIVOT_C1: "The %s-intercept is %s + %s/(1 + r). Does it contain r?" % (C1, M1, M2),
            "k5.c~" + PIVOT_C2: "The %s-intercept is (1 + r)%s + %s. Does it contain r?" % (C2, M1, M2),
            "k5.c~" + PIVOT_OPT: "The optimum moves with prices. Which bundle needs no market?",
        }),
        explain="The line rotates around e."),
    Question(
        "k6",
        "Who gains from the rate rise?",
        choices=[LENDERS, BORROWERS, EVERYONE, NOBODY],
        answers=[H("k6.c")],
        mistakes=M({
            "k6.c~" + BORROWERS: "Is borrowing cheaper or dearer now?",
            "k6.c~" + EVERYONE: "The rotation adds bundles on one side of e and removes "
                                "them on the other.",
            "k6.c~" + NOBODY: "e stays affordable, but the line around it moves.",
        }),
        explain="Monetary policy is never neutral: where you sit relative to e decides."),
]

worksheet = GuidedProblem(
    "Part 3 &middot; The worksheet",
    "The notes' worksheet: income 60 today and 63 tomorrow, r = 5%, log utility. "
    "Find the tangency, change the patience, then raise the rate.",
    WORKSHEET_QUESTIONS, draw_worksheet, figsize=(7.6, 4.0), whole_figure=True,
    outro="Bring the sheet: you will defend who gains from the rate rise.",
    sources=[NOTES("p. 12&ndash;13, worksheet")],
)


# ======================================================================
# Part 4: real rates and monetary policy (review question 5, Q6)
# ======================================================================

def draw_rates(fig, stage):
    bx, lx = fig.subplots(1, 2)
    # Illustrative optima, on each line at r = 10%: right of e for the
    # borrower, left of e for the lender.
    for ax, (m1, m2), name, opt in ((bx, (20, 100), "the borrower: income late", (60, 56)),
                                    (lx, (100, 20), "the lender: income early", (55, 69.5))):
        _frame(ax, 150, 160, "c1", "c2")
        ax.set_title(name, loc="left", color=INK, fontsize=10)
        _iline(ax, 0.10, m1, m2, color=LINE, lw=2, label="r")
        _endowment(ax, m1, m2, "e", dx=8, dy=4)
        _dot(ax, opt[0], opt[1], "", colour=CURVE)
        if stage >= 3:
            _iline(ax, 0.40, m1, m2, color=NEW, lw=1.8, ls="--", label=r"$r \uparrow$")
        _legend(ax)
    if stage >= 3:
        bx.text(0.97, 0.72, "worse off", transform=bx.transAxes, ha="right", color=NEW,
                fontsize=10)
        lx.text(0.97, 0.72, "better off", transform=lx.transAxes, ha="right",
                color=GREEN, fontsize=10)
    if stage >= 4:
        lx.text(0.97, 0.64, r"but $c_1$? ambiguous", transform=lx.transAxes, ha="right",
                color=INK, fontsize=9.5)
    if stage >= 1:
        fig.text(0.5, 0.01, r"real rate:  $1 + \rho = \frac{1 + r}{1 + \pi}$", ha="center",
                 color=INK, fontsize=11)
    fig.subplots_adjust(wspace=0.25, bottom=0.18)


RATES_QUESTIONS = [
    Question(
        "l1",
        "Review question 6: a bank quotes a nominal rate of 26% while inflation is 5%. What "
        "is the real rate &rho;?",
        form=["&rho; =", BOX, "%"],
        answers=[H("l1.0")],
        mistakes=M({"l1.0~21": "That is the shortcut r &minus; &pi;. Use "
                               "1 + &rho; = (1 + r)/(1 + &pi;).",
                    "l1.0~31": "Inflation lowers the real reward for waiting."}),
        explain="Every r in this session is really the real rate &rho;."),
    Question(
        "l2",
        "Why does the shortcut r &minus; &pi; overstate the real rate here?",
        choices=[DIVIDE, R_RISES, NO_GAP, TAXES],
        answers=[H("l2.c")],
        mistakes=M({
            "l2.c~" + R_RISES: "r is given here. Compare the two formulas.",
            "l2.c~" + NO_GAP: "Compare your answer with 26 &minus; 5.",
            "l2.c~" + TAXES: "There are no taxes in this model.",
        }),
        explain="The gap grows with the rates: fine at low inflation, misleading at high."),
    Question(
        "l3",
        "Review question 5: the central bank raises the interest rate. Who is unambiguously "
        "better off?",
        choices=[LENDER_UP, BORROWER_UP, BOTH_UP, NEITHER_UP],
        answers=[H("l3.c")],
        mistakes=M({
            "l3.c~" + BORROWER_UP: "Does a higher r make borrowing cheaper?",
            "l3.c~" + BOTH_UP: "The rotation takes bundles away on one side of e.",
            "l3.c~" + NEITHER_UP: "e is unchanged, but the line through it rotates.",
        }),
        explain="The lender can still afford her old bundle, and more besides."),
    Question(
        "l4",
        "But the effect on the lender's consumption <i>today</i> is ambiguous. Why?",
        choices=[AMBIG, ALWAYS_DOWN, INCOME_ONLY, NO_EFFECT],
        answers=[H("l4.c")],
        mistakes=M({
            "l4.c~" + ALWAYS_DOWN: "She is also richer. Does richer mean consume less today?",
            "l4.c~" + INCOME_ONLY: "Today got relatively dearer too: that is a "
                                   "substitution effect.",
            "l4.c~" + NO_EFFECT: "Under log utility with income only today it happens to "
                                 "cancel. In general?",
        }),
        explain="Session 3's two effects, on the time axis."),
]

rates = GuidedProblem(
    "Part 4 &middot; Real rates and monetary policy",
    "Two review questions: the real interest rate, and why a rate change helps some "
    "people and hurts others.",
    RATES_QUESTIONS, draw_rates, figsize=(7.6, 4.2), whole_figure=True,
    outro="Demography decides how many people sit on each side of e.",
    sources=[NOTES("p. 9&ndash;10"), NOTES("p. 13&ndash;14, review questions 5&ndash;6")],
)


# ======================================================================
# Part 5: taxes, problems A4.1 and A4.2 (30x1 + 25x2 = 300, 60% on x2)
# ======================================================================

def draw_taxes(fig, stage):
    sx, cx = fig.subplots(1, 2)
    for ax, title in ((sx, r"A4.1: $U = \frac{1}{2}x_1 + \frac{1}{2}x_2$"),
                      (cx, r"A4.2: $U = x_1^{1/2}x_2^{1/2}$")):
        _frame(ax, 12, 14, "x1", "x2")
        ax.set_title(title, loc="left", color=INK, fontsize=10)
        ax.plot([0, 10], [12, 0], color=LINE, lw=2, label="before the tax")
    for k in (4, 8, 12):
        sx.plot([0, k], [k, 0], color=CURVE, lw=0.8, ls=":", alpha=0.6)
    if stage >= 1:
        _dot(sx, 0, 12, "", colour=CURVE)
    if stage >= 2:
        sx.plot([0, 10], [7.5, 0], color=NEW, lw=1.8, ls="--", label="60% tax on x2")
        _dot(sx, 10, 0, "", colour=NEW)
    if stage >= 3:
        sx.text(0.97, 0.75, "revenue: nothing to tax", transform=sx.transAxes, ha="right",
                color=NEW, fontsize=9.5)
    xs = np.linspace(1.2, 12, 200)
    if stage >= 4:
        cx.plot(xs, 30 / xs, color=CURVE, lw=1.6)
        _dot(cx, 5, 6, "", colour=CURVE)
    if stage >= 5:
        cx.plot([0, 10], [7.5, 0], color=NEW, lw=1.8, ls="--", label="60% tax on x2")
        cx.plot(xs, 18.75 / xs, color=NEW, lw=1, alpha=0.6)
        _dot(cx, 5, 3.75, "", colour=NEW)
    if stage >= 7:
        cx.plot([0, 243.75 / 30], [243.75 / 25, 0], color=GREEN, lw=1.8, ls=":",
                label="income tax, same revenue")
        cx.plot(xs, 4.0625 * 4.875 / xs, color=GREEN, lw=1, alpha=0.6)
        _dot(cx, 4.0625, 4.875, "", colour=GREEN)
    _legend(sx)
    _legend(cx)
    fig.subplots_adjust(wspace=0.25)


TAX_QUESTIONS = [
    Question(
        "t1",
        "A4.1: U = &frac12;%s + &frac12;%s with budget 30%s + 25%s = 300. What is "
        "the optimal bundle?" % (X1, X2, X1, X2),
        form=["%s =" % X1, BOX, "&nbsp; %s =" % X2, BOX],
        answers=[H("t1.0"), H("t1.1")],
        mistakes=M({"t1.0~10": "Which good gives more utility per krone, &alpha;/p<sub>1</sub> "
                               "or &beta;/p<sub>2</sub>?"}),
        hints=["Perfect substitutes: compare utility per krone and buy only the winner."],
        explain="A corner on the cheaper-per-util good."),
    Question(
        "t2",
        "A 60%% ad valorem tax is put on %s. What is the new bundle?" % X2,
        form=["%s =" % X1, BOX, "&nbsp; %s =" % X2, BOX],
        answers=[H("t2.0"), H("t2.1")],
        mistakes=M({"t2.1~15/2": "Compare utility per krone again at the taxed price 40.",
                    "t2.1~12": "The consumer price of %s is now 25 &times; 1.6." % X2}),
        explain="The consumer jumps to the other corner."),
    Question(
        "t3",
        "How much revenue does the tax raise?",
        form=["revenue =", BOX],
        answers=[H("t3.0")],
        mistakes=M({"t3.0~180": "Revenue is the tax per unit times the quantity bought "
                                "after the tax.",
                    "t3.0~112.5": "How much %s is bought after the tax?" % X2}),
        explain="The tax base disappears: utility falls, and the state gets nothing. "
                "All of it is deadweight loss."),
    Question(
        "t4",
        "A4.2: same prices and income, but U = %s<sup>&frac12;</sup>%s<sup>&frac12;</sup>. "
        "What is the optimal bundle?" % (X1, X2),
        form=["%s =" % X1, BOX, "&nbsp; %s =" % X2, BOX],
        answers=[H("t4.0"), H("t4.1")],
        mistakes=M({"t4.0~10": "Cobb-Douglas never picks a corner. Half of income on each good."}),
        explain="Equal exponents: half of income on each good."),
    Question(
        "t5",
        "With the 60%% tax on %s?" % X2,
        form=["%s =" % X1, BOX, "&nbsp; %s =" % X2, BOX],
        answers=[H("t5.0"), H("t5.1")],
        mistakes=M({"t5.1~6": "The consumer price of %s is now 40." % X2,
                    "t5.0~4": "Good 1's price and income did not change."}),
        explain="%s holds still (constant shares); %s falls." % (X1, X2)),
    Question(
        "t6",
        "How much revenue does the tax raise now?",
        form=["revenue =", BOX],
        answers=[H("t6.0")],
        mistakes=M({"t6.0~150": "That is everything paid for %s. The state keeps only the "
                                "tax part." % X2,
                    "t6.0~90": "Use the quantity bought after the tax."}),
        hints=["Tax per unit is 40 &minus; 25."],
        explain="Demand does not collapse, so this tax raises money."),
    Question(
        "t7",
        "A4.2 (e): the government instead takes the same amount as an income tax. "
        "What is the bundle?",
        form=["%s =" % X1, BOX, "&nbsp; %s =" % X2, BOX],
        answers=[H("t7.0"), H("t7.1")],
        mistakes=M({"t7.0~5": "Income is lower now: 300 minus the revenue.",
                    "t7.1~3.75": "Prices are back to 30 and 25."}),
        explain="A parallel shift in: relative prices untouched."),
    Question(
        "t8",
        "Which does the consumer prefer?",
        choices=[INC_TAX, AD_VAL, SAME_TAX, DEP_TAX],
        answers=[H("t8.c")],
        mistakes=M({
            "t8.c~" + AD_VAL: "Compare utility, %s&middot;%s, at the two bundles." % (X1, X2),
            "t8.c~" + SAME_TAX: "Same revenue, but compare %s&middot;%s." % (X1, X2),
            "t8.c~" + DEP_TAX: "The prices are given. Compare the two bundles.",
        }),
        explain="Same money, no distortion: the income tax wins, as in session 3's tariff."),
]

taxes = GuidedProblem(
    "Part 5 &middot; Taxes: A4.1 and A4.2",
    "Two in-person problems that revisit session 3. Same budget, 30%s + 25%s = 300, "
    "and the same 60%% tax on %s, but two different tastes." % (X1, X2, X2),
    TAX_QUESTIONS, draw_taxes, figsize=(7.6, 4.0), whole_figure=True,
    outro="How elastic demand is decides whether a tax raises money or only destroys "
          "it.",
    sources=[PS("A4.1"), PS("A4.2")],
)


# ======================================================================
# Part 6: problem A4.3 (assets 5000, income 10000 and 100000, r = 5%, beta = 1)
# ======================================================================
# Drawn in thousands of kroner.

def draw_lifetime(ax, stage):
    _frame(ax, 125, 135, "c1   (thousands)", "c2   (thousands)")
    _endowment(ax, 15, 100, r"$e = (a_1 + m_1,\ m_2)$", dx=8, dy=4)
    if stage >= 1:
        _iline(ax, 0.05, 15, 100, color=LINE, lw=2.2, zorder=4, label="budget, r = 5%")
    if stage >= 2:
        _log_curve(ax, 1.0, 55.119, 57.875, 125, color=CURVE, lw=1.8)
        _dot(ax, 55.119, 57.875, "", colour=CURVE)
        _arrow(ax, (15, 100), (55.119, 57.875), CURVE)
    if stage >= 3:
        _iline(ax, 0.05, 25, 100, color=GREEN, lw=1.4, ls="--", alpha=1 if stage == 3 else 0.4,
               label=r"$m_1$ + 10")
    if stage >= 4:
        _iline(ax, 0.05, 15, 110, color=HALF, lw=1.4, ls="--", alpha=1 if stage == 4 else 0.4,
               label=r"$m_2$ + 10")
    if stage >= 5:
        _iline(ax, 0.10, 15, 100, color=NEW, lw=1.8, ls="--", alpha=1 if stage == 5 else 0.4,
               label="r = 10%")
    if stage >= 6:
        ax.axvline(15, color=MUTE, lw=1, ls=":")
        ax.text(17, 128, "no borrowing", color=MUTE, fontsize=9)
        _dot(ax, 15, 100, "", colour=INK)
    _legend(ax)


LIFETIME_QUESTIONS = [
    Question(
        "v1",
        "A4.3: assets a<sub>1</sub> = 5,000 at the start, labour income 10,000 now and "
        "100,000 next period, r = 5%%, U = ln %s + ln %s. What is lifetime wealth, "
        "the NPV of all resources? (Rounding to the nearest krone is fine.)" % (C1, C2),
        form=["M =", BOX],
        answers=[H("v1.0")],
        mistakes=M({"v1.0~115000": "Next period's 100,000 must be discounted.",
                    "v1.0~105238.1": "Don't forget the assets."}),
        hints=["Assets enter period 1: %s + %s/(1 + r) = a<sub>1</sub> + %s + %s/(1 + r)."
               % (C1, C2, M1, M2)],
        explain="The budget line's %s-intercept." % C1),
    Question(
        "v2",
        "Find optimal consumption in both periods.",
        form=["%s* =" % C1, BOX, "&nbsp; %s* =" % C2, BOX],
        answers=[H("v2.0"), H("v2.1")],
        mistakes=M({"v2.0~15000": "That is what she has in hand, not what she wants.",
                    "v2.1~100000": "That is her income next period."}),
        hints=["With &beta; = 1 and log utility, %s = M/2." % C1],
        explain="She borrows about 40,000 against next period's income."),
    Question(
        "v3",
        "Current labour income rises by 10,000. By how much does %s rise?" % C1,
        form=["&Delta;%s =" % C1, BOX],
        answers=[H("v3.0")],
        mistakes=M({"v3.0~10000": "She spreads a windfall over both periods."}),
        explain="Half of the rise in wealth."),
    Question(
        "v4",
        "Future labour income rises by 10,000 instead. By how much does %s rise?" % C1,
        form=["&Delta;%s =" % C1, BOX],
        answers=[H("v4.0")],
        mistakes=M({"v4.0~5000": "Future income is worth less today: discount it first."}),
        explain="Smaller than (3) because it is discounted."),
    Question(
        "v5",
        "The interest rate rises to 10%%. By how much does %s change?" % C1,
        form=["&Delta;%s =" % C1, BOX],
        answers=[H("v5.0")],
        mistakes=M({"v5.0~2164.5": "Check the sign: is she richer or poorer?",
                    "v5.0~2164": "Check the sign: is she richer or poorer?"}),
        hints=["Recompute M with 1.10, then %s = M/2." % C1],
        explain="A borrower: dearer borrowing and a smaller NPV both hurt."),
    Question(
        "v6",
        "Now she cannot borrow in period 1. What does she consume?",
        form=["%s =" % C1, BOX, "&nbsp; %s =" % C2, BOX],
        answers=[H("v6.0"), H("v6.1")],
        mistakes=M({"v6.0~55119": "That plan needs a loan of about 40,000."}),
        explain="A corner at e: the Euler equation holds with inequality, and she "
                "would react strongly to a windfall today."),
]

lifetime = GuidedProblem(
    "Part 6 &middot; Lifetime wealth: A4.3",
    "The in-person problem A4.3, in kroner (the figure is in thousands). A consumer "
    "with assets, low income now and high income later.",
    LIFETIME_QUESTIONS, draw_lifetime, figsize=(6.4, 4.6),
    outro="That is session 4. Next session adds uncertainty.",
    sources=[PS("A4.3")],
)


# ======================================================================
# Where every step comes from (printed pages of s04_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "i1": NOTES("p. 12 &middot; worksheet task 1"),
    "i2": NOTES("p. 12 &middot; worksheet task 1"),
    "i3": NOTES("p. 5 &middot; the NPV constraint"),
    "i4": NOTES("p. 4 &middot; eliminating borrowing"),
    "i5": NOTES("p. 4 &middot; changing endowments"),
    "i6": NOTES("p. 6 &middot; the rate pivot"),
    "j1": NOTES("p. 8 &middot; Try it (a)"),
    "j2": NOTES("p. 8 &middot; Try it (b)"),
    "j3": NOTES("p. 8 &middot; Try it (b)"),
    "j4": NOTES("p. 8 &middot; Try it (c)"),
    "j5": NOTES("p. 8 &middot; Try it (d)"),
    "j6": NOTES("p. 8 &middot; the Euler equation"),
    "k1": NOTES("p. 12 &middot; worksheet task 2"),
    "k2": NOTES("p. 12 &middot; worksheet task 2"),
    "k3": NOTES("p. 12 &middot; worksheet task 3"),
    "k4": NOTES("p. 12 &middot; worksheet task 3"),
    "k5": NOTES("p. 12 &middot; worksheet task 4"),
    "k6": NOTES("p. 13 &middot; worksheet"),
    "l1": NOTES("p. 14 &middot; review question 6"),
    "l2": NOTES("p. 14 &middot; review question 6"),
    "l3": NOTES("p. 13 &middot; review question 5"),
    "l4": NOTES("p. 13 &middot; review question 5"),
    "t1": PS("A4.1 (b)"), "t2": PS("A4.1 (c)"), "t3": PS("A4.1 (d)"),
    "t4": PS("A4.2 (b)"), "t5": PS("A4.2 (c)"), "t6": PS("A4.2 (d)"),
    "t7": PS("A4.2 (e)"), "t8": PS("A4.2 (f)"),
    "v1": PS("A4.3 (1)"), "v2": PS("A4.3 (2)"), "v3": PS("A4.3 (3)"),
    "v4": PS("A4.3 (4)"), "v5": PS("A4.3 (5)"), "v6": PS("A4.3 (6)"),
}

for _q in (BUDGET_QUESTIONS + KARI_QUESTIONS + WORKSHEET_QUESTIONS + RATES_QUESTIONS
           + TAX_QUESTIONS + LIFETIME_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
