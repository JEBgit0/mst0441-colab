"""
sandbox_s09.py - session 9 sandbox: comparative advantage, the Ricardian model.

    trade   Lab 1  two frontiers, autarky, specialization and the gains from
                   trade: points A, B and C in each country
    supply  Lab 2  the world relative supply staircase and relative demand
    wages   Lab 3  wages, unit costs and the competitiveness cutoff
    tariff  Lab 4  the small-country tariff and its four areas (context: not
                   examinable)

Released with the session 9 solutions. The maths is ricardo.py.
"""

import numpy as np

import ricardo as rc
from ricardo import FOREIGN, HOME
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, GREEN, INK, LINE, MUTE, NEW

BOTH = (HOME, FOREIGN)


# ======================================================================
# The economy the first three labs share
# ======================================================================

RUN = dict(ax=1.0, ay=2.0, E=100.0, axf=6.0, ayf=3.0, Ef=180.0, p=1.0, s=0.6, sf=0.6)
# A share of 5/8 on cloth makes the worksheet economy clear at p = 2/3.
SHEET = dict(ax=4.0, ay=5.0, E=20.0, axf=1.0, ayf=2.0, Ef=10.0, p=2 / 3, s=0.625, sf=0.625)
# Tastes chosen so that the review question's bundles (260, 40) and (40, 20),
# and the bundles (500, 100) and (100, 100) of the guided page, clear at p = 1.
VIN = dict(ax=1.0, ay=3.0, E=300.0, axf=6.0, ayf=4.0, Ef=240.0, p=1.0, s=13 / 15, sf=2 / 3)
NOR = dict(ax=2.0, ay=4.0, E=1200.0, axf=12.0, ayf=6.0, Ef=1200.0, p=1.0, s=5 / 6, sf=0.5)

NOTES_NAMES = dict(goods=("cloth", "wine"), lands=("Home", "Foreign"))
VIN_NAMES = dict(goods=("timber", "glass"), lands=("Vinland", "Estland"))
NOR_NAMES = dict(goods=("salmon", "textiles"), lands=("Norway", "Portugal"))

PRESETS = [
    dict(label="Notes p. 3 running example", kind="notes", values=RUN, **NOTES_NAMES),
    dict(label="Notes p. 4 twice as productive", kind="notes", before=RUN,
         values=dict(RUN, ax=0.5, ay=1.0), **NOTES_NAMES),
    dict(label="Notes p. 9 the market clears", kind="notes", values=RUN,
         flags=dict(clear=True), **NOTES_NAMES),
    dict(label="Notes p. 11 Try it, p = 3/2", kind="notes", before=RUN,
         values=dict(RUN, p=1.5), **NOTES_NAMES),
    dict(label="Worksheet, p = 2/3", kind="notes", values=SHEET, **NOTES_NAMES),
    dict(label="Worksheet task 3: a very large Home", kind="notes",
         values=dict(SHEET, E=1200.0), flags=dict(clear=True), **NOTES_NAMES),
    dict(label="Review Q2–5 Vinland and Estland", kind="notes", values=VIN, **VIN_NAMES),
    dict(label="A9.1 Norway and Portugal", kind="problem", values=NOR, **NOR_NAMES),
    dict(label="A9.1 (d) the edge of the range, p = 1/2", kind="problem",
         values=dict(NOR, p=0.5), **NOR_NAMES),
]


def model(v):
    return rc.Ricardo(v["ax"], v["ay"], v["E"], v["axf"], v["ayf"], v["Ef"])


def country_state(r, c, p, s):
    X, Y, pa = r.frontier(c)
    A = r.demand(c, pa, s)                       # autarky: consume what you make
    B = r.output(c, p)
    C = r.demand(c, p, s)
    return dict(X=X, Y=Y, pa=pa, A=A, B=B if B is not None else C, mix=B is None, C=C,
                m=r.income(c, p), w=r.wage(c, p), costs=r.costs(c, p), s=s,
                need=r.labor(c, *C), E=r.E[c])


