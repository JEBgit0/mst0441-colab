"""
guided_s13.py - session 13 guided page: dynamic games and credibility.

    Part 1  standards   the sequential standards game: strategies, the induced
                        matrix and backward induction
    Part 2  entry       the entry game: a threat nobody would carry out
    Part 3  subgames    information sets, strategies and proper subgames
                        (review question 1)
    Part 4  leader      Stackelberg: the API market with a committed leader
    Part 5  tsmc        the first Try it: TSMC and Samsung
    Part 6  worksheet   the worksheet: an entry tree with an exit, and the
                        server market
    Part 7  citybrew    review questions 2-3: CityBrew and BeanCo
    Part 8  deviation   the one-stage deviation principle and the centipede
                        (the second Try it, review questions 5-6)
    Part 9  problems    problems A13.1 and A13.2

Answers are hashes in answers_s13.py, generated from
answer_keys/s13_keys.py in the private repo. The maths is games.py: its
self-check reproduces every number asked for here.
"""

import numpy as np

import game_plots as gm
import guided_plots as gp
from games import Leaf, Matrix, Node
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, INK, LINE, MUTE, NEW

H, M = answers("s13")
DEL = "&delta;"

# The course's trees. Player 0 moves at the root.
STANDARDS = Node(0, "x0", [("O", Node(1, "x1", [("o", Leaf(2, 1)), ("f", Leaf(0, 0))])),
                           ("F", Node(1, "x2", [("o", Leaf(0, 0)), ("f", Leaf(1, 2))]))])
INDUCED = Matrix(["O", "F"], ["oo", "of", "fo", "ff"],
                 [[(2, 1), (2, 1), (0, 0), (0, 0)], [(0, 0), (1, 2), (0, 0), (1, 2)]])
ENTRY = Node(0, "x0", [("Out", Leaf(0, 10)),
                       ("In", Node(1, "x1", [("Fight", Leaf(-1, 1)), ("Accommodate", Leaf(2, 4))]))])
VOLUNTARY = Node(0, "x0", [("N", Leaf(1.5, 1.5)), ("Y", Node(0, "x1", [
    ("O", Node(1, "x2", [("o", Leaf(2, 1)), ("f", Leaf(0, 0))])),
    ("F", Node(1, "x3", [("o", Leaf(0, 0)), ("f", Leaf(1, 2))]))]))])
SHEET = Node(0, "x0", [("Out", Leaf(0, 12)), ("In", Node(1, "x1", [
    ("Share", Leaf(4, 6)),
    ("Fight", Node(0, "x2", [("Exit", Leaf(-1, 7)), ("Stay", Leaf(-3, 3))]))]))])
CITY = Node(0, "c0", [("Wait", Leaf(2, 6)), ("Expand", Node(1, "b", [
    ("Concede", Leaf(5, 3)),
    ("Match", Node(0, "c1", [("Hold", Leaf(1, 2)), ("Discount", Leaf(0, 1))]))]))])
CENTIPEDE = Node(0, "1a", [("N", Leaf(1, 1)), ("C", Node(1, "2a", [("n", Leaf(0, 3)), ("c", Node(
    0, "1b", [("N", Leaf(2, 2)), ("C", Node(1, "2b", [("n", Leaf(1, 4)), ("c", Leaf(3, 3))]))]))]))])
A13 = Node(0, "x0", [("Out", Leaf(0, 10)),
                     ("Enter", Node(1, "x1", [("Fight", Leaf(-2, 1)), ("Accommodate", Leaf(3, 4))]))])


# ------------------------------------------------------------------ drawing ---

def _panel(ax, xmax, ymax, xlabel, ylabel, title, xticks=(), yticks=()):
    gp.frame(ax, xmax, ymax, xlabel, ylabel)
    ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.tick_params(colors=MUTE, labelsize=8.5)


def _leader(ax, a, c, top, cournot=False, leader=False, follower=True):
    # The follower's best response (a - c - q1)/2 with q1 across and q2 up,
    # and the leader's, for the Cournot crossing.
    q = np.linspace(0, top, 200)
    if follower:
        ax.plot(q, np.clip((a - c - q) / 2, 0, None), color=CURVE, lw=2, label="follower's BR$_2$")
    if cournot:
        ax.plot(np.clip((a - c - q) / 2, 0, None), q, color=LINE, lw=1.4, ls="--",
                label="leader's BR$_1$")
        k = (a - c) / 3
        gp.dot(ax, k, k, "C", 6, 4, colour=MUTE)
    if leader:
        q1 = (a - c) / 2
        gp.dot(ax, q1, q1 / 2, "S", 6, 4, colour=GREEN)


# ======================================================================
# Part 1: the sequential standards game
# ======================================================================

def draw_standards(fig, stage):
    tree, mat = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1, 1.15]))
    plan = {}
    if stage >= 4:
        plan = {"x1": "o", "x2": "f", "x0": "O"}
    gm.tree(tree, STANDARDS, names=("Anthropic", "OpenAI"), plan=plan,
            info=[("x1", "x2")] if stage >= 6 else (), title="Anthropic ships first")
    if stage >= 2:
        gm.matrix(mat, INDUCED, "Anthropic", "OpenAI", fontsize=10,
                  nash=INDUCED.pure_nash() if stage >= 3 else (),
                  mark=(0, 1) if stage >= 5 else None, title="The induced matrix")
    else:
        mat.axis("off")
    fig.subplots_adjust(wspace=0.1)


FIRST = "OpenAI's best response to a live open protocol is to adopt it, so Anthropic, knowing this, ships the standard it prefers: the same payoffs, a different game"
FIRST_PAY = "Moving first changes the payoffs in Anthropic's favour"
FIRST_ALWAYS = "Moving first always helps"
FIRST_NONE = "Nothing changes: the game still has two equilibria and no way to pick"

PROFILE = "(O, of): a full plan, including adopting f at x2, which is never reached. (O, oo) and (F, ff) are Nash but not subgame perfect: each has OpenAI committed to a move it would not make at one of its nodes"
PROF_PATH = "The path O then o is the whole solution"
PROF_ALL = "All three Nash equilibria are subgame perfect"
PROF_FF = "(F, ff), since OpenAI prefers its own standard"

