"""
games.py - the maths of sessions 12 and 13: static games, dynamic games and
credibility.

Pure numbers, like the other session modules. Nothing here knows about widgets.

    Matrix       a finite two-player game in normal form: best responses,
                 pure Nash equilibria, iterated elimination of strictly
                 dominated strategies (IESDS), and the mixed equilibrium of a
                 2x2 game from the two indifference conditions
    duopoly      linear demand P = a - Q: Cournot, Bertrand and Stackelberg,
                 and the linear best response t_i = (a + b t_j)/2 of the
                 continuous games
    Tree         a finite game of perfect information: backward induction,
                 the subgame-perfect profile and the path of play
    deviation    the one-stage deviation check in a two-stage game

Payoffs are written the way the notes write them: (player 1, player 2), row
player first.
"""

from fractions import Fraction


# ================================================================= matrix ===

class Matrix:
    """A two-player game. payoffs[i][j] = (u1, u2) for row i and column j."""

    def __init__(self, rows, cols, payoffs):
        self.rows, self.cols = list(rows), list(cols)
        self.u = [[tuple(cell) for cell in row] for row in payoffs]

    def cell(self, i, j):
        return self.u[i][j]

    # -- best responses ---------------------------------------------------------
    def row_best(self, j, rows=None):
        # The row player's best responses to column j (all ties).
        rows = range(len(self.rows)) if rows is None else rows
        top = max(self.u[i][j][0] for i in rows)
        return [i for i in rows if self.u[i][j][0] == top]

    def col_best(self, i, cols=None):
        cols = range(len(self.cols)) if cols is None else cols
        top = max(self.u[i][j][1] for j in cols)
        return [j for j in cols if self.u[i][j][1] == top]

    def pure_nash(self):
        # Cells where each strategy is a best response to the other.
        return [(i, j) for i in range(len(self.rows)) for j in range(len(self.cols))
                if i in self.row_best(j) and j in self.col_best(i)]

    # -- dominance --------------------------------------------------------------
    def row_dominated(self, i, rows, cols):
        # The first row that strictly beats row i against every live column.
        for k in rows:
            if k != i and all(self.u[k][j][0] > self.u[i][j][0] for j in cols):
                return k
        return None

    def col_dominated(self, j, rows, cols):
        for k in cols:
            if k != j and all(self.u[i][k][1] > self.u[i][j][1] for i in rows):
                return k
        return None

    def dominant_row(self):
        # A strictly dominant strategy for the row player, or None.
        n = len(self.rows)
        for i in range(n):
            if all(self.row_dominated(k, [i, k], range(len(self.cols))) == i
                   for k in range(n) if k != i):
                return i
        return None

    def dominant_col(self):
        n = len(self.cols)
        for j in range(n):
            if all(self.col_dominated(k, range(len(self.rows)), [j, k]) == j
                   for k in range(n) if k != j):
                return j
        return None

    def iesds(self):
        """Iterated elimination of strictly dominated strategies.

        Each round deletes every strategy, of either player, that another live
        strategy strictly beats against everything still live. Returns the
        rounds, each a list of ("row" or "col", index, dominated-by index), and
        the surviving rows and columns.
        """
        rows, cols = list(range(len(self.rows))), list(range(len(self.cols)))
        rounds = []
        while True:
            gone = []
            for i in rows:
                k = self.row_dominated(i, rows, cols)
                if k is not None:
                    gone.append(("row", i, k))
            for j in cols:
                k = self.col_dominated(j, rows, cols)
                if k is not None:
                    gone.append(("col", j, k))
            if not gone:
                return rounds, rows, cols
            rounds.append(gone)
            rows = [i for i in rows if ("row", i) not in [(s, x) for s, x, _ in gone]]
            cols = [j for j in cols if ("col", j) not in [(s, x) for s, x, _ in gone]]

    # -- mixing (2x2) -----------------------------------------------------------
    def mixed(self):
        """The mixed equilibrium of a 2x2 game, from the indifference conditions.

        p is the row player's probability on row 0, q the column player's on
        column 0. p comes from making the column player indifferent, and q
        from making the row player indifferent: each player's mix is pinned
        down by the opponent's payoffs. Returns (p, q) as Fractions, or None if
        there is no fully mixed equilibrium.
        """
        (a, b), (c, d) = [[Fraction(self.u[i][j][1]) for j in (0, 1)] for i in (0, 1)]
        # Column player: p a + (1 - p) c = p b + (1 - p) d.
        den = (a - b) - (c - d)
        (A, B), (C, D) = [[Fraction(self.u[i][j][0]) for j in (0, 1)] for i in (0, 1)]
        # Row player: q A + (1 - q) B = q C + (1 - q) D.
        den2 = (A - C) - (B - D)
        if den == 0 or den2 == 0:
            return None
        p = (d - c) / den
        q = (D - B) / den2
        if not (0 < p < 1 and 0 < q < 1):
            return None
        return p, q

    def expected(self, p, q):
        # Each player's expected payoff when row 0 has probability p, column 0 q.
        probs = [[p * q, p * (1 - q)], [(1 - p) * q, (1 - p) * (1 - q)]]
        return tuple(sum(probs[i][j] * self.u[i][j][k] for i in (0, 1) for j in (0, 1))
                     for k in (0, 1))

    def row_lines(self, q):
        # The row player's expected payoff from each pure row, against q.
        return tuple(q * self.u[i][0][0] + (1 - q) * self.u[i][1][0] for i in (0, 1))

    def col_lines(self, p):
        return tuple(p * self.u[0][j][1] + (1 - p) * self.u[1][j][1] for j in (0, 1))


