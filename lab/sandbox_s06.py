"""
sandbox_s06.py - session 6 sandbox: exchange, equilibrium and welfare.

    market   Lab 1  the Edgeworth box and excess demand: incomes, demands,
                    clearing, Walras' law, the contract curve and the core
    welfare  Lab 2  the second welfare theorem: pick an efficient point and
                    see the price and the lump-sum transfer that support it

Released with the session 6 solutions. The maths is equilibrium.py.
"""

import math

import numpy as np

import edgeworth_plots as ed
from equilibrium import Economy
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, DIRECT, HALF, INK, LINE, MUTE, NEW

A_COL, B_COL, CC, CORE, LENS = LINE, CURVE, DIRECT, NEW, HALF


def economy(v):
    return Economy(v["a"], v["b"], (v["wAx"], v["wAy"]), (v["wBx"], v["wBy"]))


def box_axes(ax, e):
    # A's units along the bottom and left, B's along the top and right.
    style_axes(ax)
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(MUTE)
    ax.grid(False)
    ax.set_xlim(0, e.X)
    ax.set_ylim(0, e.Y)
    ax.set_aspect("equal")
    flip_x = lambda x: e.X - x
    flip_y = lambda y: e.Y - y
    top = ax.secondary_xaxis("top", functions=(flip_x, flip_x))
    right = ax.secondary_yaxis("right", functions=(flip_y, flip_y))
    for sec in (top, right):
        sec.tick_params(colors=B_COL, labelsize=8)
    ax.tick_params(colors=A_COL, labelsize=8)
    ax.set_xlabel(r"$x_A$ (B's $x_B$ along the top)", color=INK, fontsize=9, loc="right")
    ax.set_ylabel(r"$y_A$", color=INK, fontsize=9, loc="top")


def core_segment(ax, e):
    lo, hi = e.core()
    xs = np.linspace(lo, hi, 60)
    ax.plot(xs, [e.contract(v) for v in xs], color=CORE, lw=5, alpha=0.85,
            solid_capstyle="round", label="core", zorder=4)
    return lo, hi


def dot(ax, x, y, colour, hollow=False, ms=7, z=6):
    if hollow:
        ax.plot([x], [y], "o", mfc="white", mec=colour, mew=1.6, ms=ms + 1, zorder=z)
    else:
        ax.plot([x], [y], "o", color=colour, ms=ms, zorder=z, clip_on=False)


def tastes(share):
    return "x<sup>%s</sup>y<sup>%s</sup>" % (num(share), num(1 - share))


def contract_text(e):
    kA, kB = e.a / (1 - e.a), e.b / (1 - e.b)
    if abs(kA - kB) < 1e-9:
        return "y<sub>A</sub> = (%s/%s)&middot;x<sub>A</sub>: the diagonal, because the tastes are " \
               "identical" % (num(e.Y), num(e.X))
    top, const, slope = kB * e.Y, kA * e.X, kB - kA
    # Scale to whole numbers and cancel common factors, so the curve reads as
    # in the notes: 6x/(18 - x) rather than 12x/(36 - 2x).
    for k in range(1, 13):
        trio = [v * k for v in (top, const, abs(slope))]
        if all(abs(t - round(t)) < 1e-6 for t in trio):
            ints = [int(round(t)) for t in trio]
            g = math.gcd(math.gcd(ints[0], ints[1]), ints[2]) or 1
            top, const, mag = (t / g for t in ints)
            break
    else:
        mag = abs(slope)
    term = lambda c: "x<sub>A</sub>" if abs(c - 1) < 1e-9 else "%s&middot;x<sub>A</sub>" % num(c)
    return ("y<sub>A</sub> = %s / (%s %s %s), bowed %s the diagonal"
            % (term(top), num(const), "+" if slope > 0 else "&minus;", term(mag),
               "below" if kA > kB else "above"))


def bundle(t):
    return "(%s, %s)" % (num(t[0]), num(t[1]))


# ======================================================================
# Lab 1: the Edgeworth box and excess demand
# ======================================================================