STANDARD_QUESTIONS = [
    Question(
        "s1",
        "The standards game: Anthropic backs O, the open protocol, OpenAI F, the function-calling "
        "spec; matching beats a split and each prefers its own. Simultaneously there are two "
        "equilibria. Now Anthropic ships first and OpenAI sees it. Why does that settle it?",
        choices=[FIRST, FIRST_PAY, FIRST_ALWAYS, FIRST_NONE],
        answers=[H("s1.c")],
        mistakes=M({
            "s1.c~" + FIRST_PAY: "The payoff matrix has not changed at all.",
            "s1.c~" + FIRST_ALWAYS: "In matching pennies you would happily let your opponent "
                                    "move first.",
            "s1.c~" + FIRST_NONE: "OpenAI now sees what was shipped.",
        }),
        explain="Anthropic shipped its protocol in late 2024; by spring 2025 OpenAI had adopted "
                "it."),
    Question(
        "s2",
        "A strategy is a complete plan: an action at every information set, reached or not. How "
        "many pure strategies does each player have?",
        form=["Anthropic", BOX, "&nbsp; OpenAI", BOX],
        answers=[H("s2.0"), H("s2.1")],
        mistakes=M({"s2.1~2": "OpenAI moves at two nodes, with two actions at each: 2 &times; 2."}),
        explain="Read 'of' as: o if O was shipped, f if F was."),
    Question(
        "s3",
        "Collapse the tree into its induced matrix, two strategies against four. How many pure "
        "Nash equilibria?",
        form=["", BOX],
        answers=[H("s3.0")],
        mistakes=M({"s3.0~1": "Check (O, oo) and (F, ff) as well.",
                    "s3.0~2": "Check (O, oo), (O, of) and (F, ff)."}),
        explain="(O, oo), (O, of) and (F, ff). Going from tree to matrix loses who moved first."),
    Question(
        "s4",
        "Backward induction: at x1 OpenAI compares 1 with 0, at x2 0 with 2, and then Anthropic "
        "chooses at the root. The payoffs at the end?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("s4.0"), H("s4.1")],
        mistakes=M({"s4.0~1": "At the root O leads to (2, 1) and F to (1, 2): Anthropic picks O."}),
        explain="Thick branches: the choice at every node."),
    Question(
        "s5",
        "State the solution properly, and say which Nash equilibria fail the subgame audit.",
        choices=[PROFILE, PROF_PATH, PROF_ALL, PROF_FF],
        answers=[H("s5.c")],
        mistakes=M({
            "s5.c~" + PROF_PATH: "A strategy says what OpenAI does at x2 too.",
            "s5.c~" + PROF_ALL: "In (F, ff), OpenAI plans f at x1, where o pays 1 and f 0.",
            "s5.c~" + PROF_FF: "At the root, Anthropic compares 2 with 1.",
        }),
        explain="Backward induction predicts what would have happened, too."),
    Question(
        "s6",
        "In the simultaneous version a dashed line ties OpenAI's two nodes into one information "
        "set. How many information sets and pure strategies does OpenAI have now?",
        form=["information sets", BOX, "&nbsp; strategies", BOX],
        answers=[H("s6.0"), H("s6.1")],
        mistakes=M({"s6.1~4": "One information set, two actions: two strategies."}),
        explain="Any simultaneous-move game is a game of imperfect information."),
]

standards = GuidedProblem(
    "Part 1 &middot; The standards game, in sequence",
    "Payoffs (Anthropic, OpenAI). The same payoffs as the simultaneous game, with one change: "
    "Anthropic moves first and OpenAI sees what it shipped.",
    STANDARD_QUESTIONS, draw_standards, figsize=(8.4, 3.8), whole_figure=True,
    outro="Complete information is knowing the payoffs; perfect information is knowing where "
          "you are in the tree.",
    sources=[NOTES("p. 1&ndash;7")],
)


# ======================================================================
# Part 2: the entry game
# ======================================================================

def draw_entry(ax, stage):
    plan = {"x1": "Accommodate", "x0": "In"} if stage >= 3 else {}
    struck = [("x1", "Fight"), ("x0", "Out")] if stage >= 3 else []
    gm.tree(ax, ENTRY, names=("Anthropic", "OpenAI"), plan=plan, struck=struck,
            title="Payoffs (Anthropic, OpenAI) in $bn, net of the entry cost")


ENTRY_NE = "(In, Accommodate) and (Out, Fight)"
ENTRY_ONE = "Only (In, Accommodate)"
ENTRY_OUT = "Only (Out, Fight)"
ENTRY_NONE = "There is no pure Nash equilibrium"

SILLY = "Given Fight, staying out pays 0 against -1, so Out is a best response; and given Out, OpenAI's plan is never called on, so Fight costs it nothing. Nash never audits a plan off the path"
SILLY_REAL = "OpenAI would really fight, since it announced it would"
SILLY_NOT = "It is not a Nash equilibrium at all"
SILLY_BEST = "It is the best outcome for both"

CREDIBLE = "Change the payoffs before the game: a commitment, such as capacity built or contracts signed, that makes fighting pay OpenAI more than accommodating"
CRED_SAY = "Announce the fight louder and more often"
CRED_NOW = "Nothing can make it credible: entry is always accommodated"
CRED_SIZE = "Grow bigger, since big firms always fight"

ENTRY_QUESTIONS = [
    Question(
        "n1",
        "The entry game: Anthropic chooses Out, which pays (0, 10), or In; after In, OpenAI "
        "fights, (&minus;1, 1), or accommodates, (2, 4). Fold it into a matrix. The pure Nash "
        "equilibria?",
        choices=[ENTRY_NE, ENTRY_ONE, ENTRY_OUT, ENTRY_NONE],
        answers=[H("n1.c")],
        mistakes=M({
            "n1.c~" + ENTRY_ONE: "Check (Out, Fight): can either gain by deviating alone?",
            "n1.c~" + ENTRY_OUT: "Check (In, Accommodate) as well.",
            "n1.c~" + ENTRY_NONE: "Check (In, Accommodate).",
        }),
        explain="One sensible, one held up by words."),
    Question(
        "n2",
        "Why is (Out, Fight) a Nash equilibrium at all?",
        choices=[SILLY, SILLY_REAL, SILLY_NOT, SILLY_BEST],
        answers=[H("n2.c")],
        mistakes=M({
            "n2.c~" + SILLY_REAL: "At x1, fighting pays 1 and accommodating 4.",
            "n2.c~" + SILLY_NOT: "Check both players' deviations: neither gains.",
            "n2.c~" + SILLY_BEST: "Anthropic gets 0 instead of 2.",
        }),
        explain="Non-credible threats live in the unaudited part of the strategy."),
    Question(
        "n3",
        "Backward induction. At x1 OpenAI compares 1 with 4; at the root Anthropic compares the "
        "result with 0. The payoffs of the subgame-perfect equilibrium?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("n3.0"), H("n3.1")],
        mistakes=M({"n3.0~0": "OpenAI would accommodate, so In pays Anthropic 2."}),
        explain="(In, Accommodate): the threat fails the audit at the very subgame it is about."),
    Question(
        "n4",
        "What would it take to make the threat credible?",
        choices=[CREDIBLE, CRED_SAY, CRED_NOW, CRED_SIZE],
        answers=[H("n4.c")],
        mistakes=M({
            "n4.c~" + CRED_SAY: "Words change no payoff at x1.",
            "n4.c~" + CRED_NOW: "Change the payoffs at x1 and the answer changes.",
            "n4.c~" + CRED_SIZE: "Size is not a payoff.",
        }),
        explain="An announcement is worth nothing unless the payoffs make carrying it out optimal."),
    Question(
        "n5",
        "Fighting pays OpenAI 1 now. Above what payoff from fighting does the threat become "
        "credible, so that Anthropic stays out?",
        form=["above", BOX],
        answers=[H("n5.0")],
        mistakes=M({"n5.0~0": "Compare with what accommodating pays OpenAI at x1."}),
        explain="Then Fight is OpenAI's best move at x1, and Anthropic compares 0 with &minus;1."),
]

