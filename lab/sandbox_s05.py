"""
sandbox_s05.py - session 5 sandbox: risk, insurance and asset prices.

    risk       Lab 1  a two-outcome gamble against v(c): EU, CE, risk premium
    insurance  Lab 2  the contingent-consumption diagram and optimal cover
    assets     Lab 3  bond and perpetuity prices, and the CAPM market line
                      (context: not on the session 5 exam rubric)

Released with the session 5 solutions. The maths is uncertainty.py.
"""

import numpy as np

import uncertainty as un
from sandbox import (Lab, BEFORE, CURVE, DIRECT, INK, LINE, MUTE, NEW, legend, num,
                     style_axes, table)

SQRT, LOG, LIN, SQUARE = "sqrt(c) (risk averse)", "ln(c) (risk averse)", \
    "c (risk neutral)", "c squared (risk loving)"
CRRA = "CRRA (beyond the notes)"
KINDS = {SQRT: "sqrt", LOG: "log", LIN: "linear", SQUARE: "square", CRRA: "crra"}


def make_v(v):
    return un.V(KINDS[v["family"]], v.get("rho", 0.5))


def greek_ok(widget, text):
    widget.description = text
    if hasattr(widget, "description_allow_html"):
        widget.description_allow_html = True
    else:
        widget.description = (text.replace("&pi;", "pi").replace("&rho;", "rho")
                              .replace("&beta;", "beta").replace("&mu;", "mu"))


# ======================================================================
# Lab 1: risk attitudes
# ======================================================================

GAMBLE = dict(family=SQRT, c1=100.0, c2=400.0, p=0.5, rho=0.5)


def gamble_stats(v, vals):
    vf = make_v(v)
    out, pr = (vals["c1"], vals["c2"]), (vals["p"], 1 - vals["p"])
    ev = un.expected_value(out, pr)
    eu = un.expected_utility(vf, out, pr)
    ce = vf.inverse(eu)
    return dict(vf=vf, ev=ev, eu=eu, vev=vf(ev), ce=ce, prem=ev - ce)