def ic(ax, s, x0, y0, xmax, **kw):
    # The indifference curve of u = x^s y^(1-s) through (x0, y0).
    if x0 <= 0 or y0 <= 0:
        return
    xs = np.linspace(xmax * 0.02, xmax, 300)
    ax.plot(xs, (x0 ** s * y0 ** (1 - s) / xs ** s) ** (1 / (1 - s)), **kw)


def point(t):
    return "(%s, %s)" % (num(t[0]), num(t[1]))


class RicardoLab(Lab):
    """What the first three labs share: the sliders, the presets and the names."""

    SLIDERS = [
        ("ax", 0.5, 12.0, 0.5, 1.0, ".1f"),
        ("ay", 0.5, 12.0, 0.5, 2.0, ".1f"),
        ("E", 10.0, 1200.0, 10.0, 100.0, ".0f"),
        ("axf", 0.5, 12.0, 0.5, 6.0, ".1f"),
        ("ayf", 0.5, 12.0, 0.5, 3.0, ".1f"),
        ("Ef", 10.0, 1200.0, 10.0, 180.0, ".0f"),
        ("p", 0.05, 4.0, 0.01, 1.0, ".2f"),
        ("s", 0.05, 0.95, 0.01, 0.6, ".2f"),
        ("sf", 0.05, 0.95, 0.01, 0.6, ".2f"),
    ]
    CHECKS = [("clear", "Let the market set the price (ignore slider p)")]
    PRESETS = PRESETS

    def __init__(self):
        super().__init__()
        self.goods, self.lands = NOTES_NAMES["goods"], NOTES_NAMES["lands"]

    def on_preset(self, preset):
        self.goods, self.lands = preset["goods"], preset["lands"]

    def relabel(self):
        (x, y), (home, foreign) = self.goods, self.lands
        html_label(self.w["ax"], "a<sub>x</sub>: %s, %s" % (home, x))
        html_label(self.w["ay"], "a<sub>y</sub>: %s, %s" % (home, y))
        html_label(self.w["E"], "E: %s's labor" % home)
        html_label(self.w["axf"], "a<sub>x</sub>*: %s, %s" % (foreign, x))
        html_label(self.w["ayf"], "a<sub>y</sub>*: %s, %s" % (foreign, y))
        html_label(self.w["Ef"], "E*: %s's labor" % foreign)
        self.w["p"].description = "World price p"
        self.w["p"].disabled = self.flag("clear")
        html_label(self.w["s"], "%s's share on %s" % (home, x))
        html_label(self.w["sf"], "%s's share on %s" % (foreign, x))

    def state(self, v, clear):
        r = model(v)
        pstar = r.clearing(v["s"], v["sf"])
        p = pstar if clear else v["p"]
        lo, hi = r.range()
        return dict(r=r, p=p, pstar=pstar, lo=lo, hi=hi, inside=lo < p < hi,
                    home=country_state(r, HOME, p, v["s"]),
                    foreign=country_state(r, FOREIGN, p, v["sf"]))

    def compute(self):
        st = self.state(self.values(), self.flag("clear"))
        st["before"] = self.state(self.before, False) if self.before else None
        return st

    def name(self, c):
        return self.lands[0] if c == HOME else self.lands[1]

    # -- sentences the three readouts share --------------------------------------
    def advantage_text(self, r):
        (x, y) = self.goods
        absolute = []
        for good, g in ((0, x), (1, y)):
            who = r.absolute(good)
            absolute.append("%s: %s" % (g, self.name(who) if who else "a tie"))
        who = r.exporter_x()
        if who is None:
            comparative = ("the two autarky prices are equal, so nobody has a comparative "
                           "advantage and there is nothing to gain from trade")
        else:
            comparative = "%s in %s, %s in %s" % (self.name(who), x, self.name(r.other(who)), y)
        return "Absolute: %s. Comparative: %s." % ("; ".join(absolute), comparative)

    def range_text(self, st):
        lo, hi, p = st["lo"], st["hi"], st["p"]
        text = "Both want to trade for %s &lt; p &lt; %s. " % (num(lo), num(hi))
        if st["inside"]:
            return text + "p = %s is inside: each country makes one good only." % num(p)
        if abs(p - lo) < 1e-9 or abs(p - hi) < 1e-9:
            who = [c for c in BOTH if abs(st["r"].autarky(c) - p) < 1e-9]
            return text + ("p = %s is %s's own autarky price: it can make any mix and gains "
                           "nothing from trade." % (num(p), " and ".join(self.name(c) for c in who)))
        return text + ("p = %s is outside: both countries want to make the same good, so this "
                       "price cannot clear the market." % num(p))


