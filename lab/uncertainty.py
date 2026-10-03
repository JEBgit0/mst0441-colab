"""
uncertainty.py - the maths of session 5: asset prices and choice under risk.

Pure numbers, like consumer_theory.py. Nothing here knows about widgets.

    asset prices    bond_price, perpetuity, implied_rate, capm
    risk attitudes  Utility functions v(c), expected value and utility,
                    certainty equivalent, risk premium
    insurance       state wealth for coverage K, the budget slope,
                    optimal coverage, the insurer's expected profit

Notation follows the session 5 notes: W pre-loss wealth, D the loss, pi its
probability, q the price per krone of coverage K. Consumption is c_good in
the good state and c_bad in the bad one; diagrams put c_bad across.
"""

import math

EPS = 1e-9


# ------------------------------------------------------------ asset prices ---

def bond_price(x, F, N, r):
    # Coupons x at t = 1..N plus the face value F at N, each discounted.
    return sum(x / (1 + r) ** t for t in range(1, N + 1)) + F / (1 + r) ** N


def perpetuity(x, r):
    # PV = x/r: the fixed point of PV = (x + PV)/(1 + r).
    return x / r


def implied_rate(x, price):
    # Run the perpetuity backwards: the rate the market uses is rent over price.
    return x / price


def capm(rf, mu_m, beta):
    # mu_i = rf + beta (mu_m - rf): only market risk is priced.
    return rf + beta * (mu_m - rf)


# ---------------------------------------------------------- risk attitudes ---

class V:
    """A state utility v(c), with its derivative and inverse.

    kind: "sqrt", "log", "linear", "square", or "crra" (with rho, the
    curvature; rho = 0.5 is sqrt, rho = 1 is log, rho = 0 is linear).
    """

    def __init__(self, kind="sqrt", rho=0.5):
        self.kind, self.rho = kind, float(rho)

    def __call__(self, c):
        c = max(c, EPS)
        k = self.kind
        if k == "sqrt":
            return math.sqrt(c)
        if k == "log":
            return math.log(c)
        if k == "linear":
            return c
        if k == "square":
            return c * c
        if abs(self.rho - 1) < 1e-9:
            return math.log(c)
        return c ** (1 - self.rho) / (1 - self.rho)

    def inverse(self, u):
        k = self.kind
        if k == "sqrt":
            return u * u
        if k == "log":
            return math.exp(u)
        if k == "linear":
            return u
        if k == "square":
            return math.sqrt(max(u, 0.0))
        if abs(self.rho - 1) < 1e-9:
            return math.exp(u)
        base = u * (1 - self.rho)
        if base <= 0:
            return float("nan")                  # a level this utility never reaches
        return base ** (1 / (1 - self.rho))

    def prime(self, c):
        c = max(c, EPS)
        k = self.kind
        if k == "sqrt":
            return 0.5 / math.sqrt(c)
        if k == "log":
            return 1 / c
        if k == "linear":
            return 1.0
        if k == "square":
            return 2 * c
        return c ** (-self.rho)

    @property
    def attitude(self):
        # The sign of v'': concave averse, linear neutral, convex loving.
        if self.kind in ("sqrt", "log"):
            return "risk averse"
        if self.kind == "linear":
            return "risk neutral"
        if self.kind == "square":
            return "risk loving"
        return ("risk averse" if self.rho > 1e-9 else
                "risk loving" if self.rho < -1e-9 else "risk neutral")


def expected_value(outcomes, probs):
    return sum(p * c for c, p in zip(outcomes, probs))


def expected_utility(v, outcomes, probs):
    return sum(p * v(c) for c, p in zip(outcomes, probs))


def certainty_equivalent(v, outcomes, probs):
    # The sure wealth with the same utility as the gamble.
    return v.inverse(expected_utility(v, outcomes, probs))


def risk_premium(v, outcomes, probs):
    # EV - CE, in money: what she would pay to make the risk go away.
    return expected_value(outcomes, probs) - certainty_equivalent(v, outcomes, probs)


# --------------------------------------------------------------- insurance ---

def states(W, D, q, K):
    # The premium qK is paid in both states; the indemnity K only in the bad.
    return W - q * K, W - D + K - q * K          # (c_good, c_bad)


def budget_slope(q):
    # d c_good / d c_bad along the insurance line: -q/(1 - q).
    return -q / (1 - q)


def insurance_eu(v, W, D, pi, q, K):
    cg, cb = states(W, D, q, K)
    return (1 - pi) * v(cg) + pi * v(cb)


def optimal_coverage(v, W, D, pi, q):
    """Best K in [0, D], by golden section on a concave objective.

    Linear utility is handled exactly, because there the objective is a
    straight line in K and the answer is a corner (or anything, at q = pi).
    """
    if v.kind == "linear" or (v.kind == "crra" and abs(v.rho) < 1e-9):
        slope = pi - q
        if abs(slope) < 1e-12:
            return None                          # indifferent across [0, D]
        return D if slope > 0 else 0.0
    if v.kind == "square":                       # convex: the better endpoint
        return max((0.0, D), key=lambda k: insurance_eu(v, W, D, pi, q, k))
    lo, hi = 0.0, float(D)
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    f = lambda k: insurance_eu(v, W, D, pi, q, k)
    for _ in range(200):
        if f(c) > f(d):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    k = 0.5 * (a + b)
    return max((0.0, k, hi), key=f)


def insurer_profit(pi, q, K):
    # Premiums in both states minus the payout in the bad one: K(q - pi).
    return (1 - pi) * q * K + pi * (q * K - K)


