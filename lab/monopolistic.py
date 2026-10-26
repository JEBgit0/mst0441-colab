"""
monopolistic.py - the maths of session 11: monopolistic competition, gravity
and trade policy.

Pure numbers, like the other session modules. Nothing here knows about widgets.

    iit         the intra-industry trade index
    markup      markup pricing and free entry for one firm: price, the
                elasticity a price reveals, zero-profit output, the fixed cost
    industry    the free-entry equilibrium of an industry with constant
                elasticity: price, firm scale, units sold and varieties
    ppzz        Krugman's labor-only economy: the PP and ZZ conditions, and
                the number of varieties N = 1/((alpha/E) + beta c)
    gravity     frictionless gravity, a gravity line with given elasticities,
                the iceberg factor read off a trade shortfall, and the
                border-effect size arithmetic
    tariff      the large country's import market, linear, and the optimum
                tariff (context: not examinable)

Notation follows the notes: sigma is the elasticity of substitution between
varieties, which with many firms is each firm's demand elasticity; MC is
marginal cost and F the fixed cost; alpha and beta are the fixed and marginal
labor requirements and E the labor force.
"""

import math


# -------------------------------------------------------------------- iit ---

def iit(X, M):
    # 1 - |X - M| / (X + M): 0 for one-way trade, 1 when exports equal imports.
    return 1.0 - abs(X - M) / (X + M) if X + M > 0 else 0.0


# ----------------------------------------------------------------- markup ---

def markup(sigma):
    # The markup factor p/MC = sigma/(sigma - 1).
    return sigma / (sigma - 1.0)


def price(mc, sigma):
    return mc * markup(sigma)


def elasticity(p, mc):
    # The elasticity a price tag reveals: p/MC = eta/(eta - 1) -> eta = p/(p - MC).
    return p / (p - mc)


def zero_profit_output(F, p, mc):
    # Free entry, p = AC = MC + F/q: the markup earnings cover the fixed cost.
    return F / (p - mc)


def fixed_cost(p, mc, q):
    return (p - mc) * q


def industry(sigma, mc, F, spending):
    """The free-entry equilibrium of an industry with constant elasticity.

    Price is the constant markup over MC, firm scale comes from zero profit,
    and spending at that price buys Q units, made by n = Q/q firms, one
    variety each.
    """
    p = price(mc, sigma)
    q = zero_profit_output(F, p, mc)
    Q = spending / p
    return dict(p=p, markup=markup(sigma), q=q, Q=Q, n=Q / q, AC=mc + F / q)


# ------------------------------------------------------------------- ppzz ---

def zz(c, E, alpha, beta):
    # Zero profit, p/w = AC/w = alpha/(E c) + beta: falls with c.
    return alpha / (E * c) + beta


def pp_ces(sigma, beta):
    # Markup pricing with a constant elasticity: p/w = beta sigma/(sigma - 1),
    # flat in c.
    return beta * markup(sigma)


def ppzz(E, alpha, beta, sigma):
    # Where the flat PP meets ZZ: c = alpha (sigma - 1)/(E beta), and then
    # firm output y = E c, the number of varieties N = 1/((alpha/E) + beta c).
    c = alpha * (sigma - 1.0) / (E * beta)
    N = 1.0 / (alpha / E + beta * c)
    return dict(c=c, pw=pp_ces(sigma, beta), y=E * c, N=N)


def ces_scale(sigma, alpha, beta):
    # Firm output pinned down by the constant markup: y = (sigma - 1) alpha/beta.
    return (sigma - 1.0) * alpha / beta


def varieties(E, alpha, beta, y):
    # Full employment, E = N (alpha + beta y).
    return E / (alpha + beta * y)


# ---------------------------------------------------------------- gravity ---

def gravity(Yi, Yj, Yw):
    # Frictionless gravity: X_ij = Y_i Y_j / Y_w.
    return Yi * Yj / Yw


def gravity_factor(fYi=1.0, fYj=1.0, fd=1.0, bi=1.0, bj=1.0, rho=1.0):
    # How trade moves when exporter GDP, importer GDP and distance are scaled
    # by fYi, fYj and fd, with elasticities bi, bj and -rho.
    return fYi ** bi * fYj ** bj / fd ** rho


def iceberg(actual, predicted, sigma):
    # Trade scales with T^(1 - sigma): T = (actual/predicted)^(1/(1 - sigma)).
    return (actual / predicted) ** (1.0 / (1.0 - sigma))


def border_sizes(small_home=0.1, big_home=0.9, keep=0.5):
    """The size arithmetic behind Anderson and van Wincoop.

    Without frictions the small country sells small_home of its GDP at home
    and the rest abroad, the big one big_home. A border keeps only the share
    keep of cross-border trade, and the displaced exports are sold at home.
    The measured border effect is internal/cross-border after over before.
    """
    out = {}
    for name, home in (("small", small_home), ("big", big_home)):
        abroad = 1.0 - home
        after_abroad = keep * abroad
        after_home = 1.0 - after_abroad
        out[name] = dict(before=(home, abroad), after=(after_home, after_abroad),
                         factor=(after_home / after_abroad) / (home / abroad))
    return out


# ------------------------------------------------------- tariff (context) ---

def optimum_tariff(inverse_elasticity):
    # Johnson's formula, t = 1/eps*: the inverse export-supply elasticity.
    return inverse_elasticity