# ======================================================================
# Lab 1: frontiers and the gains from trade
# ======================================================================

class TradeLab(RicardoLab):
    TITLE = "Lab 1 &middot; Frontiers and the gains from trade"
    INTRO = ("Two countries, two goods, labor the only factor. a is the labor needed per unit "
             "and E the labor force, so a frontier runs from E/a<sub>x</sub> to "
             "E/a<sub>y</sub>. Each country consumes at A under autarky; at the world price p "
             "it produces at B and trades along the dashed line to C. Tastes are "
             "Cobb&ndash;Douglas: a fixed share of income goes to good x.")
    FIGSIZE = (8.6, 4.4)

    def figure(self, fig, st):
        (x, y) = self.goods
        axes = fig.subplots(1, 2)
        for ax, c, key in zip(axes, BOTH, ("home", "foreign")):
            s = st[key]
            style_axes(ax)
            if st["before"] is not None:
                b = st["before"][key]
                ax.plot([0, b["X"]], [b["Y"], 0], color=BEFORE, lw=1.4, ls="--", label="before")
            ax.plot([0, s["X"]], [s["Y"], 0], color=LINE, lw=2, label="frontier")
            ax.plot([0, s["m"] / st["p"]], [s["m"], 0], color=NEW, lw=1.5, ls="--",
                    label="world price line")
            xmax = self.stick(key + "x", max(s["X"], s["m"] / st["p"]) * 1.06)
            ymax = self.stick(key + "y", max(s["Y"], s["m"]) * 1.06)
            ic(ax, s["s"], *s["A"], xmax, color=CURVE, lw=1, alpha=0.6)
            ic(ax, s["s"], *s["C"], xmax, color=CURVE, lw=1.5)
            for name, pt, colour, dx in (("A", s["A"], MUTE, -12), ("B", s["B"], NEW, 6),
                                         ("C", s["C"], GREEN, 6)):
                ax.plot([pt[0]], [pt[1]], "o", color=colour, ms=7, zorder=6, clip_on=False)
                ax.annotate(name, pt, textcoords="offset points", xytext=(dx, 6), color=colour,
                            fontsize=10)
            ax.set_xlim(0, xmax)
            ax.set_ylim(0, ymax)
            ax.set_xlabel(x, color=INK, fontsize=9, loc="right")
            ax.set_ylabel(y, color=INK, fontsize=9, loc="top")
            ax.set_title(self.name(c), loc="left", color=INK, fontsize=9.5)
        legend(axes[0])
        fig.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.12, wspace=0.2)

    def describe(self, st):
        (x, y), r, p = self.goods, st["r"], st["p"]
        rows = []
        for c, key in zip(BOTH, ("home", "foreign")):
            s = st[key]
            rows.append((self.name(c), "Frontier from %s %s to %s %s, absolute slope %s: one more "
                                       "%s costs %s %s. Autarky price %s, A = %s."
                         % (num(s["X"]), x, num(s["Y"]), y, num(s["pa"]), x, num(s["pa"]), y,
                            num(s["pa"]), point(s["A"]))))
        rows.append(("Advantage", self.advantage_text(r)))
        rows.append(("World price", self.range_text(st)))
        for c, key in zip(BOTH, ("home", "foreign")):
            s = st[key]
            made = "any mix on its frontier" if s["mix"] else "B = %s" % point(s["B"])
            outside = ("outside the frontier" if s["need"] > s["E"] + 1e-9 else
                       "on the frontier: no gain")
            rows.append(("%s at p = %s" % (self.name(c), num(p)),
                         "Makes %s and consumes C = %s. Making C at home would take %s units of "
                         "labor against the %s it has: %s."
                         % (made, point(s["C"]), num(s["need"]), num(s["E"]), outside)))
        h, f = st["home"], st["foreign"]
        if not (h["mix"] or f["mix"]):
            excess = h["C"][0] + f["C"][0] - h["B"][0] - f["B"][0]
            state = ("the market for %s clears" % x if abs(excess) < 1e-6 else
                     "%s more %s wanted than made" % (num(excess), x) if excess > 0 else
                     "%s more %s made than wanted" % (num(-excess), x))
            rows.append(("Market", "World demand for %s is %s against output of %s: %s. With "
                                   "these tastes it clears at p = %s."
                         % (x, num(h["C"][0] + f["C"][0]), num(h["B"][0] + f["B"][0]), state,
                            num(st["pstar"]))))
        else:
            rows.append(("Market", "With these tastes the market clears at p = %s."
                         % num(st["pstar"])))
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "; ".join(
                "%s: slope %s &rarr; %s, wage %s &rarr; %s, C %s &rarr; %s"
                % (self.name(c), num(b[key]["pa"]), num(st[key]["pa"]), num(b[key]["w"]),
                   num(st[key]["w"]), point(b[key]["C"]), point(st[key]["C"]))
                for c, key in zip(BOTH, ("home", "foreign"))) + "."))
        return table(rows)


