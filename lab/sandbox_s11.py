"""
sandbox_s11.py - session 11 sandbox: monopolistic competition, gravity and
trade policy.

    entry    Lab 1  markup pricing and free entry: price, firm scale and the
                    number of varieties, before and after integration
    ppzz     Lab 2  Krugman's PP-ZZ picture: what a bigger market does
    gravity  Lab 3  the gravity line, a partner off it, and the iceberg
                    factor a shortfall reveals
    border   Lab 4  the size arithmetic behind border effects
    tariff   Lab 5  the large country's tariff and the optimum tariff
                    (context: not examinable)

Released with the session 11 solutions. The maths is monopolistic.py.
"""

import numpy as np
from matplotlib.ticker import FuncFormatter

import monopolistic as mc
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, GREEN, GREY, HALF, INK, LINE, MUTE, NEW


# ======================================================================
# Lab 1: markup pricing and free entry
# ======================================================================

NORDIA = dict(sigma=4.0, MC=6.0, F=200.0, S=16000.0)
TASK2 = dict(sigma=6.0, MC=5.0, F=150.0, S=9000.0)
ARLAND = dict(sigma=3.0, MC=4.0, F=100.0, S=6000.0)


class EntryLab(Lab):
    TITLE = "Lab 1 &middot; Markup pricing and free entry"
    INTRO = ("Each firm makes its own variety with a fixed cost F and a flat marginal cost MC, "
             "and faces a constant elasticity &sigma;. Markup pricing sets p = MC&sigma;/(&sigma; "
             "&minus; 1); free entry pushes profit to zero, p = AC, which fixes each firm's "
             "output. Spending on the industry then decides how many varieties there are. "
             "Integrating two identical markets doubles spending.")
    SLIDERS = [
        ("sigma", 1.2, 10.0, 0.1, 4.0, ".1f"),
        ("MC", 0.5, 20.0, 0.5, 6.0, ".1f"),
        ("F", 10.0, 1000.0, 10.0, 200.0, ".0f"),
        ("S", 500.0, 40000.0, 500.0, 16000.0, ".0f"),
    ]
    FIGSIZE = (8.8, 4.2)
    PRESETS = [
        dict(label="A11.1 (a)-(c) Nordia", kind="problem", values=NORDIA),
        dict(label="A11.1 (d) integrated", kind="problem", before=NORDIA,
             values=dict(NORDIA, S=32000.0)),
        dict(label="Worksheet task 2: σ = 6", kind="notes", values=TASK2),
        dict(label="Task 2: standards cut σ to 2", kind="notes", before=TASK2,
             values=dict(TASK2, sigma=2.0)),
        dict(label="Review Q2 Arland: σ 3 to 5", kind="notes", before=ARLAND,
             values=dict(ARLAND, sigma=5.0)),
        dict(label="Notes p. 5 Try it: σ = 5, MC = 8", kind="notes",
             values=dict(sigma=5.0, MC=8.0, F=400.0, S=20000.0)),
    ]

    def relabel(self):
        html_label(self.w["sigma"], "Elasticity &sigma;")
        self.w["MC"].description = "Marginal cost MC"
        self.w["F"].description = "Fixed cost F"
        self.w["S"].description = "Spending on the industry"

    def state(self, v):
        return mc.industry(v["sigma"], v["MC"], v["F"], v["S"])

    def compute(self):
        v = self.values()
        st = dict(v=v, live=self.state(v))
        st["before"] = self.state(self.before) if self.before else None
        return st

    def figure(self, fig, st):
        cost, mk = fig.subplots(1, 2)
        v, s = st["v"], st["live"]
        style_axes(cost)
        qtop = self.stick("q", s["q"] * 2.2)
        ptop = self.stick("p", s["p"] * 1.8)
        qs = np.linspace(qtop * 0.03, qtop, 300)
        if st["before"] is not None:
            b, bv = st["before"], self.before
            cost.plot(qs, bv["MC"] + bv["F"] / qs, color=BEFORE, lw=1.2, ls="--", label="before")
            cost.plot([b["q"]], [b["p"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        cost.plot(qs, v["MC"] + v["F"] / qs, color=LINE, lw=2, label="AC = MC + F/q")
        cost.axhline(v["MC"], color=CURVE, lw=1.6, label="MC")
        cost.axhline(s["p"], color=NEW, lw=1.2, ls="--", label="price")
        cost.fill_between([0, s["q"]], v["MC"], s["p"], color=GREEN, alpha=0.15, lw=0)
        cost.plot([s["q"]], [s["p"]], "o", color=GREEN, ms=8, zorder=6)
        cost.set_xlim(0, qtop)
        cost.set_ylim(0, ptop)
        cost.set_xlabel("output per firm q", color=INK, fontsize=9, loc="right")
        cost.set_ylabel("price, cost", color=INK, fontsize=9, loc="top")
        cost.set_title("p = AC: markup earnings (green) = F", loc="left", color=INK, fontsize=9.5)
        legend(cost)

        style_axes(mk)
        sg = np.linspace(1.15, 10, 300)
        mk.plot(sg, sg / (sg - 1), color=LINE, lw=2)
        mk.axhline(1, color=GREY, lw=0.8, ls=":")
        if st["before"] is not None:
            bs = self.before["sigma"]
            mk.plot([bs], [mc.markup(bs)], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        mk.plot([v["sigma"]], [mc.markup(v["sigma"])], "o", color=NEW, ms=8, zorder=6)
        mk.set_xlim(1, 10)
        mk.set_ylim(0, 4.5)
        mk.set_xlabel("elasticity σ", color=INK, fontsize=9, loc="right")
        mk.set_title("The markup factor σ/(σ − 1)", loc="left", color=INK, fontsize=9.5)
        fig.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.12, wspace=0.2)

    def describe(self, st):
        v, s = st["v"], st["live"]
        rows = [
            ("Price", "p = %s &times; %s/(%s &minus; 1) = %s: a markup of %s over marginal cost."
             % (num(v["MC"]), num(v["sigma"]), num(v["sigma"]), num(s["p"]), num(s["markup"], 3))),
            ("Firm scale", "Zero profit: (p &minus; MC)q = F, so q = %s/%s = %s. Average cost "
                           "there is %s, equal to the price." % (num(v["F"]), num(s["p"] - v["MC"]),
                                                                 num(s["q"]), num(s["AC"]))),
            ("Varieties", "Spending of %s buys %s units, made by n = %s firms, one variety each."
             % (num(v["S"]), num(s["Q"]), num(s["n"]))),
            ("Market power", "Every firm prices above marginal cost, and every firm earns zero: "
                             "the markup revenue exactly covers the fixed cost."),
        ]
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "Price %s &rarr; %s, firm scale %s &rarr; %s, "
                                                "varieties %s &rarr; %s."
                         % (num(b["p"]), num(s["p"]), num(b["q"]), num(s["q"]), num(b["n"]),
                            num(s["n"]))))
        return table(rows)


# ======================================================================
# Lab 2: the PP-ZZ picture
# ======================================================================

SHEET = dict(E=32.0, alpha=4.0, beta=1.0, sigma=2.0)
CES = dict(E=6000.0, alpha=20.0, beta=1.0, sigma=3.0)


class PPZZLab(Lab):
    TITLE = "Lab 2 &middot; Markup meets entry: PP and ZZ"
    INTRO = ("Krugman's labor-only economy. PP is markup pricing, p/w = &beta;&sigma;/(&sigma; "
             "&minus; 1), flat because the elasticity is constant; ZZ is zero profit, p/w = "
             "&alpha;/(Ec) + &beta;. They cross at consumption per variety c, and full "
             "employment gives the number of varieties N = 1/((&alpha;/E) + &beta;c). Trade "
             "with an identical country doubles E.")
    SLIDERS = [
        ("E", 4.0, 12000.0, 4.0, 32.0, ".0f"),
        ("alpha", 0.5, 40.0, 0.5, 4.0, ".1f"),
        ("beta", 0.25, 4.0, 0.25, 1.0, ".2f"),
        ("sigma", 1.2, 8.0, 0.1, 2.0, ".1f"),
    ]
    FIGSIZE = (6.6, 4.6)
    PRESETS = [
        dict(label="Worksheet: E = 32", kind="notes", values=SHEET),
        dict(label="Worksheet: trade doubles E", kind="notes", before=SHEET,
             values=dict(SHEET, E=64.0)),
        dict(label="Review Q3: CES, E = 6000", kind="notes", values=CES),
        dict(label="Review Q3: trade with a twin", kind="notes", before=CES,
             values=dict(CES, E=12000.0)),
    ]

    def relabel(self):
        self.w["E"].description = "Labor force E"
        html_label(self.w["alpha"], "&alpha;: fixed labor")
        html_label(self.w["beta"], "&beta;: marginal labor")
        html_label(self.w["sigma"], "Elasticity &sigma;")

    def compute(self):
        v = self.values()
        st = dict(v=v, live=mc.ppzz(v["E"], v["alpha"], v["beta"], v["sigma"]))
        b = self.before
        st["before"] = mc.ppzz(b["E"], b["alpha"], b["beta"], b["sigma"]) if b else None
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v, s = st["v"], st["live"]
        ctop = self.stick("c", s["c"] * 4)
        ptop = self.stick("p", s["pw"] * 1.8)
        cs = np.linspace(ctop * 0.02, ctop, 300)
        if st["before"] is not None:
            b, bv = st["before"], self.before
            ax.plot(cs, mc.zz(cs, bv["E"], bv["alpha"], bv["beta"]), color=BEFORE, lw=1.3,
                    ls="--", label="ZZ before")
            ax.plot([b["c"]], [b["pw"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8)
        ax.axhline(s["pw"], color=LINE, lw=2, label="PP: markup")
        ax.plot(cs, mc.zz(cs, v["E"], v["alpha"], v["beta"]), color=CURVE, lw=2,
                label="ZZ: zero profit")
        ax.plot([s["c"]], [s["pw"]], "o", color=NEW, ms=8, zorder=6)
        ax.set_xlim(0, ctop)
        ax.set_ylim(0, ptop)
        ax.set_xlabel("consumption per variety c", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("p/w", color=INK, fontsize=9, loc="top")
        legend(ax)
        fig.tight_layout()

    def describe(self, st):
        v, s = st["v"], st["live"]
        rows = [
            ("Equilibrium", "c = %s, p/w = %s. Each firm makes y = Ec = %s, which is (&sigma; "
                            "&minus; 1)&alpha;/&beta; = %s whatever the market size."
             % (num(s["c"], 4), num(s["pw"]), num(s["y"]),
                num(mc.ces_scale(v["sigma"], v["alpha"], v["beta"])))),
            ("Varieties", "N = 1/(%s + %s &times; %s) = %s." % (num(v["alpha"] / v["E"], 4),
                                                               num(v["beta"]), num(s["c"], 4),
                                                               num(s["N"]))),
        ]
        if st["before"] is not None:
            b, bv = st["before"], self.before
            rows.append(("Before &rarr; after", "E %s &rarr; %s: c %s &rarr; %s, p/w %s &rarr; "
                                                "%s, firm output %s &rarr; %s, varieties %s "
                                                "&rarr; %s."
                         % (num(bv["E"]), num(v["E"]), num(b["c"], 4), num(s["c"], 4),
                            num(b["pw"]), num(s["pw"]), num(b["y"]), num(s["y"]), num(b["N"]),
                            num(s["N"]))))
            if abs(v["E"] - 2 * bv["E"]) < 1e-9 and v["sigma"] == bv["sigma"]:
                rows.append(("Trade", "Doubling E is trade with an identical country: %s "
                                      "varieties in the integrated market, %s made in each "
                                      "country. With a flat PP only the variety gain survives."
                             % (num(s["N"]), num(s["N"] / 2))))
        return table(rows)


# ======================================================================
# Lab 3: the gravity line
# ======================================================================

PARTNERS = (200.0, 400.0, 800.0, 1600.0)
VESTLAND = dict(share=0.5, Yo=400.0, Xo=8.0, sigma=3.0)
VINLAND = dict(share=1000 / 15000 * 100, Yo=600.0, Xo=10.0, sigma=3.0)


class GravityLab(Lab):
    TITLE = "Lab 3 &middot; Gravity: the line and a partner off it"
    INTRO = ("Frictionless gravity: country i sells the share s<sub>j</sub> of everything it "
             "makes to country j, so exports to j are X = Y<sub>i</sub>Y<sub>j</sub>/Y<sub>w</sub> "
             "= (Y<sub>i</sub>/Y<sub>w</sub>)Y<sub>j</sub>. On doubling axes that is a straight "
             "line of slope one. A partner whose actual exports fall short reveals an iceberg "
             "factor: trade scales with T<sup>1 &minus; &sigma;</sup>.")
    SLIDERS = [
        ("share", 0.05, 20.0, 0.05, 0.5, ".2f"),
        ("Yo", 50.0, 3000.0, 50.0, 400.0, ".0f"),
        ("Xo", 0.5, 120.0, 0.5, 8.0, ".1f"),
        ("sigma", 1.5, 8.0, 0.5, 3.0, ".1f"),
    ]
    FIGSIZE = (6.6, 4.6)
    PRESETS = [
        dict(label="Worksheet: Vestland and Naboria", kind="notes", values=VESTLAND),
        dict(label="Notes p. 13 Try it: Vinland", kind="notes", values=VINLAND),
        dict(label="Try it: all GDPs double", kind="notes", values=dict(VINLAND, Yo=1200.0,
                                                                       Xo=80.0)),
    ]

    def relabel(self):
        html_label(self.w["share"], "Y<sub>i</sub>/Y<sub>w</sub>, in %")
        self.w["Yo"].description = "Odd partner's GDP"
        self.w["Xo"].description = "Exports to it"
        html_label(self.w["sigma"], "Elasticity &sigma;")

    def compute(self):
        v = self.values()
        s = v["share"] / 100
        pred = s * v["Yo"]
        st = dict(v=v, s=s, pred=pred, ratio=v["Xo"] / pred)
        st["T"] = mc.iceberg(v["Xo"], pred, v["sigma"]) if v["Xo"] < pred else None
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v, s = st["v"], st["s"]
        ax.set_xscale("log", base=2)
        ax.set_yscale("log", base=2)
        g = np.array([30.0, 4000.0])
        ax.plot(g, s * g, color=LINE, lw=2, label="exports = (Y$_i$/Y$_w$) × partner GDP")
        ax.plot(PARTNERS, [s * p for p in PARTNERS], "o", color=LINE, ms=6)
        ax.plot([v["Yo"]], [v["Xo"]], "o", color=NEW, ms=9, zorder=6, label="odd partner")
        ax.plot([v["Yo"], v["Yo"]], [st["pred"], v["Xo"]], color=NEW, lw=1, ls=":")
        ys = [s * p for p in PARTNERS] + [v["Xo"], st["pred"]]
        ax.set_xlim(100, 3500)
        ax.set_ylim(min(ys) / 2.5, max(ys) * 2.5)
        ax.minorticks_off()
        ax.set_xticks([125, 250, 500, 1000, 2000])
        ax.set_xticklabels(["125", "250", "500", "1000", "2000"])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "%g" % y))
        ax.set_xlabel("partner GDP (log scale)", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("exports (log scale)", color=INK, fontsize=9, loc="top")
        legend(ax, loc="upper left")
        fig.tight_layout()

    def describe(self, st):
        v = st["v"]
        rows = [
            ("The line", "Exports = %s &times; partner GDP: %s to partners of 200, 400, 800 and "
                         "1600. GDP enters with a coefficient of one because every country spends "
                         "a fixed share of its income on each variety."
             % (num(st["s"], 4), ", ".join(num(st["s"] * p, 3) for p in PARTNERS))),
            ("Odd partner", "Predicted %s, actual %s: %s times the prediction."
             % (num(st["pred"], 3), num(v["Xo"], 3), num(st["ratio"], 3))),
        ]
        if st["T"] is not None:
            rows.append(("Iceberg", "Trade scales with T<sup>1 &minus; &sigma;</sup>, so T = "
                                    "(%s)<sup>1/(1 &minus; %s)</sup> = %s: of every %s units "
                                    "shipped, 1 arrives, and the share %s melts."
                         % (num(st["ratio"], 3), num(v["sigma"]), num(st["T"], 3),
                            num(st["T"], 3), num(1 - 1 / st["T"], 3))))
        elif st["ratio"] > 1:
            rows.append(("Above the line", "More trade than size predicts: a close partner, a "
                                           "shared language or a border, low costs relative to "
                                           "everyone else's."))
        return table(rows)


# ======================================================================
# Lab 4: the border arithmetic
# ======================================================================

CANADA = dict(small=10.0, big=90.0, keep=50.0)


class BorderLab(Lab):
    TITLE = "Lab 4 &middot; Why borders look bigger for small countries"
    INTRO = ("Anderson and van Wincoop's arithmetic. Without frictions the small country sells "
             "a small share of its GDP at home, the big country a large one. A border keeps only "
             "part of cross-border trade, and displaced exports are sold at home. The measured "
             "border effect is (home/abroad) after over before.")
    SLIDERS = [
        ("small", 1.0, 50.0, 1.0, 10.0, ".0f"),
        ("big", 50.0, 99.0, 1.0, 90.0, ".0f"),
        ("keep", 5.0, 100.0, 5.0, 50.0, ".0f"),
    ]
    FIGSIZE = (6.6, 4.4)
    PRESETS = [
        dict(label="Review Q5: Canada and the U.S.", kind="notes", values=CANADA),
        dict(label="A thicker border: keep 25%", kind="extra", before=CANADA,
             values=dict(CANADA, keep=25.0)),
        dict(label="Equal sizes", kind="extra", values=dict(small=50.0, big=50.0, keep=50.0)),
    ]

    def relabel(self):
        self.w["small"].description = "Small: % sold at home"
        self.w["big"].description = "Big: % sold at home"
        self.w["keep"].description = "% of trade the border keeps"

    def compute(self):
        v = self.values()
        st = dict(v=v, live=mc.border_sizes(v["small"] / 100, v["big"] / 100, v["keep"] / 100))
        b = self.before
        st["before"] = (mc.border_sizes(b["small"] / 100, b["big"] / 100, b["keep"] / 100)
                        if b else None)
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        s = st["live"]
        homes = [s["small"]["before"][0], s["small"]["after"][0], s["big"]["before"][0],
                 s["big"]["after"][0]]
        xs = np.arange(4)
        ax.bar(xs, [100 * h for h in homes], color=GREY, width=0.6, label="sold at home")
        ax.bar(xs, [100 * (1 - h) for h in homes], bottom=[100 * h for h in homes], color=HALF,
               alpha=0.7, width=0.6, label="sold abroad")
        ax.text(0.5, 106, "×%s" % num(s["small"]["factor"], 2), ha="center", color=NEW,
                fontsize=12, weight="bold")
        ax.text(2.5, 106, "×%s" % num(s["big"]["factor"], 2), ha="center", color=NEW,
                fontsize=12, weight="bold")
        ax.set_xticks(xs)
        ax.set_xticklabels(["small,\nno border", "small,\nborder", "big,\nno border",
                            "big,\nborder"], fontsize=8.5, color=INK)
        ax.set_yticks([0, 50, 100])
        ax.tick_params(colors=MUTE, labelsize=8.5)
        ax.set_ylim(0, 115)
        ax.legend(loc="lower left", fontsize=8.5, frameon=True)
        fig.tight_layout()

    def describe(self, st):
        s = st["live"]
        rows = []
        for name in ("small", "big"):
            c = s[name]
            rows.append((name.capitalize(), "Home %s%% &rarr; %s%%, abroad %s%% &rarr; %s%%: the "
                                            "measured border effect is %s."
                         % (num(100 * c["before"][0]), num(100 * c["after"][0]),
                            num(100 * c["before"][1]), num(100 * c["after"][1]),
                            num(c["factor"], 3))))
        rows.append(("Lesson", "One true friction, two very different measurements: size inflates "
                               "the small country's number. In a regression, exporter and importer "
                               "fixed effects stand in for multilateral resistance."))
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "Small %s &rarr; %s, big %s &rarr; %s."
                         % (num(b["small"]["factor"], 3), num(s["small"]["factor"], 3),
                            num(b["big"]["factor"], 3), num(s["big"]["factor"], 3))))
        return table(rows)


# ======================================================================
# Lab 5: the large country's tariff (context)
# ======================================================================

LARGE = dict(A=100.0, B=1.0, t=20.0)


class TariffLab(Lab):
    TITLE = "Lab 5 &middot; The large country and the optimum tariff"
    INTRO = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;padding:1px 6px'>"
             "context: not examinable</span> Home's import demand is M = A &minus; p; foreign "
             "export supply is X* = Bp*. A specific tariff t drives p = p* + t, so the world "
             "price falls. Part of the revenue, e, is paid by foreigners; the triangle b + d is "
             "Home's deadweight loss; and &Delta;W = e &minus; (b + d).")
    SLIDERS = [
        ("A", 40.0, 200.0, 5.0, 100.0, ".0f"),
        ("B", 0.2, 8.0, 0.1, 1.0, ".1f"),
        ("t", 0.0, 100.0, 0.5, 20.0, ".1f"),
    ]
    FIGSIZE = (6.6, 4.8)
    CHECKS = [("best", "Set the optimum tariff (ignore slider t)")]
    PRESETS = [
        dict(label="A small tariff", kind="extra", values=LARGE),
        dict(label="The optimum tariff", kind="extra", values=LARGE, flags=dict(best=True)),
        dict(label="Elastic foreign supply: nearly small", kind="extra",
             values=dict(LARGE, B=8.0), flags=dict(best=True)),
    ]

    def relabel(self):
        self.w["A"].description = "Import demand: A"
        self.w["B"].description = "Foreign supply: B"
        self.w["t"].description = "Tariff t"
        self.w["t"].disabled = self.flag("best")

    def compute(self):
        v = self.values()
        t = mc.best_large_tariff(v["A"], v["B"]) if self.flag("best") else v["t"]
        return dict(v=v, live=mc.large_tariff(v["A"], v["B"], t),
                    best=mc.best_large_tariff(v["A"], v["B"]))

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v, T = st["v"], st["live"]
        A, B = v["A"], v["B"]
        top = self.stick("p", A * 1.05)
        ms = np.array([0, A])
        ax.plot(ms, A - ms, color=CURVE, lw=2, label="import demand")
        ax.plot(ms, ms / B, color=LINE, lw=2, label="foreign export supply")
        ax.plot([T["M0"]], [T["p0"]], "o", color=INK, ms=7)
        m1, p, ps, p0 = T["M1"], T["p"], T["pstar"], T["p0"]
        if T["t"] > 0 and m1 > 0:
            ax.fill([0, m1, m1, 0], [p0, p0, p, p], color=NEW, alpha=0.25, lw=0,
                    label="paid at home")
            ax.fill([0, m1, m1, 0], [ps, ps, p0, p0], color=GREEN, alpha=0.3, lw=0,
                    label="e: paid by foreigners")
            ax.fill([m1, T["M0"], m1], [p, p0, p0], color="#dc2626", alpha=0.3, lw=0,
                    label="b + d")
        ax.set_xlim(0, A * 1.02)
        ax.set_ylim(0, top)
        ax.set_xlabel("imports M", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("price", color=INK, fontsize=9, loc="top")
        legend(ax)
        fig.tight_layout()

    def describe(self, st):
        T = st["live"]
        if T["M1"] <= 0:
            return table([("Prohibitive", "At t = %s nothing is imported: no revenue, no terms "
                                          "of trade, only the loss." % num(T["t"]))])
        rows = [
            ("Prices", "Free trade %s. With t = %s, the home price is %s and the world price %s: "
                       "the world price falls by %s." % (num(T["p0"]), num(T["t"]), num(T["p"]),
                                                         num(T["pstar"]), num(T["p0"] - T["pstar"]))),
            ("Welfare", "e = %s, paid by foreigners; b + d = %s; &Delta;W = %s."
             % (num(T["e"]), num(T["bd"]), num(T["dW"]))),
            ("Optimum", "The best tariff here is t = %s, an ad valorem %s%% of the world price: "
                        "1/&epsilon;* with export supply through the origin, &epsilon;* = 1, "
                        "whatever B is. A small country, &epsilon;* = &infin;, should set zero."
             % (num(st["best"]), num(100 * st["best"] / mc.large_tariff(
                 st["v"]["A"], st["v"]["B"], st["best"])["pstar"]))),
            ("Retaliation", "If the partner retaliates, the terms-of-trade gains cancel and both "
                            "keep the distortions: a Prisoners' Dilemma."),
        ]
        return table(rows)


entry = EntryLab()
ppzz = PPZZLab()
gravity = GravityLab()
border = BorderLab()
tariff = TariffLab()
