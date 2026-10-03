"""
equilibrium.py - the maths of session 6: a two-person exchange economy.

Pure numbers, like consumer_theory.py and uncertainty.py. Nothing here knows
about widgets.

Two agents with Cobb-Douglas preferences, the only kind the session 6 notes
and problems use:

    u_A = x^a y^(1-a),   u_B = x^b y^(1-b)

so a and b are the shares of income each spends on good x. Endowments
wA = (x, y) and wB = (x, y); the box is X = wA_x + wB_x wide and
Y = wA_y + wB_y tall. Good y is the numeraire (p_y = 1) and p = p_x/p_y.

Allocations are written from A's corner: a point (xA, yA) in the box gives
B the bundle (X - xA, Y - yA).
"""

import math


class Economy:
    def __init__(self, a, b, wA, wB):
        self.a, self.b = float(a), float(b)
        self.wA = (float(wA[0]), float(wA[1]))
        self.wB = (float(wB[0]), float(wB[1]))
        self.X = self.wA[0] + self.wB[0]
        self.Y = self.wA[1] + self.wB[1]

    # -- utility and MRS -------------------------------------------------------
    def uA(self, x, y):
        return max(x, 0.0) ** self.a * max(y, 0.0) ** (1 - self.a)

    def uB(self, x, y):
        return max(x, 0.0) ** self.b * max(y, 0.0) ** (1 - self.b)

    def mrsA(self, x, y):
        # (du/dx)/(du/dy) = (a/(1 - a)) y/x
        return self.a / (1 - self.a) * y / x if x > 0 else math.inf

    def mrsB(self, x, y):
        return self.b / (1 - self.b) * y / x if x > 0 else math.inf

    def b_bundle(self, xA, yA):
        return self.X - xA, self.Y - yA

    # -- the market -------------------------------------------------------------
    def incomes(self, p):
        # Income is the value of what you own, at the prices being solved for.
        return p * self.wA[0] + self.wA[1], p * self.wB[0] + self.wB[1]

    def demands(self, p):
        # Cobb-Douglas spends fixed shares: x = share * m / p_x, y = (1 - share) * m.
        mA, mB = self.incomes(p)
        return ((self.a * mA / p, (1 - self.a) * mA),
                (self.b * mB / p, (1 - self.b) * mB))

    def excess(self, p):
        # Aggregate excess demand (z_x, z_y): what everyone wants minus what exists.
        (xA, yA), (xB, yB) = self.demands(p)
        return xA + xB - self.X, yA + yB - self.Y

    def walras(self, p):
        # p z_x + z_y: zero at every price, because every budget balances.
        zx, zy = self.excess(p)
        return p * zx + zy

    def price(self):
        # Clear market x and solve: (a wA_y + b wB_y)/p = (1 - a) wA_x + (1 - b) wB_x.
        top = self.a * self.wA[1] + self.b * self.wB[1]
        bottom = (1 - self.a) * self.wA[0] + (1 - self.b) * self.wB[0]
        return top / bottom if bottom > 0 else math.inf

    def equilibrium(self):
        p = self.price()
        (xA, yA), (xB, yB) = self.demands(p)
        mA, mB = self.incomes(p)
        return dict(p=p, mA=mA, mB=mB, A=(xA, yA), B=(xB, yB),
                    tradeA=(xA - self.wA[0], yA - self.wA[1]))

    # -- efficiency -------------------------------------------------------------
    def contract(self, xA):
        # MRS_A = MRS_B with B's bundle (X - xA, Y - yA), solved for yA:
        # kA yA (X - xA) = kB xA (Y - yA)  ->  yA = kB Y xA / (kA X + (kB - kA) xA)
        kA, kB = self.a / (1 - self.a), self.b / (1 - self.b)
        den = kA * self.X + (kB - kA) * xA
        return kB * self.Y * xA / den if den > 0 else self.Y

    def efficient(self, xA, yA, tol=1e-6):
        xB, yB = self.b_bundle(xA, yA)
        if min(xA, yA, xB, yB) <= 0:
            return None                       # on the edge of the box: not a tangency
        return abs(self.mrsA(xA, yA) - self.mrsB(xB, yB)) < tol * max(1.0, self.mrsA(xA, yA))

    def in_lens(self, xA, yA, tol=1e-9):
        # Weakly better than the endowment for both: individually rational.
        xB, yB = self.b_bundle(xA, yA)
        return (self.uA(xA, yA) >= self.uA(*self.wA) - tol and
                self.uB(xB, yB) >= self.uB(*self.wB) - tol)

    def core(self):
        # The stretch of the contract curve both prefer to their endowment.
        # Along the curve uA rises with xA and uB falls, so the core is an
        # interval [lo, hi] in xA, found by bisection at each end.
        uA0, uB0 = self.uA(*self.wA), self.uB(*self.wB)
        fa = lambda x: self.uA(x, self.contract(x)) - uA0
        fb = lambda x: self.uB(*self.b_bundle(x, self.contract(x))) - uB0

        def root(f, lo, hi):
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if (f(mid) > 0) == (f(hi) > 0):
                    hi = mid
                else:
                    lo = mid
            return 0.5 * (lo + hi)

        return root(fa, 0.0, self.X), root(fb, 0.0, self.X)

    def support(self, xA):
        # Second welfare theorem: the efficient point F = (xA, contract(xA)), the
        # price ratio that supports it (the common MRS), and the lump-sum
        # transfer T, in units of y, that A must hand to B so that F is
        # affordable for both. Negative T means B pays A.
        yA = self.contract(xA)
        p = self.mrsA(xA, yA)
        T = (p * self.wA[0] + self.wA[1]) - (p * xA + yA)
        return dict(F=(xA, yA), p=p, T=T)

    # -- drawing helpers --------------------------------------------------------
    def icA(self, level, x):
        # A's indifference curve: y = (level / x^a)^(1/(1 - a)).
        return (level / x ** self.a) ** (1 / (1 - self.a)) if x > 0 else math.inf

    def icB(self, level, xA):
        # B's curve in A's coordinates: B holds X - xA, so yA = Y - yB.
        xB = self.X - xA
        if xB <= 0:
            return -math.inf
        return self.Y - (level / xB ** self.b) ** (1 / (1 - self.b))


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-6: "ok " if abs(got - want) < tol else "FAIL"
    r = lambda t: tuple(round(v, 4) + 0 for v in t)

    print("s06 notes worked economy: a=3/4, b=1/2, wA=(8,8), wB=(4,4)")
    e = Economy(0.75, 0.5, (8, 8), (4, 4))
    q = e.equilibrium()
    print("  %s p* = %s, incomes %s, A %s, B %s, A's trade %s" % (
        ok(q["p"], 2), q["p"], (q["mA"], q["mB"]), r(q["A"]), r(q["B"]), r(q["tradeA"])))
    print("  %s value of A's net trade %.3f; recovered a = %.3f" % (
        ok(q["p"] * q["tradeA"][0] + q["tradeA"][1], 0), q["p"] * q["tradeA"][0] + q["tradeA"][1],
        q["p"] * q["A"][0] / q["mA"]))
    print("  %s MRS %s and %s; contract(9) = %s, contract(6) = %s, contract(12) = %s" % (
        ok(e.contract(9), 6), e.mrsA(9, 6), e.mrsB(3, 6), e.contract(9), e.contract(6), e.contract(12)))
    print("  %s z(1) = %s, z(3) = %s, walras(3) = %s" % (
        ok(e.excess(1)[0], 4), r(e.excess(1)), r(e.excess(3)), round(e.walras(3), 9)))
    s = e.support(6)
    lo, hi = e.core()
    print("  %s support F=%s: p = %s, transfer %s; core xA in [%.3f, %.3f]; CE in core %s; F in core %s" % (
        ok(s["T"], 8), r(s["F"]), s["p"], s["T"], lo, hi, e.in_lens(9, 6), e.in_lens(*s["F"])))

    print("\ns06 worksheet: a=3/4, b=1/4, wA=(2,6), wB=(6,2)")
    e = Economy(0.75, 0.25, (2, 6), (6, 2))
    q = e.equilibrium()
    print("  %s p* = %s, incomes %s, A %s, B %s" % (ok(q["p"], 1), q["p"], (q["mA"], q["mB"]),
                                                   r(q["A"]), r(q["B"])))
    print("  %s z(1/2) = %s, z(2) = %s, walras(2) = %s; MRS at omega %s, %s" % (
        ok(e.excess(2)[0], -2.5), r(e.excess(.5)), r(e.excess(2)), e.walras(2),
        e.mrsA(2, 6), round(e.mrsB(6, 2), 4)))

    print("\ns06 review Q1-5: Astrid a=2/3, Birk b=1/2, wA=(3,9), wB=(3,3)")
    e = Economy(2 / 3, 0.5, (3, 9), (3, 3))
    q = e.equilibrium()
    print("  %s box %sx%s, MRS at omega %s, %s; at (4,6): %s, %s, efficient %s" % (
        ok(e.mrsA(4, 6), 3), e.X, e.Y, round(e.mrsA(3, 9), 4), e.mrsB(3, 3),
        round(e.mrsA(4, 6), 4), e.mrsB(2, 6), e.efficient(4, 6)))
    print("  %s p* = %s, incomes %s, A %s, B %s, z(1) = %s" % (
        ok(q["p"], 3), round(q["p"], 4), r((q["mA"], q["mB"])), r(q["A"]), r(q["B"]), r(e.excess(1))))

    print("\nA6.1 identical sqrt, wA=(3,9), wB=(9,3)")
    e = Economy(0.5, 0.5, (3, 9), (9, 3))
    q = e.equilibrium()
    print("  %s p* = %s, A %s, contract(4) = %s (diagonal)" % (ok(q["p"], 1), q["p"], r(q["A"]),
                                                              e.contract(4)))

    print("\nA6.2: a=2/3, b=1/3, wA=(3,9), wB=(9,3)")
    e = Economy(2 / 3, 1 / 3, (3, 9), (9, 3))
    q = e.equilibrium()
    print("  %s p* = %s, incomes %s, A %s, B %s, A's trade %s" % (
        ok(q["p"], 1), round(q["p"], 6), r((q["mA"], q["mB"])), r(q["A"]), r(q["B"]), r(q["tradeA"])))
    print("  %s contract(8) = %s, contract(6) = %s (want 2.4); MRS at (6,6): %s, %s; efficient %s" % (
        ok(e.contract(6), 2.4), round(e.contract(8), 6), round(e.contract(6), 6),
        round(e.mrsA(6, 6), 4), round(e.mrsB(6, 6), 4), e.efficient(6, 6)))