def large_tariff(A, B, t):
    """A large importer: import demand M = A - p, foreign export supply X* = B p*.

    A specific tariff t drives p = p* + t. Free trade clears at p0 = A/(1 + B).
    e is the part of the revenue foreigners pay through the lower world price,
    b + d the deadweight triangle, and the change in welfare is e - (b + d).
    """
    p0 = A / (1.0 + B)
    pstar = max((A - t) / (1.0 + B), 0.0)
    p = pstar + t if pstar > 0 else A
    M0, M1 = A - p0, max(A - p, 0.0)
    out = dict(p0=p0, M0=M0, p=p, pstar=pstar, M1=M1, t=p - pstar)
    out["revenue"] = (p - pstar) * M1
    out["e"] = (p0 - pstar) * M1
    out["home_paid"] = (p - p0) * M1
    out["bd"] = (p - p0) * (M0 - M1) / 2
    out["foreign_loss"] = (p0 - pstar) * (M0 - M1) / 2
    out["dW"] = out["e"] - out["bd"]
    return out


def best_large_tariff(A, B):
    # dW/dt = 0 gives t = A/(2 + B). Then p* = t as well, so the ad valorem
    # rate t/p* is 1: Johnson's 1/eps*, since supply through the origin has
    # eps* = 1 at every price.
    return A / (2.0 + B)


# ------------------------------------------------------------- self-check ---

if __name__ == "__main__":
    ok = lambda got, want, tol=1e-9: "ok " if abs(got - want) < tol else "FAIL"

    print("IIT: Nordmark vehicles %s, wheat %s" % (iit(80, 40), iit(50, 0)))

    print("\nTry it: MC = 8")
    print("  %s Fjordline eta = 5: p = %s, markup %s" % (ok(price(8, 5), 10), price(8, 5), markup(5)))
    print("  %s Nordvik charges 12: eta = %s" % (ok(elasticity(12, 8), 3), elasticity(12, 8)))
    print("  %s fixed cost at 200 units: %s" % (ok(fixed_cost(10, 8, 200), 400), fixed_cost(10, 8, 200)))

    print("\nworksheet task 2: MC 5, F 150")
    for s in (6, 2):
        p = price(5, s)
        print("  %s sigma %s: p = %s, markup %s, q = %s" % (
            ok(zero_profit_output(150, p, 5) * (p - 5), 150), s, p, markup(s),
            zero_profit_output(150, p, 5)))

    print("\nreview Q2: Arland, MC 4, F 100")
    for s in (3, 5):
        p = price(4, s)
        print("  %s sigma %s: p = %s, markup %s, q = %s" % (
            ok(zero_profit_output(100, p, 4) * (p - 4), 100), s, p, markup(s),
            zero_profit_output(100, p, 4)))

    print("\nA11.1: Nordia, sigma 4, MC 6, F 200")
    a, b = industry(4, 6, 200, 16000), industry(4, 6, 200, 32000)
    print("  %s autarky %s" % (ok(a["n"], 20), a))
    print("  %s integrated %s" % (ok(b["n"], 40), b))

    print("\nworksheet PP-ZZ: alpha 4, beta 1, sigma 2")
    print("  ZZ at c = 1/16, 1/8, 1/4, 1/2: %s" % [zz(c, 32, 4, 1) for c in (1 / 16, 1 / 8, 1 / 4, 1 / 2)])
    a, b = ppzz(32, 4, 1, 2), ppzz(64, 4, 1, 2)
    print("  %s E = 32: %s" % (ok(a["N"], 4), a))
    print("  %s E = 64: %s" % (ok(b["N"], 8), b))

    print("\nreview Q3: CES, sigma 3, alpha 20, beta 1, E 6000")
    y = ces_scale(3, 20, 1)
    print("  %s y = %s, N = %s" % (ok(varieties(6000, 20, 1, y), 100), y, varieties(6000, 20, 1, y)))

    print("\ngravity")
    print("  %s Try it: %s, then %s; T = %s" % (
        ok(iceberg(10, 40, 3), 2), gravity(1000, 600, 15000), gravity(2000, 1200, 30000),
        iceberg(10, 40, 3)))
    print("  %s A11.2: GDP doubles %s, distance triples %s" % (
        ok(gravity_factor(fYj=2) * gravity_factor(fd=3), 2 / 3), gravity_factor(fYj=2),
        gravity_factor(fd=3)))
    print("  %s review Q4: GDP alone %s, all three %s" % (
        ok(gravity_factor(1.5, 4 / 3, 2), 1), gravity_factor(1.5, 4 / 3), gravity_factor(1.5, 4 / 3, 2)))
    print("  %s workshop 2 MC 7: %s" % (ok(gravity_factor(3, 2, 3), 2), gravity_factor(3, 2, 3)))
    print("  Vestland: %s; Naboria predicted %s" % ([g / 200 for g in (200, 400, 800, 1600)], 400 / 200))
    B = border_sizes()
    print("  %s borders: small %s, big %s; McCallum e^3.09 = %s" % (
        ok(B["small"]["factor"], 11), B["small"], B["big"], math.exp(3.09)))

    print("\nlarge-country tariff (context)")
    t = best_large_tariff(100, 1)
    T = large_tariff(100, 1, t)
    print("  %s A = 100, B = 1: best t = %s, p* = %s, so t/p* = %s = 1/eps* = 1/1" % (
        ok(T["t"] / T["pstar"], 1, 1e-4), t, T["pstar"], T["t"] / T["pstar"]))
