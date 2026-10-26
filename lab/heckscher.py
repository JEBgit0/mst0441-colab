"""
heckscher.py - the maths of session 10: Heckscher-Ohlin and factor prices.

Pure numbers, like the other session modules. Nothing here knows about widgets.

    HO         two goods, two factors, fixed unit input requirements: zero
               profits give factor prices (Stolper-Samuelson), full
               employment gives outputs (Rybczynski), and the cone of
               diversification says when both hold
    pct        percentage changes, and the magnification chain they form
    tariff     the small-country tariff with linear demand and supply of any
               slope (context: not examinable)

Notation follows the notes and the problem sets. Good y is the one on the
vertical axis and good x the one on the horizontal; in every course example y
is the capital-intensive good. E is labor and K capital, w the wage and r the
rental. a_Ky is the capital needed per unit of good y, and so on.
"""


class HO:
    def __init__(self, aKy, aEy, aKx, aEx):
        self.a = {"y": (float(aKy), float(aEy)), "x": (float(aKx), float(aEx))}

    # -- technology ---------------------------------------------------------------
    def intensity(self, good):
        # Capital per unit of labor, K/E, used by one industry.
        aK, aE = self.a[good]
        return aK / aE

    def capital_good(self):
        # The capital-intensive good: "y" or "x". None if the ratios tie (no
        # ranking, and none of the theorems can be signed).
        ky, kx = self.intensity("y"), self.intensity("x")
        if abs(ky - kx) < 1e-12:
            return None
        return "y" if ky > kx else "x"

    def _det(self):
        (aKy, aEy), (aKx, aEx) = self.a["y"], self.a["x"]
        return aKy * aEx - aKx * aEy

    # -- zero profits: goods prices to factor prices ----------------------------
    def factor_prices(self, py, px):
        # p_y = a_Ky r + a_Ey w and p_x = a_Kx r + a_Ex w, solved for (r, w).
        (aKy, aEy), (aKx, aEx) = self.a["y"], self.a["x"]
        d = self._det()
        r = (py * aEx - px * aEy) / d
        w = (aKy * px - aKx * py) / d
        return r, w

    def unit_cost(self, good, r, w):
        aK, aE = self.a[good]
        return aK * r + aE * w

    def price_from(self, good, r, w):
        # The zero-profit condition run backward: the price a pair (r, w) needs.
        return self.unit_cost(good, r, w)

    def per_krone(self, good, p):
        # Inputs per krone of output, (labor, capital): the point a fixed-
        # coefficient unit-value isoquant collapses to in the Lerner diagram.
        aK, aE = self.a[good]
        return aE / p, aK / p

    # -- full employment: endowments to outputs ---------------------------------
    def outputs(self, K, E):
        # a_Ky q_y + a_Kx q_x = K and a_Ey q_y + a_Ex q_x = E, solved for (q_y, q_x).
        (aKy, aEy), (aKx, aEx) = self.a["y"], self.a["x"]
        d = self._det()
        qy = (K * aEx - E * aKx) / d
        qx = (aKy * E - aEy * K) / d
        return qy, qx

    def cone(self):
        # The endowment ratios K/E at which both outputs are non-negative: the
        # cone of diversification, between the two industries' rays.
        ky, kx = self.intensity("y"), self.intensity("x")
        return min(ky, kx), max(ky, kx)

    def inside(self, K, E, tol=1e-9):
        lo, hi = self.cone()
        return lo - tol <= K / E <= hi + tol

    def labor_used(self, qy, qx):
        return self.a["y"][1] * qy + self.a["x"][1] * qx

    def capital_used(self, qy, qx):
        return self.a["y"][0] * qy + self.a["x"][0] * qx


def pct(before, after):
    # The percentage change, in percent: pct(10, 12) = 20.
    return 100.0 * (after / before - 1.0)


def chain(changes):
    # The magnification chain: {name: percent} as a list of (name, percent),
    # from the largest change down, the way the notes write r^ > p^_y > p^_x > w^.
    return sorted(changes.items(), key=lambda kv: -kv[1])


def chain_text(changes):
    return " > ".join("%s = %s%%" % (name, ("%.2f" % value).rstrip("0").rstrip("."))
                      for name, value in chain(changes))


# ------------------------------------------------------- tariff (context) ---

