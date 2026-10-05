"""
guided_s08.py - session 8 guided page: firms, tasks and technology (AI).

    Part 1  producer   hiring, markup and cost minimization (context: bachelor
                       prerequisites, not examined)
    Part 2  sigma      the elasticity of substitution and labor's share
    Part 3  cutoff     which tasks AI takes (Try it, review question 2)
    Part 4  nordvik    the saving index and the scale check (Try it)
    Part 5  kyst       kinks, not jumps (review question 4)
    Part 6  frontier   the tilted frontier, and who gains (review questions 5-6)
    Part 7  marine     problem A8.1: substitutes and complements
    Part 8  fjordline  problem A8.2: task choice and savings
    Part 9  harbor     problem A8.3: AI that needs review

Answers are hashes in answers_s08.py, generated from
answer_keys/s08_keys.py in the private repo. The maths is firms.py.
"""

import numpy as np

import firms as fm
import guided_plots as gp
from guided import BOX, NOTES, PS, GuidedProblem, Question, answers
from style import CURVE, GREEN, GREY, HALF, INK, LINE, NEW

H, M = answers("s08")

CTX = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
       "context: bachelor prerequisite, not examined</span> ")
ABAR = "A&#772;"


def _G_curve(ax, As, shares, w, rmax, **kw):
    rs = np.linspace(rmax * 0.002, rmax, 600)
    ax.plot(rs, [fm.index(As, shares, w, r) for r in rs], **kw)


def _task_bars(ax, names, values, cut, colours):
    xs = np.arange(len(values))
    ax.bar(xs, values, color=colours, width=0.6)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=9, color=INK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_yticks([])
    if cut is not None:
        ax.axhline(cut, color=INK, lw=1.6, ls="--")


# ======================================================================
# Part 1: the producer, briefly (context)
# ======================================================================

def draw_producer(fig, stage):
    bk, mo, iso = fig.subplots(1, 3)
    gp.frame(bk, 10.5, 1300, "bakers E", "kr per hour")
    bk.set_title("Hiring: VMP = w", loc="left", color=INK, fontsize=9.5)
    E = np.linspace(0, 10, 50)
    bk.plot(E, 60 * (20 - 2 * E), color=LINE, lw=2, label="VMP")
    if stage >= 1:
        bk.axhline(600, color=GREY, lw=1, ls="--")
        gp.dot(bk, 5, 600, "", colour=NEW)
    if stage >= 2:
        bk.axhline(480, color=GREY, lw=1, ls=":")
        gp.dot(bk, 6, 480, "", colour=NEW)

    gp.frame(mo, 12.5, 12.5, "q", "p")
    mo.set_title("Markup over MC", loc="left", color=INK, fontsize=9.5)
    q = np.linspace(0, 12, 50)
    mo.plot(q, 12 - q, color=INK, lw=1.8)
    mo.axhline(4, color=GREEN, lw=1.6)
    if stage >= 3:
        mo.plot(q[q <= 6], 12 - 2 * q[q <= 6], color=LINE, lw=1.6, ls="--")
        gp.dot(mo, 4, 8, "", colour=NEW)
        mo.plot([4, 4], [4, 8], color=NEW, lw=1, ls=":")
    if stage >= 4:
        mo.annotate("", xy=(5, 8), xytext=(5, 4),
                    arrowprops=dict(arrowstyle="<->", color=NEW, lw=1.2))
        mo.text(5.3, 5.7, "markup", color=NEW, fontsize=8.5)

    gp.frame(iso, 10.5, 10.5, "E", "K")
    iso.set_title("Cheapest mix", loc="left", color=INK, fontsize=9.5)
    Es = np.linspace(1.5, 10.5, 200)
    iso.plot(Es, 16 / Es, color=CURVE, lw=2)
    if stage >= 5:
        iso.plot([0, 10], [10, 0], color=GREY, lw=1.2)
        iso.plot([0, 8], [8, 0], color=LINE, lw=1.6)
        gp.dot(iso, 4, 4, "P", 6, 4, colour=LINE)
        gp.dot(iso, 2, 8, "A", 6, 2, colour=GREY)
        gp.dot(iso, 8, 2, "B", 6, 2, colour=GREY)
    fig.subplots_adjust(wspace=0.35)


PRODUCER_QUESTIONS = [
    Question(
        "k1",
        "A bakery sells loaves at 60 kroner, and the E-th baker adds 20 &minus; 2E loaves an "
        "hour. At a wage of 600 kroner an hour, how many bakers does it hire?",
        form=["E =", BOX],
        answers=[H("k1.0")],
        mistakes=M({"k1.0~10": "Hire until VMP = 60(20 &minus; 2E) equals the wage, not until "
                               "the last baker adds nothing."}),
        explain="1200 &minus; 120E = 600. The VMP line is the short-run labor demand curve."),
    Question(
        "k2",
        "The wage falls to 480. Now?",
        form=["E =", BOX],
        answers=[H("k2.0")],
        explain="Lower wage, more bakers: labor demand slopes down."),
    Question(
        "k3",
        "A firm with demand p = 12 &minus; q and marginal cost 4. Set MR = MC: output and price?",
        form=["q =", BOX, "&nbsp; p =", BOX],
        answers=[H("k3.0"), H("k3.1")],
        mistakes=M({"k3.0~8": "That is where price equals MC. MR = 12 &minus; 2q falls twice "
                              "as fast."}),
        explain="The price sits above marginal cost."),
    Question(
        "k4",
        "The demand elasticity &eta; = |dq/dp|&middot;p/q there?",
        form=["&eta; =", BOX],
        answers=[H("k4.0")],
        mistakes=M({"k4.0~1/2": "Upside down: p/q = 8/4."}),
        explain="p = &eta;/(&eta; &minus; 1)&middot;MC = 2&middot;4 = 8. Higher &eta;, smaller markup."),
    Question(
        "k5",
        "Long run: q = &radic;(EK) = 4 and w = r = 10. The cost of P = (4, 4), and of A = (2, 8)?",
        form=["P:", BOX, "&nbsp; A:", BOX],
        answers=[H("k5.0"), H("k5.1")],
        explain="At the cheapest bundle, MRTS = MP<sub>E</sub>/MP<sub>K</sub> = w/r."),
]

producer = GuidedProblem(
    "Part 1 &middot; The producer, briefly",
    CTX + "Three bachelor-level reminders the notes run through quickly: the hiring rule, "
    "the markup and the cheapest input mix.",
    PRODUCER_QUESTIONS, draw_producer, figsize=(8.4, 3.4), whole_figure=True,
    outro="What matters for AI is how the cheapest mix reacts when prices move.",
    sources=[NOTES("p. 2&ndash;4")],
)


# ======================================================================
# Part 2: the elasticity of substitution
# ======================================================================

def draw_sigma(fig, stage):
    iso, sh = fig.subplots(1, 2)
    gp.frame(iso, 10.5, 10.5, "E", "K")
    iso.set_title("q = 4", loc="left", color=INK, fontsize=9.5)
    Es = np.linspace(1.5, 10.5, 200)
    iso.plot(Es, 16 / Es, color=CURVE, lw=2)
    gp.dot(iso, 4, 4, "P", 6, 4, colour=LINE)
    iso.plot([0, 10], [0, 10], color=LINE, lw=0.8, ls=":")
    if stage >= 1:
        iso.plot([0, 10.5], [0, 10.5 / 4], color=NEW, lw=0.8, ls=":")
        gp.dot(iso, 8, 2, "B", 6, 4, colour=NEW)
        gp.arrow(iso, (4.3, 3.7), (7.6, 2.2), NEW)

    gp.frame(sh, 1.05, 1, "r/w", "labor's share of costs")
    sh.set_title("Cheaper AI: right to left", loc="left", color=INK, fontsize=9.5)
    rw = np.linspace(0.1, 1, 100)
    if stage >= 3:
        sh.plot(rw, [fm.labor_share(x, 1) for x in rw], color=GREY, lw=1.4, label="σ = 1")
    if stage >= 4:
        sh.plot(rw, [fm.labor_share(x, 2) for x in rw], color=NEW, lw=2, label="σ = 2")
        sh.plot(rw, [fm.labor_share(x, .5) for x in rw], color=LINE, lw=2, label="σ = 1/2")
        gp.dot(sh, 0.25, 0.2, "", colour=NEW)
        gp.dot(sh, 0.25, 2 / 3, "", colour=LINE)
    gp.legend(sh, loc="lower right")
    fig.subplots_adjust(wspace=0.32)


