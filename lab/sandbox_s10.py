"""
sandbox_s10.py - session 10 sandbox: Heckscher-Ohlin and factor prices.

    prices      Lab 1  zero profits: goods prices to factor prices, the
                       Lerner diagram and the magnification chain
                       (Stolper-Samuelson)
    quantities  Lab 2  full employment: endowments to outputs, the cone of
                       diversification, two countries (Rybczynski,
                       Heckscher-Ohlin and factor price equalization)
    tariff      Lab 3  the small-country tariff with linear demand and supply
                       (context: not examinable)

Released with the session 10 solutions. The maths is heckscher.py.
"""

import numpy as np

import heckscher as hk
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, GREEN, INK, LINE, MUTE, NEW

TECH = ("aKy", "aEy", "aKx", "aEx")


def model(v):
    return hk.HO(*(v[k] for k in TECH))


def pct(a, b):
    return 100.0 * (b / a - 1.0) if a else float("nan")


def signed(x):
    return ("+" if x > 1e-9 else "") + num(x) + "%"


class TechLab(Lab):
    """What the two main labs share: the four input requirements and the names."""

    NAMES = ("machinery", "garments")

    def __init__(self):
        super().__init__()
        self.goods = self.NAMES

    def on_preset(self, preset):
        self.goods = preset.get("goods", self.NAMES)

    def tech_labels(self):
        y, x = self.goods
        html_label(self.w["aKy"], "a<sub>Ky</sub>: capital, %s" % y)
        html_label(self.w["aEy"], "a<sub>Ey</sub>: labor, %s" % y)
        html_label(self.w["aKx"], "a<sub>Kx</sub>: capital, %s" % x)
        html_label(self.w["aEx"], "a<sub>Ex</sub>: labor, %s" % x)

    def intensity_text(self, ho):
        y, x = self.goods
        ky, kx = ho.intensity("y"), ho.intensity("x")
        good = ho.capital_good()
        if good is None:
            return ("Both use K/E = %s: no ranking, so none of the theorems can be signed."
                    % num(ky))
        name = y if good == "y" else x
        other = x if good == "y" else y
        return ("%s uses K/E = %s and %s uses %s: %s is capital intensive, %s labor intensive."
                % (y.capitalize(), num(ky), x, num(kx), name, other))


# ======================================================================
# Lab 1: zero profits, goods prices to factor prices
# ======================================================================

TRY = dict(aKy=5.0, aEy=2.0, aKx=1.0, aEx=2.0, py=20.0, px=12.0)
SHEET = dict(aKy=2.0, aEy=1.0, aKx=1.0, aEx=3.0, py=10.0, px=10.0)
KAR = dict(aKy=3.0, aEy=1.0, aKx=1.0, aEx=2.0, py=10.0, px=10.0)
STEEL = dict(aKy=2.0, aEy=1.0, aKx=1.0, aEx=1.0, py=10.0, px=8.0)

VIN_GOODS = ("machinery", "garments")
SHEET_GOODS = ("electronics", "textiles")
KAR_GOODS = ("robotics", "footwear")
STEEL_GOODS = ("steel", "apparel")


def price_state(v):
    ho = model(v)
    st = dict(ho=ho, py=v["py"], px=v["px"])
    if ho.capital_good() is None:
        st.update(r=None, w=None, ok=False)
        return st
    r, w = ho.factor_prices(v["py"], v["px"])
    st.update(r=r, w=w, ok=r > 1e-9 and w > 1e-9)
    return st