def tariff(pw, t, a=120.0, b=2.0, c=0.0, d=1.0):
    """A small country with demand D = a - b p and supply S = c + d p.

    The four areas between the price lines p_w and p_w + t: a is the producers'
    gain, c the revenue, b and d the two triangles nobody gets. A tariff that
    lifts the price past the autarky price stops all imports, and the price
    stays there.
    """
    autarky = (a - c) / (b + d)
    p = min(pw + t, max(autarky, pw))
    t = p - pw
    S0, D0, S1, D1 = c + d * pw, a - b * pw, c + d * p, a - b * p
    out = dict(p=p, S0=S0, D0=D0, S1=S1, D1=D1, M0=D0 - S0, M1=D1 - S1, autarky=autarky)
    out["a"] = t * (S0 + S1) / 2
    out["b"] = t * (S1 - S0) / 2
    out["c"] = t * (D1 - S1)
    out["d"] = t * (D0 - D1) / 2
    out["loss"] = out["b"] + out["d"]
    out["consumers"] = t * (D0 + D1) / 2
    return out


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-9: "ok " if abs(got - want) < tol else "FAIL"

    print("notes Try it: machinery (5, 2), garments (1, 2)")
    v = HO(5, 2, 1, 2)
    r0, w0 = v.factor_prices(20, 12)
    r1 = 2 * r0
    w1 = (12 - r1) / 2
    py1 = v.price_from("y", r1, w1)
    print("  %s K/E %s and %s; (r, w) = (%s, %s)" % (ok(r0 + w0, 7), v.intensity("y"),
                                                    v.intensity("x"), r0, w0))
    print("  %s r doubles to %s: w = %s, machinery price %s" % (ok(py1, 28), r1, w1, py1))
    print("  %s chain %s" % (ok(pct(w0, w1), -20), chain_text(
        {"r": pct(r0, r1), "py": pct(20, py1), "px": 0.0, "w": pct(w0, w1)})))
    qy, qx = v.outputs(90, 60)
    print("  %s outputs at K = 90, E = 60: %s, %s" % (ok(qy + qx, 30), qy, qx))
    qx1 = (60 - 2 * 24) / 2
    K1 = 5 * 24 + qx1
    print("  %s detective: garments %s, K = %s (+%s%%)" % (ok(K1, 126), qx1, K1, pct(90, K1)))

    print("\nworksheet: electronics (2, 1), textiles (1, 3)")
    v = HO(2, 1, 1, 3)
    r0, w0 = v.factor_prices(10, 10)
    r1, w1 = v.factor_prices(15, 10)
    print("  %s (r, w) = (%s, %s), then (%s, %s); chain %s" % (
        ok(r1 + w1, 8), r0, w0, r1, w1,
        chain_text({"r": pct(r0, r1), "py": 50.0, "px": 0.0, "w": pct(w0, w1)})))
    print("  %s per krone: electronics %s, textiles %s; 1/w = %s, 1/r = %s" % (
        ok(w0 * 0.3 + r0 * 0.1, 1), v.per_krone("y", 10), v.per_krone("x", 10), 1 / w0, 1 / r0))
    a, b = v.outputs(50, 50), v.outputs(50, 60)
    print("  %s E 50 -> 60: (qy, qx) %s -> %s; chain %s" % (
        ok(b[0] + b[1], 32), a, b,
        chain_text({"qx": pct(a[1], b[1]), "E": 20.0, "qy": pct(a[0], b[0])})))

    print("\nreview Q2-3: robotics (3, 1), footwear (1, 2)")
    v = HO(3, 1, 1, 2)
    r0, w0 = v.factor_prices(10, 10)
    r1, w1 = v.factor_prices(15, 10)
    print("  %s (r, w) = (%s, %s), then (%s, %s)" % (ok(r1 * w1, 12), r0, w0, r1, w1))
    a, b = v.outputs(60, 40), v.outputs(70, 40)
    print("  %s K 60 -> 70: %s -> %s; chain %s" % (
        ok(b[0], 20), a, b, chain_text({"qy": pct(a[0], b[0]), "K": pct(60, 70),
                                        "qx": pct(a[1], b[1])})))

    print("\nA10.1 and A10.3: steel (2, 1), apparel (1, 1)")
    v = HO(2, 1, 1, 1)
    r0, w0 = v.factor_prices(10, 8)
    r1, w1 = v.factor_prices(12, 8)
    print("  %s (r, w) = (%s, %s), then (%s, %s); chain %s" % (
        ok(r1 + w1, 8), r0, w0, r1, w1,
        chain_text({"r": pct(r0, r1), "py": 20.0, "px": 0.0, "w": pct(w0, w1)})))
    print("  %s real: r/py %s -> %s, r/px %s -> %s, w/py %s -> %s, w/px %s -> %s" % (
        ok(r1 / 12, 1 / 3), r0 / 10, r1 / 12, r0 / 8, r1 / 8, w0 / 10, w1 / 12, w0 / 8, w1 / 8))
    a, b, f = v.outputs(120, 100), v.outputs(140, 100), v.outputs(110, 100)
    print("  %s cone %s; Home %s -> %s; Foreign %s" % (ok(sum(a) + sum(b) + sum(f), 300),
                                                      v.cone(), a, b, f))
    print("      chain %s" % chain_text({"qy": pct(a[0], b[0]), "K": pct(120, 140), "E": 0.0,
                                         "qx": pct(a[1], b[1])}))

    print("\nworkshop 2 problem 3: chemicals (3, 1), textiles (1, 3)")
    v = HO(3, 1, 1, 3)
    r0, w0 = v.factor_prices(8, 8)
    r1, w1 = v.factor_prices(8, 10)
    print("  %s (r, w) = (%s, %s), then (%s, %s); chain %s" % (
        ok(r1 + w1, 4.5), r0, w0, r1, w1,
        chain_text({"w": pct(w0, w1), "px": 25.0, "py": 0.0, "r": pct(r0, r1)})))

    print("\ntariff context: Nordheim, D = 120 - 2p, S = p, world price 20")
    T = tariff(20, 10)
    print("  %s imports %s -> %s; a, b, c, d = %s, %s, %s, %s; consumers lose %s; loss %s" % (
        ok(T["a"] + T["b"] + T["c"] + T["d"], T["consumers"]), T["M0"], T["M1"], T["a"], T["b"],
        T["c"], T["d"], T["consumers"], T["loss"]))