EXTREMES = "Straight isoquants: σ = ∞; L-shaped isoquants: σ = 0"
EXT_REV = "Straight isoquants: σ = 0; L-shaped isoquants: σ = ∞"
EXT_ONE = "Both have σ = 1"
EXT_SLOPE = "σ is the slope of the isoquant: −1 for straight ones"

SHARE_FALLS = "It falls: with σ > 1 relative spending on AI rises"
SHARE_RISES = "It rises"
SHARE_SAME = "It stays the same"
SHARE_DEP = "It cannot be told without the wage"

NO_WAGE = "No: with two inputs and constant returns, more capital never lowers the wage; a wage fall needs AI to take over tasks, and a labor market model"
YES_WAGE = "Yes: labor's share falls, so wages fall"
YES_RISE = "Yes: the firm is more productive, so wages rise"
DEPENDS_SIGMA = "Only if σ is above 2"

SIGMA_QUESTIONS = [
    Question(
        "e1",
        "For q = &radic;(EK) the tangency gives K/E = w/r, so P = (4, 4) at w/r = 1. The wage "
        "falls to a quarter of r. What is the new K/E?",
        form=["K/E =", BOX],
        answers=[H("e1.0")],
        mistakes=M({"e1.0~4": "Workers got cheaper: the firm uses fewer machines per worker."}),
        explain="The cheapest bundle moves along the isoquant to B = (8, 2)."),
    Question(
        "e2",
        "&sigma; = %&Delta;(K/E) / %&Delta;(w/r). Both ratios fell by 75%. &sigma; = ?",
        form=["&sigma; =", BOX],
        answers=[H("e2.0")],
        explain="The Cobb&ndash;Douglas case."),
    Question(
        "e3",
        "Worksheet task 1: &sigma; for straight isoquants, and for L-shaped ones?",
        choices=[EXTREMES, EXT_REV, EXT_ONE, EXT_SLOPE],
        answers=[H("e3.c")],
        mistakes=M({
            "e3.c~" + EXT_REV: "With straight isoquants the firm swaps inputs at the slightest "
                               "price change.",
            "e3.c~" + EXT_ONE: "That is Cobb&ndash;Douglas, the curved case in between.",
            "e3.c~" + EXT_SLOPE: "The slope is the MRTS. &sigma; is the % change in K/E per 1% "
                                 "change in the MRTS.",
        }),
        explain="Perfect substitutes use only the cheaper input; complements keep one per one."),
    Question(
        "e4",
        "Worksheet task 2: with a CES technology and equal weights, labor's share starts at 1/2. AI gets "
        "cheaper: r/w falls from 1 to 1/4. Labor's share with &sigma; = 2, and with &sigma; = 1/2?",
        form=["&sigma; = 2:", BOX, "&nbsp; &sigma; = 1/2:", BOX],
        answers=[H("e4.0"), H("e4.1")],
        mistakes=M({"e4.0~2/3": "Swapped. With &sigma; &gt; 1 the firm swaps toward the "
                                "cheaper input by more than its price fell."}),
        hints=["Labor's share is 1/(1 + (r/w)<sup>1 &minus; &sigma;</sup>)."],
        explain="Gross substitutes: labor's share falls. Gross complements: it rises."),
    Question(
        "e5",
        "Review question 3: at Transnor, w/r rises by 10% and K/E rises by 15%. &sigma; = ?",
        form=["&sigma; =", BOX],
        answers=[H("e5.0")],
        mistakes=M({"e5.0~2/3": "Upside down: the change in K/E goes on top."}),
        explain="Above 1: AI and workers are gross substitutes at Transnor."),
    Question(
        "e6",
        "By about what percentage does rK/(wE) = (K/E)/(w/r) change?",
        form=["change =", BOX, "%"],
        answers=[H("e6.0")],
        mistakes=M({"e6.0~15": "That is K/E alone. Divide by w/r too.",
                    "e6.0~25": "Divide, don't multiply: (K/E)/(w/r)."}),
        hints=["A 1% fall in r/w changes relative spending by (&sigma; &minus; 1)%."],
        explain="About (&sigma; &minus; 1)&middot;10 = 5%; exactly 1.15/1.10 &minus; 1 &asymp; 4.5%."),
    Question(
        "e7",
        "Does labor's share of Transnor's costs rise or fall?",
        choices=[SHARE_FALLS, SHARE_RISES, SHARE_SAME, SHARE_DEP],
        answers=[H("e7.c")],
        mistakes=M({
            "e7.c~" + SHARE_RISES: "Relative spending on AI went up.",
            "e7.c~" + SHARE_SAME: "Only with &sigma; = 1.",
            "e7.c~" + SHARE_DEP: "The ratio rK/(wE) already tells you.",
        }),
        explain="AI's share of spending rises, so labor's falls."),
    Question(
        "e8",
        "(d) Does that tell you whether Transnor's wages will fall?",
        choices=[NO_WAGE, YES_WAGE, YES_RISE, DEPENDS_SIGMA],
        answers=[H("e8.c")],
        mistakes=M({
            "e8.c~" + YES_WAGE: "A share is not a wage. More capital raises each worker's "
                                "marginal product.",
            "e8.c~" + YES_RISE: "The firm takes the wage as given here.",
            "e8.c~" + DEPENDS_SIGMA: "Whatever &sigma; is, more capital never lowers the wage in "
                                     "the two-input model.",
        }),
        explain="A falling wage needs AI to take over tasks: the task model."),
]

sigma = GuidedProblem(
    "Part 2 &middot; The elasticity of substitution",
    "How strongly the cheapest mix of workers and machines reacts when relative prices move. "
    "This is where the examinable part begins.",
    SIGMA_QUESTIONS, draw_sigma, figsize=(8.0, 3.9), whole_figure=True,
    outro="Whether a degree protects you is a question about tasks.",
    sources=[NOTES("p. 4&ndash;6"), NOTES("p. 16, worksheet"), NOTES("p. 17, review question 3")],
)


# ======================================================================
# Part 3: the automation cutoff (Try it, review question 2)
# ======================================================================

TASKS = ["transcription", "analysis", "negotiation"]


def draw_cutoff(ax, stage):
    A = [4, 2, 1]
    cut = None
    if stage >= 2:
        cut = 2 if stage < 4 else 1.5
    cols = [GREY] * 3
    if stage >= 3:
        cols = [LINE, GREY, GREY]
    if stage >= 5:
        cols = [LINE, LINE, GREY]
    _task_bars(ax, TASKS, A, cut, cols)
    ax.set_ylim(0, 4.6)
    ax.set_ylabel("AI productivity A", color=INK, fontsize=10, loc="top")
    if cut is not None:
        ax.text(2.42, cut + 0.08, "cutoff r/w", color=INK, fontsize=9, ha="right")
    if stage >= 4:
        ax.axhline(2, color=GREY, lw=1, ls=":")
    if stage >= 3:
        ax.text(0.02, 0.95, "blue: AI is strictly cheaper", transform=ax.transAxes,
                color=LINE, fontsize=9)


