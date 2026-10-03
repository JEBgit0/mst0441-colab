"""
externality.py - the maths of session 7: the smoke economy.

Pure numbers, like equilibrium.py. Nothing here knows about widgets.

A smokes and B breathes. They share one unit of air: smoke S is measured from
A's end and clean air 1 - S from B's. Each owns some of good 1 (wA, wB), the
numeraire, so p is the price of a unit of smoke in units of good 1.

Three families of preferences:

    "sqrt"  u_A = x + sqrt(alpha S),   u_B = x + sqrt(beta (1 - S))   (notes Try it)
    "log"   u_A = x + alpha ln S,      u_B = x + beta ln(1 - S)       (homework, A7.3)
    "cd"    u_A = ln x + alpha ln S,   u_B = ln x + beta ln(1 - S)    (beyond the notes)

The first two are quasi-linear: willingness to pay for smoke depends on S
alone, so the efficient S is the same whoever owns the air. The third has
income effects, and the owner of the air matters for how much smoke there is.
"""

import math

EPS = 1e-12


class Smoke:
    def __init__(self, family, alpha, beta, wA, wB):
        self.family = family
        self.alpha, self.beta = float(alpha), float(beta)
        self.wA, self.wB = float(wA), float(wB)
        self.X = self.wA + self.wB

    @property
    def quasilinear(self):
        return self.family in ("sqrt", "log")

    # -- utility ----------------------------------------------------------------
    def phiA(self, S):
        S = max(S, EPS)
        return math.sqrt(self.alpha * S) if self.family == "sqrt" else self.alpha * math.log(S)

    def phiB(self, c):
        c = max(c, EPS)
        return math.sqrt(self.beta * c) if self.family == "sqrt" else self.beta * math.log(c)

    def uA(self, x, S):
        if self.family == "cd":
            return math.log(max(x, EPS)) + self.phiA(S)
        return x + self.phiA(S)

    def uB(self, x, S):
        if self.family == "cd":
            return math.log(max(x, EPS)) + self.phiB(1 - S)
        return x + self.phiB(1 - S)

    # -- willingness to pay, in units of good 1 ------------------------------------
    def mb(self, S, x=None):
        # A's marginal benefit of smoke: (du/dS)/(du/dx).
        S = max(S, EPS)
        if self.family == "sqrt":
            return 0.5 * math.sqrt(self.alpha / S)
        if self.family == "log":
            return self.alpha / S
        return self.alpha * x / S

    def md(self, S, x=None):
        # B's marginal damage from smoke: what he needs per unit to accept it.
        c = max(1 - S, EPS)
        if self.family == "sqrt":
            return 0.5 * math.sqrt(self.beta / c)
        if self.family == "log":
            return self.beta / c
        return self.beta * x / c

    # -- efficiency -------------------------------------------------------------
    def efficient(self):
        # Quasi-linear: MB = MD gives alpha/S = beta/(1 - S) for both families.
        if not self.quasilinear:
            return None
        return self.alpha / (self.alpha + self.beta)

    def contract(self, xA):
        # Equal willingness to pay at A's good 1 = xA. Flat when quasi-linear.
        if self.quasilinear:
            return self.efficient()
        a, b = self.alpha * xA, self.beta * (self.X - xA)
        return a / (a + b) if a + b > 0 else 0.5

    # -- markets ----------------------------------------------------------------
    def market(self, right):
        """Competitive equilibrium once smoke has a price.

        right "B": B owns clean air, the endowment has S = 0 and A buys smoke.
        right "A": A owns the right to smoke, the endowment has S = 1 and B
        buys clean air from A. Either way A's good 1 is wA - p (S - S0).
        """
        S0 = 1.0 if right == "A" else 0.0
        if self.quasilinear:
            S = self.efficient()
            p = self.mb(S)
        else:
            a, b, wA, wB = self.alpha, self.beta, self.wA, self.wB
            # Each agent's FOC, with the budget substituted in, solved for p:
            pA = lambda S: a * wA / (S + a * (S - S0))
            pB = lambda S: b * wB / (1 - S - b * (S - S0))
            lo, hi = (EPS, 1 / (1 + b)) if S0 == 0 else (a / (1 + a), 1 - EPS)
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if pA(mid) > pB(mid):
                    lo = mid
                else:
                    hi = mid
            S = 0.5 * (lo + hi)
            p = pA(S)
        pay = p * (S - S0)                    # from A to B; negative means B pays A
        return dict(S=S, p=p, xA=self.wA - pay, xB=self.wB + pay, pay=pay, S0=S0)

    def no_trade(self, right):
        # Nobody can pay anybody: the owner of the air goes to her corner.
        S = 1.0 if right == "A" else 0.0
        return dict(S=S, p=None, xA=self.wA, xB=self.wB, pay=0.0, S0=S)

    def surplus_loss(self, S):
        # Quasi-linear only: total value lost against S*, in units of good 1.
        if not self.quasilinear:
            return None
        if self.family == "log" and (S <= EPS or S >= 1 - EPS):
            return math.inf                    # ln 0: a corner is infinitely bad
        W = lambda s: self.phiA(s) + self.phiB(1 - s)
        return W(self.efficient()) - W(S)

    # -- drawing helpers, in the box (xA across, S up) ----------------------------
    def icA(self, level, S):
        # A's good 1 along her indifference curve at smoke S.
        if self.family == "cd":
            return math.exp(level - self.phiA(S))
        return level - self.phiA(S)

    def icB(self, level, S):
        # B's curve, in A's coordinates: xA = X - xB.
        if self.family == "cd":
            return self.X - math.exp(level - self.phiB(1 - S))
        return self.X - (level - self.phiB(1 - S))


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-6: "ok " if abs(got - want) < tol else "FAIL"
    r = lambda d: "S %.4f p %.4f xA %.4f xB %.4f" % (d["S"], d["p"], d["xA"], d["xB"])

    e = Smoke("sqrt", 1, 3, 6, 6)
    print("s07 Try it: sqrt, alpha 1, beta 3")
    print("  %s S* = %s, MB(S*) = %s, MD(S*) = %s" % (ok(e.efficient(), .25), e.efficient(),
                                                      e.mb(.25), e.md(.25)))
    e = Smoke("sqrt", 3, 1, 6, 6)
    print("  %s review Q3: S* = %s; no trade: A's right %s, B's right %s" % (
        ok(e.efficient(), .75), e.efficient(), e.no_trade("A")["S"], e.no_trade("B")["S"]))

    e = Smoke("log", 1, 3, 6, 6)
    mb_, ma_ = e.market("B"), e.market("A")
    print("\ns07 homework: log, alpha 1, beta 3, w = 6, 6")
    print("  %s B's right: %s" % (ok(mb_["xA"], 5) if abs(mb_["p"] - 4) < 1e-9 else "FAIL", r(mb_)))
    print("  %s A's right: %s" % (ok(ma_["xA"], 9), r(ma_)))

    e = Smoke("log", 1 / 3, 2 / 3, 5, 15)
    mb_, ma_ = e.market("B"), e.market("A")
    print("\nA7.3: log, alpha 1/3, beta 2/3, w = 5, 15")
    print("  %s B owns clean air: %s (want xA 14/3 = %.4f)" % (ok(mb_["S"], 1 / 3), r(mb_), 14 / 3))
    print("  %s A owns the right: %s (want xA 17/3 = %.4f)" % (ok(ma_["xA"], 17 / 3), r(ma_), 17 / 3))

    e = Smoke("cd", 1, 3, 6, 6)
    mb_, ma_ = e.market("B"), e.market("A")
    print("\nIncome effects (beyond the notes): cd, alpha 1, beta 3, w = 6, 6")
    print("  %s B's right: %s (want S 0.1, p 30)" % (ok(mb_["S"], .1, 1e-9), r(mb_)))
    print("  %s A's right: %s (want S 0.7, p 15)" % (ok(ma_["S"], .7, 1e-9), r(ma_)))
    print("  %s both on the contract curve: %.4f %.4f" % (
        ok(e.contract(mb_["xA"]) + e.contract(ma_["xA"]), .8, 1e-9), e.contract(mb_["xA"]),
        e.contract(ma_["xA"])))

    import equilibrium as eq
    rec = eq.Economy(1 / 3, 3 / 4, (6, 4), (6, 8)).equilibrium()
    print("\ns07 recap economy: p* %.4f, A %s, B %s" % (rec["p"], tuple(round(v, 4) for v in rec["A"]),
                                                     tuple(round(v, 4) for v in rec["B"])))
    print("  contract(4) = %.4f (want 9); A7.1 contract(6) = %.4f (want 12)" % (
        eq.Economy(1 / 3, 3 / 4, (6, 4), (6, 8)).contract(4), eq.Economy(.5, .5, (10, 25), (5, 5)).contract(6)))
