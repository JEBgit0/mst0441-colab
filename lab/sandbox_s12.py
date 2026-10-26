"""
sandbox_s12.py - session 12 sandbox: static games and Nash equilibrium.

    matrix   Lab 1  any two-by-two game: best responses, pure and mixed Nash
                    equilibria, and the indifference diagrams
    iesds    Lab 2  iterated elimination of strictly dominated strategies,
                    one round at a time, on the course's larger games
    duopoly  Lab 3  Cournot and Bertrand in one market: best responses,
                    prices, quantities and profits
    slopes   Lab 4  linear best responses: strategic substitutes and
                    complements, and why the equilibrium is unique

Released with the session 12 solutions. The maths is games.py, the drawing
of matrices game_plots.py.
"""

import numpy as np

import game_plots as gm
import games as gs
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, GREEN, GREY, INK, LINE, MUTE, NEW


def frac(x):
    # Probabilities print as the notes print them: 2/5, not 0.4.
    if hasattr(x, "denominator"):
        return "%d/%d" % (x.numerator, x.denominator) if x.denominator != 1 else "%d" % int(x)
    return num(x, 3)


# ======================================================================
# Lab 1: two-by-two games
# ======================================================================

CELLS = ("11", "12", "21", "22")


def game_values(rows):
    # rows = [[(u, v), (u, v)], [(u, v), (u, v)]] as slider values.
    out = {}
    for i in range(2):
        for j in range(2):
            out["u%d%d" % (i + 1, j + 1)] = float(rows[i][j][0])
            out["v%d%d" % (i + 1, j + 1)] = float(rows[i][j][1])
    return out


def two(label, kind, players, rows, cols, payoffs, **kw):
    return dict(label=label, kind=kind, values=game_values(payoffs),
                names=(players, tuple(rows), tuple(cols)), **kw)


AUDIT = [[(-20, 10), (30, -30)], [(0, -5), (0, 0)]]
GAMES = [
    two("Advertising (PD)", "notes", ("OpenAI", "Anthropic"), ("Advertise", "No ad"),
        ("Advertise", "No ad"), [[(-2, -2), (3, -3)], [(-3, 3), (0, 0)]]),
    two("AI build-out", "notes", ("OpenAI", "Anthropic"), ("Invest", "Wait"), ("Invest", "Wait"),
        [[(2, 2), (-1, 0)], [(0, -1), (1, 1)]]),
    two("Talent war", "notes", ("OpenAI", "Anthropic"), ("C", "T"), ("C", "T"),
        [[(3, 3), (1, 4)], [(4, 1), (2, 2)]]),
    two("W1 penalty kick", "problem", ("Kicker", "Goalie"), ("L", "R"), ("L", "R"),
        [[(-1, 1), (1, -1)], [(1, -1), (-1, 1)]]),
    two("W2 stag hunt", "problem", ("Hunter 1", "Hunter 2"), ("Stag", "Hare"), ("Stag", "Hare"),
        [[(3, 3), (0, 1)], [(1, 0), (1, 1)]]),
    two("Worksheet: release game", "notes", ("Anthropic", "OpenAI"), ("March", "Sept"),
        ("March", "Sept"), [[(0, 3), (2, 0)], [(3, 0), (0, 1)]]),
    two("Review Q3: data standard", "notes", ("Nordapp", "Fjordsoft"), ("A", "B"), ("A", "B"),
        [[(5, 3), (1, 1)], [(0, 0), (3, 5)]]),
    two("Review Q6: striker", "notes", ("Striker", "Keeper"), ("L", "R"), ("L", "R"),
        [[(0, 1), (2, 0)], [(1, 0), (0, 1)]]),
    two("A12.1 X or Y", "problem", ("Kvist", "Lundin"), ("X", "Y"), ("X", "Y"),
        [[(6, 6), (2, 2)], [(2, 2), (4, 4)]]),
    two("A12.2 audit", "problem", ("Berg", "Authority"), ("Evade", "Comply"), ("Audit", "Not"),
        AUDIT),
    two("A12.2 (d) penalty 40", "problem", ("Berg", "Authority"), ("Evade", "Comply"),
        ("Audit", "Not"), [[(-40, 10), (30, -30)], [(0, -5), (0, 0)]],
        before=game_values(AUDIT)),
]