class RiskLab(Lab):
    TITLE = "Lab 1 &middot; Risk attitudes"
    INTRO = ("A gamble pays c<sub>1</sub> with probability &pi; and c<sub>2</sub> "
             "otherwise. The chord between the two outcomes gives expected utility; the "
             "curve above the mean gives the utility of the mean. Their order is the "
             "attitude to risk, and the gap in money is the risk premium.")
    FAMILIES = [SQRT, LOG, LIN, SQUARE, CRRA]
    SLIDERS = [
        ("c1", 1.0, 600.0, 1.0, 100.0, ".0f"),
        ("c2", 1.0, 600.0, 1.0, 400.0, ".0f"),
        ("p", 0.0, 1.0, 0.01, 0.5, ".2f"),
        ("rho", -1.0, 3.0, 0.05, 0.5, ".2f"),
    ]
    FIGSIZE = (6.4, 4.8)
    PRESETS = [
        dict(label="Notes p. 9 gamble one", kind="notes", values=GAMBLE),
        dict(label="Notes p. 9 gamble two", kind="notes", before=GAMBLE,
             values=dict(GAMBLE, c1=16.0, c2=484.0)),
        dict(label="Gamble one, person C", kind="notes", values=dict(GAMBLE, family=SQUARE)),
        dict(label="Worksheet 4 or 16", kind="notes", values=dict(GAMBLE, c1=4.0, c2=16.0)),
        dict(label="Review Q4 Erik (B)", kind="notes",
             values=dict(GAMBLE, c1=4.0, c2=16.0, family=LIN)),
        dict(label="Review Q4 Erik (C)", kind="notes",
             values=dict(GAMBLE, c1=4.0, c2=16.0, family=SQUARE)),
        dict(label="CRRA, rho 2", kind="extra", values=dict(GAMBLE, family=CRRA, rho=2.0)),
    ]

    def relabel(self):
        self.w["c1"].description = "Outcome c1"
        self.w["c2"].description = "Outcome c2"
        greek_ok(self.w["p"], "Probability &pi; of c1")
        crra = self.w["family"].value == CRRA
        greek_ok(self.w["rho"], "&rho;, curvature" if crra else "&rho; (CRRA only)")
        self.w["rho"].disabled = not crra

    def compute(self):
        v = self.values()
        st = dict(v=v, live=gamble_stats(v, v))
        st["before"] = gamble_stats(self.before, self.before) if self.before else None
        tops = [v["c1"], v["c2"]] + ([self.before["c1"], self.before["c2"]]
                                     if self.before else [])
        st["xmax"] = self.stick("x", max(tops) * 1.1)
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v, s = st["v"], st["live"]
        vf, xmax = s["vf"], st["xmax"]
        cs = np.linspace(xmax * 0.002, xmax, 400)
        ys = np.array([vf(c) for c in cs])
        ax.plot(cs, ys, color=CURVE, lw=2, label="v(c)")
        if st["before"] is not None:
            b, bv = st["before"], self.before
            ax.plot([bv["c1"], bv["c2"]], [vf(bv["c1"]), vf(bv["c2"])], color=BEFORE,
                    lw=1.4, label="before")
            ax.plot([b["ce"]], [b["eu"]], "o", mfc="white", mec=BEFORE, mew=1.5, ms=7)
        c1, c2 = v["c1"], v["c2"]
        ax.plot([c1, c2], [vf(c1), vf(c2)], color=LINE, lw=1.6, label="chord")
        ax.plot([c1, c2], [vf(c1), vf(c2)], "o", color=LINE, ms=7)
        ax.axvline(s["ev"], color=MUTE, lw=0.8, ls=":")
        ax.plot([s["ev"]], [s["eu"]], "o", color=LINE, ms=7, zorder=5)
        ax.annotate("EU %s" % num(s["eu"]), (s["ev"], s["eu"]), textcoords="offset points",
                    xytext=(8, -12), color=LINE, fontsize=9)
        ax.plot([s["ev"]], [s["vev"]], "o", color=CURVE, ms=7, zorder=5)
        ax.annotate("v(EV)", (s["ev"], s["vev"]), textcoords="offset points",
                    xytext=(-8, 6), ha="right", color=CURVE, fontsize=9)
        ax.plot([0, s["ce"]], [s["eu"], s["eu"]], color=DIRECT, lw=1, ls="--")
        ax.plot([s["ce"]], [s["eu"]], "o", color=DIRECT, ms=7, zorder=5)
        ax.annotate("CE %s" % num(s["ce"]), (s["ce"], s["eu"]), textcoords="offset points",
                    xytext=(-8, 8), ha="right", color=DIRECT, fontsize=9)
        ax.set_xlim(0, xmax)
        lo = min(0.0, ys.min())
        ax.set_ylim(lo, ys.max() * 1.05)
        ax.set_xlabel("wealth c", color=INK, loc="right")
        ax.set_ylabel("v(c)", color=INK, loc="top")
        legend(ax, loc="lower right")
        fig.tight_layout()

    def describe(self, st):
        v, s = st["v"], st["live"]
        rel = ("&gt;" if s["vev"] > s["eu"] + 1e-9 else
               "&lt;" if s["vev"] < s["eu"] - 1e-9 else "=")
        rows = [
            ("Gamble", "%s with probability %s, %s otherwise. EV = %s."
             % (num(v["c1"]), num(v["p"]), num(v["c2"]), num(s["ev"]))),
            ("Utility", "EU = %s, against v(EV) = %s: v(EV) %s EU, so this person is %s."
             % (num(s["eu"]), num(s["vev"]), rel, s["vf"].attitude)),
            ("Money", "Certainty equivalent %s; risk premium EV &minus; CE = %s%s."
             % (num(s["ce"]), num(s["prem"]),
                " (negative: she would pay to keep the gamble)" if s["prem"] < -1e-9 else "")),
        ]
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "EV %s &rarr; %s, CE %s &rarr; %s, premium "
                                                "%s &rarr; %s"
                         % (num(b["ev"]), num(s["ev"]), num(b["ce"]), num(s["ce"]),
                            num(b["prem"]), num(s["prem"]))))
        return table(rows)


# ======================================================================
# Lab 2: insurance
# ======================================================================