WORKED = dict(a=0.75, b=0.5, wAx=8.0, wAy=8.0, wBx=4.0, wBy=4.0, p=2.0, xp=6.0, yp=6.0)
SHEET = dict(WORKED, b=0.25, wAx=2.0, wAy=6.0, wBx=6.0, wBy=2.0, p=1.0)
ASTRID = dict(WORKED, a=2 / 3, b=0.5, wAx=3.0, wAy=9.0, wBx=3.0, wBy=3.0, p=3.0, xp=4.0)
A61 = dict(WORKED, a=0.5, b=0.5, wAx=3.0, wAy=9.0, wBx=9.0, wBy=3.0, p=1.0)
A62 = dict(A61, a=2 / 3, b=1 / 3)


class MarketLab(Lab):
    TITLE = "Lab 1 &middot; The Edgeworth box and excess demand"
    INTRO = ("Two agents with Cobb&ndash;Douglas tastes: a and b are the shares of income A "
             "and B spend on good x. Each owns an endowment &omega;, and income is its value "
             "at the price ratio p = p<sub>x</sub>/p<sub>y</sub>. The market clears by "
             "itself; tick <i>Set the price by hand</i> to see what a wrong price looks like "
             "in the box and on the excess-demand curves.")
    SLIDERS = [
        ("a", 0.05, 0.95, 0.01, 0.75, ".2f"),
        ("b", 0.05, 0.95, 0.01, 0.5, ".2f"),
        ("wAx", 0.0, 20.0, 0.5, 8.0, ".1f"),
        ("wAy", 0.0, 20.0, 0.5, 8.0, ".1f"),
        ("wBx", 0.0, 20.0, 0.5, 4.0, ".1f"),
        ("wBy", 0.0, 20.0, 0.5, 4.0, ".1f"),
        ("p", 0.1, 6.0, 0.05, 2.0, ".2f"),
        ("xp", 0.0, 40.0, 0.1, 6.0, ".1f"),
        ("yp", 0.0, 40.0, 0.1, 6.0, ".1f"),
    ]
    CHECKS = [("manual", "Set the price by hand (slider p)"),
              ("lens", "Show the lens through ω and the core"),
              ("point", "Mark an allocation for A (sliders at the bottom)")]
    FIGSIZE = (8.6, 4.6)
    PRESETS = [
        dict(label="Notes p. 6 worked economy", kind="notes", values=WORKED),
        dict(label="Notes p. 5 price too steep", kind="notes", values=dict(WORKED, p=3.0),
             flags=dict(manual=True)),
        dict(label="Notes p. 10 p = 1", kind="notes", values=dict(WORKED, p=1.0),
             flags=dict(manual=True)),
        dict(label="Notes p. 14 the core", kind="notes", values=WORKED, flags=dict(lens=True)),
        dict(label="Worksheet", kind="notes", values=SHEET, flags=dict(lens=True)),
        dict(label="Review Q1–5 Astrid and Birk", kind="notes", values=ASTRID,
             flags=dict(point=True)),
        dict(label="A6.1 identical tastes", kind="problem", values=A61),
        dict(label="A6.2 different tastes", kind="problem", before=A61, values=A62),
        dict(label="A6.2 (f) equal split", kind="problem", values=A62,
             flags=dict(point=True)),
    ]

    def relabel(self):
        html_label(self.w["a"], "a: A's share on x")
        html_label(self.w["b"], "b: B's share on x")
        html_label(self.w["wAx"], "&omega;<sub>A</sub> of x")
        html_label(self.w["wAy"], "&omega;<sub>A</sub> of y")
        html_label(self.w["wBx"], "&omega;<sub>B</sub> of x")
        html_label(self.w["wBy"], "&omega;<sub>B</sub> of y")
        manual = self.flag("manual")
        html_label(self.w["p"], "Price ratio p" if manual else "p (tick 'by hand')")
        self.w["p"].disabled = not manual
        point = self.flag("point")
        html_label(self.w["xp"], "Marked x<sub>A</sub>" if point else "x<sub>A</sub> (tick 'mark')")
        html_label(self.w["yp"], "Marked y<sub>A</sub>" if point else "y<sub>A</sub> (tick 'mark')")
        self.w["xp"].disabled = self.w["yp"].disabled = not point

    def compute(self):
        v = self.values()
        e = economy(v)
        st = dict(v=v, e=e, ok=e.X > 0 and e.Y > 0)
        if not st["ok"]:
            return st
        st["pstar"] = e.price()
        st["p"] = v["p"] if self.flag("manual") else st["pstar"]
        st["eq"] = e.equilibrium()
        st["inc"] = e.incomes(st["p"])
        st["dem"] = e.demands(st["p"])
        st["z"] = e.excess(st["p"])
        st["before"] = economy(self.before) if self.before else None
        if self.flag("point"):
            st["pt"] = (min(v["xp"], e.X), min(v["yp"], e.Y))
        st["pmax"] = self.stick("p", max(st["pstar"], st["p"]) * 2.0)
        return st

    def figure(self, fig, st):
        if not st["ok"]:
            ax = fig.add_subplot()
            ax.axis("off")
            ax.text(0.5, 0.5, "Both goods need a positive total.", ha="center", color=MUTE)
            return
        gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1], wspace=0.32)
        ax = fig.add_subplot(gs[0])
        e, p = st["e"], st["p"]
        box_axes(ax, e)
        if st["before"] is not None:
            ed.contract(ax, st["before"], color=BEFORE, lw=1.4, ls="--", label="before: contract curve")
        ed.contract(ax, e, color=CC, lw=2, label="contract curve")
        if self.flag("lens"):
            ed.lens(ax, e, *e.wA, color=LENS, alpha=0.14)
            ed.ic_a(ax, e, *e.wA, color=A_COL, lw=1, ls=":")
            ed.ic_b(ax, e, *e.wA, color=B_COL, lw=1, ls=":")
            core_segment(ax, e)
        ed.price_line(ax, e, p, *e.wA, color=INK, lw=1.5, label="price line, slope −p")
        (xA, yA), (xB, yB) = st["dem"]
        bx, by = e.b_bundle(xB, yB)               # B's choice, in A's coordinates
        ed.ic_a(ax, e, xA, yA, color=A_COL, lw=1.4)
        ed.ic_b(ax, e, bx, by, color=B_COL, lw=1.4)
        if abs(xA - bx) > 1e-6 or abs(yA - by) > 1e-6:
            ax.plot([xA, bx], [yA, by], color=LENS, lw=2.5, alpha=0.7, label="the gap")
            dot(ax, xA, yA, A_COL)
            dot(ax, bx, by, B_COL)
        else:
            dot(ax, xA, yA, CC, ms=8)
        dot(ax, *e.wA, INK)
        ax.annotate("ω", e.wA, textcoords="offset points", xytext=(7, 5), color=INK,
                    fontsize=10)
        if "pt" in st:
            x, y = st["pt"]
            if 0 < x < e.X and 0 < y < e.Y:
                ed.lens(ax, e, x, y, color=NEW, alpha=0.12)
                ed.ic_a(ax, e, x, y, color=A_COL, lw=1, ls="--")
                ed.ic_b(ax, e, x, y, color=B_COL, lw=1, ls="--")
            dot(ax, x, y, NEW, hollow=True)
        legend(ax, loc="upper left")
        ax.get_legend().set_zorder(10)

        zx = fig.add_subplot(gs[1])
        style_axes(zx)
        pmax = st["pmax"]
        ps = np.linspace(pmax * 0.06, pmax, 300)
        zs = np.array([e.excess(q) for q in ps])
        zx.plot(ps, zs[:, 0], color=A_COL, lw=2, label=r"$z_x(p)$")
        zx.plot(ps, zs[:, 1], color=B_COL, lw=2, label=r"$z_y(p)$")
        zx.axhline(0, color=MUTE, lw=0.8)
        zx.axvline(p, color=INK, lw=0.8, ls=":")
        dot(zx, p, st["z"][0], A_COL)
        dot(zx, p, st["z"][1], B_COL)
        dot(zx, st["pstar"], 0, CC, ms=8)
        lim = max(e.X, e.Y) * 1.1
        zx.set_ylim(-lim, lim)
        zx.set_xlim(0, pmax)
        zx.set_xlabel(r"$p = p_x/p_y$", color=INK, fontsize=9, loc="right")
        zx.set_title("Excess demand", loc="left", color=INK, fontsize=9.5)
        legend(zx, loc="upper right")
        fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.12)

    def describe(self, st):
        if not st["ok"]:
            return table([("Economy", "Give each good a positive total.")])
        e, v, p, eq = st["e"], st["v"], st["p"], st["eq"]
        (xA, yA), (xB, yB) = st["dem"]
        zxv, zyv = st["z"]
        clears = abs(zxv) < 1e-6 and abs(zyv) < 1e-6
        if clears:
            verdict = "both markets clear"
        elif zxv > 0:
            verdict = "x is too cheap: excess demand for x, excess supply of y"
        else:
            verdict = "x is too dear: excess supply of x, excess demand for y"
        rows = [
            ("Economy", "A: u = %s, owns %s. B: u = %s, owns %s. The box is %s &times; %s."
             % (tastes(e.a), bundle(e.wA), tastes(e.b), bundle(e.wB), num(e.X), num(e.Y))),
            ("Price", ("p = %s, set by hand. The market-clearing ratio is p* = %s." %
                       (num(p), num(st["pstar"])) if self.flag("manual") else
                       "p* = %s clears the market: good x is worth %s units of y."
                       % (num(p), num(p)))),
            ("Incomes", "m<sub>A</sub> = %s&middot;%s + %s = %s; m<sub>B</sub> = %s&middot;%s + "
                        "%s = %s." % (num(p), num(e.wA[0]), num(e.wA[1]), num(st["inc"][0]),
                                      num(p), num(e.wB[0]), num(e.wB[1]), num(st["inc"][1]))),
            ("Demands", "A wants %s, B wants %s." % (bundle((xA, yA)), bundle((xB, yB)))),
            ("Excess demand", "z<sub>x</sub> = %s, z<sub>y</sub> = %s: %s."
             % (num(zxv), num(zyv), verdict)),
            ("Walras' law", "p&middot;z<sub>x</sub> + z<sub>y</sub> = %s&middot;(%s) + (%s) = %s, at "
                            "this price and every other." % (num(p), num(zxv), num(zyv),
                                                             num(e.walras(p)))),
        ]
        tA = eq["tradeA"]
        rows.append(("Equilibrium",
                     "At p* = %s: A gets %s, B gets %s. A %s %s of x and %s %s of y; the value of "
                     "her trade is %s." % (
                         num(eq["p"]), bundle(eq["A"]), bundle(eq["B"]),
                         "buys" if tA[0] >= 0 else "sells", num(abs(tA[0])),
                         "sells" if tA[1] <= 0 else "buys", num(abs(tA[1])),
                         num(eq["p"] * tA[0] + tA[1]))))
        rows.append(("Tangency", "MRS<sub>A</sub> = %s and MRS<sub>B</sub> = %s at the "
                                 "equilibrium: both equal p*, so it is on the contract curve."
                     % (num(e.mrsA(*eq["A"])), num(e.mrsB(*eq["B"])))))
        rows.append(("Contract curve", contract_text(e)))
        if self.flag("lens"):
            lo, hi = e.core()
            rows.append(("Core", "The contract curve from x<sub>A</sub> = %s to %s: efficient "
                                 "and better than &omega; for both. The equilibrium, x<sub>A</sub> "
                                 "= %s, is inside it." % (num(lo), num(hi), num(eq["A"][0]))))
        if "pt" in st:
            x, y = st["pt"]
            bxp, byp = e.b_bundle(x, y)
            if min(x, y, bxp, byp) <= 0:
                rows.append(("Marked", "A %s, B %s: on the edge of the box." %
                             (bundle((x, y)), bundle((bxp, byp)))))
            else:
                ma, mb = e.mrsA(x, y), e.mrsB(bxp, byp)
                if abs(ma - mb) < 1e-6 * max(1, ma):
                    eff = "equal, so the allocation is Pareto efficient"
                else:
                    who = "A" if ma > mb else "B"
                    eff = ("not equal, so it is not efficient: move x to %s at any rate between "
                           "%s and %s units of y per unit of x, and both gain"
                           % (who, num(min(ma, mb)), num(max(ma, mb))))
                rows.append(("Marked", "A %s, B %s. MRS<sub>A</sub> = %s, MRS<sub>B</sub> = %s: "
                                       "%s. On the contract curve, x<sub>A</sub> = %s goes with "
                                       "y<sub>A</sub> = %s. %s"
                             % (bundle((x, y)), bundle((bxp, byp)), num(ma), num(mb), eff,
                                num(x), num(e.contract(x)),
                                "Both prefer it to &omega;." if e.in_lens(x, y) else
                                "Someone prefers &omega;, so it is outside the lens.")))
        if st["before"] is not None:
            b = st["before"].equilibrium()
            rows.append(("Before &rarr; after", "p* %s &rarr; %s; A's bundle %s &rarr; %s"
                         % (num(b["p"]), num(eq["p"]), bundle(b["A"]), bundle(eq["A"]))))
        return table(rows)