ONLY_T = "Transcription only: analysis is a tie and is assigned to labor"
T_AND_A = "Transcription and analysis"
ALL_AI = "All three"
NONE_AI = "None: AI rents for twice the wage"

ANALYSIS = "Analysis switches to AI; negotiation stays with labor"
ALL_SWITCH = "All three tasks use AI"
NOTHING_CH = "Nothing changes"
NEG_SW = "Negotiation switches to AI"

WAGE_UP = "The cutoff falls: automation becomes more attractive relative to labor, but no task gets cheaper in kroner"
WAGE_CHEAP = "Every task gets cheaper"
WAGE_CUT_UP = "The cutoff rises"
WAGE_NONE = "Nothing: the wage does not enter the cutoff"

B_RISE = "AI is cheaper when A/B > r/w, so a higher B moves the task toward labor"
B_NONE = "Nothing: the cutoff only uses A"
B_AI = "It moves the task toward AI"
B_ALL = "It protects every task in the job"

CUTOFF_QUESTIONS = [
    Question(
        "c1",
        "Try it: a worker-hour costs 300 kroner and an AI-service unit 600. AI produces 4 "
        "transcription units, 2 analysis units or 1 negotiation unit per service unit. The AI "
        "cost per completed task-unit, r/A, for each?",
        form=["transcription", BOX, "&nbsp; analysis", BOX, "&nbsp; negotiation", BOX],
        answers=[H("c1.0"), H("c1.1"), H("c1.2")],
        mistakes=M({"c1.0~2400": "Divide by A: one service unit makes 4 task-units."}),
        explain="The human cost is 300 for every task: compare like with like."),
    Question(
        "c2",
        "AI is strictly cheaper when r/A < w, that is A &gt; r/w &equiv; %s. The cutoff?" % ABAR,
        form=["%s =" % ABAR, BOX],
        answers=[H("c2.0")],
        mistakes=M({"c2.0~1/2": "Upside down: r/w."}),
        explain="One number splits all tasks."),
    Question(
        "c3",
        "Which tasks are automated? (Ties go to labor.)",
        choices=[ONLY_T, T_AND_A, ALL_AI, NONE_AI],
        answers=[H("c3.c")],
        mistakes=M({
            "c3.c~" + T_AND_A: "Analysis costs 300 either way. The convention for ties?",
            "c3.c~" + ALL_AI: "Negotiation costs 600 with AI against 300 by hand.",
            "c3.c~" + NONE_AI: "Productivity matters too: compare r/A with w.",
        }),
        explain="At a tie every mixture has the same cost; the label goes to labor."),
    Question(
        "c4",
        "Review question 2: the AI price falls to 450. The new AI cost for analysis, and the new cutoff?",
        form=["analysis", BOX, "&nbsp; %s =" % ABAR, BOX],
        answers=[H("c4.0"), H("c4.1")],
        explain="The cutoff falls from 2 to 3/2."),
    Question(
        "c5",
        "Which decisions change?",
        choices=[ANALYSIS, ALL_SWITCH, NOTHING_CH, NEG_SW],
        answers=[H("c5.c")],
        mistakes=M({
            "c5.c~" + ALL_SWITCH: "Negotiation: 450 against 300.",
            "c5.c~" + NOTHING_CH: "Analysis: 225 against 300.",
            "c5.c~" + NEG_SW: "450 &gt; 300.",
        }),
        explain="A task switches only when its threshold is crossed."),
    Question(
        "c6",
        "Instead the wage rises, with AI prices and productivities fixed. What happens?",
        choices=[WAGE_UP, WAGE_CHEAP, WAGE_CUT_UP, WAGE_NONE],
        answers=[H("c6.c")],
        mistakes=M({
            "c6.c~" + WAGE_CHEAP: "The human-only method got dearer; nothing got cheaper.",
            "c6.c~" + WAGE_CUT_UP: "%s = r/w: w is underneath." % ABAR,
            "c6.c~" + WAGE_NONE: "%s = r/w." % ABAR,
        }),
        explain="Better AI at one task is a third experiment: that task's A rises, the cutoff "
                "stays put."),
    Question(
        "c7",
        "A worker produces B units of a task per hour. What does education that raises B do?",
        choices=[B_RISE, B_NONE, B_AI, B_ALL],
        answers=[H("c7.c")],
        mistakes=M({
            "c7.c~" + B_NONE: "The human cost per task-unit is w/B.",
            "c7.c~" + B_AI: "A higher B makes the human cheaper per task-unit.",
            "c7.c~" + B_ALL: "Only tasks where B rises, and the model promises no rise.",
        }),
        explain="Relative productivity matters, not the degree title."),
]

cutoff = GuidedProblem(
    "Part 3 &middot; Which tasks does AI take?",
    "Inside one task, a worker-hour and A units of AI output are perfect substitutes: "
    "y = E + A&middot;M. Compare costs per completed task-unit.",
    CUTOFF_QUESTIONS, draw_cutoff, figsize=(6.0, 4.4),
    outro="Order tasks by A and the cutoff splits them.",
    sources=[NOTES("p. 7&ndash;9"), NOTES("p. 17, review question 2")],
)


# ======================================================================
# Part 4: Nordvik's saving index (Try it)
# ======================================================================

NORD_A, NORD_X = (10, 5, 1), (0.2, 0.4, 0.4)


def draw_nordvik(ax, stage):
    gp.frame(ax, 6000, 1.05, "AI rental rate r, kroner", "saving index G")
    if stage >= 1:
        gp.dot(ax, 1000, 0.4, "(a)", 6, 4, colour=NEW)
    if stage >= 3:
        ax.axvline(500, color=GREY, lw=1, ls=":")
        ax.text(520, 0.97, "negotiation\nenters", color=GREY, fontsize=8.5, va="top")
    if stage >= 4:
        _G_curve(ax, NORD_A, NORD_X, 500, 6000, color=LINE, lw=2)
        gp.dot(ax, 100, 0.9, "(c)", 6, 4, colour=NEW)
        for r, name in ((2500, "drafting"), (5000, "transcription")):
            ax.axvline(r, color=GREY, lw=1, ls=":")
            ax.text(r + 40, 0.97, name + "\nenters", color=GREY, fontsize=8.5, va="top")


NOT_ECON = "No: the economy's tasks, cost shares and adoption need not resemble Nordvik's"
YES_ECON = "Yes: 40% is the economy's productivity gain"
YES_FIRM = "Yes, if Nordvik is a typical firm"
JOBS = "It measures the share of jobs lost"

TEN_YEAR = "Neither: a cumulative ten-year TFP estimate relative to a baseline without these advances"
ANNUAL = "An annual growth rate"
JOB_LOSS = "A forecast of jobs lost"
BOTH_TWO = "Both"

