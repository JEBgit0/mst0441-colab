"""
firms.py - the maths of session 8: firms, tasks and technology (AI).

Pure numbers, like the other session modules. Nothing here knows about widgets.

    producer   the bakery's hiring rule, the monopolist's markup (context:
               bachelor prerequisites, not examined)
    sigma      CES cost minimization with equal weights, the elasticity of
               substitution and labor's share of costs
    tasks      the automation cutoff, task savings and the fixed-weight
               saving index G (Acemoglu 2024)
    review     AI that needs a human to check its work
    frontier   a two-sector PPF tilted by a labor-saving improvement
"""

import math


# ------------------------------------------------------- producer (context) ---

def bakers(p, w, a=20.0, b=2.0):
    # VMP_E = p (a - b E) = w  ->  E = (a - w/p)/b
    return max((a - w / p) / b, 0.0)


def monopoly_linear(intercept, mc):
    # p = intercept - q, MR = intercept - 2q = MC.
    q = (intercept - mc) / 2
    p = intercept - q
    eta = p / q
    return q, p, eta


# ------------------------------------------------------------------ sigma ---

def ratio(w_over_r, sigma):
    # Cost minimization with equal-weight CES: K/E = (w/r)^sigma.
    return w_over_r ** sigma


def labor_share(r_over_w, sigma):
    # wE/(wE + rK) = 1/(1 + (r/w)^(1 - sigma)) with equal weights.
    return 1 / (1 + r_over_w ** (1 - sigma))


def ces_bundle(q, w, r, sigma):
    """Cheapest (E, K) for output q with q = (E^rho/2 + K^rho/2)^(1/rho).

    sigma = 1 is sqrt(EK); "inf" is q = E + K and 0 is min(E, K) (both with
    the notes' unit weights). A tie under perfect substitutes returns None.
    """
    if sigma == math.inf:
        if abs(w - r) < 1e-12:
            return None
        return (q, 0.0) if w < r else (0.0, q)
    if sigma == 0:
        return q, q
    k = ratio(w / r, sigma)                      # K/E
    if abs(sigma - 1) < 1e-12:
        E = q / math.sqrt(k)
    else:
        rho = (sigma - 1) / sigma
        E = q / (0.5 + 0.5 * k ** rho) ** (1 / rho)
    return E, k * E


def sigma_from(pct_ratio, pct_price):
    # The definition with simple percentage changes.
    return pct_ratio / pct_price


# ------------------------------------------------------------------ tasks ---

def cutoff(w, r):
    return r / w


def ai_cost(r, A):
    return r / A


def automated(A, w, r, B=1.0):
    # Strictly cheaper with AI: A/B > r/w. Ties go to labor.
    return A / B > r / w + 1e-12


def saving(A, w, r, B=1.0):
    # pi = max(0, 1 - c/c_H), with c_H = w/B and c_AI = r/A.
    return max(0.0, 1 - (r / A) / (w / B))


def index(As, shares, w, r):
    return sum(s * saving(A, w, r) for A, s in zip(As, shares))


def thresholds(As, w):
    # Task i crosses at r_i = w A_i.
    return [w * A for A in As]


# ----------------------------------------------------------------- review ---

def review_costs(w, h, f, t):
    # Human-only w h against AI fee plus review, f + w t.
    return w * h, f + w * t


def max_review(w, h, f):
    # AI weakly cheaper while f + w t <= w h.
    return h - f / w


def breakeven_wage(h, f, t):
    # f + w t = w h  ->  w = f/(h - t); none if review saves no hours.
    return f / (h - t) if h > t else math.inf


# --------------------------------------------------------------- frontier ---

def frontier(aX, aY, L):
    # Intercepts and the absolute slope (opportunity cost of X in Y).
    return aX * L, aY * L, aY / aX


