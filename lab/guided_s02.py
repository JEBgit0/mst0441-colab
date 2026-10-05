"""
guided_s02.py - session 2 guided page: budgets, preferences and the MRS.

    Part 1  sondre    A2.1's goods budget: build the line, then move it
    Part 2  kari      A2.2's leisure budget: the endowment, and why a wage
                      change pivots the line around it
    Part 3  curves    indifference curves and the MRS, the notes' U = xy
    Part 4  families  review question 4: match four consumers to a family

Parts are numbered, not lettered, so nobody goes looking for "Part C" in the
problem set. Every step carries a tag saying where it comes from; the full
list is in STEP_SOURCES at the bottom.

The optimum itself (tangency, L* and so on) is deliberately left out. Solving
for it is the problem set, which is where the tutor coaches.

Part 1 follows problem A2.1 (Sondre heats a flat): heating h on the
horizontal axis, the basket c on the vertical, p_c = 1, p_h = 3, m = 90.
The student builds the budget line one piece at a time, then predicts what
an income cut, a carbon levy and a doubling of everything do to it.

The figure never prints a number. Intercepts and slopes are labelled in
symbols, which is also how the exam wants them derived. The geometry is drawn
to scale from the numbers below, but the axes carry no ticks.

Answers are hashes (see guided.py). To change a question, recompute its
hashes with `python guided.py <qid>.<box> <answer>`.
"""

# PS and NOTES say where each step comes from. Problem numbers are the in-person
# problem set (A2_Problems.pdf); page numbers are the printed pages of
# s02_notes.pdf.
from guided import BOX, NOTES, PS, GuidedProblem, Question
from style import CURVE, FILL, HALF, INK, LINE, MUTE, NEW

# A2.1's numbers. Given in the problem text, so nothing is given away here.
P_C, P_H, M = 1.0, 3.0, 90.0

SHIFT = "It shifts, parallel to the old line"
PIV_C = "It pivots around the c-intercept"
PIV_H = "It pivots around the h-intercept"
SAME = "It does not move"
MOVES = [SHIFT, PIV_C, PIV_H, SAME]


# ---------------------------------------------------------------- figure ---

def _line(ax, p_c, p_h, m, **kw):
    ax.plot([0, m / p_h], [m / p_c, 0], **kw)


def _dot(ax, x, y, label, dx, dy, colour=LINE):
    ax.plot([x], [y], "o", color=colour, ms=6, zorder=5, clip_on=False)
    ax.annotate(label, (x, y), textcoords="offset points", xytext=(dx, dy),
                color=colour, fontsize=11)


def draw_sondre(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 36)
    ax.set_ylim(0, 105)

    if stage == 0:
        ax.text(0.5, 0.5, "Answer step 1 to start drawing.", transform=ax.transAxes,
                ha="center", va="center", color=MUTE, fontsize=11)
        return

    # Step 1: the constraint is written down, so the plane gets its axes.
    # Labels at the far ends, as in the notes, so they stay clear of the
    # intercepts that land mid-axis.
    ax.set_xlabel("h   (heating)", color=INK, fontsize=10, loc="right")
    ax.set_ylabel("c   (other goods)", color=INK, fontsize=10, loc="top")
    ax.text(-0.6, -3, "0", color=MUTE, ha="right", va="top", fontsize=9)

    # Steps 2 and 3: the two intercepts.
    if stage >= 2:
        _dot(ax, 0, M / P_C, r"$m/p_c$", 8, -4)
    if stage >= 3:
        _dot(ax, M / P_H, 0, r"$m/p_h$", -4, 10)

    if stage < 4:
        return

    # Step 4: the slope joins the dots. Shade the choice set and mark the
    # trade the slope stands for: give up c to get more h. Everything from
    # here on stays in the picture, so the figure ends as a summary of the
    # whole part rather than of the last step.
    _line(ax, P_C, P_H, M, color=LINE, lw=2.2, zorder=4,
          label=r"budget line, slope $-\,p_h/p_c$")
    ax.fill_between([0, M / P_H], [M / P_C, 0], 0, color=FILL, alpha=0.08, lw=0)
    ax.text(18, 7, "choice set", color=LINE, alpha=0.7, fontsize=10)

    h0, h1 = 8.0, 13.0
    c0, c1 = (M - P_H * h0) / P_C, (M - P_H * h1) / P_C
    ax.plot([h0, h1], [c0, c0], color=MUTE, lw=1.2)
    ax.plot([h1, h1], [c0, c1], color=MUTE, lw=1.2)
    ax.annotate(r"$\Delta h$", ((h0 + h1) / 2, c0), textcoords="offset points",
                xytext=(0, 6), ha="center", color=INK, fontsize=11)
    ax.annotate(r"$\Delta c = -\frac{p_h}{p_c}\,\Delta h$", (h1, (c0 + c1) / 2),
                textcoords="offset points", xytext=(8, -4), color=INK, fontsize=12)

    # Each change is drawn against the original line and then kept. The
    # newest one is at full strength; older ones fade so the eye goes to
    # whatever the student just predicted.
    fade = lambda since: 1.0 if stage == since else 0.4

    # Step 5: income halves. Same prices, so the same slope, closer in.
    if stage >= 5:
        _line(ax, P_C, P_H, M / 2, color=HALF, lw=2, ls="--", zorder=4,
              alpha=fade(5), label=r"$m \to m/2$: parallel shift")

    # Steps 6 and 7: the levy doubles p_h. Only m/p_h has p_h in it.
    if stage >= 6:
        label = r"$p_h \to 2p_h$: pivot around $m/p_c$"
        if stage >= 7:
            label = r"$p_h \to 2p_h$: pivot, slope $-\,p_h'/p_c$"
        _line(ax, P_C, 2 * P_H, M, color=NEW, lw=2, ls="--", zorder=4,
              alpha=1.0 if stage in (6, 7) else 0.4, label=label)
    if stage >= 7:
        _dot(ax, M / (2 * P_H), 0, r"$m/p_h'$", -10, 10, colour=NEW)

    # Step 8: double everything and nothing moves.
    if stage >= 8:
        ax.text(35.5, 78, r"$2p_c,\; 2p_h,\; 2m$:  the same line", color=INK,
                fontsize=11.5, ha="right")
        ax.text(35.5, 71, "only relative prices and real income matter",
                color=MUTE, fontsize=9.5, ha="right")

    leg = ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    for text in leg.get_texts():
        text.set_color(INK)