entry = GuidedProblem(
    "Part 2 &middot; A threat nobody would carry out",
    "OpenAI is the incumbent and announces that entry will be met with a fight. Should "
    "Anthropic believe it?",
    ENTRY_QUESTIONS, draw_entry, figsize=(6.2, 3.8),
    outro="Subgame perfection: a best response at every node, reached or not.",
    sources=[NOTES("p. 2&ndash;3"), NOTES("p. 9")],
)


# ======================================================================
# Part 3: information sets, strategies and subgames
# ======================================================================

def draw_subgames(ax, stage):
    gm.tree(ax, VOLUNTARY, names=("1", "2"), info=[("x2", "x3")],
            title="The voluntary standards game")
    if stage >= 4:
        ax.text(0.98, 0.95, "2 proper subgames:\nthe whole game, and\nthe one at x1",
                transform=ax.transAxes, ha="right", va="top", color=GREEN, fontsize=9)


PERFECT = "Perfect information: the wholesaler observes the price, so each of its information sets is a single node"
PERF_IMP = "Imperfect information, since the wholesaler moves second"
PERF_COMP = "Incomplete information, since the retailer does not know the wholesaler's choice"
PERF_SIM = "Imperfect information, since both players move once"

OFFPATH = "A strategy must say what the wholesaler does after a price it expects never to see: without it the matrix cannot be filled in, the retailer's choice depends on it, and a threat is exactly such an off-path plan"
OFF_BOOK = "It need not: only actions on the path count"
OFF_TIE = "Only to break ties"
OFF_LAW = "Because contracts require it"

SUBGAME_QUESTIONS = [
    Question(
        "g1",
        "Review question 1: a retailer sets its price, High or Low; a wholesaler observes it and "
        "chooses Renew or Terminate. (a) Perfect or imperfect information?",
        choices=[PERFECT, PERF_IMP, PERF_COMP, PERF_SIM],
        answers=[H("g1.c")],
        mistakes=M({
            "g1.c~" + PERF_IMP: "Moving second is fine if you see the first move.",
            "g1.c~" + PERF_COMP: "Complete information is about payoffs and rules.",
            "g1.c~" + PERF_SIM: "Imperfect means some information set has several nodes.",
        }),
        explain="Perfect and complete are different axes."),
    Question(
        "g2",
        "(b) How many pure strategies does the wholesaler have? (c) And a player with three "
        "information sets and two actions at each?",
        form=["(b)", BOX, "&nbsp; (c)", BOX],
        answers=[H("g2.0"), H("g2.1")],
        mistakes=M({"g2.0~2": "Two information sets, two actions each: RR, RT, TR, TT.",
                    "g2.1~6": "Multiply across information sets: 2 &times; 2 &times; 2."}),
        explain="Multiply the action counts across information sets."),
    Question(
        "g3",
        "Why must a strategy name an action even where the wholesaler expects never to be?",
        choices=[OFFPATH, OFF_BOOK, OFF_TIE, OFF_LAW],
        answers=[H("g3.c")],
        mistakes=M({
            "g3.c~" + OFF_BOOK: "Then you could not even state a threat.",
            "g3.c~" + OFF_TIE: "Bookkeeping, beliefs and credibility: three reasons.",
            "g3.c~" + OFF_LAW: "It is a definition, not a contract.",
        }),
        explain="Off-path play is what makes on-path play rational."),
    Question(
        "g4",
        "(d) If the wholesaler chose without seeing the price: its information sets and pure "
        "strategies? And the figure's voluntary standards game, where player 2's two nodes "
        "share one information set: how many proper subgames, the whole game included?",
        form=["(d) sets", BOX, "strategies", BOX, "&nbsp; subgames", BOX],
        answers=[H("g4.0"), H("g4.1"), H("g4.2")],
        mistakes=M({"g4.2~4": "x2 and x3 share an information set, so neither roots a subgame.",
                    "g4.2~3": "x2 and x3 share an information set, so neither roots a subgame."}),
        explain="The subgame at x1 contains a simultaneous game: solve it as a game, not node by "
                "node."),
]

subgames = GuidedProblem(
    "Part 3 &middot; Information sets, strategies and subgames",
    "An information set is a collection of nodes the mover cannot tell apart. A proper subgame "
    "starts at a single node and never cuts an information set.",
    SUBGAME_QUESTIONS, draw_subgames, figsize=(6.6, 4.0),
    outro="A subgame-perfect equilibrium is a Nash equilibrium in every proper subgame.",
    sources=[NOTES("p. 3&ndash;8"), NOTES("p. 17, review question 1")],
)


# ======================================================================
# Part 4: Stackelberg, the API market with a committed leader
# ======================================================================

def draw_leader(fig, stage):
    br, bars = fig.subplots(1, 2)
    _panel(br, 92, 50, "leader's q$_1$", "follower's q$_2$", "The follower's line is the "
           "leader's menu", xticks=[30, 45] if stage >= 2 else [30],
           yticks=([22.5, 30] if stage >= 2 else [30]) + ([45] if stage >= 1 else []))
    br.set_yticklabels(["%g" % t for t in br.get_yticks()])
    _leader(br, 100, 10, 92, cournot=True, leader=stage >= 2, follower=stage >= 1)
    if stage >= 5:
        br.plot([45, 33.75], [22.5, 22.5], color=NEW, lw=1.2, ls=":")
        gp.dot(br, 33.75, 22.5, "BR$_1$(22.5)", -8, 8, colour=NEW, ha="right")
    gp.legend(br, loc="upper right")

    for side in ("top", "right"):
        bars.spines[side].set_visible(False)
    bars.set_title("Profits: Cournot (grey) and Stackelberg", loc="left", color=INK, fontsize=9.5)
    xs = np.arange(3)
    bars.bar(xs - 0.18, [900, 900, 1800], width=0.34, color=GREY)
    if stage >= 3:
        bars.bar(xs - 0.18 + 0.36, [1012.5, 506.25, 1518.75 if stage >= 4 else 0], width=0.34,
                 color=[GREEN, CURVE, LINE])
    bars.set_xticks(xs)
    bars.set_xticklabels(["leader", "follower", "industry"], fontsize=9, color=INK)
    bars.set_yticks([])
    bars.set_ylim(0, 2000)
    fig.subplots_adjust(wspace=0.25)