# ================================================================ duopoly ===

def cournot_br(a, c, q_other):
    # max (a - q - q_j - c) q  ->  q = (a - c - q_j)/2, never negative.
    return max((a - c - q_other) / 2.0, 0.0)


def cournot(a, c1, c2=None):
    # Both best responses at once: q_i = (a - 2c_i + c_j)/3.
    c2 = c1 if c2 is None else c2
    q1 = max((a - 2 * c1 + c2) / 3.0, 0.0)
    q2 = cournot_br(a, c2, q1)
    q1 = cournot_br(a, c1, q2)
    P = a - q1 - q2
    return dict(q1=q1, q2=q2, Q=q1 + q2, P=P, pi1=(P - c1) * q1, pi2=(P - c2) * q2)


def cournot_cost(a, P):
    # The symmetric Cournot price is (a + 2c)/3; read c back off a price.
    return (3 * P - a) / 2.0


def bertrand(a, c1, c2=None):
    # Identical goods, posted prices. Equal costs: p = c and zero profits. With
    # unequal costs the cheaper firm prices at the rival's cost (or its own
    # monopoly price, if lower) and serves everyone.
    c2 = c1 if c2 is None else c2
    if c1 == c2:
        P = c1
        Q = max(a - P, 0.0)
        return dict(P=P, Q=Q, q1=Q / 2, q2=Q / 2, pi1=0.0, pi2=0.0)
    low, high = (c1, c2) if c1 < c2 else (c2, c1)
    P = min(high, (a + low) / 2.0)
    Q = max(a - P, 0.0)
    q1, q2 = (Q, 0.0) if c1 < c2 else (0.0, Q)
    return dict(P=P, Q=Q, q1=q1, q2=q2, pi1=(P - c1) * q1, pi2=(P - c2) * q2)


def stackelberg(a, c1, c2=None):
    # Firm 1 leads: it substitutes q2 = (a - c2 - q1)/2 into its own profit,
    # which collapses to ((a - 2c1 + c2) - q1) q1 / 2, so q1 = (a - 2c1 + c2)/2.
    c2 = c1 if c2 is None else c2
    q1 = max((a - 2 * c1 + c2) / 2.0, 0.0)
    q2 = cournot_br(a, c2, q1)
    P = a - q1 - q2
    return dict(q1=q1, q2=q2, Q=q1 + q2, P=P, pi1=(P - c1) * q1, pi2=(P - c2) * q2)