# ------------------------------------------------------------- questions ---

PC, PH = "p<sub>c</sub>", "p<sub>h</sub>"

SONDRE_QUESTIONS = [
    Question(
        "a1",
        "Write down Sondre's budget constraint: what he spends on the basket "
        "plus what he spends on heating equals his income.",
        form=["", BOX, "&middot; c &nbsp;+", BOX, "&middot; h &nbsp;=", BOX],
        answers=["a62d209e72f9a071", "afbd7f9c22696357", "3add2c2ca90a9299"],
        mistakes={
            "b3c647ab1530a383": "Check which price goes with which good.",
            "c004bfd89ac88b67": "Check which price goes with which good.",
        },
        hints=["Spending on a good is its price times the quantity.",
               "The number in front of each good is that good's price; the "
               "right-hand side is income m."],
        explain="%s&middot;c + %s&middot;h = m. The axes are up." % (PC, PH)),

    Question(
        "a2",
        "Suppose Sondre spends everything on the basket and buys no heating. "
        "How much <i>c</i> can he buy? That is the c-intercept.",
        form=["c =", BOX],
        answers=["f1dd28e29c4da531"],
        mistakes={"bb3863624695ca38":
                  "That is the most heating he could buy. Here h = 0."},
        hints=["Set h = 0 in the budget constraint and solve for c."],
        explain="The c-intercept is m / %s." % PC),

    Question(
        "a3",
        "Now the opposite: everything on heating, no basket. How much <i>h</i>? "
        "That is the h-intercept.",
        form=["h =", BOX],
        answers=["5588fdab8858634d"],
        mistakes={"855c9f68b3762c61": "That is the c-intercept. Now set c = 0.",
                  "f038fab04509b277": "Divide income by the price, don't multiply."},
        hints=["Set c = 0 in the budget constraint and solve for h."],
        explain="The h-intercept is m / %s." % PH),

    Question(
        "a4",
        "What is the slope of the budget line, dc/dh?",
        form=["dc/dh =", BOX],
        answers=["04bf4240e440f427"],
        mistakes={
            "4c46441b439a2a01": "Right size, wrong sign: if h goes up, c has to go down.",
            "9ee887ef9db00b28": "Upside down. Solve the budget for c and read off "
                                "the number in front of h.",
            "f45e12abcfc20b39": "Upside down, and check the sign too.",
        },
        hints=["Solve the budget constraint for c: c = ... The number in front "
               "of h is the slope.",
               "You can also use the intercepts: rise over run, from one "
               "intercept to the other."],
        explain="The slope is &minus;%s/%s: one more unit of heating costs %s/%s "
                "units of the basket. A budget slope is an opportunity cost."
                % (PH, PC, PH, PC)),

    Question(
        "a5",
        "Sondre's income falls by half. Prices stay the same. What happens to "
        "the budget line?",
        choices=MOVES,
        answers=["53349b72f139e35a"],
        mistakes={
            "ff3dc77a06e40a78": "A pivot means the slope changes. Does &minus;%s/%s "
                                "depend on m?" % (PH, PC),
            "ed9e0981cfbc056b": "A pivot means the slope changes. Does &minus;%s/%s "
                                "depend on m?" % (PH, PC),
            "02f71e8f73c7429b": "Both intercepts are m divided by a price. What "
                                "happens to them when m halves?",
        },
        explain="Both intercepts halve and the slope stays put, so the line "
                "shifts in, parallel to itself."),

    Question(
        "a6",
        "Back to the original income. A carbon levy doubles the price of "
        "heating, %s. What happens to the budget line?" % PH,
        choices=MOVES,
        answers=["ed0d51a0dc63777e"],
        mistakes={
            "4bf2e9503704f24c": "Does the slope &minus;%s/%s change when %s doubles?"
                                % (PH, PC, PH),
            "263edb86d69045b7": "Which intercept has %s in it: m/%s or m/%s? "
                                "The other one stays put." % (PH, PC, PH),
            "4e83ccdd366af4f8": "Look at the two intercepts m/%s and m/%s. Does "
                                "either of them change?" % (PC, PH),
        },
        explain="Only m/%s moves, so the line pivots inward around the "
                "c-intercept." % PH),

    Question(
        "a7",
        "With the levy in place, find the new h-intercept and the new slope.",
        form=["h-intercept =", BOX, "&nbsp; slope =", BOX],
        answers=["25d54773dd4d59da", "7301cd409f70dfa6"],
        mistakes={
            "4a9e5f9a994d5b09": "That is the old h-intercept. Use the new %s." % PH,
            "a5910af9421f0ced": "That is the old slope. Use the new %s." % PH,
            "bce49cb2dfdd81f7": "Check the sign of the slope.",
            "0827dae8a3833d35": "The slope is upside down: &minus;%s/%s." % (PH, PC),
        },
        hints=["Use the same formulas as before with the new price of heating."],
        explain="Heating's intercept halves and the line gets twice as steep."),

    Question(
        "a8",
        "Last one. Both prices and income double at the same time. What "
        "happens to the budget line?",
        choices=MOVES,
        answers=["72b4adfbd9cab661"],
        mistakes={
            "8c5371296ddfa497": "Compute the new intercepts: 2m over 2%s, and 2m "
                                "over 2%s." % (PC, PH),
            "8919273898773e7d": "Compute the new slope: &minus;2%s / 2%s." % (PH, PC),
            "ef55d592744e80f6": "Compute the new slope: &minus;2%s / 2%s." % (PH, PC),
        },
        explain="Every 2 cancels. A budget line only knows relative prices and "
                "real income."),
]

