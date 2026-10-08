"""
ricardo.py - the maths of session 9: comparative advantage, the Ricardian model.

Pure numbers, like the other session modules. Nothing here knows about widgets.

    Ricardo    two countries, two goods, one factor: frontiers, autarky
               prices, who specializes in what, wages, unit costs, the
               world relative supply staircase and the price that clears
    tariff     the small-country tariff diagram with linear demand and
               supply (context: not examinable)

Notation follows the notes. Good x is on the horizontal axis and good y is the
numeraire, so p = p_x/p_y is the relative price of x. a_x and a_y are units of
labor per unit of output and E is the labor force; Foreign is the starred
country ("f" here).
"""

import math

HOME, FOREIGN = "home", "foreign"


class Ricardo:
    def __init__(self, ax, ay, E, ax_f, ay_f, E_f):
        self.a = {HOME: (float(ax), float(ay)), FOREIGN: (float(ax_f), float(ay_f))}
        self.E = {HOME: float(E), FOREIGN: float(E_f)}

    # -- one country ------------------------------------------------------------
    def frontier(self, c):
        # Intercepts E/a_x and E/a_y, and the absolute slope a_x/a_y: the y given
        # up for one more x.
        ax, ay = self.a[c]
        return self.E[c] / ax, self.E[c] / ay, ax / ay

    def autarky(self, c):
        # Both goods are made, so the two wages are equal: p = a_x/a_y.
        return self.frontier(c)[2]

    def labor(self, c, x, y):
        # Workers needed to make the bundle (x, y) at home.
        ax, ay = self.a[c]
        return ax * x + ay * y

    def wage(self, c, p):
        # In units of y: a worker earns the better of p/a_x and 1/a_y.
        ax, ay = self.a[c]
        return max(p / ax, 1 / ay)

    def costs(self, c, p):
        # Unit costs w a_x and w a_y, in units of y.
        w = self.wage(c, p)
        return w * self.a[c][0], w * self.a[c][1]

    def output(self, c, p, tol=1e-9):
        # A straight frontier gives a corner: all x above the autarky price, all
        # y below it. At the autarky price any mix earns the same: None.
        X, Y, pa = self.frontier(c)
        if abs(p - pa) < tol:
            return None
        return (X, 0.0) if p > pa else (0.0, Y)

    def income(self, c, p):
        return self.wage(c, p) * self.E[c]

    def demand(self, c, p, s):
        # Cobb-Douglas, u = x^s y^(1-s): the share s of income goes to x.
        m = self.income(c, p)
        return s * m / p, (1 - s) * m

    # -- the two together -------------------------------------------------------
    def absolute(self, good):
        # Who needs less labor per unit of good 0 (x) or 1 (y); None for a tie.
        h, f = self.a[HOME][good], self.a[FOREIGN][good]
        return None if h == f else (HOME if h < f else FOREIGN)

    def exporter_x(self):
        # Comparative advantage in x: the lower autarky price. None if equal.
        h, f = self.autarky(HOME), self.autarky(FOREIGN)
        return None if abs(h - f) < 1e-12 else (HOME if h < f else FOREIGN)

    def other(self, c):
        return FOREIGN if c == HOME else HOME

    def range(self):
        # The bargaining range: both want to trade only between the autarky prices.
        h, f = self.autarky(HOME), self.autarky(FOREIGN)
        return min(h, f), max(h, f)

    def corner(self):
        # Relative supply on the vertical segment: the x-exporter's whole
        # frontier in x over the other country's in y.
        c = self.exporter_x() or HOME
        return self.frontier(c)[0] / self.frontier(self.other(c))[1]

    def clearing(self, s, s_f=None):
        # The price that clears the world market for x when Home spends the
        # share s on x and Foreign s_f (the same share if not given). With both
        # fully specialized, the x-exporter makes X and the other country Y, and
        # demand equals supply where p = s_o Y / ((1 - s_c) X). If that price is
        # outside the range, demand cuts a flat step instead.
        s_f = s if s_f is None else s_f
        c = self.exporter_x() or HOME
        s_c, s_o = (s, s_f) if c == HOME else (s_f, s)
        X, Y = self.frontier(c)[0], self.frontier(self.other(c))[1]
        lo, hi = self.range()
        return min(max(s_o * Y / ((1 - s_c) * X), lo), hi)

    def gaps(self):
        # Foreign undersells Home in a good when a*/a < w/w*.
        return (self.a[FOREIGN][0] / self.a[HOME][0], self.a[FOREIGN][1] / self.a[HOME][1])

    def wage_ratio(self, p):
        return self.wage(HOME, p) / self.wage(FOREIGN, p)


# ------------------------------------------------------- tariff (context) ---

def tariff(pw, t, A=100.0, c=20.0):
    """A small country with demand D = A - p and supply S = p - c.

    The four areas between the price lines p_w and p_w + t: a is the producers'
    gain, c the revenue, b and d the two triangles nobody gets. A tariff that
    lifts the price past the autarky price (A + c)/2 stops all imports, and the
    price stays there.
    """
    p = min(pw + t, max((A + c) / 2, pw))
    t = p - pw
    S0, D0, S1, D1 = pw - c, A - pw, p - c, A - p
    out = dict(p=p, S0=S0, D0=D0, S1=S1, D1=D1, M0=D0 - S0, M1=D1 - S1)
    out["a"] = t * (S0 + S1) / 2
    out["b"] = t * (S1 - S0) / 2
    out["c"] = t * (D1 - S1)
    out["d"] = t * (D0 - D1) / 2
    out["loss"] = out["b"] + out["d"]
    return out


