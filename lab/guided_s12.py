"""
guided_s12.py - session 12 guided page: static games and Nash equilibrium.

    Part 1  dilemma     the normal form and the advertising game (review
                        question 1)
    Part 2  coordinate  coordination: the AI build-out, the stag hunt and the
                        data standard (warm-up W2, review question 3)
    Part 3  iesds       iterated elimination of strictly dominated strategies:
                        the 3x3 game, the memory lines, review question 2
    Part 4  cournot     best responses, Nash equilibrium and Cournot: the API
                        market and the talent war
    Part 5  bertrand    prices instead of quantities: Bertrand, the Try it,
                        the ferries and the worksheet's power duopoly
    Part 6  mixed       mixed strategies: the penalty kick, the release game
                        and the striker (warm-up W1, review question 6)
    Part 7  standard    problem A12.1: Kvist and Lundin pick a standard
    Part 8  audit       problem A12.2: the tax authority and Berg AS
    Part 9  flatmates   problem A12.3: two games with a continuum of actions

Answers are hashes in answers_s12.py, generated from
answer_keys/s12_keys.py in the private repo. The maths is games.py: its
self-check reproduces every number asked for here.
"""

import numpy as np

import game_plots as gm
import guided_plots as gp
from games import Matrix
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, INK, LINE, MUTE, NEW

H, M = answers("s12")

# The course's games. Rows are player 1, columns player 2.
ADVERTISE = Matrix(["Advertise", "No ad"], ["Advertise", "No ad"],
                   [[(-2, -2), (3, -3)], [(-3, 3), (0, 0)]])
BUILD = Matrix(["Invest", "Wait"], ["Invest", "Wait"], [[(2, 2), (-1, 0)], [(0, -1), (1, 1)]])
DATA = Matrix(["A", "B"], ["A", "B"], [[(5, 3), (1, 1)], [(0, 0), (3, 5)]])
GRID = Matrix(["A1", "A2", "A3"], ["B1", "B2", "B3"],
              [[(2, 3), (1, 4), (3, 2)], [(4, 1), (2, 2), (2, 0)], [(3, 3), (0, 5), (2, 1)]])
PITCH = Matrix(["T", "M", "B"], ["L", "C", "R"],
               [[(3, 5), (1, 4), (2, 2)], [(4, 2), (2, 3), (1, 1)], [(2, 1), (0, 2), (3, 0)]])
TALENT = Matrix(["C", "T"], ["C", "T"], [[(3, 3), (1, 4)], [(4, 1), (2, 2)]])
KICK = Matrix(["L", "R"], ["L", "R"], [[(-1, 1), (1, -1)], [(1, -1), (-1, 1)]])
RELEASE = Matrix(["March", "Sept"], ["March", "Sept"], [[(0, 3), (2, 0)], [(3, 0), (0, 1)]])
STANDARD = Matrix(["X", "Y", "A"], ["X", "Y", "A"],
                  [[(6, 6), (2, 2), (3, 1)], [(2, 2), (4, 4), (3, 1)], [(1, 3), (1, 3), (2, 2)]])
AUDIT = Matrix(["Evade", "Comply"], ["Audit", "Not"], [[(-20, 10), (30, -30)], [(0, -5), (0, 0)]])


# ------------------------------------------------------------------ drawing ---

def _panel(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.tick_params(colors=MUTE, labelsize=8.5)


def _br_lines(ax, a, b, top, names=("BR$_1$", "BR$_2$")):
    # Linear best responses t_i = (a + b t_j)/2 for both players, player 2's
    # quantity across and player 1's up, as in the notes' figure.
    t = np.linspace(0, top, 200)
    ax.plot(t, np.clip((a + b * t) / 2, 0, None), color=LINE, lw=2, label=names[0])
    ax.plot(np.clip((a + b * t) / 2, 0, None), t, color=CURVE, lw=2, label=names[1])


def _lines(ax, lo_hi, labels, colours, title, xlabel):
    # Two expected-payoff lines against the opponent's probability q.
    for (lo, hi), label, colour in zip(lo_hi, labels, colours):
        ax.plot([0, 1], [lo, hi], color=colour, lw=2, label=label)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xlim(0, 1)
    ax.set_xlabel(xlabel, color=INK, fontsize=9, loc="right")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=MUTE, labelsize=8.5)


# ======================================================================
# Part 1: the normal form and the advertising game
# ======================================================================

def draw_dilemma(ax, stage):
    gm.matrix(ax, ADVERTISE, "OpenAI", "Anthropic", best=stage >= 3,
              nash=ADVERTISE.pure_nash() if stage >= 3 else (),
              mark=(0, 1) if stage == 0 else None)


DOMINANT = "Advertise is strictly dominant for both labs, so both advertise and get -2 each, although not advertising would give both 0"
DOM_NONE = "Neither lab has a dominant strategy, so the outcome is unpredictable"
DOM_ZERO = "Both refrain, since (0, 0) is better for both"
DOM_ONE = "Only OpenAI advertises, since it moves first"

DILEMMA = "Each lab does the individually rational thing and together they land somewhere collectively bad: the better cell (0, 0) is not an equilibrium, since each would deviate from it"
DIL_IRR = "The labs are irrational: they should both stop advertising"
DIL_ZERO = "It is zero-sum: one lab's gain is the other's loss in every cell"
DIL_COORD = "It is a coordination game with two equilibria"

NORMAL = "The players, their strategy sets and the payoff functions; complete information adds that all of this is common knowledge; static rules out moving in sequence or observing the rival first"
NORM_ORDER = "The order of moves and what each bakery saw; static rules out uncertainty"
NORM_PRICE = "The market price and the demand curve; static rules out entry"
NORM_ONE = "One bakery's options and payoffs; complete information means the other bakery is irrational"

DILEMMA_QUESTIONS = [
    Question(
        "d1",
        "The advertising game, OpenAI on the rows and Anthropic on the columns. Read the outlined "
        "cell: OpenAI advertises and Anthropic does not. The payoffs, OpenAI first?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("d1.0"), H("d1.1")],
        mistakes=M({"d1.0~-3": "Row player first: OpenAI is on the rows."}),
        explain="One cell holds both payoffs at one pair of strategies."),
    Question(
        "d2",
        "OpenAI's reasoning. If Anthropic advertises, OpenAI compares advertising with not; if "
        "Anthropic does not, the same. The four payoffs?",
        form=["Anthropic ads: advertise", BOX, "no ad", BOX, "&nbsp; no ads: advertise", BOX,
              "no ad", BOX],
        answers=[H("d2.0"), H("d2.1"), H("d2.2"), H("d2.3")],
        mistakes=M({"d2.1~3": "Read OpenAI's payoff, the first number, in the No ad row."}),
        explain="&minus;2 &gt; &minus;3 and 3 &gt; 0: advertising wins in both columns."),
    Question(
        "d3",
        "So what happens?",
        choices=[DOMINANT, DOM_NONE, DOM_ZERO, DOM_ONE],
        answers=[H("d3.c")],
        mistakes=M({
            "d3.c~" + DOM_NONE: "Compare the rows column by column: one wins in both.",
            "d3.c~" + DOM_ZERO: "From (0, 0), each lab gains 3 by advertising alone.",
            "d3.c~" + DOM_ONE: "The moves are simultaneous.",
        }),
        explain="A strict dominant strategy equilibrium: rare, and that is why it feels "
                "inevitable."),
    Question(
        "d4",
        "Why is this a prisoner's dilemma?",
        choices=[DILEMMA, DIL_IRR, DIL_ZERO, DIL_COORD],
        answers=[H("d4.c")],
        mistakes=M({
            "d4.c~" + DIL_IRR: "Each choice is a best response: perfectly rational.",
            "d4.c~" + DIL_ZERO: "(&minus;2, &minus;2) adds to &minus;4 and (0, 0) to 0.",
            "d4.c~" + DIL_COORD: "There is only one equilibrium here.",
        }),
        explain="Session 15 asks whether repeated play can get them to (0, 0)."),
    Question(
        "d5",
        "Review question 1: Kari's and Ola's bakeries each decide, simultaneously and once, "
        "whether to open on Sundays. What does the normal form need, and what do 'complete "
        "information' and 'static' add?",
        choices=[NORMAL, NORM_ORDER, NORM_PRICE, NORM_ONE],
        answers=[H("d5.c")],
        mistakes=M({
            "d5.c~" + NORM_ORDER: "The order of moves is what the normal form leaves out.",
            "d5.c~" + NORM_PRICE: "A game is players, strategies and payoffs.",
            "d5.c~" + NORM_ONE: "Both players, and common knowledge of rationality.",
        }),
        explain="N, {S<sub>i</sub>} and {v<sub>i</sub>}: list them for the story."),
]