def matrix_of(v, names):
    _, rows, cols = names
    return gs.Matrix(rows, cols, [[(v["u%d%d" % (i, j)], v["v%d%d" % (i, j)]) for j in (1, 2)]
                                  for i in (1, 2)])


class MatrixLab(Lab):
    TITLE = "Lab 1 &middot; Two-by-two games"
    INTRO = ("Any simultaneous game with two strategies each. Underlined payoffs are best "
             "responses; shaded cells are pure Nash equilibria. The two right panels are the "
             "indifference diagrams: each player's expected payoff from her two strategies "
             "against the other's mix. A player mixes only where her two lines cross, and that "
             "crossing is set by the opponent's mix.")
    SLIDERS = [(k, -50.0, 50.0, 1.0, 0.0, ".0f") for c in CELLS for k in ("u" + c, "v" + c)]
    FIGSIZE = (9.6, 3.7)
    PRESETS = GAMES

    def __init__(self):
        super().__init__()
        self.names = GAMES[0]["names"]

    def show(self):
        super().show()
        self.apply(GAMES[0])

    def on_preset(self, preset):
        self.names = preset["names"]

    def relabel(self):
        (p1, p2), rows, cols = self.names
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                html_label(self.w["u%d%d" % (i + 1, j + 1)], "%s at (%s, %s)" % (p1, r, c))
                html_label(self.w["v%d%d" % (i + 1, j + 1)], "%s at (%s, %s)" % (p2, r, c))

    def compute(self):
        g = matrix_of(self.values(), self.names)
        st = dict(g=g, nash=g.pure_nash(), mixed=g.mixed())
        st["before"] = matrix_of(self.before, self.names) if self.before else None
        return st

    def figure(self, fig, st):
        g = st["g"]
        (p1, p2), rows, cols = self.names
        mat, rl, cl = fig.subplots(1, 3, gridspec_kw=dict(width_ratios=[1.25, 1, 1]))
        gm.matrix(mat, g, p1, p2, nash=st["nash"], best=True, fontsize=10)
        for ax, lines_of, me, other, labels, colours in (
                (rl, g.row_lines, p1, p2, rows, (LINE, NEW)),
                (cl, g.col_lines, p2, p1, cols, (CURVE, NEW))):
            style_axes(ax)
            lo, hi = lines_of(1), lines_of(0)            # against prob 1 and 0 of the first
            for k, label in enumerate(labels):
                ax.plot([0, 1], [hi[k], lo[k]], color=colours[k], lw=2, label="%s plays %s" %
                        (me, label))
            if st["before"] is not None:
                bl = st["before"].row_lines if lines_of == g.row_lines else st["before"].col_lines
                b1, b0 = bl(1), bl(0)
                for k in range(2):
                    ax.plot([0, 1], [b0[k], b1[k]], color=BEFORE, lw=1, ls="--")
            ax.set_xlim(0, 1)
            first = cols[0] if lines_of == g.row_lines else rows[0]
            ax.set_xlabel("P(%s plays %s)" % (other, first), color=INK, fontsize=8.5, loc="right")
            ax.set_title("%s's expected payoff" % me, loc="left", color=INK, fontsize=9)
            legend(ax, loc="best")
        if st["mixed"] is not None:
            p, q = st["mixed"]
            rl.axvline(float(q), color=GREEN, lw=1.2, ls=":")
            cl.axvline(float(p), color=GREEN, lw=1.2, ls=":")
        fig.subplots_adjust(left=0.02, right=0.99, top=0.9, bottom=0.14, wspace=0.28)

    def describe(self, st):
        g = st["g"]
        (p1, p2), rows, cols = self.names
        br1 = "; ".join("against %s: %s" % (cols[j], " or ".join(rows[i] for i in g.row_best(j)))
                        for j in range(2))
        br2 = "; ".join("against %s: %s" % (rows[i], " or ".join(cols[j] for j in g.col_best(i)))
                        for i in range(2))
        out = [("Best responses", "%s &mdash; %s. %s &mdash; %s." % (p1, br1, p2, br2))]
        dom = []
        for who, k, names in ((p1, g.dominant_row(), rows), (p2, g.dominant_col(), cols)):
            if k is not None:
                dom.append("%s: %s is strictly dominant" % (who, names[k]))
        out.append(("Dominance", "; ".join(dom) + "." if dom else "Neither player has a strictly "
                                                                  "dominant strategy."))
        if st["nash"]:
            cells = ["(%s, %s) paying (%s, %s)" % (rows[i], cols[j], num(g.u[i][j][0]),
                                                    num(g.u[i][j][1])) for i, j in st["nash"]]
            out.append(("Pure Nash", "; ".join(cells) + "."))
            better = [(i, j) for i in range(2) for j in range(2)
                      if any(g.u[i][j][0] > g.u[a][b][0] and g.u[i][j][1] > g.u[a][b][1]
                             for a, b in st["nash"])]
            if len(st["nash"]) == 1 and better:
                i, j = better[0]
                out.append(("A dilemma", "The cell (%s, %s) is better for both, but it is not an "
                                         "equilibrium: someone gains by deviating from it."
                            % (rows[i], cols[j])))
        else:
            out.append(("Pure Nash", "None: in every cell somebody regrets their choice."))
        if st["mixed"] is not None:
            p, q = st["mixed"]
            e1, e2 = g.expected(p, q)
            out.append(("Mixed Nash", "%s plays %s with probability %s, which leaves %s "
                                      "indifferent; %s plays %s with probability %s, which leaves "
                                      "%s indifferent. Expected payoffs (%s, %s)."
                        % (p1, rows[0], frac(p), p2, p2, cols[0], frac(q), p1, frac(e1),
                           frac(e2))))
            out.append(("The twist", "Each player's mix is pinned down by the opponent's "
                                     "payoffs: change %s's payoffs and %s's mix moves, not "
                                     "%s's own." % (p1, p2, p1)))
        else:
            out.append(("Mixed Nash", "No fully mixed equilibrium: one player's lines never "
                                      "cross, so she never wants to randomize."))
        return table(out)