def improved(a, pi):
    # Labor per unit falls by pi: output per worker rises by 1/(1 - pi).
    return a / (1 - pi)


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-9: "ok " if abs(got - want) < tol else "FAIL"
    F = lambda x: str(x if abs(x - round(x)) > 1e-9 else round(x))

    print("context: bakery %s and %s bakers; monopoly %s" % (bakers(60, 600), bakers(60, 480),
                                                             monopoly_linear(12, 4)))
    E, K = ces_bundle(4, 10, 10, 1)
    print("  %s cost-min P = (%s, %s), cost %s; A, B cost %s, %s" % (
        ok(10 * E + 10 * K, 80), F(E), F(K), 10 * E + 10 * K, 10 * 2 + 10 * 8, 10 * 8 + 10 * 2))
    E, K = ces_bundle(4, 1, 4, 1)
    print("  %s w/r = 1/4 -> B = (%s, %s)" % (ok(E, 8), F(E), F(K)))

    print("\nsigma and shares")
    print("  %s labor share at r/w = 1/4: sigma 2 -> %s, sigma 1/2 -> %s" % (
        ok(labor_share(.25, 2) + labor_share(.25, .5), 1 / 5 + 2 / 3), labor_share(.25, 2),
        labor_share(.25, .5)))
    print("  %s review Q3: sigma %s; rK/wE changes %.4f%% exactly, about %s%%" % (
        ok(sigma_from(15, 10), 1.5), sigma_from(15, 10), 100 * (1.15 / 1.10 - 1), (1.5 - 1) * 10))

    print("\ntasks")
    As = (4, 2, 1)
    print("  %s Try it: AI costs %s, cutoff %s, automated %s" % (
        ok(cutoff(300, 600), 2), [ai_cost(600, A) for A in As], cutoff(300, 600),
        [automated(A, 300, 600) for A in As]))
    print("  %s review Q2 at r = 450: AI costs %s, automated %s" % (
        ok(ai_cost(450, 2), 225), [ai_cost(450, A) for A in As], [automated(A, 300, 450) for A in As]))
    As, ch = (10, 5, 1), (.2, .4, .4)
    print("  %s Nordvik: G(1000) = %s, G(100) = %s, thresholds %s" % (
        ok(index(As, ch, 500, 1000) + index(As, ch, 500, 100), .4 + .9),
        index(As, ch, 500, 1000), index(As, ch, 500, 100), thresholds(As, 500)))
    As, ch = (2, 1, .5), (.25, .5, .25)
    print("  %s Kyst: cutoff %s, automated %s, G(2) = %s, G(1) = %s, thresholds %s" % (
        ok(index(As, ch, 3, 2) + index(As, ch, 3, 1), 1 / 3 + 5 / 8), cutoff(3, 2),
        [automated(A, 3, 2) for A in As], index(As, ch, 3, 2), index(As, ch, 3, 1),
        thresholds(As, 3)))
    As, ch = (3, 2, 1), (.5, .25, .25)
    G3, G15 = index(As, ch, 2, 3), index(As, ch, 2, 1.5)
    print("  %s worksheet/Fjordline: savings %s, G(3) = %s = 5/16, cost %s; G(1.5) = %s = 19/32, cost %s" % (
        ok(G3 + G15, 5 / 16 + 19 / 32), [saving(A, 2, 3) for A in As], G3, 160 * (1 - G3), G15,
        160 * (1 - G15)))
    print("  %s kinks: G at 6, 4, 2 = %s, %s, %s (want 0, 1/6, 11/24); limit %s" % (
        ok(index(As, ch, 2, 2), 11 / 24), index(As, ch, 2, 6), index(As, ch, 2, 4),
        index(As, ch, 2, 2), index(As, ch, 2, 1e-9)))
    old = sum(s * (saving(A, 2, 1.5) - saving(A, 2, 3)) for A, s in zip(As[:2], ch[:2]))
    print("  %s Fjordline (e): already automated %s = 7/32, new %s = 1/16" % (
        ok(old, 7 / 32), old, ch[2] * saving(1, 2, 1.5)))
    print("  %s Acemoglu: %.6f, then %.6f" % (ok(.046 * round(.27 * .535, 3), .006624),
                                             .046 * round(.27 * .535, 3), .033 * .144 + .013 * .037))

    print("\nreview (Harbor, w = 30)")
    h, f, t = (1, .5, .8), (6, 3, 9), (.2, .5, .1)
    costs = [review_costs(30, *x) for x in zip(h, f, t)]
    n = (10, 20, 10)
    chosen = sum(k * min(c) for k, c in zip(n, costs))
    print("  %s costs %s; max review %s; weekly %s -> %s" % (
        ok(chosen, 540), costs, max_review(30, 1, 6), sum(k * c[0] for k, c in zip(n, costs)), chosen))
    half = [review_costs(30, a, b / 2, c) for a, b, c in zip(h, f, t)]
    print("  %s fees halved: %s -> %s; w = 40: %s; notes report %s, %s" % (
        ok(sum(k * min(c) for k, c in zip(n, half)), 465), half,
        sum(k * min(c) for k, c in zip(n, half)), [review_costs(40, *x) for x in zip(h, f, t)],
        review_costs(300, 1, 60, .25), review_costs(300, 1, 60, .9)))

    print("\nfrontier")
    print("  %s ten workers: before %s, after %s; review Q6 factor %s" % (
        ok(improved(2, .2), 2.5), frontier(2, 3, 10), frontier(improved(2, .2), 3, 10),
        improved(1, .25)))