def foc_ratio(pi, q):
    # v'(c_bad)/v'(c_good) at an interior optimum: q(1 - pi)/((1 - q) pi).
    return q * (1 - pi) / ((1 - q) * pi)


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-6: "ok " if abs(got - want) < tol else "FAIL"

    print("s05 notes: bond N=10, r=10%, x=100, F=1000")
    print("  %s PV = %.2f (want 1000)" % (ok(bond_price(100, 1000, 10, .1), 1000), bond_price(100, 1000, 10, .1)))
    print("  %s zero coupon = %.2f (want ~386)" % (ok(bond_price(0, 1000, 10, .1), 385.54, 0.01), bond_price(0, 1000, 10, .1)))
    print("  %s perpetuity 100 at 10%% = %.0f" % (ok(perpetuity(100, .1), 1000), perpetuity(100, .1)))
    print("  %s house 200k at 5%% = %.0f, at 2.5%% = %.0f, implied rate %.3f, net %.0f" % (
        ok(perpetuity(2e5, .05) + perpetuity(2e5, .025) + implied_rate(2e5, 1e7) + perpetuity(1.5e5, .025),
           4e6 + 8e6 + 0.02 + 6e6, 1e-3), perpetuity(2e5, .05), perpetuity(2e5, .025),
        implied_rate(2e5, 1e7), perpetuity(1.5e5, .025)))
    print("  %s cabin 120: %.0f at 4%%, %.0f at 6%%" % (ok(perpetuity(120, .04) - perpetuity(120, .06), 1000),
                                                     perpetuity(120, .04), perpetuity(120, .06)))

    print("\ns05 Try it: 100 or 400, fifty-fifty")
    g1, g2, half = (100, 400), (16, 484), (.5, .5)
    A, B, C = V("sqrt"), V("linear"), V("square")
    print("  %s EV %.0f, EU(A) %.0f, EU(C) %.0f" % (ok(expected_utility(A, g1, half), 15), expected_value(g1, half),
                                                  expected_utility(A, g1, half), expected_utility(C, g1, half)))
    print("  %s CE %.0f, premium %.0f (want 225, 25)" % (ok(risk_premium(A, g1, half), 25),
                                                         certainty_equivalent(A, g1, half), risk_premium(A, g1, half)))
    print("  %s spread: CE %.0f, premium %.0f (want 169, 81)" % (ok(risk_premium(A, g2, half), 81),
                                                                 certainty_equivalent(A, g2, half), risk_premium(A, g2, half)))
    print("  %s worksheet 4 or 16: EV %.0f EU %.0f CE %.0f premium %.0f" % (
        ok(risk_premium(A, (4, 16), half), 1), expected_value((4, 16), half), expected_utility(A, (4, 16), half),
        certainty_equivalent(A, (4, 16), half), risk_premium(A, (4, 16), half)))

    print("\ns05 worksheet insurance: W=100, D=50, pi=q=1/5")
    k = optimal_coverage(A, 100, 50, .2, .2)
    print("  %s slope %.2f, K* = %.2f, bundle %s" % (ok(k, 50, 1e-4), budget_slope(.2), k,
                                                   tuple(round(x, 2) for x in states(100, 50, .2, k))))

    print("\nA5.2 Ingrid: W=100, D=64, pi=1/4, sqrt")
    k = optimal_coverage(A, 100, 64, .25, .25)
    eu0 = insurance_eu(A, 100, 64, .25, .25, 0)
    print("  %s fair: K* = %.2f, wealth %.2f, EU(e) = %.0f, CE %.0f, premium %.0f" % (
        ok(k, 64, 1e-4), k, states(100, 64, .25, k)[0], eu0, A.inverse(eu0), 84 - A.inverse(eu0)))
    k = optimal_coverage(A, 100, 64, .25, 1 / 3)
    print("  %s q=1/3: slope %.2f, ratio %.2f, K* = %.2f (want 114/11 = %.2f)" % (
        ok(k, 114 / 11, 1e-4), budget_slope(1 / 3), foc_ratio(.25, 1 / 3), k, 114 / 11))
    print("  %s linear: q>pi -> K=%s, q<pi -> K=%s, q=pi -> %s" % (
        "ok " if optimal_coverage(B, 100, 64, .25, .3) == 0 and optimal_coverage(B, 100, 64, .25, .2) == 64
        and optimal_coverage(B, 100, 64, .25, .25) is None else "FAIL",
        optimal_coverage(B, 100, 64, .25, .3), optimal_coverage(B, 100, 64, .25, .2),
        optimal_coverage(B, 100, 64, .25, .25)))

    print("\nA5.1 car: W=D=50000, pi=1%, q=5%, log")
    L = V("log")
    k = optimal_coverage(L, 50000, 50000, .01, .05)
    print("  %s K* = %.1f, states %s, profit %.1f" % (ok(k, 10000, 0.5), k,
          tuple(round(x) for x in states(50000, 50000, .05, k)), insurer_profit(.01, .05, k)))
    k = optimal_coverage(L, 50000, 50000, .01, .01)
    print("  %s fair q=1%%: K* = %.1f" % (ok(k, 50000, 0.5), k))

    print("\nA5.3 and review Q6 (context)")
    print("  %s bond G at 25%% = %.1f (want 707.2)" % (ok(bond_price(100, 1000, 3, .25), 707.2, 1e-6), bond_price(100, 1000, 3, .25)))
    print("  %s CAPM beta 2: %.0f%%; beta 0.4 line %.0f%% vs 6%%" % (ok(capm(3, 8, 2), 13), capm(3, 8, 2), capm(3, 8, .4)))