# ======================================================================
# Lab 2: iterated elimination
# ======================================================================

NOTES_3 = gs.Matrix(["A1", "A2", "A3"], ["B1", "B2", "B3"],
                    [[(2, 3), (1, 4), (3, 2)], [(4, 1), (2, 2), (2, 0)], [(3, 3), (0, 5), (2, 1)]])
PITCH = gs.Matrix(["T", "M", "B"], ["L", "C", "R"],
                  [[(3, 5), (1, 4), (2, 2)], [(4, 2), (2, 3), (1, 1)], [(2, 1), (0, 2), (3, 0)]])
MEMORY = gs.Matrix(["q=0", "q=1", "q=2", "q=3"], ["0", "1", "2", "3"],
                   [[((4 - i - j) * i - i * i, (4 - i - j) * j - j * j) for j in range(4)]
                    for i in range(4)])
KVIST = gs.Matrix(["X", "Y", "A"], ["X", "Y", "A"],
                  [[(6, 6), (2, 2), (3, 1)], [(2, 2), (4, 4), (3, 1)], [(1, 3), (1, 3), (2, 2)]])

ELIM = {
    "Notes p. 5: the 3×3 game": (NOTES_3, ("Player 1", "Player 2")),
    "Review Q2: consulting pitches": (PITCH, ("Row", "Column")),
    "Notes p. 6: memory lines": (MEMORY, ("Rival j", "You")),
    "A12.1: Kvist and Lundin": (KVIST, ("Kvist", "Lundin")),
}
ELIM_NAMES = list(ELIM)