# ======================================================================
# Lab 2: the second welfare theorem
# ======================================================================

SUPPORT = dict(a=0.75, b=0.5, wAx=8.0, wAy=8.0, wBx=4.0, wBy=4.0, F=6.0)


class WelfareLab(Lab):
    TITLE = "Lab 2 &middot; The second welfare theorem"
    INTRO = ("Pick an efficient point F on the contract curve. Its common tangent gives the "
             "price ratio that supports it, and a lump-sum transfer moves the endowment "
             "onto that line, here by moving good y between the two. Then both agents "
             "choose F on their own. Cobb&ndash;Douglas tastes are convex, so this always "
             "works; the notes' Figure 10 shows how non-convex tastes break it.")
    SLIDERS = [
        ("a", 0.05, 0.95, 0.01, 0.75, ".2f"),
        ("b", 0.05, 0.95, 0.01, 0.5, ".2f"),
        ("wAx", 0.0, 20.0, 0.5, 8.0, ".1f"),
        ("wAy", 0.0, 20.0, 0.5, 8.0, ".1f"),
        ("wBx", 0.0, 20.0, 0.5, 4.0, ".1f"),
        ("wBy", 0.0, 20.0, 0.5, 4.0, ".1f"),
        ("F", 0.1, 40.0, 0.1, 6.0, ".1f"),
    ]
    CHECKS = [("lens", "Show the lens through ω and the core")]
    FIGSIZE = (6.0, 5.4)
    PRESETS = [
        dict(label="Notes p. 11 F = (6, 3)", kind="notes", values=SUPPORT,
             flags=dict(lens=True)),
        dict(label="Notes p. 14 F at the equilibrium", kind="notes",
             values=dict(SUPPORT, F=9.0), flags=dict(lens=True)),
        dict(label="A6.1 F = equal split", kind="problem",
             values=dict(a=0.5, b=0.5, wAx=3.0, wAy=9.0, wBx=9.0, wBy=3.0, F=6.0)),
        dict(label="A6.2 (f) F = (6, 2.4)", kind="problem",
             values=dict(a=2 / 3, b=1 / 3, wAx=3.0, wAy=9.0, wBx=9.0, wBy=3.0, F=6.0)),
    ]

    def relabel(self):
        html_label(self.w["a"], "a: A's share on x")
        html_label(self.w["b"], "b: B's share on x")
        html_label(self.w["wAx"], "&omega;<sub>A</sub> of x")
        html_label(self.w["wAy"], "&omega;<sub>A</sub> of y")
        html_label(self.w["wBx"], "&omega;<sub>B</sub> of x")
        html_label(self.w["wBy"], "&omega;<sub>B</sub> of y")
        html_label(self.w["F"], "F: A's x on the curve")

    def compute(self):
        v = self.values()
        e = economy(v)
        st = dict(v=v, e=e, ok=e.X > 0 and e.Y > 0)
        if not st["ok"]:
            return st
        xF = min(max(v["F"], e.X * 0.01), e.X * 0.99)
        st["xF"] = xF
        st["s"] = e.support(xF)
        st["eq"] = e.equilibrium()
        p, T = st["s"]["p"], st["s"]["T"]
        # The new endowment: A keeps her x and gives up T units of y, unless
        # that would leave the box; then move x instead.
        wx, wy = e.wA
        if 0 <= wy - T <= e.Y:
            st["new"] = (wx, wy - T)
        else:
            st["new"] = (min(max(wx - T / p, 0), e.X), wy)
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        if not st["ok"]:
            ax.axis("off")
            ax.text(0.5, 0.5, "Both goods need a positive total.", ha="center", color=MUTE)
            return
        e, s = st["e"], st["s"]
        box_axes(ax, e)
        ed.contract(ax, e, color=CC, lw=2, label="contract curve")
        if self.flag("lens"):
            ed.lens(ax, e, *e.wA, color=LENS, alpha=0.14)
            core_segment(ax, e)
        F = s["F"]
        ed.ic_a(ax, e, *F, color=A_COL, lw=1.4)
        ed.ic_b(ax, e, *F, color=B_COL, lw=1.4)
        ed.price_line(ax, e, s["p"], *F, color=INK, lw=1.6, label="supporting line")
        dot(ax, *st["eq"]["A"], CC, hollow=True)
        ax.annotate("CE from ω", st["eq"]["A"], textcoords="offset points", xytext=(8, -12),
                    color=CC, fontsize=8.5)
        dot(ax, *e.wA, MUTE)
        ax.annotate("ω", e.wA, textcoords="offset points", xytext=(7, 5), color=MUTE)
        new = st["new"]
        if abs(s["T"]) > 1e-6:
            ax.annotate("", xy=new, xytext=e.wA,
                        arrowprops=dict(arrowstyle="-|>", color=NEW, lw=1.4, shrinkA=5, shrinkB=5))
        dot(ax, *new, NEW)
        ax.annotate("ω̃", new, textcoords="offset points", xytext=(7, 5), color=NEW)
        dot(ax, *F, LENS, ms=8)
        ax.annotate("F", F, textcoords="offset points", xytext=(-12, 4), color=LENS, fontsize=11)
        legend(ax, loc="upper left")
        ax.get_legend().set_zorder(10)
        fig.subplots_adjust(left=0.08, right=0.93, top=0.92, bottom=0.1)

    def describe(self, st):
        if not st["ok"]:
            return table([("Economy", "Give each good a positive total.")])
        e, s, eq = st["e"], st["s"], st["eq"]
        F, p, T = s["F"], s["p"], s["T"]
        FB = e.b_bundle(*F)
        vA = p * e.wA[0] + e.wA[1]
        vF = p * F[0] + F[1]
        if abs(T) < 1e-6:
            move = "No transfer is needed: &omega; is already on the line, so F is the market's own outcome."
        else:
            move = ("A hands B %s units of y as a lump sum (worth the same as %s units of x)"
                    % (num(T), num(T / p)) if T > 0 else
                    "B hands A %s units of y as a lump sum (worth the same as %s units of x)"
                    % (num(-T), num(-T / p)))
            move += "; the new endowment is &omega;&#771; = %s." % bundle(st["new"])
        uA, uB = e.uA(*F), e.uB(*FB)
        uA0, uB0 = e.uA(*e.wA), e.uB(*e.wB)
        rows = [
            ("F", "A %s, B %s: on the contract curve, so Pareto efficient." % (bundle(F), bundle(FB))),
            ("Supporting price", "MRS<sub>A</sub> = MRS<sub>B</sub> = %s at F, so p = %s." % (num(p), num(p))),
            ("Values at p", "A's endowment %s is worth %s; F is worth %s." % (bundle(e.wA), num(vA), num(vF))),
            ("Transfer", move),
            ("Without it", "From &omega; the market would pick the equilibrium at p* = %s, with A at %s."
             % (num(eq["p"]), bundle(eq["A"]))),
            ("The core", "At F, A gets u = %s against %s at &omega;, and B gets %s against %s. %s"
             % (num(uA), num(uA0), num(uB), num(uB0),
                "Both are at least as well off, so F is in the core." if e.in_lens(*F) else
                "%s is worse off, so F is outside the core: nobody would trade there voluntarily, "
                "which is why it takes a transfer." % ("A" if uA < uA0 else "B"))),
        ]
        return table(rows)


market = MarketLab()
welfare = WelfareLab()