NORDVIK_QUESTIONS = [
    Question(
        "n1",
        "Nordvik: w = 500, r = 1000, A = (10, 5, 1) for transcription, drafting and "
        "negotiation. The cutoff, and the saving &pi; = max{0, 1 &minus; r/(wA)} on each task?",
        form=["%s =" % ABAR, BOX, "&nbsp; &pi; = (", BOX, ",", BOX, ",", BOX, ")"],
        answers=[H("n1.0"), H("n1.1"), H("n1.2"), H("n1.3")],
        mistakes=M({"n1.3~-1": "No task saves a negative amount: the firm can keep labor."}),
        explain="Transcription and drafting go to AI; negotiation stays with labor."),
    Question(
        "n2",
        "Baseline cost shares &chi; = (1/5, 2/5, 2/5). The fixed-weight saving index G = "
        "&Sigma; &chi;<sub>i</sub>&pi;<sub>i</sub>?",
        form=["G =", BOX],
        answers=[H("n2.0")],
        explain="For a fixed recipe: a 40% cut in unit cost, not 40% more output per worker."),
    Question(
        "n3",
        "(b) Below what AI rental rate is negotiation strictly cheaper with AI?",
        form=["r &lt;", BOX],
        answers=[H("n3.0")],
        mistakes=M({"n3.0~1000": "That is today's price. Solve r/1 &lt; 500."}),
        explain="Task i crosses at r<sub>i</sub> = wA<sub>i</sub>."),
    Question(
        "n4",
        "(c) The rental rate falls to 100. G = ?",
        form=["G =", BOX],
        answers=[H("n4.0")],
        mistakes=M({"n4.0~2/5": "Recompute every saving: all three tasks now use AI."}),
        explain="Kinks at 5000, 2500 and 500: the index is continuous and only gets steeper."),
    Question(
        "n5",
        "(d) Does Nordvik's index establish the economy's productivity gain?",
        choices=[NOT_ECON, YES_ECON, YES_FIRM, JOBS],
        answers=[H("n5.c")],
        mistakes=M({
            "n5.c~" + YES_ECON: "Exposure, adoption and realized savings are separate objects.",
            "n5.c~" + YES_FIRM: "Low-cost tasks may carry little weight in the economy's costs.",
            "n5.c~" + JOBS: "G is a cost saving, not a job count.",
        }),
        explain="Counting exposed job titles does not supply the weights either."),
    Question(
        "n6",
        "Scale check (Acemoglu 2024): affected tasks are 4.6% of GDP, and cost savings on them "
        "0.27 &times; 0.535 &asymp; 0.144. The first-pass aggregate gain, in percent?",
        form=["gain &asymp;", BOX, "%"],
        answers=[H("n6.0")],
        mistakes=M({"n6.0~4.6": "Multiply the share by the saving.",
                    "n6.0~14.4": "That is the saving on affected tasks. Weight it by their 4.6%."}),
        explain="0.046 &times; 0.144 &asymp; 0.66%: share times saving."),
    Question(
        "n7",
        "What is that 0.66%?",
        choices=[TEN_YEAR, ANNUAL, JOB_LOSS, BOTH_TWO],
        answers=[H("n7.c")],
        mistakes=M({
            "n7.c~" + ANNUAL: "It is cumulative over the paper's ten-year horizon.",
            "n7.c~" + JOB_LOSS: "It is a productivity number.",
            "n7.c~" + BOTH_TWO: "It is neither.",
        }),
        explain="Much smaller than Nordvik: both the share and the saving matter."),
]

nordvik = GuidedProblem(
    "Part 4 &middot; How large is the gain? Nordvik",
    "From task savings to one number for the firm: G = &Sigma; &chi;<sub>i</sub>&pi;<sub>i</sub>, "
    "the cost-share-weighted average saving.",
    NORDVIK_QUESTIONS, draw_nordvik, figsize=(6.4, 4.4),
    outro="The automated set jumps. The index does not.",
    sources=[NOTES("p. 10&ndash;14")],
)


# ======================================================================
# Part 5: Kyst Consulting, kinks not jumps (review question 4)
# ======================================================================

KYST_A, KYST_X = (2, 1, 0.5), (0.25, 0.5, 0.25)


def draw_kyst(ax, stage):
    gp.frame(ax, 7, 1.05, "AI rental rate r", "saving index G")
    if stage >= 4:
        gp.dot(ax, 2, 1 / 3, "r = 2", 6, 4, colour=NEW)
    if stage >= 5:
        gp.dot(ax, 1, 5 / 8, "r = 1", 6, 4, colour=NEW)
    if stage >= 6:
        _G_curve(ax, KYST_A, KYST_X, 3, 7, color=LINE, lw=2)
        for r in (6, 3, 1.5):
            ax.axvline(r, color=GREY, lw=1, ls=":")


TAN = "Transcription and data analysis"
T_ONLY = "Transcription only"
ALL3 = "All three"
NEG_ONLY = "Negotiation only"

KINKS = "Each task enters at its threshold with zero saving, so G bends there but never jumps; and G is not an exact finite change in log TFP"
JUMPS = "G jumps when a task is automated"
SMOOTH = "G is a straight line in r"
EXACT = "G is continuous, and it equals the exact change in log TFP"

KYST_QUESTIONS = [
    Question(
        "q1",
        "Review question 4: Kyst pays w = 3, AI rents at r = 2, with A = (2, 1, 1/2) for transcription, "
        "data analysis and negotiation. The cutoff?",
        form=["%s =" % ABAR, BOX],
        answers=[H("q1.0")],
        mistakes=M({"q1.0~3/2": "Upside down: r/w."}),
        explain="Compare each A with 2/3."),
    Question(
        "q2",
        "The automated set (ties to labor)?",
        choices=[TAN, T_ONLY, ALL3, NEG_ONLY],
        answers=[H("q2.c")],
        mistakes=M({
            "q2.c~" + T_ONLY: "Analysis has A = 1 &gt; 2/3.",
            "q2.c~" + ALL3: "Negotiation has A = 1/2 &lt; 2/3.",
            "q2.c~" + NEG_ONLY: "The highest A are automated first.",
        }),
        explain="Two tasks to AI."),
    Question(
        "q3",
        "Each saving &pi;<sub>i</sub> = max{0, 1 &minus; r/(wA<sub>i</sub>)}?",
        form=["&pi; = (", BOX, ",", BOX, ",", BOX, ")"],
        answers=[H("q3.0"), H("q3.1"), H("q3.2")],
        mistakes=M({"q3.2~-1/3": "Negotiation stays with labor: its saving is 0."}),
        explain="The savings use the chosen cost."),
    Question(
        "q4",
        "With &chi; = (1/4, 1/2, 1/4), the index G?",
        form=["G =", BOX],
        answers=[H("q4.0")],
        explain="A third of the all-labor cost, for this fixed recipe."),
    Question(
        "q5",
        "(c) r falls to 1. Recompute G (the automated set changes).",
        form=["G =", BOX],
        answers=[H("q5.0")],
        mistakes=M({"q5.0~13/24": "Negotiation now uses AI too: 1/2 &gt; 1/3."}),
        explain="Savings rose on the old tasks, and negotiation joined."),
    Question(
        "q6",
        "(d) The rental rates at which each task crosses, r<sub>i</sub> = wA<sub>i</sub>?",
        form=["r<sub>1</sub> =", BOX, "&nbsp; r<sub>2</sub> =", BOX, "&nbsp; r<sub>3</sub> =", BOX],
        answers=[H("q6.0"), H("q6.1"), H("q6.2")],
        explain="The figure shows the whole index curve with its kinks."),
    Question(
        "q7",
        "Why is G continuous with kinks, and is it an exact finite change in log TFP?",
        choices=[KINKS, JUMPS, SMOOTH, EXACT],
        answers=[H("q7.c")],
        mistakes=M({
            "q7.c~" + JUMPS: "At its threshold a task saves exactly zero.",
            "q7.c~" + SMOOTH: "Look at the slope: it changes at each threshold.",
            "q7.c~" + EXACT: "G approximates &Delta; ln TFP for small savings only.",
        }),
        explain="Cheaper AI raises savings on tasks already in use, between the kinks too."),
]

kyst = GuidedProblem(
    "Part 5 &middot; Kinks, not jumps: Kyst Consulting",
    "Review question 4: the cutoff, the index, and its shape as AI gets cheaper. Worksheet "
    "task 5 asks for the same picture.",
    KYST_QUESTIONS, draw_kyst, figsize=(6.4, 4.4),
    outro="Read the curve from right to left: each task enters at its own threshold.",
    sources=[NOTES("p. 17, review question 4"), NOTES("p. 13&ndash;14")],
)