class IESDSLab(Lab):
    TITLE = "Lab 2 &middot; Iterated elimination, one round at a time"
    INTRO = ("Each round deletes every strategy, of either player, that another live strategy "
             "beats against everything still live. Move the slider to add rounds: each one "
             "climbs a rung of common knowledge of rationality.")
    DROPDOWNS = [("game", "Game", ELIM_NAMES)]
    SLIDERS = [("rounds", 0.0, 4.0, 1.0, 0.0, ".0f")]
    FIGSIZE = (6.2, 4.2)
    PRESETS = ([dict(label=name.split(":")[0] + ", start", kind="problem" if name.startswith("A")
                     else "notes", values=dict(game=name, rounds=0.0)) for name in ELIM_NAMES]
               + [dict(label="Memory lines, all rounds", kind="notes",
                       values=dict(game=ELIM_NAMES[2], rounds=4.0))])

    def relabel(self):
        self.w["rounds"].description = "Rounds shown"

    def compute(self):
        g, players = ELIM[self.w["game"].value]
        rounds, rows, cols = g.iesds()
        k = int(self.w["rounds"].value)
        shown = rounds[:k]
        return dict(g=g, players=players, rounds=rounds, shown=shown,
                    srows=[i for r in shown for s, i, _ in r if s == "row"],
                    scols=[j for r in shown for s, j, _ in r if s == "col"],
                    survivors=(rows, cols), done=k >= len(rounds))

    def figure(self, fig, st):
        ax = fig.add_subplot()
        g = st["g"]
        nash = [(i, j) for i, j in g.pure_nash()] if st["done"] else ()
        gm.matrix(ax, g, *st["players"], struck_rows=st["srows"], struck_cols=st["scols"],
                  nash=nash, fontsize=10 if len(g.rows) < 4 else 9)
        fig.tight_layout()

    def describe(self, st):
        g = st["g"]
        p1, p2 = st["players"]
        rows = []
        for n, rnd in enumerate(st["rounds"]):
            text = "; ".join("%s's %s, beaten by %s" % (p1 if s == "row" else p2,
                                                        (g.rows if s == "row" else g.cols)[i],
                                                        (g.rows if s == "row" else g.cols)[k])
                             for s, i, k in rnd)
            rows.append(("Round %d%s" % (n + 1, "" if n < len(st["shown"]) else " (next)"), text))
            if n >= len(st["shown"]):
                break
        if not st["rounds"]:
            rows.append(("Rounds", "Nothing is strictly dominated: IESDS is silent here."))
        if st["done"]:
            r, c = st["survivors"]
            surv = "%s for %s and %s for %s" % (", ".join(g.rows[i] for i in r), p1,
                                               ", ".join(g.cols[j] for j in c), p2)
            rows.append(("Survivors", surv + "."))
            nash = ", ".join("(%s, %s)" % (g.rows[i], g.cols[j]) for i, j in g.pure_nash())
            rows.append(("Nash", "Pure Nash equilibria of the full game: %s. Where IESDS leaves a "
                                 "single profile, it is the unique Nash equilibrium." % nash))
        return table(rows)


# ======================================================================
# Lab 3: Cournot and Bertrand
# ======================================================================

COURNOT, BERTRAND = "Cournot: quantities", "Bertrand: posted prices"
API = dict(a=100.0, c1=10.0, c2=10.0)
TRY = dict(a=27.0, c1=3.0, c2=3.0)