COMMIT = "Commitment: OpenAI signed irreversible contracts before Anthropic moved. Fewer options change the rival's behaviour, and commitment turns an off-path plan into an on-path fact"
COMMIT_SAY = "OpenAI said it first"
COMMIT_BIG = "OpenAI is the larger firm"
COMMIT_COST = "OpenAI has lower costs"

LEADER_QUESTIONS = [
    Question(
        "l1",
        "Session 12's market, P = 100 &minus; Q and cost 10, but OpenAI commits its capacity "
        "first and Anthropic sees it. The follower's best response is q<sub>2</sub> = (90 "
        "&minus; q<sub>1</sub>)/2. Its reply to q<sub>1</sub> = 0, and where the line meets "
        "the q<sub>1</sub> axis?",
        form=["reply to 0:", BOX, "&nbsp; zero at q<sub>1</sub> =", BOX],
        answers=[H("l1.0"), H("l1.1")],
        explain="Sequential rationality forces the follower onto this line, whatever the leader "
                "did."),
    Question(
        "l2",
        "The leader substitutes the line into its profit: (90 &minus; q<sub>1</sub>)q<sub>1</sub>"
        "/2. Its quantity, and the follower's answer?",
        form=["q<sub>1</sub> =", BOX, "&nbsp; q<sub>2</sub> =", BOX],
        answers=[H("l2.0"), H("l2.1")],
        mistakes=M({"l2.0~30": "That is Cournot. The leader maximizes along the follower's line.",
                    "l2.1~45": "The follower replies with (90 &minus; 45)/2."}),
        explain="A number for the leader, a function for the follower."),
    Question(
        "l3",
        "Total output, the price, and the two profits?",
        form=["Q =", BOX, "&nbsp; P =", BOX, "&nbsp; leader", BOX, "&nbsp; follower", BOX],
        answers=[H("l3.0"), H("l3.1"), H("l3.2"), H("l3.3")],
        mistakes=M({"l3.2~1462.5": "Profit is (P &minus; 10)q<sub>1</sub>: (32.5 &minus; 10) "
                                   "&times; 45."}),
        explain="Against Cournot's 30, 30, a price of 40 and 900 each."),
    Question(
        "l4",
        "Industry profit under Stackelberg, against Cournot's 1800?",
        form=["", BOX],
        answers=[H("l4.0")],
        explain="The leader gains 112.5, the follower loses 393.75: industry profit falls, "
                "output rises, consumers prefer Stackelberg."),
    Question(
        "l5",
        "In the Cournot version OpenAI just announces 'we will serve 45'. If Anthropic believed "
        "it and served 22.5, what would OpenAI's own best response be?",
        form=["BR<sub>1</sub>(22.5) =", BOX],
        answers=[H("l5.0")],
        mistakes=M({"l5.0~45": "(90 &minus; 22.5)/2: the leader itself would walk away from 45."}),
        explain="Not self-enforcing, so the follower should not believe it."),
    Question(
        "l6",
        "So what makes 45 credible in the Stackelberg game?",
        choices=[COMMIT, COMMIT_SAY, COMMIT_BIG, COMMIT_COST],
        answers=[H("l6.c")],
        mistakes=M({
            "l6.c~" + COMMIT_SAY: "Saying it first is exactly the announcement that fails.",
            "l6.c~" + COMMIT_BIG: "The labs are identical.",
            "l6.c~" + COMMIT_COST: "Both serve at cost 10.",
        }),
        explain="In a game, fewer options can raise your payoff. Session 11: a trade agreement "
                "is a commitment device."),
]

leader = GuidedProblem(
    "Part 4 &middot; Commitment: Stackelberg",
    "Cournot with a first mover. Every q<sub>1</sub> roots its own subgame, so the follower "
    "must best-respond to whatever it sees.",
    LEADER_QUESTIONS, draw_leader, figsize=(8.0, 3.8), whole_figure=True,
    outro="S lies on the follower's line and off the leader's: that is commitment.",
    sources=[NOTES("p. 9&ndash;12")],
)


# ======================================================================
# Part 5: the Try it, TSMC and Samsung
# ======================================================================

def draw_tsmc(fig, stage):
    br, bars = fig.subplots(1, 2)
    _panel(br, 88, 46, "TSMC q$_1$", "Samsung q$_2$", "Thousands of wafers a month",
           xticks=([42] if stage >= 1 else []) + ([28] if stage >= 4 else []),
           yticks=([21] if stage >= 1 else []) + ([28] if stage >= 4 else []) + [42])
    _leader(br, 104, 20, 88, cournot=stage >= 4, leader=stage >= 1)
    gp.legend(br, loc="upper right")
    for side in ("top", "right"):
        bars.spines[side].set_visible(False)
    bars.set_title("Monthly profits, $ millions", loc="left", color=INK, fontsize=9.5)
    xs = np.arange(2)
    if stage >= 2:
        bars.bar(xs - 0.18, [882, 441], width=0.34, color=GREEN, label="Stackelberg")
    if stage >= 4:
        bars.bar(xs + 0.18, [784, 784], width=0.34, color=GREY, label="Cournot")
    bars.set_xticks(xs)
    bars.set_xticklabels(["TSMC", "Samsung"], fontsize=9, color=INK)
    bars.set_yticks([])
    bars.set_ylim(0, 1000)
    gp.legend(bars, loc="upper right")
    fig.subplots_adjust(wspace=0.25)


PAYS = "Samsung, the follower: 441 against 784. Consumers gain, since output rises from 56 to 63 and the price falls from 48 to 41"
PAYS_CONS = "Consumers, through a higher price"
PAYS_TSMC = "TSMC, which has to produce more"
PAYS_NONE = "Nobody: both earn more than under Cournot"

TSMC_QUESTIONS = [
    Question(
        "m1",
        "Try it: TSMC commits capacity first; Samsung observes it. P = 104 &minus; Q, cost 20 "
        "for both. Samsung's best response is q<sub>2</sub> = (84 &minus; q<sub>1</sub>)/2. "
        "(a) Both quantities?",
        form=["TSMC", BOX, "&nbsp; Samsung", BOX],
        answers=[H("m1.0"), H("m1.1")],
        mistakes=M({"m1.0~28": "That is Cournot. TSMC's profit collapses to (84 &minus; "
                               "q<sub>1</sub>)q<sub>1</sub>/2."}),
        explain="The leader's rule: q<sub>1</sub> = (104 &minus; c)/2."),
    Question(
        "m2",
        "The wafer price, and the monthly profits in millions?",
        form=["P =", BOX, "&nbsp; TSMC", BOX, "&nbsp; Samsung", BOX],
        answers=[H("m2.0"), H("m2.1"), H("m2.2")],
        mistakes=M({"m2.1~1722": "The margin is P &minus; 20 = 21."}),
        explain="About ten and a half billion a year for TSMC."),
    Question(
        "m3",
        "(b) Next node, TSMC commits 36 thousand wafers: same demand, same leadership. Which "
        "marginal cost is it revealing?",
        form=["c =", BOX],
        answers=[H("m3.0")],
        mistakes=M({"m3.0~68": "Solve (104 &minus; c)/2 = 36."}),
        explain="Observable capacity reveals the cost."),
    Question(
        "m4",
        "(c) Neither fab can observe the other, back at cost 20. Each Cournot quantity, the "
        "price, and each profit?",
        form=["q =", BOX, "&nbsp; P =", BOX, "&nbsp; &pi; =", BOX],
        answers=[H("m4.0"), H("m4.1"), H("m4.2")],
        explain="(104 &minus; 20)/3 each."),
    Question(
        "m5",
        "Who pays for TSMC's leadership?",
        choices=[PAYS, PAYS_CONS, PAYS_TSMC, PAYS_NONE],
        answers=[H("m5.c")],
        mistakes=M({
            "m5.c~" + PAYS_CONS: "The price falls under leadership: 41 against 48.",
            "m5.c~" + PAYS_TSMC: "TSMC earns 882 against 784.",
            "m5.c~" + PAYS_NONE: "Samsung earns 441 against 784.",
        }),
        explain="The follower loses more than the leader gains."),
]