# ======================================================================
# Part 6: the tilted frontier, and who gains (review questions 5-6, worksheet task 6)
# ======================================================================

def draw_frontier(ax, stage):
    gp.frame(ax, 28, 33, "X", "Y")
    ax.plot([0, 20], [30, 0], color=LINE, lw=2, label="before")
    if stage >= 1:
        ax.plot([0, 25], [30, 0], color=NEW, lw=2, ls="--", label="X more productive")
    if stage >= 2:
        ax.text(14, 15, "flatter: X costs\nless Y", color=NEW, fontsize=9)
    gp.legend(ax)


PRICE_IF = "Labor moves freely and both goods are produced: then pX/pY = aY/aX"
PRICE_ALWAYS = "Nothing: the tilt always lowers pX/pY"
PRICE_OPEN = "A small open economy"
PRICE_WAGE = "A fixed wage"

COND = "A consumer with unchanged income gains as X gets cheaper; a displaced worker may lose if adjustment is costly and earnings fall enough"
ALL_GAIN = "Everyone gains, because the frontier moved out"
X_LOSE = "Workers in X lose for sure"
NO_ONE = "Nobody loses in this model"

MINISTER = "Displacement can lower labor demand on automated tasks while output expansion raises it; the firm model takes the wage as given, so a labor market is needed"
MIN_RIGHT = "The minister is right: productivity always raises wages"
MIN_WRONG = "The opposite: AI always lowers wages"
MIN_EXPOSURE = "Exposure measures settle it"

FRONTIER_QUESTIONS = [
    Question(
        "x1",
        "Worksheet task 6: ten workers, output per worker 2 in X and 3 in Y. Labor needed per "
        "unit of X falls by one fifth, so a&prime;<sub>X</sub> = a<sub>X</sub>/(1 &minus; &pi;). "
        "The X intercept before and after, and the Y intercept?",
        form=["X before", BOX, "&nbsp; X after", BOX, "&nbsp; Y", BOX],
        answers=[H("x1.0"), H("x1.1"), H("x1.2")],
        mistakes=M({"x1.1~24": "Divide by 1 &minus; &pi;: 2/(4/5) = 5/2 per worker."}),
        explain="The frontier tilts outward toward X."),
    Question(
        "x2",
        "Its absolute slope, the opportunity cost of X in Y, before and after?",
        form=["before", BOX, "&nbsp; after", BOX],
        answers=[H("x2.0"), H("x2.1")],
        mistakes=M({"x2.0~2/3": "Upside down: a<sub>Y</sub>/a<sub>X</sub>."}),
        explain="X now costs less Y."),
    Question(
        "x3",
        "What must you assume to say the relative price of X falls?",
        choices=[PRICE_IF, PRICE_ALWAYS, PRICE_OPEN, PRICE_WAGE],
        answers=[H("x3.c")],
        mistakes=M({
            "x3.c~" + PRICE_ALWAYS: "The frontier alone does not determine demand.",
            "x3.c~" + PRICE_OPEN: "A small open economy faces a fixed world price instead.",
            "x3.c~" + PRICE_WAGE: "Which condition ties prices to opportunity costs?",
        }),
        explain="Prices equal opportunity costs only under those conditions."),
    Question(
        "x4",
        "Review question 6: labor per unit of X falls by &pi; = 1/4. By what factor does output per "
        "worker rise in X?",
        form=["factor", BOX],
        answers=[H("x4.0")],
        mistakes=M({"x4.0~5/4": "1/(1 &minus; &pi;), not 1 + &pi;."}),
        explain="a&prime;<sub>X</sub> = a<sub>X</sub>/(1 &minus; &pi;)."),
    Question(
        "x5",
        "Give a conditional example of one group that gains and one that loses.",
        choices=[COND, ALL_GAIN, X_LOSE, NO_ONE],
        answers=[H("x5.c")],
        mistakes=M({
            "x5.c~" + ALL_GAIN: "Feasibility says nothing about who gets the extra output.",
            "x5.c~" + X_LOSE: "Nothing is for sure without more assumptions.",
            "x5.c~" + NO_ONE: "Losses need frictions, but they are possible.",
        }),
        explain="Neither losses nor their recipients follow from a tilt alone."),
    Question(
        "x6",
        "Review question 5: a minister says \"AI raises productivity, so it must raise wages.\" Why "
        "can't the firm model establish that?",
        choices=[MINISTER, MIN_RIGHT, MIN_WRONG, MIN_EXPOSURE],
        answers=[H("x6.c")],
        mistakes=M({
            "x6.c~" + MIN_RIGHT: "The wage is an input to the firm's calculation.",
            "x6.c~" + MIN_WRONG: "Output expansion can raise demand for remaining tasks.",
            "x6.c~" + MIN_EXPOSURE: "Technical exposure is not realized adoption.",
        }),
        explain="Two forces pull in opposite directions; their strength needs demand and a "
                "labor market."),
]

frontier = GuidedProblem(
    "Part 6 &middot; The tilted frontier, and who gains",
    "A separate two-sector illustration: a fixed labor pool, constant output per worker, "
    "and a labor-saving improvement in X alone.",
    FRONTIER_QUESTIONS, draw_frontier, figsize=(6.0, 4.4),
    outro="The interesting part is the tilt, and what it does not tell you.",
    sources=[NOTES("p. 14&ndash;16"), NOTES("p. 17, review questions 5&ndash;6")],
)


# ======================================================================
# Part 7: problem A8.1, two ways to use a machine
# ======================================================================

def draw_marine(fig, stage):
    a, b = fig.subplots(1, 2)
    for ax, title in ((a, "Arrangement A"), (b, "Arrangement B")):
        gp.frame(ax, 10, 10, "worker hours", "machine hours")
        ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    if stage >= 2:
        for q, ls in ((5, "-"), (8, "--")):
            a.plot([0, q], [q, 0], color=LINE, lw=2, ls=ls)
            b.plot([q, q, 10], [10, q, q], color=CURVE, lw=2, ls=ls)
    if stage >= 3:
        a.plot([0], [5], "o", color=NEW, ms=8, clip_on=False)
        a.text(0.3, 5.4, "machine only", color=NEW, fontsize=9)
    if stage >= 4:
        gp.dot(b, 5, 5, "the kink", 6, 4, colour=NEW)
    fig.subplots_adjust(wspace=0.3)


A_SUB = "A: perfect substitutes; B: perfect complements"
A_COMP = "A: perfect complements; B: perfect substitutes"
BOTH_SUB = "Both are perfect substitutes"
BOTH_CD = "Both are Cobb–Douglas"

B_BOTTLE = "In B, output does not rise: operators are the bottleneck. In A, machines can replace worker hours"
B_RISE_OUT = "Output rises in both"
A_NONE = "In A nothing happens; in B output rises"
NO_DIFF = "Output rises by half the extra machines in both"

MACHINE = "The machine only; at equal unit costs, either method or any mixture"
GRADUAL = "A gradual switch, half and half"
WORKER = "The worker, to avoid job losses"
BOTH_ALWAYS = "Always both"

KEEP_OPS = "No: each inspection still needs an operator; if scanners were scarce, more scanners let idle operators work"
REMOVE = "Yes: cheaper scanners replace the operators"
HALF_OPS = "Half the operators can go"
MORE_PAY = "Yes, and wages rise"

TASKS_JOB = "A job is a bundle of tasks: cost and capability must be checked task by task, e.g. verifying an AI draft complements it"
RIGHT = "The employee is right"
NEVER = "Machines can never do whole jobs"
WAGE_ARG = "It is only about wages"