dilemma = GuidedProblem(
    "Part 1 &middot; The normal form and the advertising game",
    "Players, strategies and payoffs. Rows are player 1's strategies, columns player 2's, and "
    "each cell lists player 1's payoff first.",
    DILEMMA_QUESTIONS, draw_dilemma, figsize=(5.6, 3.6),
    outro="Underlined: each player's best response. Shaded: where both are best responses.",
    sources=[NOTES("p. 1&ndash;5"), NOTES("p. 15, review question 1")],
)


# ======================================================================
# Part 2: coordination games
# ======================================================================

def draw_coordinate(fig, stage):
    left, right = fig.subplots(1, 2)
    gm.matrix(left, BUILD, "OpenAI", "Anthropic", best=stage >= 1,
              nash=BUILD.pure_nash() if stage >= 2 else (), title="The AI build-out")
    if stage >= 3:
        gm.matrix(right, DATA, "Nordapp", "Fjordsoft", best=stage >= 4,
                  nash=DATA.pure_nash() if stage >= 4 else (), title="Review question 3")
    else:
        right.axis("off")


BUILD_NE = "Both invest, and both wait: each is self-confirming, nobody is tempted to leave the good one, and the problem is getting there"
BUILD_ONE = "Only both investing: waiting is dominated"
BUILD_NONE = "None: each lab wants to do the opposite of the other"
BUILD_MIX = "Only one lab invests, whichever moves first"

DATA_NE = "Both A and both B are Nash equilibria, and neither firm has a dominant strategy: each wants to match the other"
DATA_DOM = "A is dominant for Nordapp, so the only equilibrium is both A"
DATA_NONE = "There is no pure equilibrium, as in the penalty kick"
DATA_ONE = "Only (A, B) and (B, A), since each prefers its own standard"

COORD_QUESTIONS = [
    Question(
        "o1",
        "The AI build-out: each lab invests or waits. Your best response if your rival invests, "
        "and if it waits? Payoffs first: what does each give you?",
        form=["rival invests: invest", BOX, "wait", BOX, "&nbsp; rival waits: invest", BOX,
              "wait", BOX],
        answers=[H("o1.0"), H("o1.1"), H("o1.2"), H("o1.3")],
        explain="Match the rival: invest against invest, wait against wait."),
    Question(
        "o2",
        "Which outcomes are Nash equilibria?",
        choices=[BUILD_NE, BUILD_ONE, BUILD_NONE, BUILD_MIX],
        answers=[H("o2.c")],
        mistakes=M({
            "o2.c~" + BUILD_ONE: "Against waiting, waiting pays 1 and investing &minus;1.",
            "o2.c~" + BUILD_NONE: "That is the penalty kick, not this game.",
            "o2.c~" + BUILD_MIX: "The moves are simultaneous.",
        }),
        explain="Beliefs pick the equilibrium: a public grid build-out moves everyone's "
                "expectations at once."),
    Question(
        "o3",
        "Warm-up W2, the stag hunt: a stag caught together is worth 3 each, a hare 1 to whoever "
        "hunts one, and a stag hunted alone 0. How many pure Nash equilibria, and what does the "
        "stag hunter get if the other hunts hare?",
        form=["equilibria", BOX, "&nbsp; payoff", BOX],
        answers=[H("o3.0"), H("o3.1")],
        mistakes=M({"o3.0~1": "Hare against hare is self-confirming too."}),
        explain="Stag&ndash;stag and hare&ndash;hare: the same structure as the build-out."),
    Question(
        "o4",
        "Review question 3: Nordapp and Fjordsoft each commit to data standard A or B. Both A: "
        "(5, 3); both B: (3, 5); Nordapp A and Fjordsoft B: (1, 1); the reverse: (0, 0).",
        choices=[DATA_NE, DATA_DOM, DATA_NONE, DATA_ONE],
        answers=[H("o4.c")],
        mistakes=M({
            "o4.c~" + DATA_DOM: "Against B, Nordapp gets 3 from B and 1 from A.",
            "o4.c~" + DATA_NONE: "Check (A, A): neither gains by switching.",
            "o4.c~" + DATA_ONE: "A split pays at most 1: both would switch.",
        }),
        explain="Two equilibria, and each firm prefers a different one."),
]

coordinate = GuidedProblem(
    "Part 2 &middot; Coordination",
    "In a coordination game each player's best action depends on what the others do, so there "
    "is no always-best choice.",
    COORD_QUESTIONS, draw_coordinate, figsize=(8.0, 3.4), whole_figure=True,
    outro="Nothing in the Nash concept says which equilibrium will be played.",
    sources=[NOTES("p. 4"), PS("W2"), NOTES("p. 15, review question 3")],
)


# ======================================================================
# Part 3: iterated elimination of strictly dominated strategies
# ======================================================================

def draw_iesds(fig, stage):
    left, right = fig.subplots(1, 2)
    cols = [2] if stage >= 1 else []
    rows = [0, 2] if stage >= 2 else []
    cols = cols + ([0] if stage >= 2 else [])
    gm.matrix(left, GRID, "Player 1", "Player 2", struck_rows=rows, struck_cols=cols,
              nash=[(1, 1)] if stage >= 2 else (), title="The notes' 3×3 game")
    if stage >= 5:
        r_rows = [0, 2] if stage >= 7 else []
        r_cols = ([2] if stage >= 6 else []) + ([0] if stage >= 7 else [])
        gm.matrix(right, PITCH, "Row", "Column", struck_rows=r_rows, struck_cols=r_cols,
                  nash=[(1, 1)] if stage >= 7 else (), title="Review question 2")
    else:
        right.axis("off")


LADDER = "Each round climbs one rung of common knowledge: I am rational, you know I am rational, I know that you know, and so on"
LAD_ONE = "Only rationality of the player deleting a strategy matters"
LAD_LUCK = "Nothing: the order of deletion is arbitrary and so is the result"
LAD_NASH = "Each round finds one more Nash equilibrium"

PITCH_R = "R: C beats it in every row for Column"
PITCH_T = "T: M beats it in every column for Row"
PITCH_B = "B: T beats it in every column for Row"
PITCH_L = "L: C beats it in every row for Column"