def leader_cost(a, q1):
    # Equal costs: the leader's rule q1 = (a - c)/2, run backward.
    return a - 2.0 * q1


def monopoly(a, c):
    Q = max((a - c) / 2.0, 0.0)
    return dict(Q=Q, P=a - Q, pi=(a - Q - c) * Q)


def linear_br(a, b, t_other):
    # v_i = (a + b t_j) t_i - t_i^2  ->  t_i = (a + b t_j)/2.
    return max((a + b * t_other) / 2.0, 0.0)


def linear_equilibrium(a, b):
    # The symmetric crossing t = (a + b t)/2, unique when |b| < 2.
    return a / (2.0 - b)


# =================================================================== tree ===

class Leaf:
    def __init__(self, *payoffs):
        self.payoffs = tuple(payoffs)


class Node:
    """A decision node: who moves, and one child per action, in order."""

    def __init__(self, player, name, children):
        self.player = player
        self.name = name
        self.children = list(children)          # (action, Node or Leaf)


def solve(node):
    """Backward induction. Returns the payoffs at node and a dict of the
    action chosen at every decision node below it, reached or not: the
    subgame-perfect profile, not just the path. Ties go to the first action
    listed."""
    if isinstance(node, Leaf):
        return node.payoffs, {}
    plan, best, value = {}, None, None
    for action, child in node.children:
        v, sub = solve(child)
        plan.update(sub)
        if value is None or v[node.player] > value[node.player]:
            best, value = action, v
    plan[node.name] = best
    return value, plan


def path(node, plan):
    # The walk from the root under a plan: a list of actions, and the payoffs.
    steps = []
    while not isinstance(node, Leaf):
        action = plan[node.name]
        steps.append(action)
        node = dict(node.children)[action]
    return steps, node.payoffs


def decision_nodes(node):
    if isinstance(node, Leaf):
        return []
    return [node] + [n for _, c in node.children for n in decision_nodes(c)]


def strategies(node, player):
    # Pure strategies under perfect information: the product of the action
    # counts at the player's nodes, reached or not.
    count = 1
    for n in decision_nodes(node):
        if n.player == player:
            count *= len(n.children)
    return count


# ============================================================== deviation ===

def deviation_threshold(now_hold, later_hold, now_dev, later_dev):
    # Hold survives the one-stage check when now_hold + d later_hold >=
    # now_dev + d later_dev, that is when d >= (now_dev - now_hold)/(later_hold
    # - later_dev). None if the future does not punish the deviation at all.
    gap = later_hold - later_dev
    if gap <= 0:
        return None
    return (now_dev - now_hold) / gap


def continuation_for(delta, now_hold, later_hold, now_dev):
    # The punishment value z that leaves a player exactly indifferent at delta.
    return (now_hold + delta * later_hold - now_dev) / delta