class PriceLab(TechLab):
    TITLE = "Lab 1 &middot; Zero profits: goods prices to factor prices"
    INTRO = ("Two goods, two factors, fixed input requirements, perfect competition. Price "
             "equals unit cost in each good: p<sub>y</sub> = a<sub>Ky</sub>r + a<sub>Ey</sub>w "
             "and p<sub>x</sub> = a<sub>Kx</sub>r + a<sub>Ex</sub>w. Each condition is a line in "
             "the (w, r) plane, and factor prices sit where they cross. The right panel is the "
             "Lerner diagram: inputs per krone of output, and the isocost line wE + rK = 1 "
             "through both.")
    SLIDERS = [
        ("aKy", 0.5, 6.0, 0.5, 5.0, ".1f"),
        ("aEy", 0.5, 6.0, 0.5, 2.0, ".1f"),
        ("aKx", 0.5, 6.0, 0.5, 1.0, ".1f"),
        ("aEx", 0.5, 6.0, 0.5, 2.0, ".1f"),
        ("py", 1.0, 40.0, 0.5, 20.0, ".1f"),
        ("px", 1.0, 40.0, 0.5, 12.0, ".1f"),
    ]
    FIGSIZE = (8.8, 4.3)
    PRESETS = [
        dict(label="Notes p. 8 Try it (a)", kind="notes", values=TRY, goods=VIN_GOODS),
        dict(label="Try it (b) machinery at 28", kind="notes", before=TRY,
             values=dict(TRY, py=28.0), goods=VIN_GOODS),
        dict(label="Worksheet task 1", kind="notes", values=SHEET, goods=SHEET_GOODS),
        dict(label="Worksheet: electronics at 15", kind="notes", before=SHEET,
             values=dict(SHEET, py=15.0), goods=SHEET_GOODS),
        dict(label="Review Q2 Karelia", kind="notes", before=KAR, values=dict(KAR, py=15.0),
             goods=KAR_GOODS),
        dict(label="A10.1 (b) steel and apparel", kind="problem", values=STEEL,
             goods=STEEL_GOODS),
        dict(label="A10.1 (c) steel at 12", kind="problem", before=STEEL,
             values=dict(STEEL, py=12.0), goods=STEEL_GOODS),
        dict(label="Apparel up instead", kind="extra", before=STEEL, values=dict(STEEL, px=10.0),
             goods=STEEL_GOODS),
    ]

    def relabel(self):
        y, x = self.goods
        self.tech_labels()
        html_label(self.w["py"], "p<sub>y</sub>: price of %s" % y)
        html_label(self.w["px"], "p<sub>x</sub>: price of %s" % x)

    def compute(self):
        st = dict(v=self.values(), live=price_state(self.values()))
        st["before"] = price_state(self.before) if self.before else None
        return st

    def figure(self, fig, st):
        plane, lerner = fig.subplots(1, 2)
        s, v = st["live"], st["v"]
        ho = s["ho"]
        y, x = self.goods

        style_axes(plane)
        wtop = self.stick("w", max(v["py"] / v["aEy"], v["px"] / v["aEx"]))
        rtop = self.stick("r", max(v["py"] / v["aKy"], v["px"] / v["aKx"]))
        ws = np.array([0.0, wtop])
        if st["before"] is not None:
            b = st["before"]
            for good, p in (("y", b["py"]), ("x", b["px"])):
                aK, aE = b["ho"].a[good]
                plane.plot(ws, (p - aE * ws) / aK, color=BEFORE, lw=1.2, ls="--")
            if b["ok"]:
                plane.plot([b["w"]], [b["r"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        for good, p, colour, name in (("y", v["py"], LINE, y), ("x", v["px"], CURVE, x)):
            aK, aE = ho.a[good]
            plane.plot(ws, (p - aE * ws) / aK, color=colour, lw=2, label=name)
        if s["ok"]:
            plane.plot([s["w"]], [s["r"]], "o", color=NEW, ms=8, zorder=6)
        plane.set_xlim(0, wtop)
        plane.set_ylim(0, rtop)
        plane.set_xlabel("wage w", color=INK, fontsize=9, loc="right")
        plane.set_ylabel("rental r", color=INK, fontsize=9, loc="top")
        plane.set_title("Zero profits", loc="left", color=INK, fontsize=9.5)
        legend(plane)

        style_axes(lerner)
        Ey, Ky = ho.per_krone("y", v["py"])
        Ex, Kx = ho.per_krone("x", v["px"])
        etop = self.stick("le", max(Ey, Ex, 1 / s["w"] if s["ok"] else 0) * 1.1)
        ktop = self.stick("lk", max(Ky, Kx, 1 / s["r"] if s["ok"] else 0) * 1.1)
        lo, hi = ho.cone()
        es = np.array([0, etop])
        lerner.fill_between(es, lo * es, hi * es, color=GREEN, alpha=0.1, lw=0)
        for k, colour in ((ho.intensity("y"), LINE), (ho.intensity("x"), CURVE)):
            lerner.plot([0, etop], [0, k * etop], color=colour, lw=1, ls=":")
        if s["ok"]:
            lerner.plot([0, 1 / s["w"]], [1 / s["r"], 0], color=INK, lw=1.6,
                        label="isocost wE + rK = 1")
        if st["before"] is not None and st["before"]["ok"]:
            b = st["before"]
            lerner.plot([0, 1 / b["w"]], [1 / b["r"], 0], color=BEFORE, lw=1.2, ls="--",
                        label="before")
        lerner.plot([Ey], [Ky], "o", color=LINE, ms=8, zorder=6)
        lerner.plot([Ex], [Kx], "o", color=CURVE, ms=8, zorder=6)
        lerner.annotate(y, (Ey, Ky), textcoords="offset points", xytext=(6, 4), color=LINE,
                        fontsize=8.5)
        lerner.annotate(x, (Ex, Kx), textcoords="offset points", xytext=(6, 4), color=CURVE,
                        fontsize=8.5)
        lerner.set_xlim(0, etop)
        lerner.set_ylim(0, ktop)
        lerner.set_xlabel("labor per krone", color=INK, fontsize=9, loc="right")
        lerner.set_ylabel("capital per krone", color=INK, fontsize=9, loc="top")
        lerner.set_title("Lerner diagram (shaded: the cone)", loc="left", color=INK,
                         fontsize=9.5)
        if lerner.get_legend_handles_labels()[0]:
            legend(lerner)
        fig.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.12, wspace=0.22)

    def describe(self, st):
        s, v = st["live"], st["v"]
        ho = s["ho"]
        y, x = self.goods
        rows = [("Intensity", self.intensity_text(ho))]
        if s["r"] is None:
            return table(rows)
        if not s["ok"]:
            rows.append(("Factor prices", "The two conditions cross at r = %s, w = %s: one of "
                                          "them negative. At these prices one good cannot cover "
                                          "its costs with both factors paid, so the economy "
                                          "specializes in the other and the zero-profit logic "
                                          "breaks." % (num(s["r"]), num(s["w"]))))
            return table(rows)
        rows.append(("Factor prices", "r = %s and w = %s. Check: %s r + %s w = %s and %s r + %s w "
                                      "= %s."
                     % (num(s["r"]), num(s["w"]), num(v["aKy"]), num(v["aEy"]),
                        num(ho.unit_cost("y", s["r"], s["w"])), num(v["aKx"]), num(v["aEx"]),
                        num(ho.unit_cost("x", s["r"], s["w"])))))
        lo, hi = ho.cone()
        rows.append(("Lerner", "The isocost line meets the axes at 1/w = %s and 1/r = %s. Inside "
                               "the cone, %s &le; K/E &le; %s, endowments do not move w and r."
                     % (num(1 / s["w"], 3), num(1 / s["r"], 3), num(lo), num(hi))))
        b = st["before"]
        if b is not None and b["ok"]:
            ch = {"r&#770;": pct(b["r"], s["r"]), "w&#770;": pct(b["w"], s["w"]),
                  "p&#770;<sub>y</sub>": pct(b["py"], s["py"]),
                  "p&#770;<sub>x</sub>": pct(b["px"], s["px"])}
            order = " &gt; ".join("%s = %s" % (k, signed(val)) for k, val in hk.chain(ch))
            rows.append(("Chain", order))
            moved = [g for g, a, c in (("y", b["py"], s["py"]), ("x", b["px"], s["px"]))
                     if abs(a - c) > 1e-9]
            if len(moved) == 1:
                good = moved[0]
                rose = (s["py"] if good == "y" else s["px"]) > (b["py"] if good == "y" else b["px"])
                cap = ho.capital_good()
                winner = "capital" if (cap == good) == rose else "labor"
                rows.append(("Stolper&ndash;Samuelson",
                             "The price of %s %s. %s, used intensively in %s, gains in real "
                             "terms whatever its owners buy; the other factor loses."
                             % (y if good == "y" else x, "rose" if rose else "fell",
                                winner.capitalize(),
                                y if (winner == "capital") == (cap == "y") else x)))
            rows.append(("Real returns", "r/p<sub>y</sub> %s &rarr; %s, r/p<sub>x</sub> %s &rarr; "
                                         "%s; w/p<sub>y</sub> %s &rarr; %s, w/p<sub>x</sub> %s "
                                         "&rarr; %s."
                         % (num(b["r"] / b["py"], 3), num(s["r"] / s["py"], 3),
                            num(b["r"] / b["px"], 3), num(s["r"] / s["px"], 3),
                            num(b["w"] / b["py"], 3), num(s["w"] / s["py"], 3),
                            num(b["w"] / b["px"], 3), num(s["w"] / s["px"], 3))))
        return table(rows)


# ======================================================================
# Lab 2: full employment, endowments to outputs
# ======================================================================

QTRY = dict(aKy=5.0, aEy=2.0, aKx=1.0, aEx=2.0, K=90.0, E=60.0, Kf=90.0, Ef=60.0)
QSHEET = dict(aKy=2.0, aEy=1.0, aKx=1.0, aEx=3.0, K=50.0, E=50.0, Kf=50.0, Ef=50.0)
QKAR = dict(aKy=3.0, aEy=1.0, aKx=1.0, aEx=2.0, K=60.0, E=40.0, Kf=60.0, Ef=40.0)
QHOME = dict(aKy=2.0, aEy=1.0, aKx=1.0, aEx=1.0, K=120.0, E=100.0, Kf=110.0, Ef=100.0)


def quantity_state(v):
    ho = model(v)
    st = dict(ho=ho, v=v)
    if ho.capital_good() is None:
        st.update(home=None, foreign=None)
        return st
    st["home"] = ho.outputs(v["K"], v["E"])
    st["foreign"] = ho.outputs(v["Kf"], v["Ef"])
    return st


class QuantityLab(TechLab):
    TITLE = "Lab 2 &middot; Full employment: endowments to outputs"
    INTRO = ("Both factors fully employed: a<sub>Ky</sub>q<sub>y</sub> + a<sub>Kx</sub>q<sub>x</sub> "
             "= K and a<sub>Ey</sub>q<sub>y</sub> + a<sub>Ex</sub>q<sub>x</sub> = E. Each is a "
             "line in the output plane, and Home produces where they cross. Goods prices are "
             "held fixed, so factor prices and input ratios are too. Foreign has the same "
             "technology and its own endowment.")
    SLIDERS = [
        ("aKy", 0.5, 6.0, 0.5, 5.0, ".1f"),
        ("aEy", 0.5, 6.0, 0.5, 2.0, ".1f"),
        ("aKx", 0.5, 6.0, 0.5, 1.0, ".1f"),
        ("aEx", 0.5, 6.0, 0.5, 2.0, ".1f"),
        ("K", 5.0, 300.0, 1.0, 90.0, ".0f"),
        ("E", 5.0, 300.0, 1.0, 60.0, ".0f"),
        ("Kf", 5.0, 300.0, 1.0, 90.0, ".0f"),
        ("Ef", 5.0, 300.0, 1.0, 60.0, ".0f"),
    ]
    FIGSIZE = (8.8, 4.3)
    PRESETS = [
        dict(label="Notes p. 10 Try it (a)", kind="notes", values=QTRY, goods=VIN_GOODS),
        dict(label="Try it (b) capital to 126", kind="notes", before=QTRY,
             values=dict(QTRY, K=126.0), goods=VIN_GOODS),
        dict(label="Worksheet task 2: E to 60", kind="notes", before=QSHEET,
             values=dict(QSHEET, E=60.0), goods=SHEET_GOODS),
        dict(label="Review Q3 Karelia: K to 70", kind="notes", before=QKAR,
             values=dict(QKAR, K=70.0), goods=KAR_GOODS),
        dict(label="A10.3 (b) Home and Foreign", kind="problem", values=QHOME, goods=STEEL_GOODS),
        dict(label="A10.3 (c) Home's K to 140", kind="problem", before=QHOME,
             values=dict(QHOME, K=140.0), goods=STEEL_GOODS),
        dict(label="Outside the cone: K = 250", kind="extra", values=dict(QHOME, K=250.0),
             goods=STEEL_GOODS),
    ]

    def relabel(self):
        self.tech_labels()
        self.w["K"].description = "K: Home's capital"
        self.w["E"].description = "E: Home's labor"
        self.w["Kf"].description = "K*: Foreign's capital"
        self.w["Ef"].description = "E*: Foreign's labor"

    def compute(self):
        st = dict(live=quantity_state(self.values()))
        st["before"] = quantity_state(self.before) if self.before else None
        return st

    def figure(self, fig, st):
        cross, cone = fig.subplots(1, 2)
        s = st["live"]
        ho, v = s["ho"], s["v"]
        y, x = self.goods
        style_axes(cross)
        (aKy, aEy), (aKx, aEx) = ho.a["y"], ho.a["x"]
        xtop = self.stick("qx", max(v["K"] / aKx, v["E"] / aEx))
        ytop = self.stick("qy", max(v["K"] / aKy, v["E"] / aEy))
        if st["before"] is not None:
            b = st["before"]["v"]
            cross.plot([0, b["K"] / aKx], [b["K"] / aKy, 0], color=BEFORE, lw=1.2, ls="--")
            cross.plot([0, b["E"] / aEx], [b["E"] / aEy, 0], color=BEFORE, lw=1.2, ls="--")
            if st["before"]["home"] is not None:
                qy, qx = st["before"]["home"]
                cross.plot([qx], [qy], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        cross.plot([0, v["K"] / aKx], [v["K"] / aKy, 0], color=LINE, lw=2, label="capital K")
        cross.plot([0, v["E"] / aEx], [v["E"] / aEy, 0], color=CURVE, lw=2, label="labor E")
        if s["home"] is not None:
            qy, qx = s["home"]
            colour = NEW if qy >= -1e-9 and qx >= -1e-9 else MUTE
            cross.plot([qx], [qy], "o", color=colour, ms=8, zorder=6)
        cross.set_xlim(0, xtop)
        cross.set_ylim(0, ytop)
        cross.set_xlabel("q$_x$, %s" % x, color=INK, fontsize=9, loc="right")
        cross.set_ylabel("q$_y$, %s" % y, color=INK, fontsize=9, loc="top")
        cross.set_title("Home's outputs", loc="left", color=INK, fontsize=9.5)
        legend(cross)

        style_axes(cone)
        top = self.stick("e", max(v["E"], v["Ef"], v["K"] / 3, v["Kf"] / 3) * 1.3)
        ktop = self.stick("k", max(v["K"], v["Kf"]) * 1.3)
        lo, hi = ho.cone()
        es = np.array([0, top])
        cone.fill_between(es, lo * es, hi * es, color=GREEN, alpha=0.12, lw=0)
        cone.plot(es, ho.intensity("y") * es, color=LINE, lw=1, ls=":", label="%s ray" % y)
        cone.plot(es, ho.intensity("x") * es, color=CURVE, lw=1, ls=":", label="%s ray" % x)
        cone.plot([v["E"]], [v["K"]], "o", color=LINE, ms=8, zorder=6)
        cone.annotate("Home", (v["E"], v["K"]), textcoords="offset points", xytext=(6, 4),
                      color=LINE, fontsize=8.5)
        cone.plot([v["Ef"]], [v["Kf"]], "o", color=CURVE, ms=8, zorder=6)
        cone.annotate("Foreign", (v["Ef"], v["Kf"]), textcoords="offset points", xytext=(6, -12),
                      color=CURVE, fontsize=8.5)
        if st["before"] is not None:
            b = st["before"]["v"]
            cone.plot([b["E"]], [b["K"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        cone.set_xlim(0, top)
        cone.set_ylim(0, ktop)
        cone.set_xlabel("labor E", color=INK, fontsize=9, loc="right")
        cone.set_ylabel("capital K", color=INK, fontsize=9, loc="top")
        cone.set_title("Endowments and the cone", loc="left", color=INK, fontsize=9.5)
        legend(cone, loc="upper left")
        fig.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.12, wspace=0.22)

    def outputs_text(self, qy, qx, K, E):
        y, x = self.goods
        if qy < -1e-9 or qx < -1e-9:
            only = x if qy < 0 else y
            return ("The equations give %s = %s and %s = %s: a negative output. K/E = %s is "
                    "outside the cone, so the country makes only %s, and its factor prices then "
                    "depend on its endowment." % (y, num(qy), x, num(qx), num(K / E), only))
        return "%s %s and %s %s (K/E = %s)." % (y, num(qy), x, num(qx), num(K / E))

    def describe(self, st):
        s = st["live"]
        ho, v = s["ho"], s["v"]
        y, x = self.goods
        rows = [("Intensity", self.intensity_text(ho))]
        if s["home"] is None:
            return table(rows)
        lo, hi = ho.cone()
        rows.append(("Cone", "Both goods are made only for %s &le; K/E &le; %s." % (num(lo), num(hi))))
        rows.append(("Home", self.outputs_text(*s["home"], v["K"], v["E"])))
        rows.append(("Foreign", self.outputs_text(*s["foreign"], v["Kf"], v["Ef"])))
        kh, kf = v["K"] / v["E"], v["Kf"] / v["Ef"]
        cap = ho.capital_good()
        kgood, egood = (y, x) if cap == "y" else (x, y)
        if abs(kh - kf) < 1e-9:
            rows.append(("Trade", "The same K/E in both countries: the same autarky prices, and "
                                  "nothing to trade."))
        else:
            rich, poor = ("Home", "Foreign") if kh > kf else ("Foreign", "Home")
            rows.append(("Heckscher&ndash;Ohlin",
                         "%s is capital abundant (K/E = %s against %s), so it exports %s, the "
                         "capital-intensive good, and %s exports %s. This assumes identical "
                         "technologies and identical homothetic tastes."
                         % (rich, num(max(kh, kf)), num(min(kh, kf)), kgood, poor, egood)))
        both_in = ho.inside(v["K"], v["E"]) and ho.inside(v["Kf"], v["Ef"])
        rows.append(("FPE", "Both countries are inside the cone: at common goods prices they "
                            "have the same w and r, though no factor crosses the border." if both_in
                     else "At least one country is outside the cone: it specializes, and factor "
                          "price equalization fails."))
        b = st["before"]
        if b is not None and b["home"] is not None:
            (qy0, qx0), (qy1, qx1) = b["home"], s["home"]
            bv = b["v"]
            ch = {"q&#770;<sub>y</sub>": pct(qy0, qy1), "q&#770;<sub>x</sub>": pct(qx0, qx1),
                  "K&#770;": pct(bv["K"], v["K"]), "&Ecirc;": pct(bv["E"], v["E"])}
            rows.append(("Chain", " &gt; ".join("%s = %s" % (k, signed(val))
                                                for k, val in hk.chain(ch))))
            rows.append(("Rybczynski", "At fixed prices the growing factor's good expands more "
                                       "than in proportion and the other good contracts."))
        return table(rows)


# ======================================================================
# Lab 3: the small-country tariff (context)
# ======================================================================

BIKES = dict(pw=20.0, t=10.0, a=120.0, b=2.0, c=0.0, d=1.0)
WHEAT = dict(pw=40.0, t=10.0, a=100.0, b=1.0, c=-20.0, d=1.0)


class TariffLab(Lab):
    TITLE = "Lab 3 &middot; The small-country tariff"
    INTRO = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
             "context: not examinable</span> A small country imports at a given world price. "
             "Demand is D = a &minus; bp and supply S = c + dp. A specific tariff t lifts the "
             "domestic price to the world price plus t.")
    SLIDERS = [
        ("pw", 1.0, 80.0, 1.0, 20.0, ".0f"),
        ("t", 0.0, 40.0, 0.5, 10.0, ".1f"),
        ("a", 20.0, 200.0, 1.0, 120.0, ".0f"),
        ("b", 0.25, 4.0, 0.25, 2.0, ".2f"),
        ("c", -40.0, 40.0, 1.0, 0.0, ".0f"),
        ("d", 0.25, 4.0, 0.25, 1.0, ".2f"),
    ]
    FIGSIZE = (6.4, 4.8)
    PRESETS = [
        dict(label="A10.2 Nordheim's bicycles", kind="problem", values=BIKES),
        dict(label="A10.2 free trade", kind="problem", values=dict(BIKES, t=0.0)),
        dict(label="Half the tariff", kind="extra", before=BIKES, values=dict(BIKES, t=5.0)),
        dict(label="Session 9's wheat", kind="notes", values=WHEAT),
    ]

    def relabel(self):
        self.w["pw"].description = "World price"
        self.w["t"].description = "Tariff t"
        self.w["a"].description = "Demand: a"
        self.w["b"].description = "Demand: b"
        self.w["c"].description = "Supply: c"
        self.w["d"].description = "Supply: d"

    def compute(self):
        v = self.values()
        args = lambda s: (s["pw"], s["t"], s["a"], s["b"], s["c"], s["d"])
        st = dict(v=v, live=hk.tariff(*args(v)))
        st["before"] = hk.tariff(*args(self.before)) if self.before else None
        return st

    def figure(self, fig, st):
        v, T = st["v"], st["live"]
        ax = fig.add_subplot()
        style_axes(ax)
        a, b, c, d, pw, p = v["a"], v["b"], v["c"], v["d"], v["pw"], T["p"]
        pmax = self.stick("p", max(a / b, pw + v["t"]) * 1.05)
        qmax = self.stick("q", max(a, c + d * pmax) * 1.02)
        ps = np.linspace(max(0.0, -c / d), pmax, 50)
        ax.plot(c + d * ps, ps, color=LINE, lw=2, label="supply")
        ps = np.linspace(0, a / b, 50)
        ax.plot(a - b * ps, ps, color=CURVE, lw=2, label="demand")
        ax.axhline(pw, color=MUTE, lw=1.3, ls="--", label="world price")
        if T["M0"] > 0 and p > pw:
            ax.axhline(p, color=NEW, lw=1.3, ls="--", label="with the tariff")
            S0, S1, D1, D0 = T["S0"], T["S1"], T["D1"], T["D0"]
            ax.fill([0, S0, S1, 0], [pw, pw, p, p], color=LINE, alpha=0.18, lw=0)
            ax.fill([S0, S1, S1], [pw, pw, p], color=NEW, alpha=0.45, lw=0)
            ax.fill([S1, D1, D1, S1], [pw, pw, p, p], color=GREEN, alpha=0.22, lw=0)
            ax.fill([D1, D0, D1], [pw, pw, p], color=NEW, alpha=0.45, lw=0)
            mid = (pw + p) / 2
            for xx, name in ((S0 / 2, "a"), (S0 + 2 * (S1 - S0) / 3, "b"), ((S1 + D1) / 2, "c"),
                             (D1 + (D0 - D1) / 3, "d")):
                ax.text(xx, mid, name, color=INK, fontsize=10, ha="center", va="center")
        ax.set_xlim(0, qmax)
        ax.set_ylim(0, pmax)
        ax.set_xlabel("quantity", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("price", color=INK, fontsize=9, loc="top")
        legend(ax, loc="upper right")
        fig.tight_layout()

    def describe(self, st):
        v, T = st["v"], st["live"]
        if T["M0"] <= 0:
            return table([("No imports", "At a world price of %s the country supplies %s and "
                                         "demands %s: it would export, and an import tariff "
                                         "changes nothing." % (num(v["pw"]), num(T["S0"]),
                                                               num(T["D0"])))])
        rows = [
            ("Free trade", "Demand %s, supply %s, imports %s." % (num(T["D0"]), num(T["S0"]),
                                                                  num(T["M0"]))),
            ("With the tariff", "Price %s: demand %s, supply %s, imports %s.%s"
             % (num(T["p"]), num(T["D1"]), num(T["S1"]), num(T["M1"]),
                " The tariff is prohibitive: the price stops at the autarky price %s."
                % num(T["autarky"]) if T["p"] - v["pw"] < v["t"] - 1e-9 else "")),
            ("Areas", "a = %s, b = %s, c = %s, d = %s: together %s, the consumers' loss."
             % (num(T["a"]), num(T["b"]), num(T["c"]), num(T["d"]), num(T["consumers"]))),
            ("Deadweight loss", "b + d = %s: a and c go to producers and the government."
             % num(T["loss"])),
        ]
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "Loss %s &rarr; %s, revenue %s &rarr; %s."
                         % (num(b["loss"]), num(T["loss"]), num(b["c"]), num(T["c"]))))
        return table(rows)


prices = PriceLab()
quantities = QuantityLab()
tariff = TariffLab()