tsmc = GuidedProblem(
    "Part 5 &middot; TSMC and Samsung",
    "The notes' Try it: nearly every leading AI chip is fabricated by one firm, and capacity is "
    "committed years ahead. Model the advanced node as a Stackelberg game.",
    TSMC_QUESTIONS, draw_tsmc, figsize=(8.0, 3.8), whole_figure=True,
    outro="Leadership is worth something only because the commitment is observed.",
    sources=[NOTES("p. 11&ndash;12")],
)


# ======================================================================
# Part 6: the worksheet
# ======================================================================

def draw_worksheet(fig, stage):
    tree, br = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.15, 1]))
    plan = {}
    if stage >= 1:
        plan = {"x2": "Exit", "x1": "Fight"}
    if stage >= 2:
        plan["x0"] = "Out"
    gm.tree(tree, SHEET, names=("Challenger", "Incumbent"), plan=plan, fontsize=9,
            title="Entry with an exit")
    _panel(br, 50, 50, "q$_1$", "q$_2$", "The server market", xticks=range(12, 49, 12),
           yticks=range(12, 49, 12))
    br.grid(True, color="#e5e7eb", lw=0.6)
    br.set_axisbelow(True)
    gp.dot(br, 0, 24, "", colour=CURVE)
    if stage >= 5:
        _leader(br, 60, 12, 50, cournot=stage >= 6, leader=True)
    gp.legend(br, loc="upper right")
    fig.subplots_adjust(wspace=0.15)


SHEET_SPE = "Challenger: Out, and Exit after a fight; Incumbent: Fight. The outcome is (0, 12)"
SHEET_PATH = "Out, with nothing more to say"
SHEET_IN = "Challenger: In and Exit; Incumbent: Share. The outcome is (4, 6)"
SHEET_STAY = "Challenger: In and Stay; Incumbent: Share"

CREDIBLE_HERE = "Here a fight makes the challenger exit, and that leaves the incumbent 7, more than the 6 from sharing; in the lecture's game fighting paid 1 against 4"
CH_SAME = "It is the same threat; only the words differ"
CH_BIG = "The incumbent is bigger here"
CH_FIRST = "The incumbent moves first here"

HIDDEN = "(In and Stay; Share): Stay is never played, so Share is a best response and In pays 4; but at the challenger's last node Stay pays -3 against -1, so the profile fails the audit"
HID_OUT = "(Out and Exit; Fight), the subgame-perfect one"
HID_SHARE = "(In and Exit; Share), which is subgame perfect too"
HID_NONE = "There is no other Nash equilibrium"

SHEET_QUESTIONS = [
    Question(
        "w1",
        "Worksheet, left: thicken the choices from the bottom. After a fight the challenger "
        "exits, &minus;1 against &minus;3. The incumbent then compares sharing with fighting: "
        "its payoff from each?",
        form=["Share", BOX, "&nbsp; Fight", BOX],
        answers=[H("w1.0"), H("w1.1")],
        mistakes=M({"w1.1~3": "After a fight the challenger exits, so fighting pays 7."}),
        explain="The incumbent fights."),
    Question(
        "w2",
        "Write the subgame-perfect equilibrium as a full profile.",
        choices=[SHEET_SPE, SHEET_PATH, SHEET_IN, SHEET_STAY],
        answers=[H("w2.c")],
        mistakes=M({
            "w2.c~" + SHEET_PATH: "A full profile names an action at every node.",
            "w2.c~" + SHEET_IN: "Against Exit, the incumbent fights: 7 &gt; 6.",
            "w2.c~" + SHEET_STAY: "Stay pays &minus;3 against Exit's &minus;1.",
        }),
        explain="Circle the outcome on the sheet: (0, 12)."),
    Question(
        "w3",
        "Why is the threat credible here and not in the lecture's entry game?",
        choices=[CREDIBLE_HERE, CH_SAME, CH_BIG, CH_FIRST],
        answers=[H("w3.c")],
        mistakes=M({
            "w3.c~" + CH_SAME: "Compare the incumbent's payoffs at its own node.",
            "w3.c~" + CH_BIG: "Size is not in the tree.",
            "w3.c~" + CH_FIRST: "The challenger still moves first.",
        }),
        explain="A threat is credible when carrying it out is optimal at the node."),
    Question(
        "w4",
        "Worksheet task 2: find the Nash equilibrium hiding in this game that fails the audit.",
        choices=[HIDDEN, HID_OUT, HID_SHARE, HID_NONE],
        answers=[H("w4.c")],
        mistakes=M({
            "w4.c~" + HID_OUT: "That one passes the audit.",
            "w4.c~" + HID_SHARE: "Against Exit, the incumbent gains by fighting: not even Nash.",
            "w4.c~" + HID_NONE: "Let the challenger threaten to stay.",
        }),
        explain="This time the non-credible threat is the challenger's."),
    Question(
        "w5",
        "Right panel: the server market, P = 60 &minus; Q and cost 12, in thousands of dollars "
        "per server. Firm 2's line starts at 24. The committed leader's quantity and the "
        "follower's answer?",
        form=["q<sub>1</sub> =", BOX, "&nbsp; q<sub>2</sub> =", BOX],
        answers=[H("w5.0"), H("w5.1")],
        mistakes=M({"w5.0~16": "That is Cournot. The leader's rule is (60 &minus; 12)/2."}),
        explain="Label it S, on the follower's line."),
    Question(
        "w6",
        "The Cournot crossing, labelled C: each quantity, and the price under each?",
        form=["q =", BOX, "&nbsp; P Cournot", BOX, "&nbsp; P Stackelberg", BOX],
        answers=[H("w6.0"), H("w6.1"), H("w6.2")],
        explain="If your S is on the follower's line and off firm 1's, you have understood "
                "commitment."),
]