# ======================================================================
# Lab 2: world relative supply and demand
# ======================================================================

class SupplyLab(RicardoLab):
    TITLE = "Lab 2 &middot; World relative supply and demand"
    INTRO = ("World relative supply of good x, built from the two straight frontiers: flat at "
             "each autarky price, where one country makes both goods, and vertical in between, "
             "where both specialize completely. Relative demand comes from the two taste "
             "sliders. The dot is where they meet.")
    FIGSIZE = (6.4, 4.6)

    def demand_curve(self, st, p):
        # World x demanded over world y demanded at price p, each country
        # earning its income at that price.
        r, v = st["r"], self.values()
        xh, yh = r.demand(HOME, p, v["s"])
        xf, yf = r.demand(FOREIGN, p, v["sf"])
        return (xh + xf) / (yh + yf)

    def figure(self, fig, st):
        (x, y) = self.goods
        r, lo, hi = st["r"], st["lo"], st["hi"]
        ax = fig.add_subplot()
        style_axes(ax)
        corner = r.corner()
        qstar = self.demand_curve(st, st["pstar"])
        qmax = self.stick("q", max(corner, qstar) * 1.8)
        pmax = self.stick("p", max(hi, st["p"]) * 1.4)
        ax.plot([0, 0, corner, corner, qmax], [0, lo, lo, hi, hi], color=LINE, lw=2,
                label="relative supply")
        ps = np.linspace(pmax * 0.02, pmax, 300)
        ax.plot([self.demand_curve(st, p) for p in ps], ps, color=CURVE, lw=1.8,
                label="relative demand")
        if st["before"] is not None:
            b = st["before"]
            bc = b["r"].corner()
            ax.plot([0, 0, bc, bc, qmax], [0, b["lo"], b["lo"], b["hi"], b["hi"]], color=BEFORE,
                    lw=1.3, ls="--", label="before")
        ax.axhline(st["p"], color=NEW, lw=1.2, ls="--", label="world price p")
        ax.plot([qstar], [st["pstar"]], "o", color=GREEN, ms=8, zorder=6)
        ax.set_xlim(0, qmax)
        ax.set_ylim(0, pmax)
        ax.set_xlabel("world %s / world %s" % (x, y), color=INK, fontsize=9, loc="right")
        ax.set_ylabel("p", color=INK, fontsize=9, loc="top")
        legend(ax, loc="upper right")
        fig.tight_layout()

    def describe(self, st):
        (x, y), r = self.goods, st["r"]
        lo, hi, ps = st["lo"], st["hi"], st["pstar"]
        who = r.exporter_x()
        rows = [("Advantage", self.advantage_text(r))]
        if who is None:
            rows.append(("Staircase", "Both autarky prices are %s: one flat line, and no trade."
                         % num(lo)))
            return table(rows)
        low, high = self.name(who), self.name(r.other(who))
        rows.append(("Staircase", "Flat at %s, where %s makes any mix. Vertical at %s, where %s "
                                  "makes only %s and %s only %s. Flat again at %s, where %s "
                                  "makes any mix."
                     % (num(lo), low, num(r.corner()), low, x, high, y, num(hi), high)))
        if lo + 1e-9 < ps < hi - 1e-9:
            where = ("Demand cuts the vertical segment: the price is strictly between the "
                     "autarky prices and both countries gain.")
        else:
            stuck = low if ps <= lo + 1e-9 else high
            where = ("Demand cuts a flat step: the price equals %s's own autarky price, so %s "
                     "still makes both goods and gains nothing. The other country takes the "
                     "whole gain." % (stuck, stuck))
        rows.append(("Clearing price", "p = %s. %s" % (num(ps), where)))
        rows.append(("World price", self.range_text(st)))
        rows.append(("Who sets it?", "Neither country. Relative demand picks the point on the "
                                     "staircase; the two autarky prices only fence it in."))
        return table(rows)