IESDS_QUESTIONS = [
    Question(
        "e1",
        "The notes' 3&times;3 game. Start with player 2: compare B3 with B2, row by row. Player "
        "2's payoffs from B2 in rows A1, A2, A3?",
        form=["", BOX, ",", BOX, ",", BOX],
        answers=[H("e1.0"), H("e1.1"), H("e1.2")],
        mistakes=M({"e1.0~1": "Player 2's payoff is the second number."}),
        explain="Against B3's 2, 0 and 1: B2 is better in every row, so B3 is strictly dominated."),
    Question(
        "e2",
        "In what is left, player 1 has a strictly dominant strategy, and player 2 answers it. The "
        "surviving profile's payoffs?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("e2.0"), H("e2.1")],
        mistakes=M({"e2.0~4": "Given A2, player 2 compares 1 with 2 and picks B2."}),
        explain="(A2, B2): A2 pays 4 and 2, beating A1 and A3 in both columns."),
    Question(
        "e3",
        "What is common knowledge of rationality doing at each round?",
        choices=[LADDER, LAD_ONE, LAD_LUCK, LAD_NASH],
        answers=[H("e3.c")],
        mistakes=M({
            "e3.c~" + LAD_ONE: "Player 1 deletes A1 only because he knows player 2 never plays "
                               "B3.",
            "e3.c~" + LAD_LUCK: "With strict dominance the order does not change the survivors.",
            "e3.c~" + LAD_NASH: "IESDS deletes strategies; it does not search for equilibria.",
        }),
        explain="Rationality alone deletes once; every further round needs one more rung."),
    Question(
        "e4",
        "The memory lines: &pi;<sub>i</sub> = (4 &minus; q<sub>i</sub> &minus; q<sub>j</sub>)"
        "q<sub>i</sub> &minus; q<sub>i</sub>&sup2;. Your payoffs from adding 3 lines when the "
        "rival adds 0, 1, 2 and 3?",
        form=["", BOX, ",", BOX, ",", BOX, ",", BOX],
        answers=[H("e4.0"), H("e4.1"), H("e4.2"), H("e4.3")],
        mistakes=M({"e4.0~3": "Do not drop the cost: (4 &minus; 3)3 &minus; 9."}),
        explain="Adding 2 lines pays 0, &minus;2, &minus;4, &minus;6: better in every row, so 3 "
                "is dominated."),
    Question(
        "e5",
        "Eliminate on: 3 goes, then 2, then 0. How many lines does each maker add, and what does "
        "each earn? Then solve with calculus: the best response is q<sub>i</sub> = (4 &minus; "
        "q<sub>j</sub>)/4. The symmetric equilibrium?",
        form=["lines", BOX, "payoff", BOX, "&nbsp; calculus q* =", BOX],
        answers=[H("e5.0"), H("e5.1"), H("e5.2")],
        mistakes=M({"e5.2~4/3": "The cost q<sub>i</sub>&sup2; adds &minus;2q<sub>i</sub> to the "
                                "first-order condition: don't drop it.",
                    "e5.2~1": "That is the grid answer. Solve q = (4 &minus; q)/4."}),
        explain="1 is the nearest whole line to 4/5: the matrix and the calculus agree."),
    Question(
        "e6",
        "Review question 2: two consulting firms pitch. Which strategy is strictly dominated in "
        "the first round?",
        choices=[PITCH_R, PITCH_T, PITCH_B, PITCH_L],
        answers=[H("e6.c")],
        mistakes=M({
            "e6.c~" + PITCH_T: "Against R, T pays 2 and M only 1.",
            "e6.c~" + PITCH_B: "Against R, B pays 3 and T only 2.",
            "e6.c~" + PITCH_L: "Against T, L pays 5 and C only 4.",
        }),
        explain="L also beats R. Once R is gone, Row's B and T lose to M."),
    Question(
        "e7",
        "Continue until nothing more can be deleted. The surviving profile's payoffs?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("e7.0"), H("e7.1")],
        mistakes=M({"e7.1~2": "With only M left, Column compares L's 2 with C's 3."}),
        explain="(M, C). Say what common knowledge does at each round."),
]

iesds = GuidedProblem(
    "Part 3 &middot; Iterated elimination (IESDS)",
    "A strategy is strictly dominated if another strategy pays more against everything the "
    "opponent might do. Delete it, and ask again on the smaller game.",
    IESDS_QUESTIONS, draw_iesds, figsize=(8.0, 3.4), whole_figure=True,
    outro="When dominance is silent, Nash still speaks; where both speak, they agree.",
    sources=[NOTES("p. 5&ndash;7"), NOTES("p. 15, review question 2")],
)


# ======================================================================
# Part 4: best responses, Nash equilibrium and Cournot
# ======================================================================

def draw_cournot(fig, stage):
    br, mat = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.1, 1]))
    _panel(br, 96, 96, "rival's quantity q$_2$", "your quantity q$_1$", "Best responses",
           xticks=[30, 90] if stage >= 2 else ([90] if stage >= 1 else []),
           yticks=([45] if stage >= 1 else []) + ([30] if stage >= 2 else []))
    if stage == 0:
        gp.start(br)
    if stage >= 1:
        q = np.linspace(0, 90, 100)
        br.plot(q, (90 - q) / 2, color=LINE, lw=2, label="BR$_1$")
    if stage >= 2:
        br.plot((90 - q) / 2, q, color=CURVE, lw=2, label="BR$_2$")
        gp.dot(br, 30, 30, "(30, 30)", 6, 4, colour=GREEN)
    gp.legend(br, loc="upper right")
    if stage >= 3:
        gm.matrix(mat, TALENT, "OpenAI", "Anthropic", best=stage >= 4,
                  nash=TALENT.pure_nash() if stage >= 4 else (), title="The talent war")
    else:
        mat.axis("off")
    fig.subplots_adjust(wspace=0.2)


TALENT_NE = "(T, T), paying (2, 2): raiding is a best response to both of the rival's choices, so it is the only profile where both best-respond"
TALENT_CC = "(C, C), paying (3, 3), since both prefer it"
TALENT_TWO = "(C, T) and (T, C): one lab builds, the other raids"
TALENT_NONE = "There is no pure equilibrium"

NASH = "Each player's strategy is a best response to the others': nobody gains by deviating alone"
NASH_BEST = "The profile with the highest total payoff"
NASH_DOM = "A profile in which every player plays a dominant strategy"
NASH_FAIR = "A profile both players would agree to in advance"