sondre = GuidedProblem(
    "Part 1 &middot; Sondre's budget line",
    "Sondre spends his whole income <i>m</i> = 90 on heating <i>h</i> and a "
    "basket of other goods <i>c</i>. The basket costs %s = 1 and heating costs "
    "%s = 3. Heating goes on the horizontal axis. Each right answer draws the "
    "next piece of the figure." % (PC, PH),
    SONDRE_QUESTIONS,
    draw_sondre,
    outro="You built the budget line and moved it three ways. Part 2 does the "
          "same for Kari's leisure budget.",
    sources=[PS("A2.1"), NOTES("p. 1&ndash;3")],
)


# ======================================================================
# Part 2: Kari's leisure budget (A2.2)
# ======================================================================
# Leisure L across, consumption C up. T = 120, w = 25, V = 600, basket price
# 1, so C = w(T - L) + V. The lesson is the endowment E = (T, V): no wage or
# tax can move it, because if she does not work there is nothing to tax.

T, W_K, V = 120.0, 25.0, 600.0
TAX = 0.4
W_UP = 30.0               # only for the picture of a wage rise: any w' > w
TAXED = "#0891b2"         # the after-tax line


def _leisure_line(ax, w, v, **kw):
    ax.plot([0, T], [w * T + v, v], **kw)