class DuopolyLab(Lab):
    TITLE = "Lab 3 &middot; Quantities or prices: Cournot and Bertrand"
    INTRO = ("Two firms, identical goods, inverse demand P = a &minus; Q and constant marginal "
             "costs. In Cournot each firm picks a quantity: q<sub>i</sub> = (a &minus; "
             "c<sub>i</sub> &minus; q<sub>j</sub>)/2. In Bertrand each posts a price and buyers "
             "go to the cheaper one. The left panel shows the best responses, with the rival's "
             "quantity across.")
    DROPDOWNS = [("mode", "Competition", [COURNOT, BERTRAND])]
    SLIDERS = [
        ("a", 10.0, 160.0, 1.0, 100.0, ".0f"),
        ("c1", 0.0, 60.0, 1.0, 10.0, ".0f"),
        ("c2", 0.0, 60.0, 1.0, 10.0, ".0f"),
    ]
    FIGSIZE = (8.8, 4.2)
    PRESETS = [
        dict(label="Notes p. 9 API market", kind="notes", values=dict(API, mode=COURNOT)),
        dict(label="Notes p. 10 API, posted prices", kind="notes", values=dict(API, mode=BERTRAND),
             before=dict(API, mode=COURNOT)),
        dict(label="Try it (a) P = 27 − Q", kind="notes", values=dict(TRY, mode=COURNOT)),
        dict(label="Try it (b) cost 9", kind="notes", before=dict(TRY, mode=COURNOT),
             values=dict(TRY, c1=9.0, c2=9.0, mode=COURNOT)),
        dict(label="Try it (c) reprice instantly", kind="notes", values=dict(TRY, mode=BERTRAND)),
        dict(label="Worksheet: power duopoly", kind="notes",
             values=dict(a=90.0, c1=30.0, c2=30.0, mode=COURNOT)),
        dict(label="Review Q4-5: ferries", kind="notes",
             values=dict(a=60.0, c1=6.0, c2=6.0, mode=COURNOT)),
        dict(label="Unequal costs", kind="extra", values=dict(API, c2=25.0, mode=COURNOT)),
    ]

    def relabel(self):
        self.w["a"].description = "Demand intercept a"
        self.w["c1"].description = "Firm 1's cost"
        self.w["c2"].description = "Firm 2's cost"

    def outcomes(self, v):
        return dict(cournot=gs.cournot(v["a"], v["c1"], v["c2"]),
                    bertrand=gs.bertrand(v["a"], v["c1"], v["c2"]))

    def chosen(self, v, out):
        return out["cournot"] if v["mode"] == COURNOT else out["bertrand"]

    def compute(self):
        v = self.values()
        st = dict(v=v, out=self.outcomes(v))
        st["live"] = self.chosen(v, st["out"])
        if self.before:
            bo = self.outcomes(self.before)
            st["before"] = self.chosen(self.before, bo)
        else:
            st["before"] = None
        return st

    def draw_br(self, ax, st):
        v = st["v"]
        a, c1, c2 = v["a"], v["c1"], v["c2"]
        top = self.stick("q", max(a - c1, a - c2) * 1.05)
        q = np.linspace(0, top, 200)
        ax.plot(q, [gs.cournot_br(a, c1, x) for x in q], color=LINE, lw=2, label="BR$_1$")
        ax.plot([gs.cournot_br(a, c2, x) for x in q], q, color=CURVE, lw=2, label="BR$_2$")
        c = st["out"]["cournot"]
        ax.plot([c["q2"]], [c["q1"]], "o", color=GREEN, ms=8, zorder=6, label="Cournot")
        ax.set_xlim(0, top)
        ax.set_ylim(0, top)
        ax.set_xlabel("rival's quantity q$_2$", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("q$_1$", color=INK, fontsize=9, loc="top")
        ax.set_title("Best responses", loc="left", color=INK, fontsize=9.5)

    def figure(self, fig, st):
        br, bars = fig.subplots(1, 2)
        style_axes(br)
        self.draw_br(br, st)
        legend(br)
        self.draw_bars(bars, st)
        fig.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.12, wspace=0.22)

    def bar_items(self, st):
        v, out = st["v"], st["out"]
        comp = min(v["c1"], v["c2"])
        return [("Cournot", out["cournot"]["P"], LINE), ("Bertrand", out["bertrand"]["P"], NEW),
                ("price takers", comp, GREY)]

    def draw_bars(self, ax, st):
        style_axes(ax)
        items = self.bar_items(st)
        xs = np.arange(len(items))
        ax.bar(xs, [p for _, p, _ in items], color=[c for _, _, c in items], width=0.6)
        for x, (_, p, _) in zip(xs, items):
            ax.text(x, p, num(p), ha="center", va="bottom", color=INK, fontsize=9)
        ax.set_xticks(xs)
        ax.set_xticklabels([n for n, _, _ in items], fontsize=9)
        ax.set_ylim(0, self.stick("P", st["v"]["a"] * 0.7))
        ax.set_title("The market price", loc="left", color=INK, fontsize=9.5)

    def describe(self, st):
        v, out = st["v"], st["out"]
        c, b = out["cournot"], out["bertrand"]
        comp = max(v["a"] - min(v["c1"], v["c2"]), 0)
        rows = [
            ("Cournot", "q<sub>1</sub> = %s, q<sub>2</sub> = %s, Q = %s, P = %s; profits %s and %s."
             % (num(c["q1"]), num(c["q2"]), num(c["Q"]), num(c["P"]), num(c["pi1"]),
                num(c["pi2"]))),
            ("Bertrand", "P = %s, Q = %s; profits %s and %s.%s"
             % (num(b["P"]), num(b["Q"]), num(b["pi1"]), num(b["pi2"]),
                " Two firms deliver the competitive output." if v["c1"] == v["c2"] else
                " The cheaper firm prices at its rival's cost and serves everyone.")),
            ("Price takers", "P = MC: total output %s." % num(comp)),
            ("Why so different?", "A Cournot firm that expands accepts a lower price on all its "
                                  "output; a Bertrand firm that undercuts by a cent takes the "
                                  "whole market."),
        ]
        if st["before"] is not None:
            bf, lv = st["before"], st["live"]
            rows.append(("Before &rarr; after", "Price %s &rarr; %s, output %s &rarr; %s."
                         % (num(bf["P"]), num(lv["P"]), num(bf["Q"]), num(lv["Q"]))))
        if v["c1"] == v["c2"] and v["mode"] == COURNOT:
            rows.append(("Read the cost", "With equal costs the Cournot price is (a + 2c)/3, so a "
                                          "price of %s reveals c = %s."
                         % (num(c["P"]), num(gs.cournot_cost(v["a"], c["P"])))))
        return table(rows)