worksheet = GuidedProblem(
    "Part 6 &middot; The worksheet",
    "The two panels to finish before the in-person session: an entry tree where the challenger "
    "can exit after a fight, and the server market's best responses.",
    SHEET_QUESTIONS, draw_worksheet, figsize=(8.4, 3.9), whole_figure=True,
    outro="Bring the sheet: we open by going through it.",
    sources=[NOTES("p. 17, worksheet")],
)


# ======================================================================
# Part 7: review questions 2-3, CityBrew and BeanCo
# ======================================================================

def draw_city(ax, stage):
    plan = {}
    if stage >= 2:
        plan = {"c1": "Hold", "b": "Concede", "c0": "Expand"}
    struck = [("b", "Match")] if stage >= 4 else []
    gm.tree(ax, CITY, names=("CityBrew", "BeanCo"), plan=plan, struck=struck,
            title="Payoffs (CityBrew, BeanCo)")


CITY_SPE = "CityBrew: Expand, and Hold if matched; BeanCo: Concede"
CITY_PATH = "Expand, then Concede"
CITY_WAIT = "CityBrew: Wait; BeanCo: Match"
CITY_DISC = "CityBrew: Expand, and Discount if matched; BeanCo: Match"

THREAT = "(Wait and Hold; Match) is Nash: given Match, expanding pays CityBrew 1 against 2 from waiting, and BeanCo's plan is never called on. But in the subgame at BeanCo's node, matching pays 2 against 3 from conceding, so the threat should not be believed"
THREAT_GOOD = "The announcement is credible, since BeanCo said it publicly"
THREAT_ROOT = "The profile fails at the root: CityBrew should expand"
THREAT_NONE = "There is no Nash equilibrium in which CityBrew waits"

CITY_QUESTIONS = [
    Question(
        "c1",
        "Review question 2: CityBrew expands or waits; after Expand, BeanCo concedes or matches; "
        "after Match, CityBrew holds or discounts. How many proper subgames, counting the whole "
        "game?",
        form=["", BOX],
        answers=[H("c1.0")],
        mistakes=M({"c1.0~2": "Every decision node roots one: the root, BeanCo's node and "
                              "CityBrew's second node."}),
        explain="Perfect information: every node roots a subgame."),
    Question(
        "c2",
        "Backward induction: the payoffs of the subgame-perfect outcome?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("c2.0"), H("c2.1")],
        mistakes=M({"c2.0~2": "Concede pays BeanCo 3, matching only 2 after CityBrew holds."}),
        explain="Hold 1 &gt; Discount 0; Concede 3 &gt; Match 2; Expand 5 &gt; Wait 2."),
    Question(
        "c3",
        "State it as a full strategy profile, not just the path.",
        choices=[CITY_SPE, CITY_PATH, CITY_WAIT, CITY_DISC],
        answers=[H("c3.c")],
        mistakes=M({
            "c3.c~" + CITY_PATH: "CityBrew also has a plan at the node after Match.",
            "c3.c~" + CITY_WAIT: "Work from the bottom: BeanCo would concede.",
            "c3.c~" + CITY_DISC: "After Match, holding pays 1 and discounting 0.",
        }),
        explain="The plan at the unreached node is part of the answer."),
    Question(
        "c4",
        "Review question 3: BeanCo's CEO announces 'if you expand, we will match, whatever it "
        "costs'.",
        choices=[THREAT, THREAT_GOOD, THREAT_ROOT, THREAT_NONE],
        answers=[H("c4.c")],
        mistakes=M({
            "c4.c~" + THREAT_GOOD: "Words change no payoff at BeanCo's node.",
            "c4.c~" + THREAT_ROOT: "Given Match, waiting is CityBrew's best response.",
            "c4.c~" + THREAT_NONE: "Exhibit (Wait and Hold; Match) and check both deviations.",
        }),
        explain="Three sentences on the exam."),
]

city = GuidedProblem(
    "Part 7 &middot; CityBrew and BeanCo",
    "Review questions 2 and 3: a three-stage tree, solved from the bottom.",
    CITY_QUESTIONS, draw_city, figsize=(6.4, 4.2),
    outro="Draw and label the tree yourself.",
    sources=[NOTES("p. 18, review questions 2&ndash;3")],
)


# ======================================================================
# Part 8: the one-stage deviation principle and the centipede
# ======================================================================

def draw_deviation(fig, stage):
    lines, cent = fig.subplots(1, 2)
    for side in ("top", "right"):
        lines.spines[side].set_visible(False)
    lines.set_title("Hold against undercut", loc="left", color=INK, fontsize=9.5)
    lines.set_xlabel(r"discount factor $\delta$", color=INK, fontsize=9, loc="right")
    lines.set_xlim(0, 1)
    lines.set_ylim(2.5, 10.5)
    lines.tick_params(colors=MUTE, labelsize=8.5)
    lines.plot([0, 1], [3, 9], color=LINE, lw=2, label="hold: 3 + 6δ")
    lines.plot([0, 1], [5, 8], color=NEW, lw=2, label="undercut: 5 + 3δ")
    if stage >= 1:
        gp.dot(lines, 2 / 3, 7, "δ* = 2/3", -8, 8, colour=GREEN, ha="right")
    if stage >= 3:
        lines.plot([0, 1], [7, 10], color=NEW, lw=1.4, ls="--", label="grab 7: 7 + 3δ")
    lines.legend(loc="upper left", fontsize=8.5, frameon=False)

    plan = {}
    if stage >= 5:
        plan = {"2b": "n", "1b": "N", "2a": "n", "1a": "N"}
    gm.tree(cent, CENTIPEDE, names=("1", "2"), plan=plan, labels=False, fontsize=9,
            title="The centipede")
    fig.subplots_adjust(wspace=0.15)


SCOPE = "Zermelo guarantees a backward-induction solution in any finite game of perfect information, unique if no player ties. Chess has one that nobody can compute, and grandmasters stop the centipede at once while most people continue: backward induction is scoped by common knowledge of rationality"
SCOPE_FALSE = "The centipede experiments falsify backward induction"
SCOPE_CHESS = "Chess has no solution, since it is too long"
SCOPE_INF = "Zermelo needs infinite games"