INGRID = dict(family=SQRT, W=100.0, D=64.0, pi=0.25, q=0.25, rho=0.5)


def insurance_state(v):
    vf = make_v(v)
    W, D, pi, q = v["W"], min(v["D"], v["W"]), v["pi"], v["q"]
    k = un.optimal_coverage(vf, W, D, pi, q)
    indifferent = k is None
    k_draw = 0.0 if indifferent else k
    cg, cb = un.states(W, D, q, k_draw)
    eu = un.insurance_eu(vf, W, D, pi, q, k_draw)
    eu0 = un.insurance_eu(vf, W, D, pi, q, 0)
    return dict(vf=vf, W=W, D=D, pi=pi, q=q, K=k, Kd=k_draw, indifferent=indifferent,
                cg=cg, cb=cb, eu=eu, eu0=eu0, ce=vf.inverse(eu), ce0=vf.inverse(eu0),
                ew=W - pi * D)


class InsuranceLab(Lab):
    TITLE = "Lab 2 &middot; Insurance"
    INTRO = ("Wealth W, a loss D with probability &pi;, and cover K at q per krone. "
             "Buying cover slides you from the endowment e along the budget line toward "
             "the certainty line. The lower panel is expected utility for every K.")
    FAMILIES = [SQRT, LOG, LIN, CRRA]
    SLIDERS = [
        ("W", 1.0, 200.0, 1.0, 100.0, ".0f"),
        ("D", 0.0, 200.0, 1.0, 64.0, ".0f"),
        ("pi", 0.005, 0.95, 0.005, 0.25, ".3f"),
        ("q", 0.005, 0.95, 0.005, 0.25, ".3f"),
        ("rho", 0.05, 4.0, 0.05, 0.5, ".2f"),
    ]
    FIGSIZE = (6.4, 7.0)
    PRESETS = [
        dict(label="Worksheet", kind="notes",
             values=dict(INGRID, D=50.0, pi=0.2, q=0.2)),
        dict(label="Notes p. 6 flood", kind="notes",
             values=dict(INGRID, D=50.0, pi=0.01, q=0.01)),
        dict(label="A5.2 fair", kind="problem", values=INGRID),
        dict(label="A5.2 (e) q = 1/3", kind="problem", before=INGRID,
             values=dict(INGRID, q=1 / 3)),
        dict(label="A5.2 (f) linear", kind="problem",
             values=dict(INGRID, family=LIN, q=1 / 3)),
        dict(label="A5.1 car (thousands)", kind="problem",
             values=dict(INGRID, family=LOG, W=50.0, D=50.0, pi=0.01, q=0.05)),
        dict(label="A5.1 fair premium", kind="problem",
             before=dict(INGRID, family=LOG, W=50.0, D=50.0, pi=0.01, q=0.05),
             values=dict(INGRID, family=LOG, W=50.0, D=50.0, pi=0.01, q=0.01)),
        dict(label="CRRA, rho 3", kind="extra",
             values=dict(INGRID, family=CRRA, rho=3.0, q=1 / 3)),
    ]

    def relabel(self):
        self.w["W"].description = "Wealth W"
        self.w["D"].description = "Loss D"
        greek_ok(self.w["pi"], "Probability &pi;")
        self.w["q"].description = "Price q per krone"
        crra = self.w["family"].value == CRRA
        greek_ok(self.w["rho"], "&rho;, curvature" if crra else "&rho; (CRRA only)")
        self.w["rho"].disabled = not crra

    def compute(self):
        v = self.values()
        st = dict(v=v, live=insurance_state(v))
        st["before"] = insurance_state(self.before) if self.before else None
        tops = [v["W"]] + ([self.before["W"]] if self.before else [])
        st["top"] = self.stick("t", max(tops) * 1.08)
        return st

    def draw_contingent(self, ax, s, top, colour, dashed=False, label=""):
        g0, b0 = un.states(s["W"], s["D"], s["q"], 0)
        g1, b1 = un.states(s["W"], s["D"], s["q"], s["D"])
        ax.plot([b0, b1], [g0, g1], color=colour, lw=2, ls="--" if dashed else "-",
                label=label)
        ax.plot([b0], [g0], "s", color=LINE, ms=7, zorder=6)

    def eu_curve(self, ax, s, level, top, **kw):
        cbs = np.linspace(top * 0.005, top, 300)
        cgs = []
        for cb in cbs:
            rest = (level - s["pi"] * s["vf"](cb)) / (1 - s["pi"])
            try:
                cgs.append(s["vf"].inverse(rest))
            except (ValueError, OverflowError, ZeroDivisionError):
                cgs.append(np.nan)
        ax.plot(cbs, cgs, **kw)

    def figure(self, fig, st):
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.3], hspace=0.3)
        ax = fig.add_subplot(gs[0])
        style_axes(ax)
        s, top = st["live"], st["top"]
        ax.plot([0, top], [0, top], color=MUTE, lw=1, ls="--", label="certainty line")
        if st["before"] is not None:
            b = st["before"]
            self.draw_contingent(ax, b, top, BEFORE, label="before, slope %s"
                                 % num(un.budget_slope(b["q"])))
            if not b["indifferent"]:
                ax.plot([b["cb"]], [b["cg"]], "o", mfc="white", mec=BEFORE, mew=1.5, ms=8)
        self.draw_contingent(ax, s, top, LINE, dashed=st["before"] is not None,
                             label="budget, slope %s" % num(un.budget_slope(s["q"])))
        if s["vf"].kind != "linear":
            self.eu_curve(ax, s, s["eu0"], top, color=MUTE, lw=1, ls=":")
            self.eu_curve(ax, s, s["eu"], top, color=CURVE, lw=1.8, label="EU through K*")
        g0, b0 = un.states(s["W"], s["D"], s["q"], 0)
        ax.annotate("e = (%s, %s)" % (num(b0), num(g0)), (b0, g0), textcoords="offset points",
                    xytext=(8, 6), color=LINE, fontsize=9)
        if not s["indifferent"]:
            ax.plot([s["cb"]], [s["cg"]], "o", color=CURVE, ms=8, zorder=7)
            ax.annotate("(%s, %s)" % (num(s["cb"]), num(s["cg"])), (s["cb"], s["cg"]),
                        textcoords="offset points", xytext=(8, -14), color=INK, fontsize=9.5)
        ax.set_xlim(0, top)
        ax.set_ylim(0, top)
        ax.set_xlabel("c_bad", color=INK, loc="right")
        ax.set_ylabel("c_good", color=INK, loc="top")
        legend(ax, loc="lower right")

        ex = fig.add_subplot(gs[1])
        style_axes(ex)
        ks = np.linspace(s["D"] * 0.002 + 1e-6, s["D"], 200) if s["D"] > 0 else np.array([0.0])
        eus = [un.insurance_eu(s["vf"], s["W"], s["D"], s["pi"], s["q"], k) for k in ks]
        ex.plot(ks, eus, color=CURVE, lw=1.8)
        if not s["indifferent"]:
            ex.plot([s["Kd"]], [s["eu"]], "o", color=CURVE, ms=7)
        finite = [e for e in eus if np.isfinite(e)]
        if finite:
            lo, hi = min(finite), max(finite)
            pad = 0.1 * max(hi - lo, 1e-9)
            ex.set_ylim(max(lo, hi - 8 * max(hi - lo, 1e-9)) - pad, hi + pad)
        ex.set_xlim(0, max(s["D"], 1e-9))
        ex.set_xlabel("cover K", color=INK, loc="right")
        ex.set_title("Expected utility EU(K)", loc="left", color=INK, fontsize=9.5)
        fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.07)

    def describe(self, st):
        s = st["live"]
        fair = abs(s["q"] - s["pi"]) < 1e-9
        price = ("fair (q = &pi;)" if fair else
                 "loaded (q &gt; &pi;)" if s["q"] > s["pi"] else "subsidised (q &lt; &pi;)")
        rows = [
            ("Endowment", "e = (%s, %s): %s if all goes well, %s after the loss. Expected "
                          "wealth %s." % (num(s["W"] - s["D"]), num(s["W"]), num(s["W"]),
                                          num(s["W"] - s["D"]), num(s["ew"]))),
            ("Price", "q = %s per krone, %s; budget slope &minus;q/(1 &minus; q) = %s."
             % (num(s["q"], 3), price, num(un.budget_slope(s["q"])))),
        ]
        if s["indifferent"]:
            rows.append(("Cover", "Risk neutral at a fair price: every K from 0 to D gives "
                                  "the same expected wealth, so she is indifferent."))
        else:
            K, D = s["K"], s["D"]
            kind = ("full cover" if abs(K - D) < 1e-3 * max(D, 1) else
                    "no cover" if K < 1e-3 * max(D, 1) else "partial cover")
            rows.append(("Cover", "K* = %s of D = %s: %s. Wealth %s in the good state, %s "
                                  "in the bad." % (num(K), num(D), kind, num(s["cg"]),
                                                   num(s["cb"]))))
            if s["vf"].kind != "linear":
                rows.append(("First-order condition",
                             "v'(c_bad)/v'(c_good) = q(1 &minus; &pi;)/((1 &minus; q)&pi;) = %s "
                             "%s" % (num(un.foc_ratio(s["pi"], s["q"])),
                                     ": equal marginal utility, on the certainty line."
                                     if fair else "&gt; 1: she stays above the certainty line."
                                     if s["q"] > s["pi"] else "&lt; 1.")))
            rows.append(("Insurer", "Expected profit K(q &minus; &pi;) = %s."
                         % num(un.insurer_profit(s["pi"], s["q"], K))))
        if s["vf"].kind != "linear":
            rows.append(("Risk premium", "At e: EU = %s, certainty equivalent %s, so the "
                                         "premium is %s &minus; %s = %s."
                         % (num(s["eu0"]), num(s["ce0"]), num(s["ew"]), num(s["ce0"]),
                            num(s["ew"] - s["ce0"]))))
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "K* %s &rarr; %s"
                         % ("any" if b["indifferent"] else num(b["K"]),
                            "any" if s["indifferent"] else num(s["K"]))))
        return table(rows)