def tariff_from_imports(pw, imports, A=100.0, c=20.0):
    # Imports are D - S = A + c - 2p: read the domestic price off the quantity.
    return (A + c - imports) / 2 - pw


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-9: "ok " if abs(got - want) < tol else "FAIL"

    print("notes: Home (1, 2, 100), Foreign (6, 3, 180)")
    r = Ricardo(1, 2, 100, 6, 3, 180)
    print("  %s frontiers %s and %s; range %s; x exported by %s" % (
        ok(r.autarky(HOME) + r.autarky(FOREIGN), 2.5), r.frontier(HOME), r.frontier(FOREIGN),
        r.range(), r.exporter_x()))
    print("  %s autarky A = %s, A* = %s" % (ok(r.demand(HOME, .5, .6)[0], 60),
                                           r.demand(HOME, .5, .6), r.demand(FOREIGN, 2, .6)))
    print("  %s p = 1: output %s, %s; C = %s, C* = %s" % (
        ok(r.demand(FOREIGN, 1, .6)[0], 36), r.output(HOME, 1), r.output(FOREIGN, 1),
        r.demand(HOME, 1, .6), r.demand(FOREIGN, 1, .6)))
    print("  %s corner %s; clearing price %s" % (ok(r.clearing(.6), .9), r.corner(), r.clearing(.6)))
    big = Ricardo(1, 2, 10000, 6, 3, 180)
    print("  %s a very large Home: clearing price %s, its own autarky price" % (
        ok(big.clearing(.6), .5), big.clearing(.6)))
    print("  %s wages %s, %s; costs %s, %s; gaps %s" % (
        ok(r.wage_ratio(1), 3), r.wage(HOME, 1), r.wage(FOREIGN, 1), r.costs(HOME, 1),
        r.costs(FOREIGN, 1), r.gaps()))
    print("  %s Try it, p = 3/2: wages %s, %s; cutoff %s; 40 cloth buys %s wine" % (
        ok(r.wage_ratio(1.5), 4.5), r.wage(HOME, 1.5), r.wage(FOREIGN, 1.5), r.wage_ratio(1.5),
        40 * 1.5))

    print("\nworksheet: Home (4, 5, 20), Foreign (1, 2, 10)")
    r = Ricardo(4, 5, 20, 1, 2, 10)
    p = 2 / 3
    print("  %s frontiers %s and %s; x exported by %s" % (
        ok(r.autarky(HOME), .8), r.frontier(HOME), r.frontier(FOREIGN), r.exporter_x()))
    print("  %s p = 2/3: wages %s, %s; costs %s, %s" % (
        ok(r.wage(HOME, p), .2), r.wage(HOME, p), r.wage(FOREIGN, p), r.costs(HOME, p),
        r.costs(FOREIGN, p)))

    print("\nreview Q2-5: Vinland (1, 3, 300), Estland (6, 4, 240)")
    r = Ricardo(1, 3, 300, 6, 4, 240)
    print("  %s frontiers %s and %s; corner %s" % (
        ok(r.corner(), 5), r.frontier(HOME), r.frontier(FOREIGN), r.corner()))
    print("  %s labor for (260, 40) and (40, 20): %s, %s; with those tastes the market clears at %s" % (
        ok(r.clearing(13 / 15, 2 / 3), 1), r.labor(HOME, 260, 40), r.labor(FOREIGN, 40, 20),
        r.clearing(13 / 15, 2 / 3)))
    print("  %s p = 1: wages %s, %s; costs %s, %s; gaps %s" % (
        ok(r.wage_ratio(1), 4), r.wage(HOME, 1), r.wage(FOREIGN, 1), r.costs(HOME, 1),
        r.costs(FOREIGN, 1), r.gaps()))

    print("\nA9.1: Norway (2, 4, 1200), Portugal (12, 6, 1200)")
    r = Ricardo(2, 4, 1200, 12, 6, 1200)
    print("  %s frontiers %s and %s; range %s" % (
        ok(r.frontier(HOME)[0] + r.frontier(FOREIGN)[1], 800), r.frontier(HOME),
        r.frontier(FOREIGN), r.range()))
    print("  %s labor for (500, 100) and (100, 100): %s, %s" % (
        ok(r.labor(HOME, 500, 100) + r.labor(FOREIGN, 100, 100), 3200), r.labor(HOME, 500, 100),
        r.labor(FOREIGN, 100, 100)))
    print("  %s p = 1: wages %s, %s; costs %s, %s; ratio %s, gaps %s" % (
        ok(r.wage_ratio(1), 3), r.wage(HOME, 1), r.wage(FOREIGN, 1), r.costs(HOME, 1),
        r.costs(FOREIGN, 1), r.wage_ratio(1), r.gaps()))

    print("\ntariff Try it: D = 100 - p, S = p - 20, world price 40")
    t = tariff_from_imports(40, 20)
    T, half = tariff(40, t), tariff(40, t / 2)
    print("  %s tariff %s, price %s; a, b, c, d = %s, %s, %s, %s; loss %s" % (
        ok(T["loss"], 100), t, T["p"], T["a"], T["b"], T["c"], T["d"], T["loss"]))
    print("  %s halved: loss %s, revenue %s" % (ok(half["loss"] + half["c"], 175), half["loss"],
                                               half["c"]))
    stop = tariff(40, 30)
    print("  %s a tariff of 30 is prohibitive: price %s, imports %s, revenue %s" % (
        ok(stop["p"], 60), stop["p"], stop["M1"], stop["c"]))