# ======================================================================
# Lab 4: linear best responses
# ======================================================================

class SlopeLab(Lab):
    TITLE = "Lab 4 &middot; Strategic substitutes and complements"
    INTRO = ("Payoffs v<sub>i</sub> = (a + bt<sub>j</sub>)t<sub>i</sub> &minus; "
             "t<sub>i</sub>&sup2;, so the first-order condition gives the best response "
             "t<sub>i</sub> = (a + bt<sub>j</sub>)/2, and the second derivative, &minus;2, says it "
             "is a maximum. b &lt; 0: strategic substitutes, best responses slope down. b &gt; 0: "
             "complements, they slope up. Cournot is b = &minus;1 with a = demand intercept "
             "minus cost.")
    SLIDERS = [
        ("a", 1.0, 100.0, 1.0, 10.0, ".0f"),
        ("b", -1.8, 1.8, 0.1, -1.0, ".1f"),
    ]
    FIGSIZE = (6.0, 4.8)
    PRESETS = [
        dict(label="A12.3 Game A: flatmates", kind="problem", values=dict(a=10.0, b=-1.0)),
        dict(label="A12.3 Game B: managers, a = 6", kind="problem", values=dict(a=6.0, b=1.0)),
        dict(label="Notes p. 8 API Cournot", kind="notes", values=dict(a=90.0, b=-1.0)),
        dict(label="Notes p. 8 memory lines", kind="notes", values=dict(a=2.0, b=-0.5)),
        dict(label="Strong complements", kind="extra", values=dict(a=6.0, b=1.6)),
    ]

    def relabel(self):
        self.w["a"].description = "a"
        self.w["b"].description = "b: slope × 2"

    def compute(self):
        v = self.values()
        return dict(v=v, t=gs.linear_equilibrium(v["a"], v["b"]))

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v, t = st["v"], st["t"]
        top = self.stick("t", max(t, v["a"] / 2) * 2.2)
        x = np.linspace(0, top, 200)
        ax.plot(x, [gs.linear_br(v["a"], v["b"], z) for z in x], color=LINE, lw=2, label="BR$_i$")
        ax.plot([gs.linear_br(v["a"], v["b"], z) for z in x], x, color=CURVE, lw=2, label="BR$_j$")
        ax.plot([t], [t], "o", color=GREEN, ms=8, zorder=6)
        ax.set_xlim(0, top)
        ax.set_ylim(0, top)
        ax.set_xlabel("t$_j$", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("t$_i$", color=INK, fontsize=9, loc="top")
        legend(ax)
        fig.tight_layout()

    def describe(self, st):
        v, t = st["v"], st["t"]
        kind = ("strategic substitutes: the more the other does, the less you want to"
                if v["b"] < 0 else "strategic complements: the more the other does, the more "
                                   "you want to" if v["b"] > 0 else "independent choices")
        return table([
            ("Best response", "t<sub>i</sub> = (%s %s %s t<sub>j</sub>)/2: %s."
             % (num(v["a"]), "+" if v["b"] >= 0 else "&minus;", num(abs(v["b"])), kind)),
            ("Equilibrium", "t* = a/(2 &minus; b) = %s for both." % num(t, 3)),
            ("Unique", "Each best response is a straight line with slope %s, less than 1 in size, "
                       "so the two lines cross exactly once. In a coordination game the best "
                       "response jumps between strategies, and can meet the other's in several "
                       "places." % num(v["b"] / 2)),
        ])


matrix = MatrixLab()
iesds = IESDSLab()
duopoly = DuopolyLab()
slopes = SlopeLab()