MARINE_QUESTIONS = [
    Question(
        "m1",
        "A8.1: in arrangement A a worker or a machine can complete the same inspection. In "
        "B each inspection needs one operator and one scanner together. Which is which?",
        choices=[A_SUB, A_COMP, BOTH_SUB, BOTH_CD],
        answers=[H("m1.c")],
        mistakes=M({
            "m1.c~" + A_COMP: "In A either input is enough on its own.",
            "m1.c~" + BOTH_SUB: "In B extra scanners cannot replace the operator.",
            "m1.c~" + BOTH_CD: "Neither allows smooth substitution with diminishing returns.",
        }),
        explain="A: &sigma; = &infin;. B: &sigma; = 0."),
    Question(
        "m2",
        "(a, b) The firm adds machines but no workers. And the isoquant shapes?",
        choices=[B_BOTTLE, B_RISE_OUT, A_NONE, NO_DIFF],
        answers=[H("m2.c")],
        mistakes=M({
            "m2.c~" + B_RISE_OUT: "In B, a scanner without an operator does nothing.",
            "m2.c~" + A_NONE: "The other way round.",
            "m2.c~" + NO_DIFF: "The two arrangements behave very differently.",
        }),
        explain="The figure draws a straight isoquant for A and an L for B."),
    Question(
        "m3",
        "(c) In A the machine becomes cheaper per completed inspection. No switching costs. "
        "Which method does the firm choose, and what if unit costs match?",
        choices=[MACHINE, GRADUAL, WORKER, BOTH_ALWAYS],
        answers=[H("m3.c")],
        mistakes=M({
            "m3.c~" + GRADUAL: "No setup costs or capacity limits: nothing slows the switch.",
            "m3.c~" + WORKER: "The firm minimizes cost.",
            "m3.c~" + BOTH_ALWAYS: "With straight isoquants, only the cheaper input.",
        }),
        explain="A corner, except at the tie."),
    Question(
        "m4",
        "(d) In B scanners become cheaper. Can Nordvik remove the operators?",
        choices=[KEEP_OPS, REMOVE, HALF_OPS, MORE_PAY],
        answers=[H("m4.c")],
        mistakes=M({
            "m4.c~" + REMOVE: "Look at the L: the operator requirement does not move.",
            "m4.c~" + HALF_OPS: "One operator per inspection, whatever scanners cost.",
            "m4.c~" + MORE_PAY: "More useful hours do not establish a wage increase.",
        }),
        explain="Complements: a cheaper scanner can make more operator hours useful."),
    Question(
        "m5",
        "(e) \"If a machine can do one of my tasks, it can do my whole job.\" What is missing?",
        choices=[TASKS_JOB, RIGHT, NEVER, WAGE_ARG],
        answers=[H("m5.c")],
        mistakes=M({
            "m5.c~" + RIGHT: "A job contains several tasks with different costs.",
            "m5.c~" + NEVER: "Too strong: some jobs may be fully automated.",
            "m5.c~" + WAGE_ARG: "It is about tasks and costs.",
        }),
        explain="Review complements the AI draft rather than disappearing with it."),
]

marine = GuidedProblem(
    "Part 7 &middot; Two ways to use a machine: A8.1",
    "Nordvik Marine's inspections, two arrangements with the same quality.",
    MARINE_QUESTIONS, draw_marine, figsize=(7.4, 3.7), whole_figure=True,
    outro="Inside a task, AI and labor are substitutes; across tasks, they can be complements.",
    sources=[PS("A8.1")],
)


# ======================================================================
# Part 8: problem A8.2, Fjordline Furniture
# ======================================================================

FJ_A, FJ_X = (3, 2, 1), (0.5, 0.25, 0.25)
FJ_NAMES = ["cutting", "assembly", "finishing"]


def draw_fjordline(fig, stage):
    bars, g = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1, 1.1]))
    for side in ("top", "right"):
        bars.spines[side].set_visible(False)
    bars.set_title("Machine cost per task-unit", loc="left", color=INK, fontsize=9.5)
    xs = np.arange(3)
    bars.set_xticks(xs)
    bars.set_xticklabels(FJ_NAMES, fontsize=9, color=INK)
    bars.set_yticks([])
    bars.set_ylim(0, 3.4)
    bars.axhline(2, color=INK, lw=1.6, ls="--")
    bars.text(2.45, 2.07, "wage w", color=INK, fontsize=9, ha="right")
    if stage >= 2:
        costs = [3 / a for a in FJ_A]
        bars.bar(xs - 0.18, costs, width=0.34,
                 color=[LINE if c < 2 else GREY for c in costs], label="r = 3")
    if stage >= 7:
        costs = [1.5 / a for a in FJ_A]
        bars.bar(xs + 0.18, costs, width=0.34, color=NEW, alpha=0.8, label="r = 3/2")
    gp.legend(bars, loc="upper left")

    gp.frame(g, 6.5, 1.05, "machine rent r", "saving index G")
    if stage >= 5:
        gp.dot(g, 3, 5 / 16, "r = 3", 6, 4, colour=LINE)
    if stage >= 7:
        gp.dot(g, 1.5, 19 / 32, "r = 3/2", 6, 4, colour=NEW)
    if stage >= 9:
        _G_curve(g, FJ_A, FJ_X, 2, 6.5, color=LINE, lw=2)
        for r in (6, 4, 2):
            g.axvline(r, color=GREY, lw=1, ls=":")
    fig.subplots_adjust(wspace=0.3)


CUT_ASM = "Cutting and assembly by machine; finishing by labor"
ALL_MACH = "All three by machine"
CUT_ONLY = "Cutting only"
NONE_MACH = "None: machines rent for more than the wage"

UNION = "Displacement removes labor from automated tasks, while lower costs can expand sales and demand for remaining tasks; the model takes the wage as given, so it needs product demand and a labor market"
UNION_RIGHT = "The union is right: automation lowers wages"
MGMT_RIGHT = "Management is right: lower costs raise wages"
BOTH_RIGHT = "Both are right at once"

FEASIBLE = "The feasible production set expands weakly, outward where the improved tasks matter; neither a parallel shift nor gains for every worker follow"
PARALLEL = "The frontier shifts out in parallel"
EVERY = "Every worker gains"
SHRINKS = "The production set shrinks"