COURNOT_QUESTIONS = [
    Question(
        "k1",
        "The API compute market: P = 100 &minus; Q, serving cost 10. Lab i maximizes "
        "(100 &minus; q<sub>i</sub> &minus; q<sub>j</sub>)q<sub>i</sub> &minus; 10q<sub>i</sub>, "
        "so q<sub>i</sub> = (90 &minus; q<sub>j</sub>)/2. Your best response if the rival serves "
        "0, and if it serves 90?",
        form=["q<sub>j</sub> = 0:", BOX, "&nbsp; q<sub>j</sub> = 90:", BOX],
        answers=[H("k1.0"), H("k1.1")],
        mistakes=M({"k1.0~90": "Divide by two: the first-order condition has 2q<sub>i</sub>."}),
        explain="It falls by half a unit for every unit the rival adds."),
    Question(
        "k2",
        "Impose symmetry, q = (90 &minus; q)/2. Each lab's quantity, total output, the price "
        "and each lab's profit?",
        form=["q* =", BOX, "&nbsp; Q =", BOX, "&nbsp; P =", BOX, "&nbsp; &pi; =", BOX],
        answers=[H("k2.0"), H("k2.1"), H("k2.2"), H("k2.3")],
        mistakes=M({"k2.0~45": "That is the monopoly-style reply to zero. Both best-respond "
                               "at once.",
                    "k2.3~1200": "Profit is (P &minus; 10)q: the serving cost counts."}),
        explain="The Cournot&ndash;Nash equilibrium: keep 30, 40 and 900 warm for session 13."),
    Question(
        "k3",
        "The parked benchmark: if the labs were price takers, P = MC. Total output?",
        form=["Q =", BOX],
        answers=[H("k3.0")],
        explain="Cournot produces less than the competitive 90."),
    Question(
        "k4",
        "The talent war: each lab builds compute (C) or raids the rival's talent (T). Both C: "
        "(3, 3); both T: (2, 2); C against T: 1 for the builder, 4 for the raider. The Nash "
        "equilibrium?",
        choices=[TALENT_NE, TALENT_CC, TALENT_TWO, TALENT_NONE],
        answers=[H("k4.c")],
        mistakes=M({
            "k4.c~" + TALENT_CC: "From (C, C) each lab gains 1 by raiding.",
            "k4.c~" + TALENT_TWO: "The builder would rather raid: 2 beats 1.",
            "k4.c~" + TALENT_NONE: "Check (T, T): neither gains by switching.",
        }),
        explain="A prisoner's dilemma underneath: (3, 3) is right there and unreachable."),
    Question(
        "k5",
        "So what is a Nash equilibrium?",
        choices=[NASH, NASH_BEST, NASH_DOM, NASH_FAIR],
        answers=[H("k5.c")],
        mistakes=M({
            "k5.c~" + NASH_BEST: "(3, 3) has the highest total and is not an equilibrium.",
            "k5.c~" + NASH_DOM: "That is a special case; the coordination games have none.",
            "k5.c~" + NASH_FAIR: "No agreement: mutual best responses.",
        }),
        explain="A checkable property: interrogate each player in turn."),
]

cournot = GuidedProblem(
    "Part 4 &middot; Best responses, Nash and Cournot",
    "A best response is optimal against one specific play of the others: fix the other side, "
    "then optimize your own.",
    COURNOT_QUESTIONS, draw_cournot, figsize=(8.0, 3.8), whole_figure=True,
    outro="Where the best responses cross, each player best-responds to the other.",
    sources=[NOTES("p. 7&ndash;10")],
)


# ======================================================================
# Part 5: Bertrand, the Try it, the ferries and the power duopoly
# ======================================================================