def draw_kari(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    # Room to the right of T: every line meets at E, so E's labels go out
    # there, where nothing else is drawn.
    ax.set_xlim(0, 158)
    ax.set_ylim(0, 4700)

    if stage == 0:
        ax.text(0.5, 0.5, "Answer step 1 to start drawing.", transform=ax.transAxes,
                ha="center", va="center", color=MUTE, fontsize=11)
        return

    ax.set_xlabel("L   (leisure)", color=INK, fontsize=10, loc="right")
    ax.set_ylabel("C   (consumption)", color=INK, fontsize=10, loc="top")
    ax.text(-1.5, -60, "0", color=MUTE, ha="right", va="top", fontsize=9)

    # Step 2: the endowment. T sits on the axis, E straight above it.
    if stage >= 2:
        ax.plot([T, T], [0, V], color=MUTE, lw=1, ls=":")
        ax.annotate(r"$T$", (T, 0), textcoords="offset points", xytext=(0, -14),
                    ha="center", color=INK, fontsize=11, annotation_clip=False)
        ax.plot([T], [V], "s", color=LINE, ms=7, zorder=6)
        ax.annotate(r"$E = (T,\,V)$", (T, V), textcoords="offset points",
                    xytext=(8, 2), ha="left", color=LINE, fontsize=11)

    # Step 3: full income, work every waking hour.
    if stage >= 3:
        _dot(ax, 0, W_K * T + V, r"$wT + V$", 8, -4)

    if stage < 4:
        return

    # Step 4: the line, the choice set under it, and which way is work.
    _leisure_line(ax, W_K, V, color=LINE, lw=2.2, zorder=4,
                  label=r"budget line, slope $-\,w$")
    ax.fill_between([0, T], [W_K * T + V, V], 0, color=FILL, alpha=0.08, lw=0)
    ax.annotate("", xy=(T - 38, 110), xytext=(T - 2, 110),
                arrowprops=dict(arrowstyle="->", color=MUTE, lw=1.2))
    ax.text(T - 40, 110, r"work more: $h = T - L$  ", color=MUTE, fontsize=9.5,
            ha="right", va="center")

    fade = lambda since: 1.0 if stage == since else 0.4

    # Step 5: a wage rise pivots around E, because E has no wage in it.
    if stage >= 5:
        _leisure_line(ax, W_UP, V, color=NEW, lw=2, ls="--", zorder=4,
                      alpha=fade(5), label=r"$w\uparrow$: pivot around $E$")

    # Step 6: the labour tax is a wage cut, so the same pivot, inward.
    if stage >= 6:
        _leisure_line(ax, (1 - TAX) * W_K, V, color=TAXED, lw=2, ls="--",
                      zorder=4, alpha=fade(6),
                      label=r"tax $t$: slope $-(1-t)\,w$")
        _dot(ax, 0, (1 - TAX) * W_K * T + V, r"$(1-t)\,wT + V$", 8, -4,
             colour=TAXED)

    # Step 7: a cut in V is income, not a price: E itself drops.
    if stage >= 7:
        _leisure_line(ax, W_K, V / 2, color=HALF, lw=2, ls="--", zorder=4,
                      label=r"$V \to V/2$: shift, $E$ moves down")
        ax.plot([T], [V / 2], "s", color=HALF, ms=7, zorder=6)
        ax.annotate(r"$E' = (T,\,V/2)$", (T, V / 2), textcoords="offset points",
                    xytext=(8, -6), ha="left", color=HALF, fontsize=11)

    leg = ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    for text in leg.get_texts():
        text.set_color(INK)


E_FIX = "The endowment point E stays put"
CI_FIX = "The C-intercept (full income) stays put"
PAR = "Neither: the line shifts parallel"
NOMOVE = "The line does not move"
DOWN = "It shifts down, parallel, and E moves down with it"
PIV_E = "It pivots around E"
PIV_CI = "It pivots around the C-intercept"

KARI_QUESTIONS = [
    Question(
        "b1",
        "Kari consumes what she earns from working plus the transfer. Fill in "
        "her budget constraint.",
        form=["C =", BOX, "&middot; (120 &minus; L) &nbsp;+", BOX],
        answers=["0bd7405df02f6cb4", "9bb8a46f3483ac54"],
        mistakes={
            "dcd06ce66aec113c": "Which number is paid per hour worked, and which "
                                "arrives whatever she does?",
            "9bd8e86d8f45e59e": "Which number is paid per hour worked, and which "
                                "arrives whatever she does?",
        },
        hints=["120 &minus; L is the hours she works. What does each hour pay?"],
        explain="C = w(T &minus; L) + V. The axes are up."),

    Question(
        "b2",
        "Kari does not work at all. Where is she? This is her endowment point E.",
        form=["L =", BOX, "&nbsp; C =", BOX],
        answers=["7338ddbb1133a174", "84f811c12a6051f3"],
        mistakes={
            "94db4be15a7efe89": "If she does not work, how much of her time is leisure?",
            "1792d2cf9afb162c": "She still receives the transfer.",
            "68493952224f2a0e": "That is what she gets by working every hour. "
                                "Here she works none.",
        },
        hints=["Not working means h = 0, so L = T. Put that into the budget."],
        explain="E = (T, V): keep all your time and you still have the transfer."),

    Question(
        "b3",
        "Now the other end: Kari works every waking hour, so L = 0. How much "
        "can she consume? This is her full income.",
        form=["C =", BOX],
        answers=["49de35a53fc60f56"],
        mistakes={
            "84bd4b9e3095cb04": "Don't forget the transfer V on top of her earnings.",
            "9ce03b32ab930b9f": "That is the endowment, where she works zero hours.",
        },
        hints=["Set L = 0 in the budget constraint."],
        explain="Full income is wT + V, the C-intercept."),

    Question(
        "b4",
        "What is the slope of the budget line, dC/dL?",
        form=["dC/dL =", BOX],
        answers=["3a29333297c0147c"],
        mistakes={
            "194bf6b85827e71d": "Right size, wrong sign: more leisure means less "
                                "consumption.",
            "02e49fdc5b0ad017": "Upside down. One more hour of leisure costs how "
                                "much consumption?",
        },
        hints=["Multiply out C = w(T &minus; L) + V. The number in front of L is "
               "the slope."],
        explain="The slope is &minus;w: the wage is the price of an hour of leisure."),

    Question(
        "b5",
        "Kari's wage rises. Which point on her budget line stays where it is?",
        choices=[E_FIX, CI_FIX, PAR, NOMOVE],
        answers=["6c5c6064e812e03e"],
        mistakes={
            "82403bfee4aa0ab9": "Full income is wT + V. Does it have w in it?",
            "be3381b3e27947ca": "The slope is &minus;w. Does it change when w rises?",
            "d4f1fb4e4e9b9c72": "The slope is &minus;w. Does it change when w rises?",
        },
        explain="E = (T, V) has no w in it, so the line pivots around E. Unlike "
                "a banana price, a higher wage also makes Kari richer: full "
                "income wT + V rises."),

    Question(
        "b6",
        "Back to w = 25. The government taxes labour income at 40%, but the "
        "transfer V is not taxed. What does Kari keep per hour worked, and "
        "what is her new full income?",
        form=["net wage =", BOX, "&nbsp; full income =", BOX],
        answers=["720b38cfc78cdfd2", "8127f0e2a114002e"],
        mistakes={
            "5970d7c6241ac7ae": "That is the tax per hour. What does she keep?",
            "842753445ea8f2b9": "That is the share she keeps. Multiply it by the wage.",
            "159a10823893a4eb": "Don't forget V. It is not taxed.",
            "59c07bb4b34c9487": "That is full income without the tax.",
        },
        hints=["The net wage is (1 &minus; t)w. Full income uses the net wage."],
        explain="The tax is a wage cut to (1 &minus; t)w. The line pivots in "
                "around E: if she doesn't work, there is nothing to tax."),

    Question(
        "b7",
        "No tax again. The transfer V is cut in half. What happens to the "
        "budget line?",
        choices=[DOWN, PIV_E, PIV_CI, SAME],
        answers=["46e69b248fdb3e8f"],
        mistakes={
            "359e3f0d11b23cdb": "A pivot changes the slope &minus;w. Does V change it? "
                                "And look at E = (T, V): does it stay put?",
            "68985ce20f8f46b7": "A pivot changes the slope &minus;w. Does V change it?",
            "9d692219df07cd31": "Both E = (T, V) and wT + V contain V.",
        },
        explain="V is income, not a price. The slope stays &minus;w, and the whole "
                "line drops by the cut, E included."),
]

kari = GuidedProblem(
    "Part 2 &middot; Kari's leisure budget",
    "Kari has <i>T</i> = 120 waking hours a week, split between leisure "
    "<i>L</i> and work <i>h</i> = <i>T</i> &minus; <i>L</i>. Her wage is "
    "<i>w</i> = 25 and she receives a transfer <i>V</i> = 600 whether she "
    "works or not. The consumption basket costs 1. Leisure goes on the "
    "horizontal axis.",
    KARI_QUESTIONS,
    draw_kari,
    outro="A wage change pivots the line around E; an income change moves E "
          "itself. Part 3 turns from what Kari can afford to what she wants.",
    sources=[PS("A2.2"), NOTES("p. 3&ndash;5")],
)


# ======================================================================
# Part 3: indifference curves and the MRS (the notes' U = xy example)
# ======================================================================

A_PT, B_PT, Z_PT = (2.0, 4.0), (4.0, 2.0), (3.0, 6.0)


def _hyperbola(ax, level, **kw):
    import numpy as np
    xs = np.linspace(level / 9.4, 9.0, 300)
    ax.plot(xs, level / xs, **kw)


def _tangent(ax, pt, slope, half, label, dx, dy):
    # The label hangs below-left of the bundle, under both the curve and the
    # tangent, which is the one patch of the picture that is always empty.
    x0, y0 = pt
    ax.plot([x0 - half, x0 + half], [y0 - slope * half, y0 + slope * half],
            color=NEW, lw=2, zorder=5)
    ax.annotate(label, pt, textcoords="offset points", xytext=(dx, dy),
                ha="right", va="top", color=NEW, fontsize=10)


def draw_curves(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9.5)
    ax.set_xlabel("x", color=INK, fontsize=11, loc="right")
    ax.set_ylabel("y", color=INK, fontsize=11, loc="top", rotation=0)
    ax.text(-0.1, -0.1, "0", color=MUTE, ha="right", va="top", fontsize=9)

    # Bundle a is given in the question, so it is there from the start.
    ax.plot(*A_PT, "o", color=CURVE, ms=7, zorder=6)
    ax.annotate(r"$a$", A_PT, textcoords="offset points", xytext=(8, 4),
                color=CURVE, fontsize=12)

    # Step 1: utility at a fixes the curve through it.
    if stage >= 1:
        level = A_PT[0] * A_PT[1]
        if stage >= 6:
            # Step 6: everything above the curve is preferred to a.
            import numpy as np
            xs = np.linspace(level / 9.4, 9.0, 300)
            ax.fill_between(xs, level / xs, 9.5, color=CURVE, alpha=0.06, lw=0)
            ax.text(6.2, 7.6, "preferred to $a$", color=CURVE, alpha=0.8,
                    fontsize=10)
        _hyperbola(ax, level, color=CURVE, lw=2.2, zorder=4)
        ax.text(7.6, level / 7.6 + 0.3, r"$U = U_0$", color=CURVE, fontsize=11)

    # Step 2: a second bundle on the same curve.
    if stage >= 2:
        ax.plot(*B_PT, "o", color=CURVE, ms=7, zorder=6)
        ax.annotate(r"$b$", B_PT, textcoords="offset points", xytext=(0, 10),
                    ha="center", color=CURVE, fontsize=12)

    # Steps 3 and 4: the slope at each bundle. Steep where y is plentiful,
    # flat where it is scarce: the same person, a different willingness.
    if stage >= 3:
        _tangent(ax, A_PT, -A_PT[1] / A_PT[0], 0.8, "steep", -10, -6)
    if stage >= 4:
        _tangent(ax, B_PT, -B_PT[1] / B_PT[0], 1.6, "flat", -8, -12)

    if stage >= 5:
        ax.text(5.0, 4.6, r"$MRS = \frac{dy}{dx} = -\frac{U_x}{U_y} = -\frac{y}{x}$",
                color=INK, fontsize=12)

    # Step 6: more of both is a higher curve (monotonicity).
    if stage >= 6:
        level = Z_PT[0] * Z_PT[1]
        _hyperbola(ax, level, color=CURVE, lw=1.6, ls="--", alpha=0.7, zorder=4)
        ax.plot(*Z_PT, "o", color=CURVE, ms=7, zorder=6)
        ax.annotate(r"$z$", Z_PT, textcoords="offset points", xytext=(8, 2),
                    color=CURVE, fontsize=12)
        ax.text(7.6, level / 7.6 + 0.3, r"$U_1 > U_0$", color=CURVE, fontsize=11)

    if stage >= 7:
        ax.text(0.98, 0.02, "one curve through every bundle, and they never cross",
                transform=ax.transAxes, ha="right", va="bottom", color=MUTE,
                fontsize=9.5)


SCARCE = "Along the curve y gets scarcer, so each extra x is worth less y"
UFALLS = "Utility falls as you move down the curve"
PRICES = "The prices change along the curve"
CONST = "It doesn't: the MRS is the same everywhere"
HIGHER = "On a higher indifference curve"
SAMEC = "On the same indifference curve"
LOWER = "On a lower indifference curve"
DEPENDS = "It depends on the utility numbers"
NOCROSS = "No: it would break transitivity"
YES_ODD = "Yes, if the person's tastes are unusual"
YES_ONE = "Yes, but only at one bundle"
YES_SUB = "Only for perfect substitutes"

CURVE_QUESTIONS = [
    Question(
        "c1",
        "A person has utility U = x&middot;y. What utility does bundle "
        "a = (2, 4) give?",
        form=["U(a) =", BOX],
        answers=["27c221fca1a74071"],
        mistakes={"d958a4e2f18d815d": "U is x <i>times</i> y, not x plus y."},
        explain="Every bundle with x&middot;y = U<sub>0</sub> is on the same "
                "indifference curve as a."),

    Question(
        "c2",
        "Bundle b has x = 4 and sits on the same indifference curve as a. "
        "What is its y?",
        form=["y =", BOX],
        answers=["3ccdaf2ecc13452a"],
        mistakes={"dde779a40d2b2389": "Same curve means the same utility: x&middot;y "
                                      "must equal U(a)."},
        hints=["Solve x&middot;y = U(a) for y with x = 4."],
        explain="a and b are equally good: the person is indifferent between them."),

    Question(
        "c3",
        "What is the slope of the indifference curve, dy/dx, at a = (2, 4)?",
        form=["dy/dx =", BOX],
        answers=["7b608b21ef0f41c2"],
        mistakes={
            "3eb712355ac8687a": "Right size, wrong sign: indifference curves slope "
                                "down.",
            "714a1c2ee8861c8f": "Upside down. dy/dx = &minus;U<sub>x</sub>/U<sub>y</sub>.",
        },
        hints=["Along the curve dU = U<sub>x</sub> dx + U<sub>y</sub> dy = 0, so "
               "dy/dx = &minus;U<sub>x</sub>/U<sub>y</sub>.",
               "With U = x&middot;y, U<sub>x</sub> = y and U<sub>y</sub> = x."],
        explain="dy/dx = &minus;y/x. At a the person would give up 2 units of y "
                "for one more x."),

    Question(
        "c4",
        "And at b = (4, 2)?",
        form=["dy/dx =", BOX],
        answers=["35ca857b5ae9dd6d"],
        mistakes={
            "07583e1ed063de28": "Right size, wrong sign.",
            "997f0890891c8bee": "That is the slope at a. Use b's x and y.",
        },
        hints=["Same formula, dy/dx = &minus;y/x, at the new bundle."],
        explain="At b the person gives up only half a unit of y for one more x."),

    Question(
        "c5",
        "Same person, same curve, but very different willingness to trade at a "
        "and at b. Why does the curve get flatter as x grows?",
        choices=[SCARCE, UFALLS, PRICES, CONST],
        answers=["321a2716fb341f14"],
        mistakes={
            "0b1ad06ad26a447b": "Every point on one indifference curve has the "
                                "same utility.",
            "0f87add3adb317a8": "There are no prices in an indifference curve. It "
                                "is about taste only.",
            "99271600b7064199": "Compare your answers at a and at b.",
        },
        explain="That is convexity: the MRS falls as you move along the curve, so "
                "averages beat extremes."),

    Question(
        "c6",
        "Bundle z has more of both goods than a. Where does z lie?",
        choices=[HIGHER, SAMEC, LOWER, DEPENDS],
        answers=["bcfec37c6d4681a2"],
        mistakes={
            "f32a5dd1169ce74d": "To stay on a curve you must give something up. "
                                "Did z give anything up?",
            "2f97ad901a577af4": "More is better (monotonicity).",
            "36766268e3269567": "Utility is ordinal, but the ranking is not up for "
                                "grabs: more of both is better.",
        },
        explain="Monotonicity: more is better, so better lies to the northeast."),

    Question(
        "c7",
        "Can two of the same person's indifference curves cross?",
        choices=[NOCROSS, YES_ODD, YES_ONE, YES_SUB],
        answers=["4d9be326340768d4"],
        mistakes={
            "dffb6d966f22a289": "Different people's curves can cross. What about "
                                "one person's own curves?",
            "c7b5d347d0bbcc9b": "Suppose they cross at one bundle. That bundle is "
                                "indifferent to points on both curves. Now use "
                                "monotonicity.",
            "1ad35f05b06ae1d2": "Straight-line curves are still one person's curves. "
                                "The same logic applies.",
        },
        explain="At the crossing, transitivity would make two bundles equally good "
                "even though one has more of both."),
]

curves = GuidedProblem(
    "Part 3 &middot; Indifference curves and the MRS",
    "A person's tastes are U = <i>x</i>&middot;<i>y</i>. Bundle <i>a</i> = (2, 4) "
    "is marked. Find the curve it sits on, then measure how willing the person "
    "is to trade along it.",
    CURVE_QUESTIONS,
    draw_curves,
    outro="The MRS is what you are <i>willing</i> to give up; the budget slope is "
          "what the market <i>requires</i>. Session 2's optimum is where the two "
          "meet, and that is the problem set.",
    sources=[NOTES("p. 5&ndash;9"), NOTES("p. 14, review questions 3 and 5")],
)


# ======================================================================
# Part 4: which family? (review question 4)
# ======================================================================

CD, SUB, COM, QL = ("Cobb-Douglas", "Perfect substitutes", "Perfect complements",
                    "Quasilinear")

# (who, x-axis good, y-axis good, family, formula) in question order.
PEOPLE = [
    ("Ali", "oat milk", "cow milk", SUB, r"$U = \alpha x_1 + \beta x_2$"),
    ("Berit", "skis", "ski boots", COM, r"$U = \min\{\alpha x_1, \beta x_2\}$"),
    ("Carl", "food", "housing", CD, r"$U = x_1^{\alpha} x_2^{\beta}$"),
    ("Dina", "phone plan", "everything else", QL, r"$U = \ln x_1 + x_2$"),
]


def _family_curves(ax, family):
    import numpy as np
    style = dict(color=CURVE, lw=1.8)
    if family == SUB:
        for k in (2.0, 3.5, 5.0):
            ax.plot([0, k], [k, 0], **style)
    elif family == COM:
        for k in (1.2, 2.2, 3.2):
            ax.plot([k, k, 5.8], [5.8, k, k], **style)
    elif family == CD:
        xs = np.linspace(0.25, 5.8, 200)
        for k in (1.5, 3.5, 6.5):
            ax.plot(xs, k / xs, **style)
    else:
        xs = np.linspace(0.2, 5.8, 200)
        for k in (2.0, 3.2, 4.4):
            ax.plot(xs, k - 0.9 * np.log(xs), **style)


def draw_families(fig, stage):
    axes = fig.subplots(2, 2)
    for i, (ax, (who, gx, gy, family, formula)) in enumerate(zip(axes.flat, PEOPLE)):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_xlabel(gx, color=MUTE, fontsize=8.5, loc="right")
        ax.set_ylabel(gy, color=MUTE, fontsize=8.5, loc="top")
        if stage > i:
            # Formula in the title, not on the panel: the L-shapes and lines
            # fill the corners where it would otherwise sit.
            _family_curves(ax, family)
            ax.set_title("%s: %s\n%s" % (who, family, formula), color=INK,
                         fontsize=9.5, loc="left")
        else:
            ax.set_title("%s\n " % who, color=MUTE, fontsize=9.5, loc="left")
            ax.text(3, 3, "?", ha="center", va="center", color=MUTE, fontsize=28)
    fig.subplots_adjust(hspace=0.45, wspace=0.25)


FAMILIES = [CD, SUB, COM, QL]

FAMILY_QUESTIONS = [
    Question(
        "d1",
        "Ali treats oat milk and cow milk as interchangeable, one for one. "
        "Which utility family describes him?",
        choices=FAMILIES,
        answers=["8b857542cea28eae"],
        mistakes={
            "cea9805b45bef7c5": "Does Ali want a mix for its own sake? He swaps one "
                                "for the other at a fixed rate.",
            "4c177e50b8b36359": "Complements are used together in a fixed ratio. Ali "
                                "uses one <i>instead</i> of the other.",
            "1e170d7093df50a9": "For Ali the rate of exchange never changes, whatever "
                                "he already has.",
        },
        explain="Straight-line curves: a constant MRS, and the optimum is usually "
                "a corner."),

    Question(
        "d2",
        "Berit uses exactly one ski boot per ski. An extra ski or an extra boot "
        "on its own is useless to her. Which family?",
        choices=FAMILIES,
        answers=["faa80694894a4a9e"],
        mistakes={
            "08ff3e2c5b1f2bbb": "With Cobb-Douglas, more of one good always helps a "
                                "little. Does an extra ski help Berit?",
            "4601b370377da867": "Can a boot replace a ski?",
            "d99c2f3a3f42e69f": "Does either good give her value on its own?",
        },
        explain="L-shaped curves: the optimum sits on the kink, where tangency "
                "is not defined."),

    Question(
        "d3",
        "Carl always spends the same share of his budget on food and on housing, "
        "whatever the prices. Which family?",
        choices=FAMILIES,
        answers=["806ca4b1c8718e25"],
        mistakes={
            "d93d57c7818d343a": "Substitutes put everything on the cheaper good. Carl "
                                "always buys both.",
            "a1b38f0d7fd398ec": "Complements fix the ratio of <i>quantities</i>. Carl "
                                "fixes the ratio of <i>spending</i>.",
            "93c10fea3d0ca671": "Which family made the exponents the budget shares in "
                                "Sondre's problem?",
        },
        explain="Cobb-Douglas: the exponents are the budget shares."),

    Question(
        "d4",
        "Dina values her phone plan in money terms, with diminishing value, and "
        "values everything else linearly. Which family?",
        choices=FAMILIES,
        answers=["a63f06f7b3af5dce"],
        mistakes={
            "19b64f62bfe89bca": "In Cobb-Douglas neither good is valued linearly.",
            "47829ff832078c0a": "Substitutes are linear in both goods, but her phone "
                                "plan has diminishing value.",
            "9feaf05c2556535b": "Does she need the two in a fixed ratio?",
        },
        explain="Quasilinear: curved in one good, linear in the other. The curves "
                "are vertical shifts of each other, so extra income never changes "
                "the phone plan."),
]

families = GuidedProblem(
    "Part 4 &middot; Which utility family?",
    "Four consumers describe their tastes. Match each one to a utility family "
    "from the session. Each right answer draws that person's indifference curves.",
    FAMILY_QUESTIONS,
    draw_families,
    figsize=(6.4, 5.2),
    whole_figure=True,
    outro="That is session 2. Next session puts the budget and the curves "
          "together and moves the prices.",
    sources=[NOTES("p. 8 and p. 14, review question 4")],
)


# ======================================================================
# Where every step comes from
# ======================================================================
# One table, so it can be checked against the course material in one place.
# "Try it" means the "Try it before reading on" boxes in the notes: the first
# (goods budget) on p. 2, the second (leisure budget) on p. 5.

STEP_SOURCES = {
    "a1": PS("A2.1 (a)"),
    "a2": PS("A2.1 (a)"),
    "a3": PS("A2.1 (a)"),
    "a4": PS("A2.1 (a)"),
    "a5": NOTES("p. 2 &middot; Try it (d)"),
    "a6": PS("A2.1 (e)"),
    "a7": PS("A2.1 (e)"),
    "a8": NOTES("p. 2 &middot; Try it (f)"),

    "b1": PS("A2.2 (a)"),
    "b2": PS("A2.2 (a)"),
    "b3": PS("A2.2 (a)"),
    "b4": PS("A2.2 (a)"),
    "b5": NOTES("p. 4&ndash;5 &middot; Try it (c)"),
    "b6": PS("A2.2 (c)"),
    "b7": NOTES("p. 5 &middot; Try it (d)"),

    "c1": NOTES("p. 9 &middot; MRS example"),
    "c2": NOTES("p. 9 &middot; MRS example"),
    "c3": NOTES("p. 9 &middot; MRS example"),
    "c4": NOTES("p. 9 &middot; MRS example"),
    "c5": NOTES("p. 9 &middot; MRS example"),
    "c6": NOTES("p. 6 &middot; indifference curves"),
    "c7": NOTES("p. 14 &middot; review question 3"),

    "d1": NOTES("p. 14 &middot; review question 4"),
    "d2": NOTES("p. 14 &middot; review question 4"),
    "d3": NOTES("p. 14 &middot; review question 4"),
    "d4": NOTES("p. 14 &middot; review question 4"),
}

for _q in SONDRE_QUESTIONS + KARI_QUESTIONS + CURVE_QUESTIONS + FAMILY_QUESTIONS:
    _q.source = STEP_SOURCES[_q.qid]