FJORDLINE_QUESTIONS = [
    Question(
        "f1",
        "A8.2: workers cost w = 2 per hour, machines rent for r = 3, and machine "
        "productivity is A = (3, 2, 1) for cutting, assembly and finishing. (a) The cutoff?",
        form=["%s =" % ABAR, BOX],
        answers=[H("f1.0")],
        mistakes=M({"f1.0~2/3": "Upside down: r/w."}),
        explain="At A = %s the methods tie." % ABAR),
    Question(
        "f2",
        "(b) The machine unit costs r/A<sub>i</sub>?",
        form=["cutting", BOX, "&nbsp; assembly", BOX, "&nbsp; finishing", BOX],
        answers=[H("f2.0"), H("f2.1"), H("f2.2")],
        explain="Compare each with w = 2."),
    Question(
        "f3",
        "Assign each task to its cheaper method.",
        choices=[CUT_ASM, ALL_MACH, CUT_ONLY, NONE_MACH],
        answers=[H("f3.c")],
        mistakes=M({
            "f3.c~" + ALL_MACH: "Finishing costs 3 by machine against 2 by hand.",
            "f3.c~" + CUT_ONLY: "Assembly: 3/2 &lt; 2.",
            "f3.c~" + NONE_MACH: "Compare per task-unit, r/A, not r.",
        }),
        explain="Worksheet tasks 3&ndash;4 use these same numbers."),
    Question(
        "f4",
        "(c) Each saving &pi;<sub>i</sub> = 1 &minus; c<sub>i</sub>/w, with c<sub>i</sub> the "
        "chosen cost?",
        form=["&pi; = (", BOX, ",", BOX, ",", BOX, ")"],
        answers=[H("f4.0"), H("f4.1"), H("f4.2")],
        mistakes=M({"f4.2~-1/2": "The saving uses the chosen cost, not the rejected machine."}),
        explain="No task saves a negative amount."),
    Question(
        "f5",
        "Shares &chi; = (1/2, 1/4, 1/4). The index G, and the new cost of the all-labor order "
        "that cost 160?",
        form=["G =", BOX, "&nbsp; cost =", BOX],
        answers=[H("f5.0"), H("f5.1")],
        mistakes=M({"f5.1~50": "That is the saving. The order now costs 160(1 &minus; G)."}),
        explain="31.25% for a fixed order: a cost reduction, not an exact log TFP gain."),
    Question(
        "f6",
        "(d) At which rental rate is finishing tied?",
        form=["r =", BOX],
        answers=[H("f6.0")],
        explain="The machine is strictly cheaper for finishing when r &lt; 2."),
    Question(
        "f7",
        "Set r = 3/2. The new index and the order cost?",
        form=["G =", BOX, "&nbsp; cost =", BOX],
        answers=[H("f7.0"), H("f7.1")],
        mistakes=M({"f7.0~5/16": "Recompute: all three tasks now use machines."}),
        explain="The cutoff is 3/4: all three productivities exceed it."),
    Question(
        "f8",
        "(e) Split &Delta;G = 9/32: savings on tasks already automated, and on newly automated "
        "finishing?",
        form=["already", BOX, "&nbsp; new", BOX],
        answers=[H("f8.0"), H("f8.1")],
        mistakes=M({"f8.0~9/32": "That is the total. Finishing contributes (1/4)(1/4)."}),
        explain="At the tie itself, switching finishing saves exactly zero."),
    Question(
        "f9",
        "Worksheet task 5 with these numbers: G at r = 4 and at r = 2?",
        form=["G(4) =", BOX, "&nbsp; G(2) =", BOX],
        answers=[H("f9.0"), H("f9.1")],
        mistakes=M({"f9.0~0": "At r = 4 cutting is already automated: 1 &minus; 4/6."}),
        explain="Thresholds at 6, 4 and 2; G approaches 1 as r approaches zero."),
    Question(
        "f10",
        "(f) The union says automation must lower wages; management says lower costs must raise "
        "them.",
        choices=[UNION, UNION_RIGHT, MGMT_RIGHT, BOTH_RIGHT],
        answers=[H("f10.c")],
        mistakes=M({
            "f10.c~" + UNION_RIGHT: "Lower costs can expand sales and raise demand for "
                                    "remaining tasks.",
            "f10.c~" + MGMT_RIGHT: "Displacement removes labor from automated tasks.",
            "f10.c~" + BOTH_RIGHT: "They predict opposite things; the model determines neither.",
        }),
        explain="The wage is an input to the calculation, not an equilibrium outcome."),
    Question(
        "f11",
        "(g) Cheaper machines reflect a genuine resource saving. What happens to the economy's "
        "feasible production set?",
        choices=[FEASIBLE, PARALLEL, EVERY, SHRINKS],
        answers=[H("f11.c")],
        mistakes=M({
            "f11.c~" + PARALLEL: "Its shape depends on which sectors use the improved tasks.",
            "f11.c~" + EVERY: "Feasibility says nothing about who receives the extra output.",
            "f11.c~" + SHRINKS: "Old plans stay feasible.",
        }),
        explain="Some workers can lose even when the economy can produce more."),
]

fjordline = GuidedProblem(
    "Part 8 &middot; Fjordline Furniture: A8.2",
    "Task choice, savings and a lower rental rate, for a fixed order. These are also the "
    "worksheet's numbers for tasks 3&ndash;5.",
    FJORDLINE_QUESTIONS, draw_fjordline, figsize=(8.0, 3.9), whole_figure=True,
    outro="About 15&ndash;20% of an exam paper, and the worksheet's gain panel.",
    sources=[PS("A8.2"), NOTES("p. 16, worksheet tasks 3&ndash;5")],
)


# ======================================================================
# Part 9: problem A8.3, AI that needs review
# ======================================================================

HB_NAMES = ["summary", "compliance", "chart"]
HB_H, HB_F, HB_T = (1, 0.5, 0.8), (6, 3, 9), (0.2, 0.5, 0.1)


def draw_harbor(ax, stage):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    xs = np.arange(3)
    ax.set_xticks(xs)
    ax.set_xticklabels(HB_NAMES, fontsize=9, color=INK)
    ax.set_yticks([])
    ax.set_ylim(0, 34)
    ax.set_ylabel("cost per task-unit", color=INK, fontsize=10, loc="top")
    if stage >= 1:
        ax.bar(xs - 0.18, [30 * h for h in HB_H], width=0.34, color=GREY, label="human only")
    if stage >= 2:
        ax.bar(xs + 0.18, HB_F, width=0.34, color=LINE, label="AI fee")
        ax.bar(xs + 0.18, [30 * t for t in HB_T], bottom=HB_F, width=0.34, color=HALF,
               label="review hours")
    if stage >= 6:
        ax.bar(xs + 0.18, [f / 2 for f in HB_F], width=0.34, color="none", edgecolor=NEW,
               lw=1.5, ls="--", label="fee halved")
    gp.legend(ax, loc="upper right")


SUM_CHART = "AI for the summary and the chart; human for compliance"
ALL_AI3 = "AI for all three: the fees are low"
SUM_ONLY = "AI for the summary only"
HUMAN_ALL = "Human for all three"

NO_SWITCH = "No task changes method: compliance stays human because its review alone takes as long as doing it"
COMP_SW = "Compliance switches to AI"
CHART_BACK = "The chart switches back to human"
ALL_SW = "All switch to AI"

NO_HOURS = "AI's advantage is w(h − t) − f: a higher wage helps AI only where it saves human hours, and compliance saves none"
WAGE_ALL = "It does: every task becomes cheaper with AI"
WAGE_FEE = "Because fees rise with wages"
WAGE_REV = "Because review is unpaid"

NOT_EMPLOY = "No: lower costs may expand orders and workers may take other tasks; we need demand, task needs at the new scale and labor-market adjustment"
YES_EMPLOY = "Yes: employment falls by 15 hours a week"
YES_ZERO = "Yes: employment falls to zero eventually"
MORE_EMPLOY = "Yes: employment must rise"