# ============================================================= self-check ===

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-9: "ok " if abs(got - want) < tol else "FAIL"

    print("session 12")
    ad = Matrix("AN", "AN", [[(-2, -2), (3, -3)], [(-3, 3), (0, 0)]])
    print("  advertising: dominant %s, %s; Nash %s" % (ad.dominant_row(), ad.dominant_col(),
                                                     ad.pure_nash()))
    build = Matrix("IN", "IN", [[(2, 2), (-1, 0)], [(0, -1), (1, 1)]])
    print("  build-out: Nash %s, mixed %s" % (build.pure_nash(), build.mixed()))
    g = Matrix(["A1", "A2", "A3"], ["B1", "B2", "B3"],
               [[(2, 3), (1, 4), (3, 2)], [(4, 1), (2, 2), (2, 0)], [(3, 3), (0, 5), (2, 1)]])
    print("  3x3: IESDS %s" % (g.iesds(),))
    mem = Matrix(range(4), range(4), [[((4 - i - j) * i - i * i, (4 - i - j) * j - j * j)
                                       for j in range(4)] for i in range(4)])
    print("  memory grid: rows are the rival, columns you; IESDS %s" % (mem.iesds()[1:],))
    talent = Matrix("CT", "CT", [[(3, 3), (1, 4)], [(4, 1), (2, 2)]])
    print("  talent war: Nash %s" % talent.pure_nash())
    c = cournot(100, 10)
    print("  %s API Cournot %s; Bertrand %s" % (ok(c["pi1"], 900), c, bertrand(100, 10)))
    c = cournot(27, 3)
    print("  %s Try it %s; cost at P = 15: %s; Bertrand %s" % (
        ok(c["pi1"], 64), c, cournot_cost(27, 15), bertrand(27, 3)))
    kick = Matrix("LR", "LR", [[(-1, 1), (1, -1)], [(1, -1), (-1, 1)]])
    print("  penalty: Nash %s, mixed %s" % (kick.pure_nash(), kick.mixed()))
    # Release game, Anthropic on the rows, OpenAI on the columns, M then S.
    rel = Matrix("MS", "MS", [[(0, 3), (2, 0)], [(3, 0), (0, 1)]])
    print("  %s release: Nash %s, mixed (p Anthropic March, q OpenAI March) %s" % (
        ok(float(rel.mixed()[1]), 0.4), rel.pure_nash(), rel.mixed()))
    print("  %s power duopoly %s" % (ok(cournot(90, 30)["q1"], 20), cournot(90, 30)))
    rq2 = Matrix("TMB", "LCR", [[(3, 5), (1, 4), (2, 2)], [(4, 2), (2, 3), (1, 1)],
                                [(2, 1), (0, 2), (3, 0)]])
    print("  review Q2: IESDS %s" % (rq2.iesds(),))
    rq3 = Matrix("AB", "AB", [[(5, 3), (1, 1)], [(0, 0), (3, 5)]])
    print("  review Q3: Nash %s, dominant %s %s" % (rq3.pure_nash(), rq3.dominant_row(),
                                                  rq3.dominant_col()))
    print("  %s review Q4 ferry %s; Q5 %s" % (ok(cournot(60, 6)["pi1"], 324), cournot(60, 6),
                                            bertrand(60, 6)))
    st = Matrix("LR", "LR", [[(0, 1), (2, 0)], [(1, 0), (0, 1)]])
    print("  review Q6 striker: Nash %s, mixed %s" % (st.pure_nash(), st.mixed()))
    stag = Matrix("SH", "SH", [[(3, 3), (0, 1)], [(1, 0), (1, 1)]])
    print("  A12 W2 stag hunt: Nash %s, mixed %s" % (stag.pure_nash(), stag.mixed()))
    kl = Matrix("XYA", "XYA", [[(6, 6), (2, 2), (3, 1)], [(2, 2), (4, 4), (3, 1)],
                               [(1, 3), (1, 3), (2, 2)]])
    print("  A12.1: IESDS %s" % (kl.iesds(),))
    red = Matrix("XY", "XY", [[(6, 6), (2, 2)], [(2, 2), (4, 4)]])
    p, q = red.mixed()
    print("  %s A12.1 reduced: Nash %s, mixed %s, expected %s, P(differ) %s" % (
        ok(float(p), 1 / 3), red.pure_nash(), (p, q), red.expected(p, q),
        p * (1 - q) + (1 - p) * q))
    berg = Matrix(["Evade", "Comply"], ["Audit", "Not"], [[(-20, 10), (30, -30)], [(0, -5), (0, 0)]])
    berg2 = Matrix(["Evade", "Comply"], ["Audit", "Not"], [[(-40, 10), (30, -30)], [(0, -5), (0, 0)]])
    print("  A12.2: Nash %s; mixed (p evade, q audit) %s; doubled %s" % (
        berg.pure_nash(), berg.mixed(), berg2.mixed()))
    print("  %s A12.3: flatmates %s, managers e = a for a = 6: %s" % (
        ok(linear_equilibrium(10, -1), 10 / 3), linear_equilibrium(10, -1), linear_equilibrium(6, 1)))

    print("\nsession 13")
    entry = Node(0, "x0", [("Out", Leaf(0, 10)),
                           ("In", Node(1, "x1", [("Fight", Leaf(-1, 1)),
                                                 ("Accommodate", Leaf(2, 4))]))])
    print("  entry: SPE %s, path %s" % (solve(entry)[1], path(entry, solve(entry)[1])))
    std = Node(0, "x0", [("O", Node(1, "x1", [("o", Leaf(2, 1)), ("f", Leaf(0, 0))])),
                         ("F", Node(1, "x2", [("o", Leaf(0, 0)), ("f", Leaf(1, 2))]))])
    print("  standards: SPE %s; player 2 has %s strategies" % (solve(std)[1], strategies(std, 1)))
    s = stackelberg(100, 10)
    print("  %s Stackelberg %s; announced 45 -> BR1(22.5) = %s" % (
        ok(s["pi1"], 1012.5), s, cournot_br(100, 10, 22.5)))
    s = stackelberg(104, 20)
    print("  %s TSMC %s; cost revealed by 36: %s; Cournot %s" % (
        ok(s["pi1"], 882), s, leader_cost(104, 36), cournot(104, 20)))
    work = Node(0, "root", [("Out", Leaf(0, 12)),
                            ("In", Node(1, "inc", [("Share", Leaf(4, 6)),
                                                   ("Fight", Node(0, "after", [("Exit", Leaf(-1, 7)),
                                                                               ("Stay", Leaf(-3, 3))]))]))])
    print("  worksheet tree: SPE %s, path %s" % (solve(work)[1], path(work, solve(work)[1])))
    print("  %s server: Stackelberg %s; Cournot %s" % (ok(stackelberg(60, 12)["q1"], 24),
                                                       stackelberg(60, 12), cournot(60, 12)))
    city = Node(0, "c0", [("Wait", Leaf(2, 6)),
                          ("Expand", Node(1, "b", [("Concede", Leaf(5, 3)),
                                                   ("Match", Node(0, "c1", [("Hold", Leaf(1, 2)),
                                                                            ("Discount", Leaf(0, 1))]))]))])
    print("  review Q2 CityBrew: SPE %s, path %s" % (solve(city)[1], path(city, solve(city)[1])))
    print("  %s review Q4 salmon: %s; Cournot %s" % (ok(stackelberg(36, 0)["pi1"], 162),
                                                     stackelberg(36, 0), cournot(36, 0)))
    print("  %s Try it: delta* %s; z at 1/2: %s; grab 7: %s" % (
        ok(deviation_threshold(3, 6, 5, 3), 2 / 3), deviation_threshold(3, 6, 5, 3),
        continuation_for(0.5, 3, 6, 5), deviation_threshold(3, 6, 7, 3)))
    print("  %s review Q5: delta* %s" % (ok(deviation_threshold(-1, 0, 2, -4), 0.75),
                                         deviation_threshold(-1, 0, 2, -4)))
    cent = Node(0, "1a", [("N", Leaf(1, 1)), ("C", Node(1, "2a", [("n", Leaf(0, 3)), ("c", Node(
        0, "1b", [("N", Leaf(2, 2)), ("C", Node(1, "2b", [("n", Leaf(1, 4)), ("c", Leaf(3, 3))]))]))]))])
    print("  centipede: %s" % (path(cent, solve(cent)[1]),))
    print("  %s A13.1: %s; Cournot %s" % (ok(stackelberg(24, 0)["pi1"], 72), stackelberg(24, 0),
                                          cournot(24, 0)))
    a13 = Node(0, "E", [("Out", Leaf(0, 10)),
                        ("Enter", Node(1, "I", [("Fight", Leaf(-2, 1)), ("Accommodate", Leaf(3, 4))]))])
    print("  A13.2: SPE %s, path %s" % (solve(a13)[1], path(a13, solve(a13)[1])))
