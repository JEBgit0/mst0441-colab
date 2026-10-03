"""
consumer_theory.py - the maths behind budgets, preferences, utility and choice.

Pure numbers. No tkinter, no matplotlib, nothing that knows about the app, so
the same file serves every course that needs a two-good choice problem:

    MST 0441 s02   goods budget p1*x1 + p2*x2 = m
    MST 0441 s02   leisure budget  w*L + C = w*T + V
    MST 0441 s03   demand functions, Engel curves, Slutsky decomposition
    MST 0440       two-period consumption C1 + C2/(1+r) = Y1 + Y2/(1+r)

All three are the same object: a line in the plane with a slope equal to minus
a price ratio. Budget.leisure() and Budget.intertemporal() are just constructors
that fill in the prices and the endowment for you.

Axis convention: x1 is horizontal, x2 is vertical, and every slope reported is
dx2/dx1. Session 2's first figure puts C1 on the vertical axis, so there it is
good 2. Choose which good is which when you build the Budget; the maths does
not care.

Quick use:
    b = Budget.goods(p1=3, p2=2, m=300)
    u = LogUtility(2, 3)
    c = u.demand(b)              # -> Choice(x1=40, x2=90, ...)
    xs, ys = u.indifference_curve(c.utility, 1, 200)
"""

from __future__ import annotations

import math
import numpy as np

EPS = 1e-12          # keeps logs and divisions away from exactly zero
BIG = 1e12           # stand-in for "off the top of the picture"


# ---------------------------------------------------------------- helpers ---

def _as_float_array(x):
    # Lets every formula below take a scalar or a numpy array without branching.
    return np.asarray(x, dtype=float)


def _golden_max(f, lo, hi, tol=1e-10, iters=300):
    # Maximise a single-peaked f on [lo, hi]. Used only where a family has no
    # closed-form demand; the analytic families never touch this.
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = float(lo), float(hi)
    c, d = b - gr * (b - a), a + gr * (b - a)
    for _ in range(iters):
        if b - a < tol:
            break
        if f(c) > f(d):
            b = d
        else:
            a = c
        c, d = b - gr * (b - a), a + gr * (b - a)
    return 0.5 * (a + b)


def _golden_min(f, lo, hi, **kw):
    # Same search, flipped: used for the cheapest bundle on an indifference curve.
    return _golden_max(lambda x: -f(x), lo, hi, **kw)


# ----------------------------------------------------------------- budget ---

class Budget:
    """The choice set: every bundle with p1*x1 + p2*x2 <= m.

    Income m can be handed over directly, or it can come from an endowment
    (e1, e2) the consumer owns and can sell at those same prices. The endowment
    form is what makes leisure and two-period consumption work: the line always
    passes through the endowment, so a price change pivots the line about it
    instead of shifting the whole thing.
    """

    def __init__(self, p1, p2, m=None, e1=0.0, e2=0.0,
                 names=("x1", "x2"), x1_cap=None):
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.e1 = float(e1)
        self.e2 = float(e2)
        # No income given: the endowment is the income. This is "full income".
        self.m = float(self.p1 * self.e1 + self.p2 * self.e2) if m is None else float(m)
        self.names = names
        # Some goods run out before the budget does: you cannot buy back more
        # leisure than the T hours you started with. None means no such limit.
        self.x1_cap = None if x1_cap is None else float(x1_cap)

    # -- named constructors, one per course --------------------------------
    @classmethod
    def goods(cls, p1, p2, m, names=("x1", "x2")):
        # Plain two-good budget. Session 2's first figure: m=100, p1=2, p2=4.
        return cls(p1, p2, m, names=names)

    @classmethod
    def leisure(cls, w, V, T, pc=1.0):
        # C = w*(T - L) + V, written as w*L + pc*C = w*T + V.
        # Good 1 is leisure, priced at the wage; good 2 is the consumption basket.
        # V arrives in money, so the endowment in baskets is V/pc.
        return cls(w, pc, None, e1=T, e2=V / pc, names=("L", "C"), x1_cap=T)

    @classmethod
    def intertemporal(cls, r, Y1, Y2):
        # C1 + C2/(1+r) = Y1 + Y2/(1+r). Today's price is 1, tomorrow's is the
        # discount factor, and the endowment is the income stream (MST 0440).
        return cls(1.0, 1.0 / (1.0 + r), None, e1=Y1, e2=Y2, names=("C1", "C2"))

    # -- the geometry -------------------------------------------------------
    @property
    def slope(self):
        # dx2/dx1 along the line: the opportunity cost of one more unit of x1.
        return -self.p1 / self.p2

    @property
    def price_ratio(self):
        # p1/p2, the number the MRS has to match at an interior optimum.
        return self.p1 / self.p2

    @property
    def max_x1(self):
        # Spend it all on good 1, but never past a cap like T hours of leisure.
        raw = self.m / self.p1
        return raw if self.x1_cap is None else min(raw, self.x1_cap)

    @property
    def max_x2(self):
        # Spend it all on good 2: the vertical intercept, m/p2.
        return self.m / self.p2

    def x2_at(self, x1):
        # Height of the line above a given x1.
        return (self.m - self.p1 * _as_float_array(x1)) / self.p2

    def x1_at(self, x2):
        # The mirror image, solving the line the other way round.
        return (self.m - self.p2 * _as_float_array(x2)) / self.p1

    def line(self, n=2):
        # Two points are enough for a straight line; n>2 is there for clipping.
        xs = np.linspace(0.0, self.max_x1, max(2, n))
        return xs, self.x2_at(xs)

    def contains(self, x1, x2, tol=1e-9):
        # Is this bundle inside the triangle?
        return self.p1 * x1 + self.p2 * x2 <= self.m + tol

    def spending(self, x1, x2):
        # What the bundle actually costs, for checking a budget is exhausted.
        return self.p1 * x1 + self.p2 * x2

    # -- running the machinery backwards ------------------------------------
    def implied_p2(self, x1, x2):
        # Session 2 part (e): see somebody's bundle, read off the price they face.
        return (self.m - self.p1 * x1) / x2

    def implied_p1(self, x1, x2):
        return (self.m - self.p2 * x2) / x1

    def replace(self, **kw):
        # New budget with some fields changed: doubling p2, halving m, and so on.
        # Endowment budgets keep their endowment, so income is recomputed, which
        # is exactly why a wage rise pivots rather than shifts.
        from_endowment = (self.e1 != 0.0 or self.e2 != 0.0)
        p1 = kw.get("p1", self.p1)
        p2 = kw.get("p2", self.p2)
        e1 = kw.get("e1", self.e1)
        e2 = kw.get("e2", self.e2)
        m = None if from_endowment and "m" not in kw else kw.get("m", self.m)
        cap = kw.get("x1_cap", self.x1_cap)
        return Budget(p1, p2, m, e1, e2, names=self.names, x1_cap=cap)

    def describe(self):
        # One line for the readout strip.
        return "%s: %.2f*%s + %.2f*%s = %.2f   slope %.3f" % (
            "budget", self.p1, self.names[0], self.p2, self.names[1],
            self.m, self.slope)