HARBOR_QUESTIONS = [
    Question(
        "h1",
        "A8.3: Harbor Advice pays w = 30. Human-only hours per task-unit are 1, 1/2 and "
        "4/5. The human-only cost of each?",
        form=["summary", BOX, "&nbsp; compliance", BOX, "&nbsp; chart", BOX],
        answers=[H("h1.0"), H("h1.1"), H("h1.2")],
        explain="c<sup>H</sup> = w&middot;h."),
    Question(
        "h2",
        "AI fees are 6, 3 and 9, plus review of 1/5, 1/2 and 1/10 hour. The AI-with-review cost "
        "of each?",
        form=["summary", BOX, "&nbsp; compliance", BOX, "&nbsp; chart", BOX],
        answers=[H("h2.0"), H("h2.1"), H("h2.2")],
        mistakes=M({"h2.0~6": "Include the review: f + w&middot;t.",
                    "h2.1~3": "Include the review: 3 + 30/2."}),
        explain="c<sup>AI</sup> = f + w&middot;t: the fee is only part of AI's cost."),
    Question(
        "h3",
        "(a) Choose the cheaper method for each.",
        choices=[SUM_CHART, ALL_AI3, SUM_ONLY, HUMAN_ALL],
        answers=[H("h3.c")],
        mistakes=M({
            "h3.c~" + ALL_AI3: "Compliance: 18 with AI against 15 by hand.",
            "h3.c~" + SUM_ONLY: "Chart: 12 against 24.",
            "h3.c~" + HUMAN_ALL: "Summary: 12 against 30.",
        }),
        explain="AI's low compliance fee is misleading: review alone takes as long as the job."),
    Question(
        "h4",
        "(b) The highest review time t that keeps AI weakly cheaper for a summary?",
        form=["t =", BOX, "hours"],
        answers=[H("h4.0")],
        mistakes=M({"h4.0~1": "6 + 30t &le; 30."}),
        explain="At the boundary both cost 30: either method."),
    Question(
        "h5",
        "(c) The weekly order: 10 summaries, 20 compliance checks and 10 charts. All-human cost, "
        "chosen-method cost, and human hours that remain (including review)?",
        form=["all-human", BOX, "&nbsp; chosen", BOX, "&nbsp; hours", BOX],
        answers=[H("h5.0"), H("h5.1"), H("h5.2")],
        mistakes=M({"h5.2~3": "Compliance stays human: 20 &times; 1/2 = 10 hours."}),
        explain="Human hours fall from 28 to 13 for this fixed order."),
    Question(
        "h6",
        "(d) AI fees fall by half; wages and review fixed. Weekly cost, and saving relative to "
        "the original all-human order?",
        form=["cost", BOX, "&nbsp; saving", BOX],
        answers=[H("h6.0"), H("h6.1")],
        explain="The fee cut saves another 75 without automating anything new."),
    Question(
        "h7",
        "Which tasks changed method in (d)?",
        choices=[NO_SWITCH, COMP_SW, CHART_BACK, ALL_SW],
        answers=[H("h7.c")],
        mistakes=M({
            "h7.c~" + COMP_SW: "3/2 + 15 against 15.",
            "h7.c~" + CHART_BACK: "Cheaper fees can only help AI.",
            "h7.c~" + ALL_SW: "Compliance: 33/2 against 15.",
        }),
        explain="Human hours stay at 13."),
    Question(
        "h8",
        "(e) Original fees, wage 40: the same choices. Why doesn't a higher wage make AI cheaper "
        "on every task?",
        choices=[NO_HOURS, WAGE_ALL, WAGE_FEE, WAGE_REV],
        answers=[H("h8.c")],
        mistakes=M({
            "h8.c~" + WAGE_ALL: "Compliance: 20 by hand against 23 with AI.",
            "h8.c~" + WAGE_FEE: "Fees are fixed here.",
            "h8.c~" + WAGE_REV: "Review hours are paid at w.",
        }),
        explain="A wage rise favors AI only where it saves human hours."),
    Question(
        "h9",
        "(f) Does the fixed-order fall in hours predict total employment?",
        choices=[NOT_EMPLOY, YES_EMPLOY, YES_ZERO, MORE_EMPLOY],
        answers=[H("h9.c")],
        mistakes=M({
            "h9.c~" + YES_EMPLOY: "Only for a fixed order. Orders may grow.",
            "h9.c~" + YES_ZERO: "AI still requires human review.",
            "h9.c~" + MORE_EMPLOY: "Nothing here says it must.",
        }),
        explain="A useful tool is not necessarily a labor-saving tool."),
]

harbor = GuidedProblem(
    "Part 9 &middot; AI that needs review: A8.3",
    "Compare completed tasks, not drafts: the AI method costs its fee plus the human hours "
    "needed to check it.",
    HARBOR_QUESTIONS, draw_harbor, figsize=(6.4, 4.4),
    outro="Choose the cheaper completed report, not the cheaper draft.",
    sources=[PS("A8.3"), NOTES("p. 9")],
)


# ======================================================================
# Where every step comes from (printed pages of s08_notes.pdf)
# ======================================================================

STEP_SOURCES = {
    "k1": NOTES("p. 2 &middot; bakery"), "k2": NOTES("p. 2 &middot; bakery"),
    "k3": NOTES("p. 3 &middot; markup"), "k4": NOTES("p. 3 &middot; markup"),
    "k5": NOTES("p. 4 &middot; cost minimization"),
    "e1": NOTES("p. 4 &middot; elasticity"), "e2": NOTES("p. 4 &middot; elasticity"),
    "e3": NOTES("p. 16 &middot; worksheet task 1"), "e4": NOTES("p. 16 &middot; worksheet task 2"),
    "e5": NOTES("p. 17 &middot; review question 3 (a)"), "e6": NOTES("p. 17 &middot; review question 3 (b)"),
    "e7": NOTES("p. 17 &middot; review question 3 (b)"), "e8": NOTES("p. 17 &middot; review question 3 (d)"),
    "c1": NOTES("p. 7 &middot; Try it"), "c2": NOTES("p. 8 &middot; the cutoff"),
    "c3": NOTES("p. 8 &middot; Try it"), "c4": NOTES("p. 17 &middot; review question 2"),
    "c5": NOTES("p. 17 &middot; review question 2"), "c6": NOTES("p. 9 &middot; comparative statics"),
    "c7": NOTES("p. 14 &middot; education"),
    "n1": NOTES("p. 11 &middot; Try it (a)"), "n2": NOTES("p. 11 &middot; Try it (a)"),
    "n3": NOTES("p. 11 &middot; Try it (b)"), "n4": NOTES("p. 11 &middot; Try it (c)"),
    "n5": NOTES("p. 11 &middot; Try it (d)"), "n6": NOTES("p. 12 &middot; scale check"),
    "n7": NOTES("p. 12 &middot; scale check"),
    "q1": NOTES("p. 17 &middot; review question 4 (a)"), "q2": NOTES("p. 17 &middot; review question 4 (a)"),
    "q3": NOTES("p. 17 &middot; review question 4 (b)"), "q4": NOTES("p. 17 &middot; review question 4 (b)"),
    "q5": NOTES("p. 17 &middot; review question 4 (c)"), "q6": NOTES("p. 17 &middot; review question 4 (d)"),
    "q7": NOTES("p. 17 &middot; review question 4 (d)"),
    "x1": NOTES("p. 16 &middot; worksheet task 6"), "x2": NOTES("p. 16 &middot; worksheet task 6"),
    "x3": NOTES("p. 16 &middot; worksheet task 6"), "x4": NOTES("p. 17 &middot; review question 6"),
    "x5": NOTES("p. 17 &middot; review question 6"), "x6": NOTES("p. 17 &middot; review question 5"),
    "m1": PS("A8.1 (a)"), "m2": PS("A8.1 (a)&ndash;(b)"), "m3": PS("A8.1 (c)"), "m4": PS("A8.1 (d)"),
    "m5": PS("A8.1 (e)"),
    "f1": PS("A8.2 (a)"), "f2": PS("A8.2 (b)"), "f3": PS("A8.2 (b)"), "f4": PS("A8.2 (c)"), "f5": PS("A8.2 (c)"),
    "f6": PS("A8.2 (d)"), "f7": PS("A8.2 (d)"), "f8": PS("A8.2 (e)"),
    "f9": NOTES("p. 16 &middot; worksheet task 5"), "f10": PS("A8.2 (f)"), "f11": PS("A8.2 (g)"),
    "h1": PS("A8.3 (a)"), "h2": PS("A8.3 (a)"), "h3": PS("A8.3 (a)"), "h4": PS("A8.3 (b)"), "h5": PS("A8.3 (c)"),
    "h6": PS("A8.3 (d)"), "h7": PS("A8.3 (d)"), "h8": PS("A8.3 (e)"), "h9": PS("A8.3 (f)"),
}

for _q in (PRODUCER_QUESTIONS + SIGMA_QUESTIONS + CUTOFF_QUESTIONS + NORDVIK_QUESTIONS
           + KYST_QUESTIONS + FRONTIER_QUESTIONS + MARINE_QUESTIONS + FJORDLINE_QUESTIONS
           + HARBOR_QUESTIONS):
    _q.source = STEP_SOURCES[_q.qid]