DEVIATION_QUESTIONS = [
    Question(
        "v1",
        "Try it: two labs play a two-stage pricing game, payoffs in billions. Holding the posted "
        "price pays 3 + 6%s; undercutting grabs 5 now but triggers a price war worth 3%s. (a) "
        "For which %s does holding survive the one-stage deviation check? The threshold %s*?"
        % (DEL, DEL, DEL, DEL),
        form=["%s* =" % DEL, BOX],
        answers=[H("v1.0")],
        mistakes=M({"v1.0~3/2": "Upside down: 3&delta; &ge; 2."}),
        explain="The deviation gains 2 today and costs 3 tomorrow."),
    Question(
        "v2",
        "(b) The labs are just barely willing to hold at %s = 1/2. Which price-war continuation "
        "value z replaces the 3?" % DEL,
        form=["z =", BOX],
        answers=[H("v2.0")],
        mistakes=M({"v2.0~3": "Solve 3 + 6(1/2) = 5 + z/2."}),
        explain="A harsher punishment: less patience suffices."),
    Question(
        "v3",
        "(c) A viral product raises the grab from 5 to 7. The threshold now?",
        form=["%s* =" % DEL, BOX],
        answers=[H("v3.0")],
        mistakes=M({"v3.0~2/3": "Redo it: 3 + 6&delta; &ge; 7 + 3&delta;."}),
        explain="Above one: no discount factor sustains peace against that temptation."),
    Question(
        "v4",
        "Review question 5: a candidate profile gives player 2 &minus;1 now and 0 next stage; "
        "deviating pays 2 now and &minus;4 next stage. The candidate survives for %s at least?"
        % DEL,
        form=["%s &ge;" % DEL, BOX],
        answers=[H("v4.0")],
        mistakes=M({"v4.0~4/3": "Upside down: &minus;1 &ge; 2 &minus; 4&delta;."}),
        explain="One change at one information set: if none helps, no combination does."),
    Question(
        "v5",
        "The centipede: continuing grows the pot, and following the spine to the end pays "
        "(3, 3). Backward induction: where does play end, and with which payoffs?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("v5.0"), H("v5.1")],
        mistakes=M({"v5.0~3": "At the last node player 2 takes 4 rather than 3. Work back."}),
        explain="Player 1 stops at once. Rosenthal invented the game for exactly this."),
    Question(
        "v6",
        "Review question 6: what does Zermelo guarantee, and what do chess and the centipede "
        "experiments say about the scope of backward induction?",
        choices=[SCOPE, SCOPE_FALSE, SCOPE_CHESS, SCOPE_INF],
        answers=[H("v6.c")],
        mistakes=M({
            "v6.c~" + SCOPE_FALSE: "Scoped, not falsified: where common knowledge holds, people "
                                   "do play it.",
            "v6.c~" + SCOPE_CHESS: "Chess is finite with perfect information.",
            "v6.c~" + SCOPE_INF: "Finite, so the induction has somewhere to start.",
        }),
        explain="Existence is not computability."),
]

deviation = GuidedProblem(
    "Part 8 &middot; One-stage deviations and the centipede",
    "To check subgame perfection, change one action at one information set and see whether the "
    "payoff rises. Then a game built to make backward induction sweat.",
    DEVIATION_QUESTIONS, draw_deviation, figsize=(8.4, 3.8), whole_figure=True,
    outro="Session 15 puts the one-stage deviation principle to work on repeated games.",
    sources=[NOTES("p. 13&ndash;16"), NOTES("p. 18, review questions 5&ndash;6")],
)


# ======================================================================
# Part 9: problems A13.1 and A13.2
# ======================================================================

def draw_problems(fig, stage):
    br, tree = fig.subplots(1, 2)
    _panel(br, 25, 25, "q$_1$", "q$_2$", "A13.1: P = 24 − Q",
           xticks=([12] if stage >= 2 else []) + ([8] if stage >= 4 else []),
           yticks=([12] if stage >= 1 else []) + ([6] if stage >= 2 else [])
           + ([8] if stage >= 4 else []))
    _leader(br, 24, 0, 25, cournot=stage >= 4, leader=stage >= 2, follower=stage >= 1)
    gp.legend(br, loc="upper right")
    plan = {"x1": "Accommodate", "x0": "Enter"} if stage >= 8 else {}
    gm.tree(tree, A13, names=("E", "I"), plan=plan, struck=[("x1", "Fight")] if stage >= 8 else (),
            title="A13.2: payoffs (E, I)")
    fig.subplots_adjust(wspace=0.15)


FIRST_MOVE = "The leader gains (72 against 64) and the follower loses more (36 against 64): industry profit falls from 128 to 108, while output rises from 16 to 18 and the price falls, so consumers gain"
FM_ALL = "Both firms gain from the leader moving first"
FM_CONS = "Consumers lose, since the leader has market power"
FM_SAME = "Nothing changes except who moves first"

REVISE = "Moving first is worth something only because q1 is fixed: firm 2 best-responds to it. If firm 1 could quietly revise q1 after seeing q2, it would move to its own best response, firm 2 would anticipate that, and the game would collapse back to Cournot"
REV_BETTER = "Firm 1 would do even better with the option to revise"
REV_SAME = "Nothing would be lost: the leader can always re-optimize"
REV_FOLLOW = "Firm 2 would become the leader"

A13_NE = "(Enter, Accommodate) and (Stay Out, Fight)"
A13_ONE = "Only (Enter, Accommodate)"
A13_OUT = "Only (Stay Out, Fight)"
A13_NONE = "No pure Nash equilibrium"

A13_THREAT = "At its own node the incumbent gets 1 from fighting and 4 from accommodating, so Fight is not a best response there. To make it credible it must change its payoffs before the game, by a commitment like the Stackelberg leader's capacity"
A13_WORDS = "Fight is credible because the incumbent announced it"
A13_OUTW = "The entrant's payoff from staying out makes Fight credible"
A13_NOTH = "Nothing can make the threat credible"