# ----------------------------------------------------------------- choice ---

class Choice:
    """The optimal bundle, plus everything the plot and the readout want."""

    def __init__(self, x1, x2, utility, budget, kind="interior",
                 mrs=None, lam=None, tied=False):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.utility = float(utility)      # the level of the curve it sits on
        self.budget = budget
        self.kind = kind                   # interior | corner | kink
        self.mrs = mrs                     # |dx2/dx1| of the curve at the point
        self.lam = lam                     # marginal utility of money
        self.tied = tied                   # substitutes with a matching price ratio

    @property
    def bundle(self):
        return self.x1, self.x2

    @property
    def shares(self):
        # Budget shares, the thing that stays constant under Cobb-Douglas.
        m = self.budget.m
        return (self.budget.p1 * self.x1 / m, self.budget.p2 * self.x2 / m)

    def summary(self):
        n1, n2 = self.budget.names
        kind = self.kind + (", tied" if self.tied else "")
        s = "%s* = %.3f   %s* = %.3f   U = %.4f   (%s)" % (
            n1, self.x1, n2, self.x2, self.utility, kind)
        if self.mrs is not None:
            s += "   |MRS| = %.3f vs p1/p2 = %.3f" % (
                self.mrs, self.budget.price_ratio)
        return s


# -------------------------------------------------------------- utilities ---

def _respect_cap(budget, x1, kind):
    # A formula can ask for more of good 1 than exists: with a big enough V the
    # tangency wants more leisure than the T hours in the week. The honest
    # answer is the corner, where the person simply does not work.
    cap = budget.x1_cap
    if cap is not None and x1 > cap:
        x1, kind = cap, "corner"
    return x1, float(budget.x2_at(x1)), kind


class Utility:
    """Base class. A family only has to supply u() and mu().

    Everything else - the MRS, the indifference curve, the optimal bundle -
    has a working default here, so a new utility function costs two methods.
    Override the defaults when a closed form exists, which is faster and exact.
    """

    name = "utility"
    label = "U(x1, x2)"

    # -- the two things a family must define --------------------------------
    def u(self, x1, x2):
        raise NotImplementedError

    def mu(self, x1, x2):
        # Marginal utilities (dU/dx1, dU/dx2). Default is a central difference,
        # accurate enough for plotting and a fine safety net for new families.
        h = 1e-6
        x1 = _as_float_array(x1)
        x2 = _as_float_array(x2)
        u1 = (self.u(x1 + h, x2) - self.u(x1 - h, x2)) / (2 * h)
        u2 = (self.u(x1, x2 + h) - self.u(x1, x2 - h)) / (2 * h)
        return u1, u2

    # -- what everything else is built from ---------------------------------
    def mrs(self, x1, x2):
        # How much x2 you are WILLING to give up for one more x1: U1/U2.
        # Reported as a positive magnitude; the curve's slope is minus this.
        u1, u2 = self.mu(x1, x2)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.abs(u1 / u2)

    def slope(self, x1, x2):
        # dx2/dx1 along an indifference curve, from dU = U1 dx1 + U2 dx2 = 0.
        return -self.mrs(x1, x2)

    def indifference(self, x1, level):
        # x2 such that u(x1, x2) = level. Default solves it by bisection, which
        # works for any utility rising in x2. Closed forms override this.
        x1 = _as_float_array(x1)
        out = np.empty(x1.shape if x1.ndim else (1,), dtype=float)
        flat = np.atleast_1d(x1)
        for i, a in enumerate(flat):
            lo, hi = 0.0, 1.0
            for _ in range(80):                      # grow the bracket first
                if self.u(a, hi) >= level:
                    break
                hi *= 2.0
            else:
                out[i] = np.nan
                continue
            for _ in range(200):                     # then squeeze it
                mid = 0.5 * (lo + hi)
                if self.u(a, mid) < level:
                    lo = mid
                else:
                    hi = mid
            out[i] = 0.5 * (lo + hi)
        return out.reshape(x1.shape) if x1.ndim else float(out[0])

    def indifference_curve(self, level, x1_lo, x1_hi, n=200):
        # Sampled curve for plotting. Points where the level is unreachable come
        # back as nan, so matplotlib simply breaks the line there.
        xs = np.linspace(max(x1_lo, EPS), x1_hi, n)
        return xs, self.indifference(xs, level)

    def curve_through(self, x1, x2, x1_lo, x1_hi, n=200):
        # The one curve that passes through a given bundle, e.g. the optimum.
        return self.indifference_curve(self.u(x1, x2), x1_lo, x1_hi, n)

    # -- choice --------------------------------------------------------------
    def demand(self, budget):
        # Default: walk the budget line and take the best point on it, checking
        # both ends so corner solutions are not missed. Families with a formula
        # override this and never run the search.
        hi = budget.max_x1
        f = lambda a: float(self.u(a, budget.x2_at(a)))
        x1 = _golden_max(f, EPS, max(hi - EPS, EPS))
        best = max([EPS, x1, hi - EPS], key=f)       # compare against the corners
        x2 = float(budget.x2_at(best))
        kind = "corner" if best <= 1e-6 or best >= hi - 1e-6 else "interior"
        return Choice(best, x2, self.u(best, x2), budget, kind,
                      mrs=float(self.mrs(best, x2)))


