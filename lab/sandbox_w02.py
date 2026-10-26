"""
sandbox_w02.py - workshop 2 sandbox: the second mock exam, with every number shown.

    saltdal  Problem 1  which tasks go to AI, and the saving index (session 8's
                        task lab, with four tasks)
    trade    Problem 2  bicycles and grain: frontiers and the gains from trade
                        (session 9's trade lab)
    wages    Problem 2  wages and unit costs (session 9's wage lab)
    factors  Problem 3  chemicals and textiles: Stolper-Samuelson (session
                        10's price lab)
    boards   Problem 4  board games under monopolistic competition (session
                        11's entry lab; the paper gives no numbers)

Released with the workshop 2 solutions. Nothing new is computed here: the
labs and the maths are the ones from sessions 8 to 11.
"""

from sandbox_s08 import TaskLab
from sandbox_s09 import TradeLab, WageLab
from sandbox_s10 import PriceLab
from sandbox_s11 import EntryLab

# ======================================================================
# Problem 1: Saltdal Freight
# ======================================================================

SALTDAL = dict(w=400.0, r=800.0, A1=4.0, A2=2.0, A3=1.25, A4=0.5, x1=0.3, x2=0.25, x3=0.3,
               x4=0.15, C0=200000.0)


class SaltdalLab(TaskLab):
    TASKS = 4
    TITLE = "Problem 1 &middot; Saltdal Freight"
    INTRO = ("Four tasks per shipment. A worker-hour makes one task-unit at w = 400 kroner; an "
             "AI-service unit costs r and makes A<sub>i</sub> task-units. AI wins a task when "
             "r/A<sub>i</sub> &lt; w, and ties stay with labor. The saving index G weights each "
             "task's saving by its cost share &chi;<sub>i</sub>.")
    SLIDERS = [
        ("w", 50.0, 800.0, 10.0, 400.0, ".0f"),
        ("r", 50.0, 2000.0, 10.0, 800.0, ".0f"),
        ("A1", 0.25, 6.0, 0.25, 4.0, ".2f"),
        ("A2", 0.25, 6.0, 0.25, 2.0, ".2f"),
        ("A3", 0.25, 6.0, 0.25, 1.25, ".2f"),
        ("A4", 0.25, 6.0, 0.25, 0.5, ".2f"),
        ("x1", 0.0, 1.0, 0.05, 0.3, ".2f"),
        ("x2", 0.0, 1.0, 0.05, 0.25, ".2f"),
        ("x3", 0.0, 1.0, 0.05, 0.3, ".2f"),
        ("x4", 0.0, 1.0, 0.05, 0.15, ".2f"),
        ("C0", 0.0, 400000.0, 10000.0, 200000.0, ".0f"),
    ]
    PRESETS = [
        dict(label="1(a)–(b) r = 800", kind="problem", values=SALTDAL),
        dict(label="1(c) r = 600", kind="problem", before=SALTDAL, values=dict(SALTDAL, r=600.0)),
        dict(label="Route planning's tie, r = 500", kind="extra", values=dict(SALTDAL, r=500.0)),
    ]

    def task_names(self):
        return ["customs", "invoicing", "routes", "calls"]


# ======================================================================
# Problem 2: bicycles and grain
# ======================================================================

BIKES = dict(ax=4.0, ay=2.0, E=24.0, axf=3.0, ayf=1.0, Ef=15.0, p=2.5, s=0.5, sf=0.5)
NAMES = dict(goods=("bicycles", "grain"), lands=("Home", "Foreign"))
BIKE_PRESETS = [
    dict(label="2(a)–(b) autarky price 2 at Home", kind="problem", values=dict(BIKES, p=2.0),
         **NAMES),
    dict(label="2(c)–(d) free trade, p = 5/2", kind="problem", values=BIKES,
         flags=dict(clear=True), **NAMES),
    dict(label="Tastes tilt to bicycles", kind="extra", before=BIKES,
         values=dict(BIKES, s=0.6, sf=0.6), flags=dict(clear=True), **NAMES),
]


def _paper_sliders(sliders):
    # The paper's labor forces need whole numbers, not the session's steps of 10.
    return [(k, 1.0, 120.0, 1.0, v, ".0f") if k in ("E", "Ef") else (k, lo, hi, st, v, f)
            for k, lo, hi, st, v, f in sliders]


class BicycleTradeLab(TradeLab):
    TITLE = "Problem 2 &middot; Bicycles and grain: frontiers and trade"
    SLIDERS = _paper_sliders(TradeLab.SLIDERS)
    PRESETS = BIKE_PRESETS

    def __init__(self):
        super().__init__()
        self.goods, self.lands = NAMES["goods"], NAMES["lands"]


class BicycleWageLab(WageLab):
    TITLE = "Problem 2 &middot; Wages and unit costs"
    SLIDERS = _paper_sliders(WageLab.SLIDERS)
    PRESETS = BIKE_PRESETS[1:]

    def __init__(self):
        super().__init__()
        self.goods, self.lands = NAMES["goods"], NAMES["lands"]


# ======================================================================
# Problem 3: chemicals and textiles
# ======================================================================

CHEM = dict(aKy=3.0, aEy=1.0, aKx=1.0, aEx=3.0, py=8.0, px=8.0)
CHEM_GOODS = ("chemicals", "textiles")


class ChemicalsLab(PriceLab):
    TITLE = "Problem 3 &middot; Chemicals and textiles"
    NAMES = CHEM_GOODS
    PRESETS = [
        dict(label="3(a) p = (8, 8)", kind="problem", values=CHEM, goods=CHEM_GOODS),
        dict(label="3(b) textiles at 10", kind="problem", before=CHEM,
             values=dict(CHEM, px=10.0), goods=CHEM_GOODS),
        dict(label="Chemicals at 10 instead", kind="extra", before=CHEM,
             values=dict(CHEM, py=10.0), goods=CHEM_GOODS),
    ]


# ======================================================================
# Problem 4: board games
# ======================================================================

# The paper gives no numbers, so these are problem A11.1's.
BOARDS = dict(sigma=4.0, MC=6.0, F=200.0, S=16000.0)


class BoardLab(EntryLab):
    TITLE = "Problem 4 &middot; Board games"
    INTRO = ("Nordøy and Sørøy are identical, and the paper gives no numbers, so these are "
             "problem A11.1's. Opening trade between two identical countries doubles spending "
             "on the industry. With a constant elasticity the markup cannot move: watch which "
             "numbers change and which do not.")
    PRESETS = [
        dict(label="Nordøy alone (A11.1's numbers)", kind="extra", values=BOARDS),
        dict(label="Nordøy and Sørøy trade", kind="extra", before=BOARDS,
             values=dict(BOARDS, S=32000.0)),
    ]


saltdal = SaltdalLab()
trade = BicycleTradeLab()
wages = BicycleWageLab()
factors = ChemicalsLab()
boards = BoardLab()