PROBLEM_QUESTIONS = [
    Question(
        "p1",
        "A13.1 (a): P = 24 &minus; Q, zero marginal cost, firm 1 first. Firm 2's best response "
        "is q<sub>2</sub> = (24 &minus; q<sub>1</sub>)/2. Its reply to q<sub>1</sub> = 0?",
        form=["", BOX],
        answers=[H("p1.0")],
        explain="Show the first-order condition on the exam."),
    Question(
        "p2",
        "(b)&ndash;(c) Firm 1's quantity, firm 2's, total output and the price?",
        form=["q<sub>1</sub>", BOX, "&nbsp; q<sub>2</sub>", BOX, "&nbsp; Q", BOX, "&nbsp; P", BOX],
        answers=[H("p2.0"), H("p2.1"), H("p2.2"), H("p2.3")],
        mistakes=M({"p2.0~8": "That is Cournot. Maximize (24 &minus; q<sub>1</sub>)"
                              "q<sub>1</sub>/2."}),
        explain="Firm 1's profit along firm 2's line is (24 &minus; q<sub>1</sub>)q<sub>1</sub>/2."),
    Question(
        "p3",
        "(d) Each firm's profit?",
        form=["firm 1", BOX, "&nbsp; firm 2", BOX],
        answers=[H("p3.0"), H("p3.1")],
        explain="P times quantity, with zero cost."),
    Question(
        "p4",
        "(e) The Cournot benchmark for this demand: each quantity, the price, each profit?",
        form=["q", BOX, "&nbsp; P", BOX, "&nbsp; &pi;", BOX],
        answers=[H("p4.0"), H("p4.1"), H("p4.2")],
        explain="24/3 each."),
    Question(
        "p5",
        "(f) Compare the two outcomes.",
        choices=[FIRST_MOVE, FM_ALL, FM_CONS, FM_SAME],
        answers=[H("p5.c")],
        mistakes=M({
            "p5.c~" + FM_ALL: "Firm 2 earns 36 against 64.",
            "p5.c~" + FM_CONS: "The price falls from 8 to 6.",
            "p5.c~" + FM_SAME: "Quantities, price and profits all change.",
        }),
        explain="Who gains, who loses, industry profit, output, consumers: all five."),
    Question(
        "p6",
        "(g) Why is moving first worth anything, and what would be lost if firm 1 could quietly "
        "revise q<sub>1</sub>?",
        choices=[REVISE, REV_BETTER, REV_SAME, REV_FOLLOW],
        answers=[H("p6.c")],
        mistakes=M({
            "p6.c~" + REV_BETTER: "In a game, more options can lower your payoff.",
            "p6.c~" + REV_SAME: "Firm 2 would not believe q<sub>1</sub> = 12 any more.",
            "p6.c~" + REV_FOLLOW: "Neither would be committed: simultaneous play.",
        }),
        explain="Five sentences and a drawing, if it helps."),
    Question(
        "p7",
        "A13.2: an entrant chooses Enter or Stay Out, (0, 10); after Enter the incumbent fights, "
        "(&minus;2, 1), or accommodates, (3, 4). (b) The pure Nash equilibria?",
        choices=[A13_NE, A13_ONE, A13_OUT, A13_NONE],
        answers=[H("p7.c")],
        mistakes=M({
            "p7.c~" + A13_ONE: "Check (Stay Out, Fight): given Fight, staying out pays 0 "
                               "against &minus;2.",
            "p7.c~" + A13_OUT: "Check (Enter, Accommodate) too.",
            "p7.c~" + A13_NONE: "Write the normal form and check each cell.",
        }),
        explain="The lecture's entry game with new numbers."),
    Question(
        "p8",
        "(c) The subgame-perfect equilibrium's payoffs?",
        form=["(", BOX, ",", BOX, ")"],
        answers=[H("p8.0"), H("p8.1")],
        mistakes=M({"p8.0~0": "The incumbent would accommodate: 4 &gt; 1."}),
        explain="(Enter, Accommodate)."),
    Question(
        "p9",
        "(d)&ndash;(e) Why is the other equilibrium not subgame perfect, and how could the "
        "incumbent make its threat credible?",
        choices=[A13_THREAT, A13_WORDS, A13_OUTW, A13_NOTH],
        answers=[H("p9.c")],
        mistakes=M({
            "p9.c~" + A13_WORDS: "Words change no payoff at the incumbent's node.",
            "p9.c~" + A13_OUTW: "Credibility is about the incumbent's own payoffs.",
            "p9.c~" + A13_NOTH: "A commitment that makes fighting pay more than 4 would do it.",
        }),
        explain="Relate it to Problem 1: commitment turns a plan into a fact."),
]

problems = GuidedProblem(
    "Part 9 &middot; Stackelberg and an empty threat: A13.1&ndash;A13.2",
    "Exam preparation: attempt these after the in-person session.",
    PROBLEM_QUESTIONS, draw_problems, figsize=(8.0, 3.8), whole_figure=True,
    outro="About 20% and 10% of an exam paper.",
    sources=[PS("A13.1"), PS("A13.2")],
)


# ======================================================================
# Where every step comes from (printed pages of s13_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "s1": NOTES("p. 1&ndash;2 &middot; the standards game"), "s2": NOTES("p. 5 &middot; strategies"),
    "s3": NOTES("p. 5 &middot; the induced matrix"), "s4": NOTES("p. 6&ndash;7 &middot; backward induction"),
    "s5": NOTES("p. 9 &middot; the audit"), "s6": NOTES("p. 4 &middot; information sets"),
    "n1": NOTES("p. 3 &middot; two equilibria"), "n2": NOTES("p. 3 &middot; one silly"),
    "n3": NOTES("p. 9 &middot; the entry game solved"), "n4": NOTES("p. 9 &middot; credibility"),
    "n5": NOTES("p. 9 &middot; credibility"),
    "g1": NOTES("p. 17 &middot; review question 1(a)"), "g2": NOTES("p. 17 &middot; review question 1(b)&ndash;(c)"),
    "g3": NOTES("p. 5 &middot; complete plans"), "g4": NOTES("p. 8 &middot; subgames"),
    "l1": NOTES("p. 9&ndash;10 &middot; Stackelberg"), "l2": NOTES("p. 10 &middot; Stackelberg"),
    "l3": NOTES("p. 11 &middot; the table"), "l4": NOTES("p. 11 &middot; the table"),
    "l5": NOTES("p. 12 &middot; the announcement"), "l6": NOTES("p. 12 &middot; commitment"),
    "m1": NOTES("p. 11 &middot; Try it (a)"), "m2": NOTES("p. 12 &middot; Try it (a)"),
    "m3": NOTES("p. 12 &middot; Try it (b)"), "m4": NOTES("p. 12 &middot; Try it (c)"),
    "m5": NOTES("p. 12 &middot; Try it (c)"),
    "w1": NOTES("p. 17 &middot; worksheet"), "w2": NOTES("p. 17 &middot; worksheet"),
    "w3": NOTES("p. 17 &middot; worksheet"), "w4": NOTES("p. 17 &middot; task 2"),
    "w5": NOTES("p. 17 &middot; worksheet"), "w6": NOTES("p. 17 &middot; worksheet"),
    "c1": NOTES("p. 18 &middot; review question 2"), "c2": NOTES("p. 18 &middot; review question 2"),
    "c3": NOTES("p. 18 &middot; review question 2"), "c4": NOTES("p. 18 &middot; review question 3"),
    "v1": NOTES("p. 14 &middot; Try it (a)"), "v2": NOTES("p. 14 &middot; Try it (b)"),
    "v3": NOTES("p. 14 &middot; Try it (c)"), "v4": NOTES("p. 18 &middot; review question 5"),
    "v5": NOTES("p. 15 &middot; the centipede"), "v6": NOTES("p. 18 &middot; review question 6"),
    "p1": PS("A13.1 (a)"), "p2": PS("A13.1 (b)&ndash;(c)"), "p3": PS("A13.1 (d)"),
    "p4": PS("A13.1 (e)"), "p5": PS("A13.1 (f)"), "p6": PS("A13.1 (g)"),
    "p7": PS("A13.2 (b)"), "p8": PS("A13.2 (c)"), "p9": PS("A13.2 (d)&ndash;(e)"),
}

for _q in (STANDARD_QUESTIONS + ENTRY_QUESTIONS + SUBGAME_QUESTIONS + LEADER_QUESTIONS
           + TSMC_QUESTIONS + SHEET_QUESTIONS + CITY_QUESTIONS + DEVIATION_QUESTIONS
           + PROBLEM_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