class CobbDouglas(Utility):
    """U = x1^a * x2^b. The workhorse: fixed budget shares a/(a+b), b/(a+b)."""

    name = "cobb-douglas"

    def __init__(self, a=0.5, b=0.5):
        self.a, self.b = float(a), float(b)
        self.label = "U = x1^%.2f x2^%.2f" % (self.a, self.b)

    def u(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), 0.0)
        x2 = np.maximum(_as_float_array(x2), 0.0)
        return x1 ** self.a * x2 ** self.b

    def mu(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (self.a * x1 ** (self.a - 1) * x2 ** self.b,
                self.b * x1 ** self.a * x2 ** (self.b - 1))

    def mrs(self, x1, x2):
        # U1/U2 collapses to (a/b)*(x2/x1): the exponents cancel most of it.
        x1 = np.maximum(_as_float_array(x1), EPS)
        return (self.a / self.b) * (_as_float_array(x2) / x1)

    def indifference(self, x1, level):
        # x1^a x2^b = U0  =>  x2 = (U0 / x1^a)^(1/b).
        x1 = np.maximum(_as_float_array(x1), EPS)
        return (level / x1 ** self.a) ** (1.0 / self.b)

    def demand(self, budget):
        # Tangency (a/b)(x2/x1) = p1/p2 into the budget gives the share rule.
        s = self.a / (self.a + self.b)
        x1 = s * budget.m / budget.p1
        x1, x2, kind = _respect_cap(budget, x1, "interior")
        return Choice(x1, x2, self.u(x1, x2), budget, kind,
                      mrs=float(self.mrs(x1, x2)),
                      lam=float(self.mu(x1, x2)[0] / budget.p1))


class LogUtility(CobbDouglas):
    """U = a*ln(x1) + b*ln(x2). Same family in disguise, so same choices.

    Only the utility numbers differ, and utility is ordinal, so every bundle
    this picks is the bundle Cobb-Douglas picks with the same a and b.
    """

    name = "log"

    def __init__(self, a=1.0, b=1.0):
        super().__init__(a, b)
        self.label = "U = %.2f ln x1 + %.2f ln x2" % (self.a, self.b)

    def u(self, x1, x2):
        with np.errstate(divide="ignore", invalid="ignore"):
            return (self.a * np.log(np.maximum(_as_float_array(x1), EPS))
                    + self.b * np.log(np.maximum(_as_float_array(x2), EPS)))

    def mu(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (self.a / x1, self.b / x2)

    def indifference(self, x1, level):
        # a ln x1 + b ln x2 = U0  =>  x2 = exp((U0 - a ln x1)/b).
        x1 = np.maximum(_as_float_array(x1), EPS)
        return np.exp((level - self.a * np.log(x1)) / self.b)


class PerfectSubstitutes(Utility):
    """U = a*x1 + b*x2. Straight curves, constant MRS, corner solutions."""

    name = "perfect substitutes"

    def __init__(self, a=1.0, b=1.0):
        self.a, self.b = float(a), float(b)
        self.label = "U = %.2f x1 + %.2f x2" % (self.a, self.b)

    def u(self, x1, x2):
        return self.a * _as_float_array(x1) + self.b * _as_float_array(x2)

    def mu(self, x1, x2):
        # Constant, which is the whole point: willingness to trade never changes.
        ones = np.ones_like(_as_float_array(x1))
        return (self.a * ones, self.b * ones)

    def mrs(self, x1, x2):
        return np.full_like(_as_float_array(x1), self.a / self.b)

    def indifference(self, x1, level):
        # a x1 + b x2 = U0, a straight line with slope -a/b everywhere.
        return (level - self.a * _as_float_array(x1)) / self.b

    def demand(self, budget):
        # Compare marginal utility per krone and put the whole budget on the
        # winner. Tangency cannot pick the point; only the ranking of a/p1
        # against b/p2 can.
        v1 = self.a / budget.p1
        v2 = self.b / budget.p2
        tied = abs(v1 - v2) < 1e-12
        if v1 >= v2:
            x1, x2 = budget.max_x1, budget.x2_at(budget.max_x1)
        else:
            x1, x2 = 0.0, budget.max_x2
        return Choice(x1, x2, self.u(x1, x2), budget,
                      "interior" if tied else "corner",
                      mrs=self.a / self.b, tied=tied)


class PerfectComplements(Utility):
    """U = min(a*x1, b*x2). L-shaped curves; the MRS at the kink does not exist."""

    name = "perfect complements"

    def __init__(self, a=1.0, b=1.0):
        self.a, self.b = float(a), float(b)
        self.label = "U = min(%.2f x1, %.2f x2)" % (self.a, self.b)

    def u(self, x1, x2):
        return np.minimum(self.a * _as_float_array(x1), self.b * _as_float_array(x2))

    def mu(self, x1, x2):
        # Zero on the long arm of the L, undefined at the corner itself.
        a1 = self.a * _as_float_array(x1)
        b2 = self.b * _as_float_array(x2)
        return (np.where(a1 < b2, self.a, 0.0), np.where(b2 < a1, self.b, 0.0))

    def indifference(self, x1, level):
        # Below the kink no amount of x2 reaches the level, so it is undefined.
        x1 = _as_float_array(x1)
        kink1 = level / self.a
        with np.errstate(invalid="ignore"):
            return np.where(x1 >= kink1 - 1e-12, level / self.b, np.nan)

    def indifference_curve(self, level, x1_lo, x1_hi, n=200):
        # Draw the L explicitly: down the vertical arm, then out the horizontal.
        k1, k2 = level / self.a, level / self.b
        top = max(k2 * 3.0, k2 + 1.0)
        xs = np.array([k1, k1, max(x1_hi, k1 * 1.5)])
        ys = np.array([top, k2, k2])
        return xs, ys

    def demand(self, budget):
        # No tangency to find: the optimum always sits on the kink a*x1 = b*x2,
        # so substitute that straight into the budget.
        x1 = budget.m * self.b / (budget.p1 * self.b + budget.p2 * self.a)
        x1, x2, kind = _respect_cap(budget, x1, "kink")
        if kind == "kink":
            x2 = (self.a / self.b) * x1
        return Choice(x1, x2, self.u(x1, x2), budget, kind)


class Quasilinear(Utility):
    """U = a*f(x1) + x2, with f = ln or sqrt. Curved in x1, linear in x2.

    Curves are vertical shifts of each other, so income never moves x1 once the
    price ratio is fixed. All extra income goes to good 2 until x2 hits zero.
    """

    name = "quasilinear"

    def __init__(self, a=1.0, kind="log"):
        self.a, self.kind = float(a), kind
        self.label = "U = %.2f %s(x1) + x2" % (self.a, kind)

    def _f(self, x1):
        x1 = np.maximum(_as_float_array(x1), EPS)
        return np.log(x1) if self.kind == "log" else np.sqrt(x1)

    def u(self, x1, x2):
        return self.a * self._f(x1) + _as_float_array(x2)

    def mu(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), EPS)
        d = self.a / x1 if self.kind == "log" else self.a / (2 * np.sqrt(x1))
        return (d, np.ones_like(x1))

    def indifference(self, x1, level):
        # x2 = U0 - a f(x1): every curve is the same shape, shifted vertically.
        return level - self.a * self._f(x1)

    def demand(self, budget):
        # f'(x1) = p1/p2 fixes x1 on its own, with no income term in sight.
        r = budget.price_ratio
        x1 = (self.a / r) if self.kind == "log" else (self.a / (2 * r)) ** 2
        # A3.1's corner: when m < a*p2 the tangency x1 costs more than the whole
        # budget, so everything goes on good 1 and nothing on good 2.
        kind = "corner" if x1 >= budget.max_x1 - 1e-12 else "interior"
        x1 = min(x1, budget.max_x1)                  # cannot outspend the budget
        x1, x2, kind = _respect_cap(budget, x1, kind)
        if x2 < 1e-12:                               # corner: all of it on good 1
            x1, x2, kind = budget.max_x1, 0.0, "corner"
        return Choice(x1, x2, self.u(x1, x2), budget, kind,
                      mrs=float(self.mrs(x1, max(x2, EPS))))


class AdditivePower(Utility):
    """U = x1^a + x2^b. The form session 2 uses to give two people different tastes.

    With a = 1 and b either 3/4 or 1/4 this draws the two curves in the
    "can different people have different preferences for leisure" figure.
    No tidy closed-form demand, so it falls back on the base-class search.
    """

    name = "additive power"

    def __init__(self, a=1.0, b=0.75):
        self.a, self.b = float(a), float(b)
        self.label = "U = x1^%.2f + x2^%.2f" % (self.a, self.b)

    def u(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), 0.0)
        x2 = np.maximum(_as_float_array(x2), 0.0)
        return x1 ** self.a + x2 ** self.b

    def mu(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (self.a * x1 ** (self.a - 1), self.b * x2 ** (self.b - 1))

    def indifference(self, x1, level):
        # x2 = (U0 - x1^a)^(1/b), undefined once x1 alone exceeds the level.
        x1 = np.maximum(_as_float_array(x1), 0.0)
        rest = level - x1 ** self.a
        with np.errstate(invalid="ignore"):
            return np.where(rest > 0, np.abs(rest) ** (1.0 / self.b), np.nan)


class DiscountedCRRA(Utility):
    """U = u(c1) + b*u(c2) with u(c) = (c^(1-s) - 1)/(1-s), and ln c at s = 1.

    Session 4's preferences written out. Two parameters, doing two jobs:

        beta   the discount factor, how loudly tomorrow speaks
        sigma  the curvature of the per-period utility, which is the inverse
               elasticity of substitution across time

    Sigma is the one worth playing with. Small sigma and the two dates are near
    substitutes, so a small move in r swings the bundle a long way along the
    line. Large sigma and the consumer smooths at almost any cost, sitting near
    the endowment whatever the rate does. At sigma = 1 this is exactly
    LogUtility(1, beta), which is the case the notes solve by hand.

    Constructed as (sigma, beta) rather than (a, b), so it is deliberately left
    out of the FAMILIES dict below: it does not share that signature.
    """

    name = "discounted crra"

    def __init__(self, sigma=1.0, beta=1.0):
        self.sigma = float(sigma)
        self.beta = float(beta)
        # At sigma = 1 the power form is 0/0, so branch to logs once and reuse.
        self.log = abs(self.sigma - 1.0) < 1e-9
        # sigma = 0 is zero curvature, which is a linear u: worth naming, since
        # it is the point where this family coincides with perfect substitutes.
        self.flat = self.sigma < 1e-9
        if self.log:
            self.label = "U = ln c1 + %.2f ln c2" % self.beta
        elif self.flat:
            self.label = "U = c1 + %.2f c2   [sigma = 0]" % self.beta
        else:
            self.label = ("U = u(c1) + %.2f u(c2)   [sigma = %.2f]"
                          % (self.beta, self.sigma))

    # -- the per-period function and its inverse ----------------------------
    def _u1(self, c):
        # u(c). The "- 1" is an affine shift, so it cannot change any choice;
        # it just keeps u continuous in sigma as sigma passes through 1.
        c = np.maximum(_as_float_array(c), EPS)
        if self.log:
            return np.log(c)
        return (c ** (1.0 - self.sigma) - 1.0) / (1.0 - self.sigma)

    def _inv(self, level):
        # The c that delivers a given per-period utility. Levels out of range
        # come back nan, which is how the curve knows where to stop.
        if self.log:
            return np.exp(_as_float_array(level))
        base = 1.0 + (1.0 - self.sigma) * _as_float_array(level)
        with np.errstate(invalid="ignore"):
            return np.where(base > 0, base ** (1.0 / (1.0 - self.sigma)), np.nan)

    # -- the four things a family supplies ----------------------------------
    def u(self, x1, x2):
        return self._u1(x1) + self.beta * self._u1(x2)

    def mu(self, x1, x2):
        # u'(c) = c^(-sigma), with the discount factor riding on period 2 only.
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (x1 ** (-self.sigma), self.beta * x2 ** (-self.sigma))

    def mrs(self, x1, x2):
        # U1/U2 collapses to (1/beta)(x2/x1)^sigma: the intertemporal MRS, the
        # left-hand side of the Euler equation once it is written as a slope.
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (x2 / x1) ** self.sigma / self.beta

    def indifference(self, x1, level):
        # u(c1) + beta u(c2) = U0  =>  c2 = u^-1( (U0 - u(c1)) / beta ).
        return self._inv((_as_float_array(level) - self._u1(x1)) / self.beta)

    def demand(self, budget):
        # Euler: u'(c1) = (p1/p2) beta u'(c2), so c2 = g*c1 with
        # g = (beta * p1/p2)^(1/sigma). One unknown left, and the budget fixes it.
        R = budget.price_ratio
        if self.flat:
            # At sigma = 0 that exponent is 1/0. The limit is well behaved:
            # with no curvature nothing gets smoothed, so the whole budget goes
            # to whichever date is cheaper per unit of utility. Take the limit
            # directly rather than letting the formula divide by zero.
            tied = abs(self.beta * R - 1.0) < 1e-12
            x1 = 0.0 if self.beta * R > 1.0 else budget.max_x1
            x1, x2, kind = _respect_cap(budget, x1, "corner")
            return Choice(x1, x2, self.u(x1, x2), budget,
                          "interior" if tied else kind,
                          mrs=1.0 / self.beta, tied=tied)
        g = (self.beta * R) ** (1.0 / self.sigma)
        x1 = budget.m / (budget.p1 + budget.p2 * g)
        x1 = min(x1, budget.m / budget.p1)         # never outspend the budget
        x1, x2, kind = _respect_cap(budget, x1, "interior")
        return Choice(x1, x2, self.u(x1, x2), budget, kind,
                      mrs=float(self.mrs(x1, max(x2, EPS))),
                      lam=float(self.mu(x1, max(x2, EPS))[0] / budget.p1))


class CES(Utility):
    """U = (a*x1^r + b*x2^r)^(1/r) with r = (s - 1)/s. Beyond the course notes.

    s is the elasticity of substitution, the one number that says how easily
    the two goods replace each other. The course families are its landmarks:

        s -> infinity   perfect substitutes
        s = 1           Cobb-Douglas (and log)
        s -> 0          perfect complements

    It is here for one picture the notes draw but no course family can
    produce: the backward-bending labour supply curve. With s < 1 leisure and
    consumption are poor substitutes, so as the wage climbs the income effect
    eventually beats the substitution effect and hours fall.
    """

    name = "ces"

    def __init__(self, a=1.0, b=1.0, s=0.5):
        self.a, self.b, self.s = float(a), float(b), float(s)
        self.cd = abs(self.s - 1.0) < 1e-6        # the r = 0 limit is Cobb-Douglas
        self.r = 0.0 if self.cd else (self.s - 1.0) / self.s
        self.label = "U = CES(%.2f x1, %.2f x2), sigma = %.2f" % (self.a, self.b, self.s)

    def u(self, x1, x2):
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        if self.cd:
            w = self.a + self.b
            return x1 ** (self.a / w) * x2 ** (self.b / w)
        return (self.a * x1 ** self.r + self.b * x2 ** self.r) ** (1.0 / self.r)

    def mrs(self, x1, x2):
        # (a/b) (x2/x1)^(1/s): the further the ratio is from 1, the steeper
        # the trade, and the faster the steeper when s is small.
        x1 = np.maximum(_as_float_array(x1), EPS)
        x2 = np.maximum(_as_float_array(x2), EPS)
        return (self.a / self.b) * (x2 / x1) ** (1.0 / self.s)

    def indifference(self, x1, level):
        x1 = np.maximum(_as_float_array(x1), EPS)
        if self.cd:
            w = self.a + self.b
            return (level / x1 ** (self.a / w)) ** (w / self.b)
        rest = (level ** self.r - self.a * x1 ** self.r) / self.b
        with np.errstate(invalid="ignore", divide="ignore"):
            # Where the level cannot be reached at this x1 the curve has ended.
            return np.where(rest > 0, np.abs(rest) ** (1.0 / self.r), np.nan)

    def demand(self, budget):
        # Tangency gives x2/x1 = (b p1 / (a p2))^s; the budget fixes the level.
        g = (self.b * budget.p1 / (self.a * budget.p2)) ** self.s
        x1 = budget.m / (budget.p1 + budget.p2 * g)
        x1, x2, kind = _respect_cap(budget, x1, "interior")
        return Choice(x1, x2, self.u(x1, x2), budget, kind,
                      mrs=float(self.mrs(x1, max(x2, EPS))))


FAMILIES = {                     # for a dropdown in the tab later
    "Cobb-Douglas": CobbDouglas,
    "Log": LogUtility,
    "Perfect substitutes": PerfectSubstitutes,
    "Perfect complements": PerfectComplements,
    "Quasilinear": Quasilinear,
    "Additive power": AdditivePower,
}


# ------------------------------------------------- comparative statics ------
# Not needed to draw session 2, but they are one line each given the classes
# above, and session 3 is built entirely out of them.

def hours_worked(choice, T):
    # Labour supply is just the leisure that was not chosen.
    return T - choice.x1


def reservation_wage(utility, V, T, pc=1.0):
    # The wage that makes the endowment itself a tangency: below it the person
    # works zero hours. It is the MRS evaluated at "keep all your time".
    return float(utility.mrs(T, V / pc)) * pc


def real_rate(r, pi):
    # 1 + rho = (1 + r)/(1 + pi). Session 4: the nominal rate is only half the
    # story, because tomorrow's kroner buy less. Every r in the model is really
    # this rho, which is why the shortcut r - pi drifts off at high rates.
    return (1.0 + float(r)) / (1.0 + float(pi)) - 1.0


def bond(choice, m1):
    # b1 = m1 - c1, the one number that says which side of the endowment you
    # are on. Positive is lending (you saved), negative is borrowing.
    return float(m1) - choice.x1


def present_value(stream, rho):
    # sum m_n / (1 + rho)^(n-1), the N-period constraint from the end of the
    # session. With two payments it is just the NPV the budget line uses.
    return float(sum(m / (1.0 + rho) ** n for n, m in enumerate(stream)))


def expenditure(utility, p1, p2, level, x1_hi=None):
    # Cheapest bundle that still reaches a given utility level: the Hicksian
    # side of session 3. Searches along the indifference curve rather than the
    # budget line, so it works for any family with an indifference() method.
    hi = x1_hi if x1_hi is not None else 1e4
    cost = lambda a: p1 * a + p2 * float(utility.indifference(a, level))
    x1 = _golden_min(cost, EPS, hi)
    x2 = float(utility.indifference(x1, level))
    return x1, x2, p1 * x1 + p2 * x2


def slutsky(utility, budget_old, budget_new):
    # The three bundles of the Hicks decomposition:
    #   A  the original choice
    #   B  new prices, old utility  (A -> B is the substitution effect)
    #   C  the new choice           (B -> C is the income effect)
    a = utility.demand(budget_old)
    c = utility.demand(budget_new)
    bx1, bx2, _ = expenditure(utility, budget_new.p1, budget_new.p2, a.utility,
                              x1_hi=max(budget_old.max_x1, budget_new.max_x1) * 5)
    # Good 2 gets its own three numbers: session 3's tariff falls on good 2,
    # and under log utility good 1's two effects cancel to exactly zero.
    return {"A": (a.x1, a.x2), "B": (bx1, bx2), "C": (c.x1, c.x2),
            "substitution": bx1 - a.x1, "income": c.x1 - bx1,
            "total": c.x1 - a.x1,
            "substitution2": bx2 - a.x2, "income2": c.x2 - bx2,
            "total2": c.x2 - a.x2}


# ------------------------------------------------------------ self-check ----
# Every number below is taken from the MST 0441 session notes, so running this
# file checks the maths against the course rather than against itself.

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-6: "ok " if abs(got - want) < tol else "FAIL"

    print("s02 goods budget: m=100, p1=2, p2=4, C1 on the vertical axis")
    b = Budget.goods(p1=4, p2=2, m=100, names=("C2", "C1"))   # C2 horizontal
    print("  %s vertical intercept m/P1 = %.1f (want 50)" % (ok(b.max_x2, 50), b.max_x2))
    print("  %s horizontal intercept m/P2 = %.1f (want 25)" % (ok(b.max_x1, 25), b.max_x1))
    print("  %s slope dC1/dC2 = %.1f (want -2)" % (ok(b.slope, -2), b.slope))
    p2 = b.implied_p1(12, 20)          # part (e): bundle C1=20, C2=12
    print("  %s implied P2 from the bundle = %.1f (want 5)" % (ok(p2, 5), p2))
    dbl = b.replace(p1=8, p2=4, m=200)  # part (f): double everything
    print("  %s doubling all: intercepts %.1f, %.1f unchanged" % (
        ok(dbl.max_x1, 25), dbl.max_x1, dbl.max_x2))

    print("\ns02 leisure budget: V=100, w=20, T=16, U = C*L")
    lb = Budget.leisure(w=20, V=100, T=16)
    print("  %s full income = %.0f (want 420)" % (ok(lb.m, 420), lb.m))
    print("  %s slope = %.0f (want -20)" % (ok(lb.slope, -20), lb.slope))
    ch = CobbDouglas(1, 1).demand(lb)   # half of full income on each good
    print("  %s L* = %.2f (want 10.5), C* = %.1f (want 210)" % (
        ok(ch.x1, 10.5), ch.x1, ch.x2))
    print("  %s tangency: |MRS| %.3f = w %.3f" % (
        ok(ch.mrs, lb.price_ratio), ch.mrs, lb.price_ratio))

    print("\ns02 review q6: U = x1^(1/3) x2^(2/3), m=18, p=(2,3)")
    c = CobbDouglas(1 / 3, 2 / 3).demand(Budget.goods(2, 3, 18))
    print("  %s bundle = (%.1f, %.1f) (want (3, 4))" % (ok(c.x1, 3), c.x1, c.x2))

    print("\ns03 worked example: U = 2 ln x1 + 3 ln x2, p=(3,2), m=300")
    c = LogUtility(2, 3).demand(Budget.goods(3, 2, 300))
    print("  %s bundle = (%.0f, %.0f) (want (40, 90))" % (ok(c.x1, 40), c.x1, c.x2))
    print("  %s budget share on good 1 = %.2f (want 0.40)" % (
        ok(c.shares[0], 0.4), c.shares[0]))

    print("\ns03 labour supply: U = ln C + ln L, m=1000, T=112, p=10, w=20")
    lb = Budget.leisure(w=20, V=1000, T=112, pc=10)
    c = LogUtility(1, 1).demand(lb)
    want_L = 1000 / (2 * 20) + 112 / 2                 # L* = m/2w + T/2
    want_C = (1000 + 20 * 112) / (2 * 10)              # C* = (m + wT)/2p
    print("  %s L* = %.1f (want %.1f), h* = %.1f" % (
        ok(c.x1, want_L), c.x1, want_L, hours_worked(c, 112)))
    print("  %s C* = %.1f (want %.1f)" % (ok(c.x2, want_C), c.x2, want_C))
    print("  %s reservation wage (m=60, T=10) = %.1f (want 6)" % (
        ok(reservation_wage(LogUtility(1, 1), 60, 10), 6),
        reservation_wage(LogUtility(1, 1), 60, 10)))

    print("\nspecial cases and the numeric fallback")
    sub = PerfectSubstitutes(1, 1).demand(Budget.goods(2, 4, 100))
    print("  %s substitutes go to the cheap corner: (%.0f, %.0f), kind=%s" % (
        ok(sub.x1, 50), sub.x1, sub.x2, sub.kind))
    com = PerfectComplements(1, 1).demand(Budget.goods(2, 4, 120))
    print("  %s complements sit on the kink: (%.0f, %.0f), kind=%s" % (
        ok(com.x1, 20), com.x1, com.x2, com.kind))
    num = AdditivePower(1, 1).demand(Budget.goods(2, 4, 100))   # linear in both
    print("  %s search finds the same corner as substitutes: x1 = %.1f" % (
        ok(num.x1, 50, 1e-3), num.x1))
    base = CobbDouglas(0.5, 0.5)
    check = base.demand(Budget.goods(3, 2, 300))
    guess = Utility.demand(base, Budget.goods(3, 2, 300))       # force the search
    print("  %s formula %.3f vs search %.3f agree" % (
        ok(check.x1, guess.x1, 1e-4), check.x1, guess.x1))

    print("\ns04 Kari: m=(50, 60), r=20%, U = ln c1 + (2/3) ln c2")
    ib = Budget.intertemporal(r=0.20, Y1=50, Y2=60)
    print("  %s NPV = %.0f (want 100), FV = %.0f (want 120), slope %.1f (want -1.2)"
          % (ok(ib.m, 100), ib.m, ib.max_x2, ib.slope))
    k = LogUtility(1, 2 / 3).demand(ib)
    print("  %s c1* = %.0f (want 60), c2* = %.0f (want 48)" % (
        ok(k.x1, 60), k.x1, k.x2))
    print("  %s b1 = %.0f (want -10, borrows), repays %.0f (want 12)" % (
        ok(bond(k, 50), -10), bond(k, 50), -bond(k, 50) * 1.20))
    # Part (c) inverted: observe c1 = 80, read off the discount factor.
    print("  %s Sondre picks c1 = 80, so beta = %.2f (want 0.25)" % (
        ok(ib.m / 80 - 1, 0.25), ib.m / 80 - 1))
    # Part (d): a bonus of 12 next year is worth 10 today, spent at share 1/(1+b).
    boost = LogUtility(1, 2 / 3).demand(Budget.intertemporal(0.20, 50, 72))
    print("  %s a bonus of 12 next year lifts c1 by %.0f (want 6)" % (
        ok(boost.x1 - k.x1, 6), boost.x1 - k.x1))

    print("\ns04 worksheet: m=(60, 63), r=5%")
    wb = Budget.intertemporal(r=0.05, Y1=60, Y2=63)
    half = LogUtility(1, 0.5).demand(wb)
    print("  %s beta=1/2 gives (%.0f, %.0f) (want (80, 42)), borrows %.0f" % (
        ok(half.x1, 80), half.x1, half.x2, -bond(half, 60)))
    one = LogUtility(1, 1.0).demand(wb)
    print("  %s beta=1 sits on the endowment: c1 = %.0f (want 60), b1 = %.0f" % (
        ok(one.x1, 60), one.x1, bond(one, 60)))
    # The rate rise from task 4: the line pivots, the endowment cannot move.
    up = Budget.intertemporal(r=0.25, Y1=60, Y2=63)
    print("  %s r: 5%% -> 25%% pivots about e, slope %.2f -> %.2f, NPV %.1f -> %.1f"
          % (ok(up.slope, -1.25), wb.slope, up.slope, wb.m, up.m))
    print("  %s e stays affordable at both rates: %s / %s" % (
        ok(float(wb.contains(60, 63) and up.contains(60, 63)), 1.0),
        wb.contains(60, 63), up.contains(60, 63)))

    print("\ns04 CRRA and inflation")
    print("  %s sigma=1 reproduces the log bundle: c1 = %.2f vs %.2f" % (
        ok(DiscountedCRRA(1.0, 0.5).demand(wb).x1, half.x1, 1e-6),
        DiscountedCRRA(1.0, 0.5).demand(wb).x1, half.x1))
    sm = DiscountedCRRA(4.0, 0.5).demand(wb)      # heavy smoother
    print("  %s high sigma hugs the endowment: c1 = %.1f (e1 = 60)" % (
        "ok " if abs(sm.x1 - 60) < abs(half.x1 - 60) else "FAIL", sm.x1))
    print("  %s review q6: r=26%%, pi=5%% gives rho = %.4f (want 0.20), r-pi = 0.21"
          % (ok(real_rate(0.26, 0.05), 0.20, 1e-9), real_rate(0.26, 0.05)))

    print("\ns03 tariff: 50%% on good 2, U = 2 ln x1 + 3 ln x2, m=300")
    u = LogUtility(2, 3)
    before, after = Budget.goods(3, 2, 300), Budget.goods(3, 3, 300)
    d = slutsky(u, before, after)
    print("  %s good 2 falls 90 -> %.0f, good 1 holds at %.0f" % (
        ok(u.demand(after).x2, 60), u.demand(after).x2, u.demand(after).x1))
    print("  decomposition on good 1: sub %+.2f, inc %+.2f, total %+.2f" % (
        d["substitution"], d["income"], d["total"]))
    print("  %s on good 2 the two effects add up: %+.2f %+.2f = %+.0f (want -30)" % (
        ok(d["substitution2"] + d["income2"], -30), d["substitution2"], d["income2"],
        d["total2"]))
    lump = u.demand(Budget.goods(3, 2, 240))
    print("  %s lump sum of 60: (%.0f, %.0f), U %.2f > tariff U %.2f (notes: 19.76 > 19.66)"
          % (ok(round(lump.utility, 2), 19.76, 1e-9), lump.x1, lump.x2, lump.utility,
             u.demand(after).utility))

    print("\ns03 labour supply worksheet: U = ln C + ln L, m=60, T=10")
    for w, want in ((10, 2), (15, 3), (30, 4)):
        h = hours_worked(CobbDouglas(1, 1).demand(Budget.leisure(w, 60, 10)), 10)
        print("  %s w = %d gives h* = %.0f (want %d)" % (ok(h, want), w, h, want))

    print("\nCES, beyond the notes")
    for s in (0.5, 1.0, 3.0):
        c = CES(1, 1, s).demand(Budget.goods(3, 2, 300))
        print("  sigma=%.1f: (%.2f, %.2f), spends %.0f" % (s, c.x1, c.x2, 3 * c.x1 + 2 * c.x2))
    print("  %s sigma=1 matches Cobb-Douglas: x1 = %.2f vs %.2f" % (
        ok(CES(2, 3, 1.0).demand(Budget.goods(3, 2, 300)).x1, 40),
        CES(2, 3, 1.0).demand(Budget.goods(3, 2, 300)).x1, 40.0))
    hs = [hours_worked(CES(1, 1, 0.5).demand(Budget.leisure(w, 100, 100)), 100)
          for w in (2, 6, 20, 60)]
    print("  %s sigma=0.5 labour supply bends back: h = %s" % (
        "ok " if hs[1] > hs[0] and hs[3] < hs[2] else "FAIL",
        ", ".join("%.1f" % h for h in hs)))