def draw_bertrand(fig, stage):
    bars, br = fig.subplots(1, 2)
    for side in ("top", "right"):
        bars.spines[side].set_visible(False)
    bars.set_title("API market: the price", loc="left", color=INK, fontsize=9.5)
    names = ["Cournot", "Bertrand", "price takers"]
    values = [40, 10 if stage >= 1 else 0, 10 if stage >= 1 else 0]
    xs = np.arange(3)
    bars.bar(xs, values, color=[LINE, NEW, GREY], width=0.6)
    for x, v in zip(xs, values):
        if v:
            bars.text(x, v + 1, "%d" % v, ha="center", color=INK, fontsize=9)
    bars.set_xticks(xs)
    bars.set_xticklabels(names, fontsize=9, color=INK)
    bars.set_yticks([])
    bars.set_ylim(0, 48)

    _panel(br, 64, 64, "q$_2$", "q$_1$", "Worksheet: the power duopoly",
           xticks=[20, 40, 60], yticks=[20, 40, 60])
    br.grid(True, color="#e5e7eb", lw=0.6)
    br.set_axisbelow(True)
    gp.dot(br, 0, 30, "", colour=LINE)
    if stage >= 7:
        q = np.linspace(0, 60, 100)
        br.plot(q, (60 - q) / 2, color=LINE, lw=2, label="BR$_1$")
        br.plot((60 - q) / 2, q, color=CURVE, lw=2, label="BR$_2$")
        gp.dot(br, 20, 20, "C", 6, 4, colour=GREEN)
    gp.legend(br, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


UNDERCUT = "Either lab could cut its price by a cent, take the whole market and nearly double its profit, so no common price above marginal cost survives"
UC_COLLUDE = "The labs would agree to raise the price above 20"
UC_DEMAND = "At 20 demand is too low for both labs"
UC_COST = "20 is below marginal cost"

SOFT = "In Cournot a firm that expands must accept a lower price on all its output, so competition is soft; in Bertrand with identical goods the smallest cut steals the whole market"
SOFT_N = "Bertrand needs many firms to reach the competitive price"
SOFT_SAME = "They give the same price once costs are equal"
SOFT_COST = "Bertrand firms have lower costs"

BERTRAND_QUESTIONS = [
    Question(
        "b1",
        "Same API market, P = 100 &minus; Q and cost 10, but the labs post prices and buyers "
        "route to the cheaper one. The Bertrand price, total quantity and each lab's profit?",
        form=["P =", BOX, "&nbsp; Q =", BOX, "&nbsp; &pi; =", BOX],
        answers=[H("b1.0"), H("b1.1"), H("b1.2")],
        mistakes=M({"b1.0~40": "That is Cournot. With posted prices, undercutting never stops "
                               "above cost."}),
        explain="Two firms deliver the competitive 90."),
    Question(
        "b2",
        "Review question 5: why is any common price above marginal cost, say 20 on the ferry "
        "route, not a Nash equilibrium?",
        choices=[UNDERCUT, UC_COLLUDE, UC_DEMAND, UC_COST],
        answers=[H("b2.c")],
        mistakes=M({
            "b2.c~" + UC_COLLUDE: "A Nash check is about one firm deviating alone.",
            "b2.c~" + UC_DEMAND: "Demand is positive at 20.",
            "b2.c~" + UC_COST: "Marginal cost on the route is 6.",
        }),
        explain="A profitable unilateral deviation: the Nash test fails."),
    Question(
        "b3",
        "Try it (a): P = 27 &minus; Q, serving cost 3, quantities. Each lab's quantity, the "
        "price and each lab's daily profit?",
        form=["q* =", BOX, "&nbsp; P =", BOX, "&nbsp; &pi; =", BOX],
        answers=[H("b3.0"), H("b3.1"), H("b3.2")],
        mistakes=M({"b3.0~12": "Solve q = (24 &minus; q)/2."}),
        hints=["The best response is q<sub>i</sub> = (24 &minus; q<sub>j</sub>)/2."],
        explain="$64 million a day per lab."),
    Question(
        "b4",
        "(b) A year later the price is 15, same demand, still Cournot. The Cournot price is "
        "(27 + 2c)/3. Which marginal cost is the market revealing?",
        form=["c =", BOX],
        answers=[H("b4.0")],
        mistakes=M({"b4.0~6": "Solve (27 + 2c)/3 = 15: 2c = 18."}),
        explain="Serving costs tripled: heavier reasoning models."),
    Question(
        "b5",
        "(c) Capacity turns abundant and the labs reprice instantly. The price and total "
        "quantity?",
        form=["P =", BOX, "&nbsp; Q =", BOX],
        answers=[H("b5.0"), H("b5.1")],
        explain="The strategic variable alone moves the price from 11 to 3."),
    Question(
        "b6",
        "Review question 4: ferries, P = 60 &minus; Q, cost 6 a crossing. The Cournot quantity "
        "each, the price, each operator's profit, and the price-taking total output?",
        form=["q* =", BOX, "&nbsp; P =", BOX, "&nbsp; &pi; =", BOX, "&nbsp; competitive Q =", BOX],
        answers=[H("b6.0"), H("b6.1"), H("b6.2"), H("b6.3")],
        explain="36 crossings against the competitive 54."),
    Question(
        "b7",
        "Worksheet task 3: two power producers sell to a data-center corridor with demand "
        "90 &minus; Q and cost 30. BR<sub>1</sub> starts at the marked intercept, 30. Where does "
        "it end on the q<sub>2</sub> axis, and where is the Cournot point?",
        form=["ends at", BOX, "&nbsp; q* =", BOX, "&nbsp; P =", BOX],
        answers=[H("b7.0"), H("b7.1"), H("b7.2")],
        mistakes=M({"b7.0~30": "BR<sub>1</sub> = (60 &minus; q<sub>2</sub>)/2 hits zero at "
                               "q<sub>2</sub> = 60."}),
        explain="Price takers would sell 60; posted prices would push the price to 30."),
    Question(
        "b8",
        "Why do quantities and prices give such different outcomes in the same market?",
        choices=[SOFT, SOFT_N, SOFT_SAME, SOFT_COST],
        answers=[H("b8.c")],
        mistakes=M({
            "b8.c~" + SOFT_N: "Two are enough: that is Bertrand's surprise.",
            "b8.c~" + SOFT_SAME: "40 against 10 in the API market.",
            "b8.c~" + SOFT_COST: "Same demand, same cost of 10.",
        }),
        explain="Cournot where capacity is set in advance; Bertrand where repricing is instant."),
]

bertrand = GuidedProblem(
    "Part 5 &middot; Prices instead of quantities: Bertrand",
    "Same demand, same costs, same two firms; only the strategic variable changes.",
    BERTRAND_QUESTIONS, draw_bertrand, figsize=(8.0, 3.8), whole_figure=True,
    outro="Two firms stuck at zero profit have 900 reasons each to escape: session 15.",
    sources=[NOTES("p. 10&ndash;12"), NOTES("p. 14, worksheet task 3"),
             NOTES("p. 16, review questions 4&ndash;5")],
)


# ======================================================================
# Part 6: mixed strategies
# ======================================================================

def draw_mixed(fig, stage):
    kick, rel = fig.subplots(1, 2)
    _lines(kick, [(1, -1), (-1, 1)], ["kick L: 1 − 2q", "kick R: 2q − 1"], [LINE, NEW],
           "Penalty kick: the kicker's payoff", "goalie's q (dives left)")
    kick.set_ylim(-1.2, 1.2)
    kick.axhline(0, color=GREY, lw=0.6)
    kick.set_yticks([-1, 0, 1])
    if stage >= 2:
        kick.axvline(0.5, color=GREEN, lw=1.2, ls=":")
        gp.dot(kick, 0.5, 0, "q* = 1/2", 6, 6, colour=GREEN)
    kick.set_xticks([0, 0.5, 1] if stage >= 2 else [0, 1])
    gp.legend(kick, loc="upper center")

    if stage >= 3:
        _lines(rel, [(2, 0), (0, 3)], ["Anthropic March: 2 − 2q", "Anthropic Sept: 3q"],
               [LINE, CURVE], "Release game: Anthropic's payoff", "q = P(OpenAI picks March)")
        rel.set_ylim(0, 3.3)
        rel.set_yticks([1, 2, 3])
        rel.set_xticks([0, 1] + ([0.4] if stage >= 4 else []))
        if stage >= 4:
            gp.dot(rel, 0.4, 1.2, "q* = 2/5", 6, 6, colour=GREEN)
        gp.legend(rel, loc="upper center")
    else:
        rel.axis("off")
    fig.subplots_adjust(wspace=0.25)


OPPONENT = "A player mixes only if her two pure strategies pay the same, and what makes them pay the same is the opponent's mix. So Anthropic's probability is whatever leaves OpenAI indifferent, and it comes from OpenAI's payoffs"
OPP_OWN = "Each player's mix comes from her own payoffs"
OPP_RANDOM = "Probabilities are arbitrary: any mix is an equilibrium"
OPP_FIFTY = "Mixed equilibria always use 1/2 and 1/2"

FOOT = "The striker mixes to keep the keeper indifferent, and the keeper's payoffs are symmetric, so the striker's mix is 1/2; the stronger foot makes the striker's payoffs asymmetric, so it moves the keeper's mix"
FOOT_OWN = "A stronger left foot makes the striker kick left more often"
FOOT_NONE = "The stronger foot has no effect on the equilibrium"
FOOT_KEEP = "The keeper dives right more, away from the stronger foot"

MIXED_QUESTIONS = [
    Question(
        "x1",
        "Warm-up W1, the penalty kick: a goal is +1 for the kicker and &minus;1 for the goalie, "
        "a save the reverse. The goalie dives left with probability q. The kicker's expected "
        "payoff from kicking left is q(&minus;1) + (1 &minus; q)(1) = 1 &minus; 2q. Both lines "
        "at q = 3/4?",
        form=["kick L", BOX, "&nbsp; kick R", BOX],
        answers=[H("x1.0"), H("x1.1")],
        mistakes=M({"x1.0~1/2": "1 &minus; 2(3/4) is negative: the goalie leans left."}),
        explain="Against a goalie leaning left, kick right: all weight slides to the better line."),
    Question(
        "x2",
        "The kicker is only willing to mix where the lines cross. The goalie's q*, and by the "
        "same logic the kicker's p*?",
        form=["q* =", BOX, "&nbsp; p* =", BOX],
        answers=[H("x2.0"), H("x2.1")],
        explain="The indifference condition. Expected payoff zero: perfect unpredictability."),
    Question(
        "x3",
        "Worksheet task 1&ndash;2: the release game. OpenAI wants the same month as Anthropic; "
        "Anthropic wants a clear window. Payoffs (Anthropic, OpenAI): both March (0, 3); "
        "Anthropic March alone (2, 0); Anthropic September alone (3, 0); both September (0, 1). "
        "With q = P(OpenAI picks March), Anthropic's payoff from March and from September at "
        "q = 0 and at q = 1?",
        form=["March: q = 0", BOX, "q = 1", BOX, "&nbsp; Sept: q = 0", BOX, "q = 1", BOX],
        answers=[H("x3.0"), H("x3.1"), H("x3.2"), H("x3.3")],
        mistakes=M({"x3.3~1": "Anthropic's payoff is the first number: (3, 0)."}),
        explain="One line falls from 2, the other rises to 3. No pure equilibrium exists."),
    Question(
        "x4",
        "Where the lines cross: the q* that makes Anthropic indifferent?",
        form=["q* =", BOX],
        answers=[H("x4.0")],
        mistakes=M({"x4.0~1/4": "That is Anthropic's own mix. Solve 2 &minus; 2q = 3q.",
                    "x4.0~1/2": "Solve 2 &minus; 2q = 3q."}),
        explain="OpenAI picks March with probability 2/5."),
    Question(
        "x5",
        "And Anthropic's probability p of March, from OpenAI's indifference: 3p = 1 &minus; p?",
        form=["p* =", BOX],
        answers=[H("x5.0")],
        mistakes=M({"x5.0~2/5": "That is OpenAI's mix."}),
        explain="Anthropic picks March with probability 1/4."),
    Question(
        "x6",
        "Why does Anthropic's mix come from OpenAI's payoffs?",
        choices=[OPPONENT, OPP_OWN, OPP_RANDOM, OPP_FIFTY],
        answers=[H("x6.c")],
        mistakes=M({
            "x6.c~" + OPP_OWN: "The single most common error in this topic.",
            "x6.c~" + OPP_RANDOM: "Only the indifference mix keeps the other willing to mix.",
            "x6.c~" + OPP_FIFTY: "2/5 and 1/4 here.",
        }),
        explain="Your mix keeps the opponent guessing."),
    Question(
        "x7",
        "Review question 6: the striker scores 2 to the left, 1 to the right, 0 if saved; the "
        "keeper gets 1 for a save. (L, L): (0, 1); (L, R): (2, 0); (R, L): (1, 0); (R, R): (0, 1). "
        "The keeper's probability of diving left, and the striker's of kicking left?",
        form=["keeper q =", BOX, "&nbsp; striker p =", BOX],
        answers=[H("x7.0"), H("x7.1")],
        mistakes=M({"x7.0~1/3": "Striker indifferent: 2(1 &minus; q) = q.",
                    "x7.1~2/3": "Keeper indifferent: p = 1 &minus; p."}),
        explain="The keeper dives left two times in three; the striker still mixes 50-50."),
    Question(
        "x8",
        "Why does the striker's stronger left foot show up in the keeper's mix?",
        choices=[FOOT, FOOT_OWN, FOOT_NONE, FOOT_KEEP],
        answers=[H("x8.c")],
        mistakes=M({
            "x8.c~" + FOOT_OWN: "The striker's p comes from the keeper's payoffs: 1/2.",
            "x8.c~" + FOOT_NONE: "The keeper now dives left with probability 2/3.",
            "x8.c~" + FOOT_KEEP: "Toward it: q = 2/3 on the left.",
        }),
        explain="Two sentences on the exam."),
]

mixed = GuidedProblem(
    "Part 6 &middot; Mixed strategies",
    "Some games have no pure equilibrium: in every cell the loser wants to switch. Let the "
    "players randomize, and look for the mix that keeps the other side indifferent.",
    MIXED_QUESTIONS, draw_mixed, figsize=(8.0, 3.8), whole_figure=True,
    outro="Bring the worksheet: I want to hear the word indifferent.",
    sources=[NOTES("p. 12&ndash;14"), PS("W1"), NOTES("p. 16, review question 6")],
)


# ======================================================================
# Part 7: problem A12.1, Kvist and Lundin pick a standard
# ======================================================================

def draw_standard(fig, stage):
    mat, lines = fig.subplots(1, 2)
    gm.matrix(mat, STANDARD, "Kvist", "Lundin", struck_rows=[2] if stage >= 2 else (),
              struck_cols=[2] if stage >= 2 else (), best=stage >= 3,
              nash=[(0, 0), (1, 1)] if stage >= 3 else ())
    if stage >= 4:
        _lines(lines, [(2, 6), (4, 2)], ["Kvist plays X: 2 + 4q", "Kvist plays Y: 4 − 2q"],
               [LINE, CURVE], "Kvist's expected profit", "q = P(Lundin plays X)")
        lines.set_ylim(0, 6.5)
        lines.set_xticks([0, 1 / 3, 1])
        lines.set_xticklabels(["0", "1/3", "1"])
        lines.set_yticks([2, 4, 6])
        gp.dot(lines, 1 / 3, 10 / 3, "10/3", 6, 6, colour=GREEN)
        gp.legend(lines, loc="upper center")
    else:
        lines.axis("off")
    fig.subplots_adjust(wspace=0.2)


FORMAL = "Players {Kvist, Lundin}, each with strategies {X, Y, A}, and payoffs as in the matrix. Normal form, because both commit simultaneously: nobody observes the other's move first"
FORM_TREE = "A game tree, because Kvist moves first"
FORM_TWO = "Players and payoffs only: strategies are not part of a game"
FORM_REPEAT = "A repeated game, because both build on the standard for years"

DOMINATED = "A pays 1, 1 and 2 against X, Y and A, while X pays 6, 2 and 3 (and Y 2, 4 and 3): A is strictly dominated by X, and also by Y. A dominated strategy is never a best response, so no Nash equilibrium uses it"
DOM_Y_ONLY = "A is dominated by Y only, so deleting it may lose an equilibrium"
DOM_NOT = "A is not dominated, since it pays 3 to the other firm against X"
DOM_X_DOM = "X is strictly dominant, so the game is solved by dominance"

RANKING = "(X, X) pays 6 each, (Y, Y) 4 and the mixed 10/3, below both because the firms miscoordinate with probability 4/9. Moving from (Y, Y) to (X, X) needs coordinated expectations, such as a regulator's standard or a public commitment, since Nash itself does not say which equilibrium is played"
RANK_MIX = "The mixed equilibrium is best, since it spreads the risk"
RANK_STUCK = "Nothing can move the industry once it is at (Y, Y), and Nash predicts it stays"
RANK_TAX = "A tax on Y makes Y dominated, which is the only way out"

STANDARD_QUESTIONS = [
    Question(
        "s1",
        "A12.1 (a): Kvist and Lundin commit simultaneously and irreversibly to standard X, Y or "
        "their own stack A. State the game formally.",
        choices=[FORMAL, FORM_TREE, FORM_TWO, FORM_REPEAT],
        answers=[H("s1.c")],
        mistakes=M({
            "s1.c~" + FORM_TREE: "They commit at the same time.",
            "s1.c~" + FORM_TWO: "A game is players, strategies and payoffs.",
            "s1.c~" + FORM_REPEAT: "Each commits once.",
        }),
        explain="One sentence on what makes it normal form."),
    Question(
        "s2",
        "(b) Show that A is strictly dominated for both firms.",
        choices=[DOMINATED, DOM_Y_ONLY, DOM_NOT, DOM_X_DOM],
        answers=[H("s2.c")],
        mistakes=M({
            "s2.c~" + DOM_Y_ONLY: "Compare A with X too: 6 &gt; 1, 2 &gt; 1, 3 &gt; 2.",
            "s2.c~" + DOM_NOT: "Dominance compares a player's own payoffs.",
            "s2.c~" + DOM_X_DOM: "Against Y, X pays 2 and Y 4.",
        }),
        explain="Two sentences on why deleting it loses no equilibrium."),
    Question(
        "s3",
        "(c) In the reduced 2&times;2 game, how many pure Nash equilibria are there, and what "
        "does each firm earn in the better one?",
        form=["equilibria", BOX, "&nbsp; better one pays", BOX],
        answers=[H("s3.0"), H("s3.1")],
        mistakes=M({"s3.0~1": "Check (Y, Y): against Y, Y pays 4 and X only 2."}),
        explain="(X, X) and (Y, Y). Verify that neither firm wants to deviate from either."),
    Question(
        "s4",
        "(d) The mixed equilibrium. With q = P(Lundin plays X), Kvist's X pays 6q + 2(1 &minus; q) "
        "and Y pays 2q + 4(1 &minus; q). The q that makes Kvist indifferent, and by symmetry "
        "Kvist's p?",
        form=["q =", BOX, "&nbsp; p =", BOX],
        answers=[H("s4.0"), H("s4.1")],
        mistakes=M({"s4.0~2/3": "Solve 2 + 4q = 4 &minus; 2q: 6q = 2.",
                    "s4.0~1/2": "Solve 2 + 4q = 4 &minus; 2q."}),
        explain="Derived from the opponent's indifference, as a simple fraction."),
    Question(
        "s5",
        "(e) Each firm's expected profit in the mixed equilibrium, and the probability that they "
        "end up on different standards?",
        form=["profit", BOX, "&nbsp; P(different)", BOX],
        answers=[H("s5.0"), H("s5.1")],
        mistakes=M({"s5.1~2/9": "Two ways to differ: p(1 &minus; q) + (1 &minus; p)q.",
                    "s5.0~4": "Put q = 1/3 into 2 + 4q."}),
        explain="Both pure strategies pay 10/3 at q = 1/3, so the mix does too."),
    Question(
        "s6",
        "(f) Rank the three equilibria, and answer the regulator.",
        choices=[RANKING, RANK_MIX, RANK_STUCK, RANK_TAX],
        answers=[H("s6.c")],
        mistakes=M({
            "s6.c~" + RANK_MIX: "10/3 is below both 6 and 4.",
            "s6.c~" + RANK_STUCK: "Nash does not say which equilibrium is played.",
            "s6.c~" + RANK_TAX: "Shifting expectations is enough: X is already a best response "
                                "to X.",
        }),
        explain="Five sentences on the exam."),
]

standard = GuidedProblem(
    "Part 7 &middot; Kvist and Lundin pick a standard: A12.1",
    "Profits in millions of kroner, (Kvist, Lundin). Standard X is the better technology, but "
    "only if the other firm builds on it too.",
    STANDARD_QUESTIONS, draw_standard, figsize=(8.0, 3.6), whole_figure=True,
    outro="About 25&ndash;30% of an exam paper. Most lost marks come from stopping at the pure "
          "equilibria.",
    sources=[PS("A12.1")],
)


# ======================================================================
# Part 8: problem A12.2, the tax authority and Berg AS
# ======================================================================

def draw_audit(fig, stage):
    mat, lines = fig.subplots(1, 2)
    gm.matrix(mat, AUDIT, "Berg AS", "Authority", best=stage >= 1)
    if stage >= 2:
        _lines(lines, [(30, -20), (0, 0)], ["Berg evades", "Berg complies"], [NEW, GREY],
               "Berg's expected payoff", "q = P(audit)")
        lines.set_ylim(-42, 34)
        lines.axhline(0, color=GREY, lw=0.6)
        lines.set_yticks([-40, -20, 0, 30])
        ticks = [0, 0.6, 1] + ([3 / 7] if stage >= 4 else [])
        lines.set_xticks(ticks)
        lines.set_xticklabels([{0: "0", 0.6: "3/5", 1: "1"}.get(t, "3/7") for t in ticks])
        gp.dot(lines, 0.6, 0, "", colour=GREEN)
        if stage >= 4:
            lines.plot([0, 1], [30, -40], color=NEW, lw=1.6, ls="--", label="penalty 40")
            gp.dot(lines, 3 / 7, 0, "", colour=NEW)
        gp.legend(lines, loc="lower left")
    else:
        lines.axis("off")
    fig.subplots_adjust(wspace=0.2)


NO_PURE = "In every cell someone regrets: at (Evade, Audit) Berg would comply, at (Comply, Audit) the authority would not audit, at (Comply, Not) Berg would evade, and at (Evade, Not) the authority would audit"
NP_ONE = "(Comply, Not) is an equilibrium: nobody evades and nobody audits"
NP_TWO = "(Evade, Audit) and (Comply, Not) are both equilibria"
NP_DOM = "Comply is dominant for Berg, so (Comply, Not) is the answer"

PENALTY = "A tougher penalty lowers the audit rate, not evasion: evasion p is pinned by the authority's indifference, so it only moves if the authority's payoffs move. To cut evasion, change those: cheaper audits, or a bigger reward for catching evaders"
PEN_WORKS = "Doubling the penalty halves evasion"
PEN_BERG = "Evasion depends only on Berg's payoffs"
PEN_NONE = "Nothing changes at all"

AUDIT_QUESTIONS = [
    Question(
        "a1",
        "A12.2 (a): Berg evades or complies; the authority audits or not, at the same time. "
        "Why is there no pure Nash equilibrium?",
        choices=[NO_PURE, NP_ONE, NP_TWO, NP_DOM],
        answers=[H("a1.c")],
        mistakes=M({
            "a1.c~" + NP_ONE: "Against no audits, Berg gets 30 from evading.",
            "a1.c~" + NP_TWO: "At (Evade, Audit) Berg gets &minus;20 and would comply.",
            "a1.c~" + NP_DOM: "Comply pays 0 always; evading pays 30 when nobody audits.",
        }),
        explain="Check each of the four cells in turn on the exam."),
    Question(
        "a2",
        "(b) q is the probability of an audit. Berg's payoff from evading is &minus;20q + 30(1 "
        "&minus; q), from complying 0. The q that makes Berg indifferent?",
        form=["q =", BOX],
        answers=[H("a2.0")],
        mistakes=M({"a2.0~1/9": "That is Berg's own mix. Solve &minus;20q + 30 &minus; 30q = 0."}),
        explain="Above 3/5 Berg complies, below it Berg evades."),
    Question(
        "a3",
        "(c) p is the probability that Berg evades. The authority's audit pays 10p &minus; 5(1 "
        "&minus; p), not auditing &minus;30p. The p that makes it indifferent?",
        form=["p =", BOX],
        answers=[H("a3.0")],
        mistakes=M({"a3.0~3/5": "That is the audit rate. Solve 10p &minus; 5 + 5p = &minus;30p."}),
        explain="The equilibrium: Berg evades with probability 1/9, the authority audits with 3/5."),
    Question(
        "a4",
        "(d) The penalty doubles to 40; the authority's payoffs are unchanged. The new q and p?",
        form=["q =", BOX, "&nbsp; p =", BOX],
        answers=[H("a4.0"), H("a4.1")],
        mistakes=M({"a4.1~1/18": "The authority's payoffs did not change, so neither does p."}),
        explain="Uncomfortable: the audit rate falls, evasion stays at 1/9."),
    Question(
        "a5",
        "(e) What does a tougher penalty actually do here?",
        choices=[PENALTY, PEN_WORKS, PEN_BERG, PEN_NONE],
        answers=[H("a5.c")],
        mistakes=M({
            "a5.c~" + PEN_WORKS: "p stayed at 1/9.",
            "a5.c~" + PEN_BERG: "The other way round: Berg's mix comes from the authority's "
                                "payoffs.",
            "a5.c~" + PEN_NONE: "The audit rate fell from 3/5 to 3/7.",
        }),
        explain="Five sentences on the exam."),
]

audit = GuidedProblem(
    "Part 8 &middot; The tax authority and Berg AS: A12.2",
    "Payoffs in hundreds of thousands of kroner, (Berg, Authority). Fines go to the treasury, "
    "not the authority, which is judged on compliance.",
    AUDIT_QUESTIONS, draw_audit, figsize=(8.0, 3.6), whole_figure=True,
    outro="About 15&ndash;20% of an exam paper.",
    sources=[PS("A12.2")],
)


# ======================================================================
# Part 9: problem A12.3, two games with a continuum of actions
# ======================================================================

def draw_flatmates(fig, stage):
    a, b = fig.subplots(1, 2)
    _panel(a, 11, 11, "t$_j$", "t$_i$", "Game A: the flatmates",
           xticks=[10] if stage >= 1 else [], yticks=[5] if stage >= 1 else [])
    if stage == 0:
        gp.start(a)
    if stage >= 1:
        t = np.linspace(0, 10, 50)
        a.plot(t, (10 - t) / 2, color=LINE, lw=2, label="BR$_i$")
        a.plot((10 - t) / 2, t, color=CURVE, lw=2, label="BR$_j$")
    if stage >= 2:
        gp.dot(a, 10 / 3, 10 / 3, "10/3", 6, 4, colour=GREEN)
    gp.legend(a, loc="upper right")
    _panel(b, 15, 15, "e$_j$", "e$_i$", "Game B, with a = 6",
           xticks=[6] if stage >= 3 else [], yticks=[3, 6] if stage >= 3 else [])
    if stage >= 3:
        e = np.linspace(0, 15, 50)
        b.plot(e, (6 + e) / 2, color=LINE, lw=2, label="BR$_i$")
        b.plot((6 + e) / 2, e, color=CURVE, lw=2, label="BR$_j$")
        gp.dot(b, 6, 6, "e = a", 6, -12, colour=GREEN)
    gp.legend(b, loc="upper left")
    fig.subplots_adjust(wspace=0.25)


SLOPES = "Game A slopes down: strategic substitutes, the more you clean the less I want to. Game B slopes up: strategic complements. Cournot is like A: more output from the rival lowers my marginal revenue"
SLOPES_REV = "A is complements and B substitutes; Cournot is complements"
SLOPES_SAME = "Both are substitutes, like Cournot"
SLOPES_CB = "Both are complements, like Cournot"

UNIQUE = "Each best response is a straight line with slope 1/2 or -1/2, so the two lines cross exactly once; in the standards game the best response jumps between X and Y, which lets it meet the other's in several places"
UNI_SOC = "The second-order condition guarantees uniqueness in any game"
UNI_SYM = "Symmetric games always have one equilibrium"
UNI_CONT = "Continuous games never have multiple equilibria"

FLAT_QUESTIONS = [
    Question(
        "f1",
        "A12.3 (a): v<sub>i</sub> = (10 &minus; t<sub>j</sub>)t<sub>i</sub> &minus; "
        "t<sub>i</sub>&sup2;. The first-order condition gives t<sub>i</sub> = (10 &minus; "
        "t<sub>j</sub>)/2, and the second derivative is &minus;2. The best response when the "
        "other flatmate cleans 0, and when she cleans 10?",
        form=["t<sub>j</sub> = 0:", BOX, "&nbsp; t<sub>j</sub> = 10:", BOX],
        answers=[H("f1.0"), H("f1.1")],
        mistakes=M({"f1.0~10": "Divide by two: d/dt of t&sup2; is 2t."}),
        explain="A maximum, since &minus;2 &lt; 0. Check the second-order condition on the exam."),
    Question(
        "f2",
        "(b) The Nash equilibrium of Game A?",
        form=["t* =", BOX],
        answers=[H("f2.0")],
        mistakes=M({"f2.0~5": "Solve t = (10 &minus; t)/2: 3t = 10."}),
        explain="Draw both best responses and mark the crossing."),
    Question(
        "f3",
        "(c) Game B: v<sub>i</sub> = (a + e<sub>j</sub>)e<sub>i</sub> &minus; "
        "e<sub>i</sub>&sup2;, so e<sub>i</sub> = (a + e<sub>j</sub>)/2. The equilibrium effort, "
        "as a multiple of a, and with a = 6?",
        form=["e* =", BOX, "&times; a; &nbsp; at a = 6:", BOX],
        answers=[H("f3.0"), H("f3.1")],
        mistakes=M({"f3.0~1/2": "Solve e = (a + e)/2: e = a."}),
        explain="Leave the answer in terms of a on the exam."),
    Question(
        "f4",
        "(d) Which game has downward-sloping best responses, and which property is that?",
        choices=[SLOPES, SLOPES_REV, SLOPES_SAME, SLOPES_CB],
        answers=[H("f4.c")],
        mistakes=M({
            "f4.c~" + SLOPES_REV: "In A, more cleaning by j lowers i's best response.",
            "f4.c~" + SLOPES_SAME: "In B, more effort by j raises i's best response.",
            "f4.c~" + SLOPES_CB: "The Cournot best response (90 &minus; q)/2 slopes down.",
        }),
        explain="Substitutes slope down, complements up."),
    Question(
        "f5",
        "(e) Why is each equilibrium unique, when the standards game had three?",
        choices=[UNIQUE, UNI_SOC, UNI_SYM, UNI_CONT],
        answers=[H("f5.c")],
        mistakes=M({
            "f5.c~" + UNI_SOC: "It makes each best response a single value, not a single "
                               "crossing.",
            "f5.c~" + UNI_SYM: "The standards game is symmetric, with three equilibria.",
            "f5.c~" + UNI_CONT: "Steeper best responses could cross several times.",
        }),
        explain="Four sentences on the exam."),
]

flatmates = GuidedProblem(
    "Part 9 &middot; Two games with a continuum of actions: A12.3",
    "Each player chooses a number. Best responses come from the first-order condition, and the "
    "equilibrium is where they cross.",
    FLAT_QUESTIONS, draw_flatmates, figsize=(8.0, 3.8), whole_figure=True,
    outro="About 15&ndash;20% of an exam paper.",
    sources=[PS("A12.3")],
)


# ======================================================================
# Where every step comes from (printed pages of s12_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "d1": NOTES("p. 3 &middot; reading a cell"), "d2": NOTES("p. 3&ndash;4 &middot; the dilemma"),
    "d3": NOTES("p. 5 &middot; dominance"), "d4": NOTES("p. 3 &middot; the dilemma"),
    "d5": NOTES("p. 15 &middot; review question 1"),
    "o1": NOTES("p. 4 &middot; the build-out"), "o2": NOTES("p. 4 &middot; the build-out"),
    "o3": PS("W2"), "o4": NOTES("p. 15 &middot; review question 3"),
    "e1": NOTES("p. 5&ndash;6 &middot; IESDS"), "e2": NOTES("p. 6 &middot; IESDS"),
    "e3": NOTES("p. 5 &middot; the ladder"), "e4": NOTES("p. 6 &middot; memory lines"),
    "e5": NOTES("p. 7&ndash;8 &middot; memory lines"),
    "e6": NOTES("p. 15 &middot; review question 2"), "e7": NOTES("p. 15 &middot; review question 2"),
    "k1": NOTES("p. 7&ndash;8 &middot; best response"), "k2": NOTES("p. 9&ndash;10 &middot; Cournot"),
    "k3": NOTES("p. 2 &middot; the benchmark"), "k4": NOTES("p. 9 &middot; the talent war"),
    "k5": NOTES("p. 9 &middot; Nash equilibrium"),
    "b1": NOTES("p. 10 &middot; Bertrand"), "b2": NOTES("p. 16 &middot; review question 5"),
    "b3": NOTES("p. 11 &middot; Try it (a)"), "b4": NOTES("p. 12 &middot; Try it (b)"),
    "b5": NOTES("p. 12 &middot; Try it (c)"), "b6": NOTES("p. 16 &middot; review question 4"),
    "b7": NOTES("p. 14 &middot; worksheet task 3"), "b8": NOTES("p. 10 &middot; why so different"),
    "x1": PS("W1"), "x2": NOTES("p. 13 &middot; indifference"),
    "x3": NOTES("p. 14 &middot; worksheet tasks 1&ndash;2"),
    "x4": NOTES("p. 14 &middot; worksheet task 2"), "x5": NOTES("p. 14 &middot; worksheet task 2"),
    "x6": NOTES("p. 13 &middot; the twist"), "x7": NOTES("p. 16 &middot; review question 6"),
    "x8": NOTES("p. 16 &middot; review question 6"),
    "s1": PS("A12.1 (a)"), "s2": PS("A12.1 (b)"), "s3": PS("A12.1 (c)"), "s4": PS("A12.1 (d)"),
    "s5": PS("A12.1 (e)"), "s6": PS("A12.1 (f)"),
    "a1": PS("A12.2 (a)"), "a2": PS("A12.2 (b)"), "a3": PS("A12.2 (c)"), "a4": PS("A12.2 (d)"),
    "a5": PS("A12.2 (e)"),
    "f1": PS("A12.3 (a)"), "f2": PS("A12.3 (b)"), "f3": PS("A12.3 (c)"), "f4": PS("A12.3 (d)"),
    "f5": PS("A12.3 (e)"),
}

for _q in (DILEMMA_QUESTIONS + COORD_QUESTIONS + IESDS_QUESTIONS + COURNOT_QUESTIONS
           + BERTRAND_QUESTIONS + MIXED_QUESTIONS + STANDARD_QUESTIONS + AUDIT_QUESTIONS
           + FLAT_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