# ======================================================================
# Lab 3: wages, unit costs and the cutoff
# ======================================================================

class WageLab(RicardoLab):
    TITLE = "Lab 3 &middot; Wages, unit costs and the cutoff"
    INTRO = ("Good y is the numeraire. A worker earns the value of what she makes in the "
             "industry that pays best, so w = max(p/a<sub>x</sub>, 1/a<sub>y</sub>). A unit "
             "cost is the wage times the labor requirement. The right panel is session 8's "
             "cutoff with a country in place of the machine: Foreign undersells Home in a good "
             "when a*/a is below the wage ratio w/w*.")
    FIGSIZE = (8.6, 4.2)

    def figure(self, fig, st):
        (x, y), (home, foreign) = self.goods, self.lands
        cx, gx = fig.subplots(1, 2)
        h, f = st["home"], st["foreign"]
        style_axes(cx)
        xs = np.arange(2)
        cx.bar(xs - 0.18, h["costs"], width=0.34, color=LINE, label=home)
        cx.bar(xs + 0.18, f["costs"], width=0.34, color=CURVE, label=foreign)
        cx.axhline(st["p"], color=NEW, lw=1, ls=":")
        cx.axhline(1, color=MUTE, lw=1, ls=":")
        cx.set_xticks(xs)
        cx.set_xticklabels([x, y], fontsize=9)
        cx.set_ylim(0, self.stick("c", max(h["costs"] + f["costs"]) * 1.25))
        cx.set_title("Unit cost w·a (dotted: the prices p and 1)", loc="left", color=INK,
                     fontsize=9.5)
        legend(cx)

        style_axes(gx)
        gaps = st["r"].gaps()
        ratio = h["w"] / f["w"]
        order = sorted(range(2), key=lambda i: gaps[i])
        gx.bar(xs, [gaps[i] for i in order], width=0.55,
               color=[CURVE if gaps[i] < ratio - 1e-9 else LINE if gaps[i] > ratio + 1e-9
                      else MUTE for i in order])
        gx.axhline(ratio, color=INK, lw=1.6, ls="--", label="cutoff w/w* = %s" % num(ratio))
        if st["before"] is not None:
            b = st["before"]
            gx.axhline(b["home"]["w"] / b["foreign"]["w"], color=BEFORE, lw=1.2, ls=":",
                       label="before")
        gx.set_xticks(xs)
        gx.set_xticklabels([(x, y)[i] for i in order], fontsize=9)
        gx.set_ylim(0, self.stick("g", max(max(gaps), ratio) * 1.25))
        gx.set_title("Productivity gap a*/a (blue: %s wins)" % home, loc="left", color=INK,
                     fontsize=9.5)
        legend(gx, loc="upper left")
        fig.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.1, wspace=0.2)

    def describe(self, st):
        (x, y), (home, foreign) = self.goods, self.lands
        h, f, p, r = st["home"], st["foreign"], st["p"], st["r"]
        gaps, ratio = r.gaps(), h["w"] / f["w"]

        def industry(c, s):
            ax_, ay_ = r.a[c]
            if s["mix"]:
                return "both industries pay the same"
            return ("it makes %s, so w = p/a<sub>x</sub>" % x if p / ax_ > 1 / ay_ else
                    "it makes %s, so w = 1/a<sub>y</sub>" % y)

        def cheaper(i):
            a, b = h["costs"][i], f["costs"][i]
            return "a tie" if abs(a - b) < 1e-9 else "cheaper in " + (home if a < b else foreign)

        rows = [
            ("Wages", "%s: %s (%s). %s: %s (%s). Ratio w/w* = %s."
             % (home, num(h["w"], 3), industry(HOME, h), foreign, num(f["w"], 3),
                industry(FOREIGN, f), num(ratio, 3))),
            ("Unit costs", "%s: %s %s against %s %s, %s. %s: %s %s against %s %s, %s."
             % (x, home, num(h["costs"][0], 3), foreign, num(f["costs"][0], 3), cheaper(0),
                y, home, num(h["costs"][1], 3), foreign, num(f["costs"][1], 3), cheaper(1))),
            ("Cutoff", "Gaps a*/a: %s %s, %s %s. %s undersells %s where the gap is below %s."
             % (x, num(gaps[0], 3), y, num(gaps[1], 3), foreign, home, num(ratio, 3))),
            ("World price", self.range_text(st)),
            ("Two questions", "What a country exports follows the ratio of its labor "
                              "requirements. How rich its workers are follows the levels."),
        ]
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "%s's wage %s &rarr; %s, %s's %s &rarr; %s; "
                                                "cutoff %s &rarr; %s."
                         % (home, num(b["home"]["w"], 3), num(h["w"], 3), foreign,
                            num(b["foreign"]["w"], 3), num(f["w"], 3),
                            num(b["home"]["w"] / b["foreign"]["w"], 3), num(ratio, 3))))
        return table(rows)


