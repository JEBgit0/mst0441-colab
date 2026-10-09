"""
sandbox_w01.py - workshop 1 sandbox: the first mock exam, with every number shown.

    sunniva  Problem 1  the budget, the price cut and the optimum (session 2's
                        goods lab with the paper's numbers)
    trade    Problem 2  Home and Foreign in the Edgeworth box (session 6's
                        market lab, with room for the paper's endowments)
    air      Problem 3  pollution without a price, and with tradable rights
                        (session 7's smoke lab)

Released with the workshop 1 solutions. Nothing new is computed here: the labs
and the maths are the ones from sessions 2, 6 and 7.
"""

from sandbox_s02 import GoodsLab
from sandbox_s06 import WORKED, MarketLab
from sandbox_s07 import FREE_A, MARKET_A, TRY, SmokeLab

# ======================================================================
# Problem 1: Sunniva
# ======================================================================

SUNNIVA = dict(family="Cobb-Douglas", p1=3.0, p2=1.0, m=900.0, a=0.5, b=0.5)
NAMES = ("x", "y")


class SunnivaLab(GoodsLab):
    TITLE = "Problem 1 &middot; Sunniva's trips"
    INTRO = ("Trips x across and the basket y up, with 900 to spend. The paper's "
             "u = x<sup>&alpha;</sup>y<sup>1 &minus; &alpha;</sup> is Cobb&ndash;Douglas with "
             "weights that sum to one: set &alpha; and &beta; = 1 &minus; &alpha;.")
    SLIDERS = [(k, lo, hi, st, SUNNIVA[k], f) for k, lo, hi, st, _, f in GoodsLab.SLIDERS]
    PRESETS = [
        dict(label="1(a)–(b) a trip costs 3", kind="problem", names=NAMES, values=SUNNIVA),
        dict(label="1(c), 1(e) a trip costs 2", kind="problem", names=NAMES, before=SUNNIVA,
             values=dict(SUNNIVA, p1=2.0)),
        dict(label="α = 1/4: fewer trips, same pivot", kind="extra", names=NAMES,
             before=dict(SUNNIVA, a=0.25, b=0.75), values=dict(SUNNIVA, p1=2.0, a=0.25, b=0.75)),
    ]

    def __init__(self):
        super().__init__()
        self.names = NAMES


# ======================================================================
# Problem 2: Home and Foreign
# ======================================================================

# Home is A and Foreign is B. The marked allocation starts at the equilibrium.
TRADE = dict(WORKED, a=0.5, b=1 / 3, wAx=10.0, wAy=60.0, wBx=30.0, wBy=60.0, p=2.0,
             xp=20.0, yp=40.0)


class TradeLab(MarketLab):
    TITLE = "Problem 2 &middot; Home and Foreign"
    INTRO = ("Home is A, in the south-west corner, and Foreign is B. Trips are good x and the "
             "basket is good y, the numeraire. The box is 40 wide and 120 tall, and it is "
             "drawn to scale, so it is narrow.")
    SLIDERS = [(k, lo, 150.0 if k.startswith("w") or k in ("xp", "yp") else hi, st, TRADE[k], f)
               for k, lo, hi, st, _, f in MarketLab.SLIDERS]
    PRESETS = [
        dict(label="2(b) the endowment and the lens", kind="problem", values=TRADE,
             flags=dict(lens=True)),
        dict(label="2(c) the market clears", kind="problem", values=TRADE),
        dict(label="2(c) a trip at 1: too cheap", kind="problem", values=dict(TRADE, p=1.0),
             flags=dict(manual=True)),
        dict(label="2(d) the MRSs at the equilibrium", kind="problem", values=TRADE,
             flags=dict(point=True)),
    ]


# ======================================================================
# Problem 3: pollution
# ======================================================================

# The paper gives no utility functions. These are the session 7 notes' own:
# pollution is the notes' smoke S, and clean air is 1 - S.
AIR = dict(TRY, regime=FREE_A)


class AirLab(SmokeLab):
    TITLE = "Problem 3 &middot; Pollution"
    INTRO = ("Country A pollutes and country B breathes: pollution P is the smoke S of "
             "session 7, measured from A's corner, and clean air is C = 1 &minus; S. The "
             "paper gives no utility functions, so the numbers here are the session 7 notes' "
             "own. Compare the two regimes, not the numbers.")
    PRESETS = [
        dict(label="3(a) no rule of law: A pollutes", kind="problem", values=AIR),
        dict(label="3(b) A holds the rights, quotas traded", kind="problem", before=AIR,
             values=dict(AIR, regime=MARKET_A)),
    ]


sunniva = SunnivaLab()
trade = TradeLab()
air = AirLab()