# ======================================================================
# Lab 3: asset prices (context)
# ======================================================================

BOND = dict(x=100.0, F=1000.0, N=10.0, r=0.10, rf=3.0, mu_m=8.0, beta=0.4, mu_i=6.0)


class AssetLab(Lab):
    TITLE = "Lab 3 &middot; Asset prices and the market line"
    INTRO = ("<span style='background:#fef3c7;color:#b45309;border-radius:4px;"
             "padding:1px 6px'>context: not on the session 5 exam rubric</span> "
             "Left: a bond's price against the interest rate, and a perpetuity paying "
             "the same coupon forever. Right: the CAPM market line and one asset.")
    SLIDERS = [
        ("x", 0.0, 200.0, 1.0, 100.0, ".0f"),
        ("F", 0.0, 2000.0, 10.0, 1000.0, ".0f"),
        ("N", 1.0, 40.0, 1.0, 10.0, ".0f"),
        ("r", 0.01, 0.30, 0.005, 0.10, ".3f"),
        ("rf", 0.0, 10.0, 0.25, 3.0, ".2f"),
        ("mu_m", 0.0, 20.0, 0.25, 8.0, ".2f"),
        ("beta", -1.0, 3.0, 0.05, 0.4, ".2f"),
        ("mu_i", -5.0, 25.0, 0.25, 6.0, ".2f"),
    ]
    FIGSIZE = (7.4, 4.2)
    PRESETS = [
        dict(label="Notes p. 3 bond", kind="notes", values=BOND),
        dict(label="Notes p. 3 no coupon", kind="notes", values=dict(BOND, x=0.0)),
        dict(label="A5.3 bond G, r to 25%", kind="problem",
             before=dict(BOND, N=3.0), values=dict(BOND, N=3.0, r=0.25)),
        dict(label="Worksheet cabin", kind="notes",
             before=dict(BOND, x=120.0, F=0.0, N=40.0, r=0.04),
             values=dict(BOND, x=120.0, F=0.0, N=40.0, r=0.06)),
        dict(label="Review Q6 CAPM", kind="notes", values=BOND),
    ]

    def relabel(self):
        names = dict(x="Coupon x", F="Face value F", N="Maturity N", r="Interest rate r",
                     rf="Risk-free r_f (%)", mu_m="Market return (%)",
                     beta="Asset &beta;", mu_i="Asset return (%)")
        for k, d in names.items():
            greek_ok(self.w[k], d)

    def compute(self):
        v = self.values()
        N = int(round(v["N"]))
        st = dict(v=v, N=N, pv=un.bond_price(v["x"], v["F"], N, v["r"]),
                  perp=un.perpetuity(v["x"], v["r"]) if v["r"] > 0 else float("inf"),
                  line=un.capm(v["rf"], v["mu_m"], v["beta"]))
        if self.before:
            b = self.before
            st["pv0"] = un.bond_price(b["x"], b["F"], int(round(b["N"])), b["r"])
            st["perp0"] = un.perpetuity(b["x"], b["r"])
        return st

    def figure(self, fig, st):
        bx, cx = fig.subplots(1, 2)
        v = st["v"]
        style_axes(bx)
        rs = np.linspace(0.01, 0.30, 200)
        bx.plot(rs, [un.bond_price(v["x"], v["F"], st["N"], r) for r in rs], color=LINE,
                lw=2, label="bond, N = %d" % st["N"])
        if v["x"] > 0:
            bx.plot(rs, v["x"] / rs, color=CURVE, lw=1.4, ls="--", label="perpetuity x/r")
        bx.plot([v["r"]], [st["pv"]], "o", color=LINE, ms=7, zorder=5)
        if self.before:
            bx.plot([self.before["r"]], [st["pv0"]], "o", mfc="white", mec=BEFORE, mew=1.5,
                    ms=7, zorder=5)
        top = max(un.bond_price(v["x"], v["F"], st["N"], 0.01), 1.0)
        bx.set_ylim(0, top * 1.05)
        bx.set_xlim(0, 0.3)
        bx.set_xlabel("interest rate r", color=INK, loc="right")
        bx.set_ylabel("price today", color=INK, loc="top")
        bx.set_title("Price down, yield up", loc="left", color=INK, fontsize=9.5)
        legend(bx)

        style_axes(cx)
        bs = np.linspace(-1, 3, 50)
        cx.plot(bs, [un.capm(v["rf"], v["mu_m"], b) for b in bs], color=LINE, lw=2,
                label="market line")
        cx.plot([1], [v["mu_m"]], "o", color=LINE, ms=7)
        cx.plot([v["beta"]], [st["line"]], "o", mfc="white", mec=LINE, mew=1.5, ms=7)
        cx.plot([v["beta"]], [v["mu_i"]], "o", color=NEW, ms=8, zorder=5, label="the asset")
        cx.set_xlabel("beta", color=INK, loc="right")
        cx.set_ylabel("expected return (%)", color=INK, loc="top")
        cx.set_title("The market line", loc="left", color=INK, fontsize=9.5)
        legend(cx, loc="upper left")
        fig.subplots_adjust(left=0.09, right=0.98, top=0.9, bottom=0.14, wspace=0.28)

    def describe(self, st):
        v = st["v"]
        rows = [
            ("Bond", "Coupon %s for %d years plus %s at the end, at r = %s%%: price %s."
             % (num(v["x"]), st["N"], num(v["F"]), num(100 * v["r"]), num(st["pv"]))),
            ("Perpetuity", "The coupon %s forever: x/r = %s." % (num(v["x"]), num(st["perp"]))),
        ]
        if self.before:
            rows.append(("Before &rarr; after", "bond %s &rarr; %s, perpetuity %s &rarr; %s"
                         % (num(st["pv0"]), num(st["pv"]), num(st["perp0"]), num(st["perp"]))))
        gap = v["mu_i"] - st["line"]
        rows.append(("CAPM", "Required return r<sub>f</sub> + &beta;(&mu;<sub>m</sub> &minus; "
                             "r<sub>f</sub>) = %s%%. The asset offers %s%%: %s."
                     % (num(st["line"]), num(v["mu_i"]),
                        "above the line, so buyers bid its price up and its return down"
                        if gap > 1e-9 else "below the line, so its price falls"
                        if gap < -1e-9 else "on the line")))
        return table(rows)


risk = RiskLab()
insurance = InsuranceLab()
assets = AssetLab()