# ======================================================================
# Lab 4: the small-country tariff (context)
# ======================================================================

WHEAT = dict(pw=40.0, t=10.0, A=100.0, c=20.0)


class TariffLab(Lab):
    TITLE = "Lab 4 &middot; The small-country tariff"
    INTRO = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
             "context: not examinable</span> A small country imports at a given world price. "
             "Demand is D = A &minus; p and supply is S = p &minus; c. A specific tariff t lifts "
             "the domestic price to the world price plus t, for home producers too.")
    SLIDERS = [
        ("pw", 5.0, 80.0, 1.0, 40.0, ".0f"),
        ("t", 0.0, 40.0, 0.5, 10.0, ".1f"),
        ("A", 60.0, 160.0, 1.0, 100.0, ".0f"),
        ("c", 0.0, 40.0, 1.0, 20.0, ".0f"),
    ]
    FIGSIZE = (6.4, 4.8)
    PRESETS = [
        dict(label="Notes p. 17 Try it", kind="notes", values=WHEAT),
        dict(label="Try it (c) half the tariff", kind="notes", before=WHEAT,
             values=dict(WHEAT, t=5.0)),
        dict(label="Free trade", kind="notes", values=dict(WHEAT, t=0.0)),
        dict(label="Four times the tariff", kind="notes", before=dict(WHEAT, t=2.5),
             values=WHEAT),
    ]

    def relabel(self):
        self.w["pw"].description = "World price"
        self.w["t"].description = "Tariff t"
        self.w["A"].description = "Demand: A"
        self.w["c"].description = "Supply: c"

    def compute(self):
        v = self.values()
        st = dict(v=v, live=rc.tariff(v["pw"], v["t"], v["A"], v["c"]))
        st["before"] = (rc.tariff(self.before["pw"], self.before["t"], self.before["A"],
                                  self.before["c"]) if self.before else None)
        return st

    def figure(self, fig, st):
        v, T = st["v"], st["live"]
        ax = fig.add_subplot()
        style_axes(ax)
        A, c, pw, p = v["A"], v["c"], v["pw"], T["p"]
        qmax = self.stick("q", A * 0.9)
        pmax = self.stick("p", max(A, p) * 0.85)
        ax.plot([0, pmax - c], [c, pmax], color=LINE, lw=2, label="supply")
        ax.plot([A - pmax, A], [pmax, 0], color=CURVE, lw=2, label="demand")
        ax.axhline(pw, color=MUTE, lw=1.3, ls="--", label="world price")
        if T["M0"] > 0 and p > pw:
            ax.axhline(p, color=NEW, lw=1.3, ls="--", label="with the tariff")
            ax.fill([0, T["S0"], T["S1"], 0], [pw, pw, p, p], color=LINE, alpha=0.18, lw=0)
            ax.fill([T["S0"], T["S1"], T["S1"]], [pw, pw, p], color=NEW, alpha=0.45, lw=0)
            ax.fill([T["S1"], T["D1"], T["D1"], T["S1"]], [pw, pw, p, p], color=GREEN,
                    alpha=0.22, lw=0)
            ax.fill([T["D1"], T["D0"], T["D1"]], [pw, pw, p], color=NEW, alpha=0.45, lw=0)
            mid = (pw + p) / 2
            for x, name in ((T["S0"] / 2, "a"), (T["S0"] + 2 * (T["S1"] - T["S0"]) / 3, "b"),
                            ((T["S1"] + T["D1"]) / 2, "c"),
                            (T["D1"] + (T["D0"] - T["D1"]) / 3, "d")):
                ax.text(x, mid, name, color=INK, fontsize=10, ha="center", va="center")
        ax.set_xlim(0, qmax)
        ax.set_ylim(0, pmax)
        ax.set_xlabel("quantity", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("price", color=INK, fontsize=9, loc="top")
        legend(ax, loc="upper center")
        fig.tight_layout()

    def describe(self, st):
        v, T = st["v"], st["live"]
        if T["M0"] <= 0:
            return table([("No imports", "At a world price of %s the country supplies %s and "
                                         "demands %s: it would export, and an import tariff "
                                         "changes nothing." % (num(v["pw"]), num(T["S0"]),
                                                               num(T["D0"])))])
        t = T["p"] - v["pw"]
        rows = [
            ("Free trade", "Supply %s, demand %s, imports %s." % (num(T["S0"]), num(T["D0"]),
                                                                  num(T["M0"]))),
            ("With the tariff", "Domestic price %s: supply %s, demand %s, imports %s.%s"
             % (num(T["p"]), num(T["S1"]), num(T["D1"]), num(T["M1"]),
                " The tariff is prohibitive: the price stops at the autarky price."
                if t < v["t"] - 1e-9 else "")),
            ("Areas", "a = %s (producers gain), b = %s (production distortion), c = %s "
                      "(revenue), d = %s (consumption distortion)."
             % (num(T["a"]), num(T["b"]), num(T["c"]), num(T["d"]))),
            ("Who gets what", "Consumers lose a + b + c + d = %s. a and c are transfers, so the "
                              "national loss is b + d = %s."
             % (num(T["a"] + T["b"] + T["c"] + T["d"]), num(T["loss"]))),
        ]
        if T["loss"] > 0:
            rows.append(("Revenue per loss", "%s of revenue for each unit of deadweight loss."
                         % num(T["c"] / T["loss"])))
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "Loss %s &rarr; %s, revenue %s &rarr; %s. The "
                                                "loss goes with the square of the tariff."
                         % (num(b["loss"]), num(T["loss"]), num(b["c"]), num(T["c"]))))
        return table(rows)


trade = TradeLab()
supply = SupplyLab()
wages = WageLab()
tariff = TariffLab()
