"""
sandbox_s08.py - session 8 sandbox: firms, tasks and technology (AI).

    substitution  Lab 1  the cheapest mix of workers and machines, sigma, and
                         labor's share of costs
    tasks         Lab 2  the automation cutoff, task savings and the saving
                         index G, with its kinks
    review        Lab 3  AI that needs a human to check it, for one task
    tilt          Lab 4  the two-sector frontier tilted by a labor saving

Released with the session 8 solutions. The maths is firms.py.
"""

import math

import numpy as np

import firms as fm
from sandbox import Lab, html_label, legend, num, style_axes, table
from style import BEFORE, CURVE, GREY, INK, LINE, MUTE, NEW


def pct_change(a, b):
    return 100 * (b / a - 1) if a else float("nan")


# ======================================================================
# Lab 1: substitution
# ======================================================================

CES = "CES (set σ with the slider)"
SUBS = "Perfect substitutes, σ = ∞"
COMPS = "Perfect complements, σ = 0"

P_NOTES = dict(family=CES, sigma=1.0, w=10.0, r=10.0, q=4.0)


def sigma_of(v):
    return {SUBS: math.inf, COMPS: 0.0}.get(v["family"], v["sigma"])


def substitution_state(v):
    s = sigma_of(v)
    b = fm.ces_bundle(v["q"], v["w"], v["r"], s)
    st = dict(sigma=s, bundle=b)
    if b is not None:
        E, K = b
        st.update(E=E, K=K, cost=v["w"] * E + v["r"] * K,
                  ratio=K / E if E > 0 else math.inf,
                  share=v["w"] * E / (v["w"] * E + v["r"] * K))
    return st


def isoquant(ax, q, sigma, top, **kw):
    if sigma == math.inf:
        ax.plot([0, q], [q, 0], **kw)
        return
    if sigma == 0:
        ax.plot([q, q, top], [top, q, q], **kw)
        return
    Es = np.linspace(top * 0.01, top, 400)
    if abs(sigma - 1) < 1e-9:
        Ks = q * q / Es
    else:
        rho = (sigma - 1) / sigma
        with np.errstate(all="ignore"):
            inner = (q ** rho - 0.5 * Es ** rho) / 0.5
            Ks = np.where(inner > 0, inner ** (1 / rho), np.nan)
    ax.plot(Es, Ks, **kw)


class SubstitutionLab(Lab):
    TITLE = "Lab 1 &middot; Substitution: workers and machines"
    INTRO = ("Make q units as cheaply as possible from workers E (wage w) and machines or AI "
             "capital K (rental r). The CES technology has equal weights, so &sigma; = 1 is "
             "q = &radic;(EK). Freeze a 'before' and move w or r to measure &sigma; from the "
             "two bundles.")
    FAMILIES = [CES, SUBS, COMPS]
    SLIDERS = [
        ("sigma", 0.1, 4.0, 0.05, 1.0, ".2f"),
        ("w", 0.5, 40.0, 0.5, 10.0, ".1f"),
        ("r", 0.5, 40.0, 0.5, 10.0, ".1f"),
        ("q", 1.0, 10.0, 0.5, 4.0, ".1f"),
    ]
    FIGSIZE = (8.4, 4.2)
    PRESETS = [
        dict(label="Notes p. 4 P = (4, 4)", kind="notes", values=P_NOTES),
        dict(label="Notes p. 4 wage to a quarter", kind="notes", before=P_NOTES,
             values=dict(P_NOTES, w=2.5)),
        dict(label="Notes p. 5 σ = 2, cheaper AI", kind="notes",
             before=dict(P_NOTES, sigma=2.0), values=dict(P_NOTES, sigma=2.0, r=2.5)),
        dict(label="Notes p. 5 σ = 1/2, cheaper AI", kind="notes",
             before=dict(P_NOTES, sigma=0.5), values=dict(P_NOTES, sigma=0.5, r=2.5)),
        dict(label="Notes p. 4 perfect substitutes", kind="notes",
             values=dict(P_NOTES, family=SUBS, r=8.0)),
        dict(label="Notes p. 4 perfect complements", kind="notes",
             values=dict(P_NOTES, family=COMPS, r=5.0)),
        dict(label="Review Q3 Transnor", kind="notes", before=dict(P_NOTES, sigma=1.5),
             values=dict(P_NOTES, sigma=1.5, w=11.0)),
    ]

    def relabel(self):
        ces = self.w["family"].value == CES
        html_label(self.w["sigma"], "&sigma;" if ces else "&sigma; (CES only)")
        self.w["sigma"].disabled = not ces
        self.w["w"].description = "Wage w"
        self.w["r"].description = "Rental r"
        self.w["q"].description = "Output q"

    def compute(self):
        v = self.values()
        st = dict(v=v, live=substitution_state(v))
        st["before"] = substitution_state(self.before) if self.before else None
        st["top"] = self.stick("t", v["q"] * 2.6)
        return st

    def figure(self, fig, st):
        ax, sh = fig.subplots(1, 2)
        v, s, top = st["v"], st["live"], st["top"]
        style_axes(ax)
        if st["before"] is not None and st["before"]["bundle"] is not None:
            b = st["before"]
            ax.plot([b["E"]], [b["K"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8, zorder=6,
                    label="before")
        isoquant(ax, v["q"], s["sigma"], top, color=CURVE, lw=2, label="isoquant q = %s" % num(v["q"]))
        if s["bundle"] is not None:
            E, K = s["E"], s["K"]
            C = s["cost"]
            ax.plot([0, C / v["w"]], [C / v["r"], 0], color=LINE, lw=1.5,
                    label="isocost, slope −w/r")
            ax.plot([E], [K], "o", color=LINE, ms=8, zorder=7)
            if E > 0:
                ax.plot([0, top], [0, top * K / E], color=MUTE, lw=0.8, ls=":")
        else:
            ax.plot([0, v["q"]], [v["q"], 0], color=LINE, lw=3, alpha=0.5, label="every bundle ties")
        ax.set_xlim(0, top)
        ax.set_ylim(0, top)
        ax.set_xlabel("workers E", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("machines K", color=INK, fontsize=9, loc="top")
        legend(ax)

        style_axes(sh)
        here = v["r"] / v["w"]
        xmax = self.stick("rw", max(2.0, here * 1.2,
                                    self.before["r"] / self.before["w"] * 1.2 if self.before else 0))
        rw = np.linspace(xmax * 0.02, xmax, 200)
        sig = s["sigma"]
        if sig not in (0.0, math.inf) and abs(sig - 1) > 1e-9:
            sh.plot(rw, [fm.labor_share(x, sig) for x in rw], color=NEW, lw=2,
                    label="σ = %s" % num(sig))
        sh.plot(rw, [0.5] * len(rw), color=MUTE, lw=1, ls="--", label="σ = 1")
        if st["before"] is not None and st["before"]["bundle"] is not None:
            sh.plot([self.before["r"] / self.before["w"]], [st["before"]["share"]], "o",
                    mfc="white", mec=BEFORE, mew=1.6, ms=8, zorder=5)
        if s["bundle"] is not None:
            sh.plot([here], [s["share"]], "o", color=NEW, ms=8, zorder=6)
        sh.set_xlim(0, xmax)
        sh.set_ylim(0, 1)
        sh.set_xlabel("r/w (AI cheaper: to the left)", color=INK, fontsize=9, loc="right")
        sh.set_title("Labor's share of costs", loc="left", color=INK, fontsize=9.5)
        legend(sh, loc="lower right")
        fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.13, wspace=0.25)

    def describe(self, st):
        v, s = st["v"], st["live"]
        sig = s["sigma"]
        rows = [("Technology", {math.inf: "Perfect substitutes, q = E + K: straight isoquants, "
                                          "&sigma; = &infin;.",
                                0.0: "Perfect complements, q = min(E, K): L-shaped isoquants, "
                                     "&sigma; = 0."}.get(
            sig, "CES with equal weights, &sigma; = %s%s." % (
                num(sig), ": q = &radic;(EK)" if abs(sig - 1) < 1e-9 else "")))]
        if s["bundle"] is None:
            rows.append(("Cheapest mix", "w = r: every bundle on the straight isoquant costs the "
                                         "same."))
            return table(rows)
        rows.append(("Cheapest mix", "E = %s, K = %s at cost %s. K/E = %s against w/r = %s."
                     % (num(s["E"]), num(s["K"]), num(s["cost"]), num(s["ratio"]),
                        num(v["w"] / v["r"]))))
        rows.append(("Labor's share", "wE/(wE + rK) = %s." % num(s["share"])))
        b = st["before"]
        if b is not None and b["bundle"] is not None:
            bv = self.before
            dr = pct_change(b["ratio"], s["ratio"]) if b["E"] > 0 and s["E"] > 0 else float("nan")
            dp = pct_change(bv["w"] / bv["r"], v["w"] / v["r"])
            text = "K/E %s &rarr; %s (%s%%), w/r %s &rarr; %s (%s%%)" % (
                num(b["ratio"]), num(s["ratio"]), num(dr, 1), num(bv["w"] / bv["r"]),
                num(v["w"] / v["r"]), num(dp, 1))
            if abs(dp) > 1e-9 and math.isfinite(dr):
                text += ": %%&Delta;(K/E)/%%&Delta;(w/r) = %s" % num(dr / dp)
                lr = math.log(s["ratio"] / b["ratio"]) if b["ratio"] > 0 and s["ratio"] > 0 else None
                lp = math.log((v["w"] / v["r"]) / (bv["w"] / bv["r"]))
                if lr is not None:
                    text += ", or %s in logs" % num(lr / lp)
            rows.append(("Before &rarr; after", text + "."))
            shares = "labor's share %s &rarr; %s" % (num(b["share"]), num(s["share"]))
            # With perfect substitutes the firm may hire no workers at all. Then
            # rK/(wE) divides by zero, so there is no percentage change to report.
            if b["share"] > 0 and s["share"] > 0:
                shares += (", so relative spending on capital rK/(wE) changed by %s%%"
                           % num(pct_change((1 - b["share"]) / b["share"],
                                            (1 - s["share"]) / s["share"]), 1))
            rows.append(("Shares", shares + "."))
        rows.append(("Wages", "Two inputs, constant returns, a fixed labor force: more capital "
                              "never lowers the wage, whatever &sigma; is. That needs the task model."))
        return table(rows)


# ======================================================================
# Lab 2: tasks and the saving index
# ======================================================================

TRY = dict(w=300.0, r=600.0, A1=4.0, A2=2.0, A3=1.0, x1=1 / 3, x2=1 / 3, x3=1 / 3, C0=100.0)
NORD = dict(w=500.0, r=1000.0, A1=10.0, A2=5.0, A3=1.0, x1=0.2, x2=0.4, x3=0.4, C0=100.0)
KYST = dict(w=3.0, r=2.0, A1=2.0, A2=1.0, A3=0.5, x1=0.25, x2=0.5, x3=0.25, C0=100.0)
FJORD = dict(w=2.0, r=3.0, A1=3.0, A2=2.0, A3=1.0, x1=0.5, x2=0.25, x3=0.25, C0=160.0)


def task_state(v):
    A = [v["A1"], v["A2"], v["A3"]]
    raw = [v["x1"], v["x2"], v["x3"]]
    tot = sum(raw) or 1.0
    shares = [x / tot for x in raw]
    w, r = v["w"], v["r"]
    pis = [fm.saving(a, w, r) for a in A]
    G = sum(s * p for s, p in zip(shares, pis))
    return dict(A=A, shares=shares, w=w, r=r, pis=pis, G=G, auto=[fm.automated(a, w, r) for a in A],
                thr=fm.thresholds(A, w), cost=v["C0"] * (1 - G))


class TaskLab(Lab):
    TITLE = "Lab 2 &middot; Which tasks does AI take, and how much does it save?"
    INTRO = ("Three tasks. A worker-hour makes one task-unit at wage w; an AI-service unit makes "
             "A<sub>i</sub> task-units at rental r. AI wins a task when r/A<sub>i</sub> &lt; w, that "
             "is A<sub>i</sub> &gt; r/w (ties go to labor). The saving index G weights each task's "
             "saving by its share &chi;<sub>i</sub> of the all-labor cost; the shares are rescaled "
             "to sum to one.")
    SLIDERS = [
        ("w", 0.5, 600.0, 0.5, 300.0, ".1f"),
        ("r", 0.05, 6000.0, 0.05, 600.0, ".2f"),
        ("A1", 0.05, 12.0, 0.05, 4.0, ".2f"),
        ("A2", 0.05, 12.0, 0.05, 2.0, ".2f"),
        ("A3", 0.05, 12.0, 0.05, 1.0, ".2f"),
        ("x1", 0.0, 1.0, 0.01, 1 / 3, ".2f"),
        ("x2", 0.0, 1.0, 0.01, 1 / 3, ".2f"),
        ("x3", 0.0, 1.0, 0.01, 1 / 3, ".2f"),
        ("C0", 0.0, 1000.0, 1.0, 100.0, ".0f"),
    ]
    FIGSIZE = (8.4, 4.2)
    PRESETS = [
        dict(label="Notes p. 7 Try it", kind="notes", values=TRY),
        dict(label="Review Q2 r = 450", kind="notes", before=TRY, values=dict(TRY, r=450.0)),
        dict(label="Notes p. 11 Nordvik (a)", kind="notes", values=NORD),
        dict(label="Nordvik (c) r = 100", kind="notes", before=NORD, values=dict(NORD, r=100.0)),
        dict(label="Review Q4 Kyst", kind="notes", values=KYST),
        dict(label="Kyst (c) r = 1", kind="notes", before=KYST, values=dict(KYST, r=1.0)),
        dict(label="A8.2 Fjordline", kind="problem", values=FJORD),
        dict(label="A8.2 (d) r = 3/2", kind="problem", before=FJORD, values=dict(FJORD, r=1.5)),
        dict(label="A8.2 tie at r = 2", kind="problem", values=dict(FJORD, r=2.0)),
    ]

    def relabel(self):
        self.w["w"].description = "Wage w"
        self.w["r"].description = "AI rental r"
        for i in (1, 2, 3):
            html_label(self.w["A%d" % i], "A<sub>%d</sub>, task %d" % (i, i))
            html_label(self.w["x%d" % i], "&chi;<sub>%d</sub>, cost share" % i)
        self.w["C0"].description = "All-labor order cost"

    def compute(self):
        v = self.values()
        st = dict(v=v, live=task_state(v))
        st["before"] = task_state(self.before) if self.before else None
        top = max(st["live"]["thr"] + [v["r"]] + ([self.before["r"]] if self.before else []))
        st["rmax"] = self.stick("r", top * 1.15)
        return st

    def figure(self, fig, st):
        bx, gx = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1, 1.2]))
        s = st["live"]
        style_axes(bx)
        xs = np.arange(3)
        bx.bar(xs, s["A"], color=[LINE if a else GREY for a in s["auto"]], width=0.6)
        bx.axhline(s["r"] / s["w"], color=INK, lw=1.6, ls="--", label="cutoff r/w = %s"
                   % num(s["r"] / s["w"]))
        if st["before"] is not None:
            b = st["before"]
            bx.axhline(b["r"] / b["w"], color=BEFORE, lw=1.2, ls=":", label="before")
        bx.set_xticks(xs)
        bx.set_xticklabels(["task 1", "task 2", "task 3"], fontsize=9)
        bx.set_title("AI productivity A (blue: AI)", loc="left", color=INK, fontsize=9.5)
        legend(bx)

        style_axes(gx)
        rmax = st["rmax"]
        rs = np.linspace(rmax * 0.001, rmax, 600)
        gx.plot(rs, [fm.index(s["A"], s["shares"], s["w"], r) for r in rs], color=LINE, lw=2)
        for t in s["thr"]:
            if t <= rmax:
                gx.axvline(t, color=MUTE, lw=0.8, ls=":")
        gx.plot([s["r"]], [s["G"]], "o", color=NEW, ms=8, zorder=5)
        if st["before"] is not None:
            b = st["before"]
            gx.plot([b["r"]], [b["G"]], "o", mfc="white", mec=BEFORE, mew=1.6, ms=8, zorder=5)
        gx.set_xlim(0, rmax)
        gx.set_ylim(0, 1.02)
        gx.set_xlabel("AI rental r (cheaper to the left)", color=INK, fontsize=9, loc="right")
        gx.set_title("Saving index G(r): kinks, not jumps", loc="left", color=INK, fontsize=9.5)
        fig.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.13, wspace=0.22)

    def describe(self, st):
        s = st["live"]
        w, r = s["w"], s["r"]
        lines = []
        for i in range(3):
            ai = r / s["A"][i]
            choice = ("AI" if s["auto"][i] else
                      "labor (a tie: either method)" if abs(ai - w) < 1e-9 else "labor")
            lines.append("task %d: human %s, AI %s &rarr; %s, saving %s, share %s"
                         % (i + 1, num(w), num(ai), choice, num(s["pis"][i]), num(s["shares"][i])))
        rows = [
            ("Cutoff", "A&#772; = r/w = %s: AI takes every task with A above it." % num(r / w)),
            ("Tasks", "<br>".join(lines)),
            ("Index", "G = &Sigma; &chi;<sub>i</sub>&pi;<sub>i</sub> = %s: the fixed order's cost "
                      "falls from %s to %s. A cost reduction for a fixed recipe, not an exact "
                      "change in log TFP." % (num(s["G"], 4), num(st["v"]["C0"]), num(s["cost"]))),
            ("Thresholds", "Tasks cross at r<sub>i</sub> = wA<sub>i</sub> = %s."
             % ", ".join(num(t) for t in s["thr"])),
        ]
        waiting = [(t, i) for i, t in enumerate(s["thr"]) if t <= r + 1e-9]
        if waiting:
            t, i = max(waiting)
            rows.append(("Next", "Task %d switches to AI once r falls below %s." % (i + 1, num(t))))
        else:
            rows.append(("Next", "Every task already uses AI; cheaper AI only deepens the savings."))
        if st["before"] is not None:
            b = st["before"]
            old = sum(sh * (p1 - p0) for sh, p0, p1, a0 in
                      zip(s["shares"], b["pis"], s["pis"], b["auto"]) if a0)
            new = sum(sh * (p1 - p0) for sh, p0, p1, a0 in
                      zip(s["shares"], b["pis"], s["pis"], b["auto"]) if not a0)
            rows.append(("Before &rarr; after", "G %s &rarr; %s: %s from tasks already automated, "
                                                "%s from newly automated ones."
                         % (num(b["G"], 4), num(s["G"], 4), num(old, 4), num(new, 4))))
        return table(rows)


# ======================================================================
# Lab 3: AI that needs review
# ======================================================================

REPORT = dict(w=300.0, h=1.0, f=60.0, t=0.25)
SUMMARY = dict(w=30.0, h=1.0, f=6.0, t=0.2)


class ReviewLab(Lab):
    TITLE = "Lab 3 &middot; AI that needs review"
    INTRO = ("One completed task. By hand it takes h hours at wage w. With AI it costs a fee f "
             "plus t hours of human review. Compare completed tasks, not drafts: AI wins when "
             "f + wt &lt; wh.")
    SLIDERS = [
        ("w", 1.0, 400.0, 1.0, 300.0, ".0f"),
        ("h", 0.0, 2.0, 0.05, 1.0, ".2f"),
        ("f", 0.0, 200.0, 0.5, 60.0, ".1f"),
        ("t", 0.0, 2.0, 0.05, 0.25, ".2f"),
    ]
    FIGSIZE = (8.4, 4.0)
    PRESETS = [
        dict(label="Notes p. 9 report, quarter-hour review", kind="notes", values=REPORT),
        dict(label="Notes p. 9 review 9/10 hour", kind="notes", before=REPORT,
             values=dict(REPORT, t=0.9)),
        dict(label="A8.3 summary", kind="problem", values=SUMMARY),
        dict(label="A8.3 compliance", kind="problem",
             values=dict(SUMMARY, h=0.5, f=3.0, t=0.5)),
        dict(label="A8.3 chart", kind="problem", values=dict(SUMMARY, h=0.8, f=9.0, t=0.1)),
        dict(label="A8.3 (d) summary fee halved", kind="problem", before=SUMMARY,
             values=dict(SUMMARY, f=3.0)),
        dict(label="A8.3 (e) compliance at w = 40", kind="problem",
             before=dict(SUMMARY, h=0.5, f=3.0, t=0.5), values=dict(SUMMARY, w=40.0, h=0.5, f=3.0, t=0.5)),
    ]

    def relabel(self):
        self.w["w"].description = "Wage w"
        self.w["h"].description = "Hours by hand h"
        self.w["f"].description = "AI fee f"
        self.w["t"].description = "Review hours t"

    def compute(self):
        v = self.values()
        cH, cA = fm.review_costs(v["w"], v["h"], v["f"], v["t"])
        return dict(v=v, cH=cH, cA=cA, tmax=fm.max_review(v["w"], v["h"], v["f"]),
                    wstar=fm.breakeven_wage(v["h"], v["f"], v["t"]),
                    wtop=self.stick("w", max(v["w"], 1) * 2))

    def figure(self, fig, st):
        wx, tx = fig.subplots(1, 2)
        v = st["v"]
        style_axes(wx)
        ws = np.linspace(0, st["wtop"], 100)
        wx.plot(ws, ws * v["h"], color=MUTE, lw=2, label="by hand, wh")
        wx.plot(ws, v["f"] + ws * v["t"], color=LINE, lw=2, label="AI + review, f + wt")
        wx.axvline(v["w"], color=INK, lw=0.8, ls=":")
        if math.isfinite(st["wstar"]) and st["wstar"] <= st["wtop"]:
            wx.plot([st["wstar"]], [st["wstar"] * v["h"]], "o", color=NEW, ms=7, zorder=5)
        wx.set_xlim(0, st["wtop"])
        wx.set_ylim(0, None)
        wx.set_xlabel("wage w", color=INK, fontsize=9, loc="right")
        wx.set_title("Cost per completed task", loc="left", color=INK, fontsize=9.5)
        legend(wx, loc="upper left")

        style_axes(tx)
        ts = np.linspace(0, 2, 100)
        tx.plot(ts, v["f"] + v["w"] * ts, color=LINE, lw=2, label="AI + review")
        tx.axhline(st["cH"], color=MUTE, lw=2, label="by hand")
        tx.plot([v["t"]], [st["cA"]], "o", color=NEW, ms=8, zorder=5)
        tx.set_xlim(0, 2)
        tx.set_ylim(0, None)
        tx.set_xlabel("review hours t", color=INK, fontsize=9, loc="right")
        tx.set_title("At this wage", loc="left", color=INK, fontsize=9.5)
        legend(tx, loc="upper left")
        fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.13, wspace=0.22)

    def describe(self, st):
        v = st["v"]
        cH, cA = st["cH"], st["cA"]
        pick = ("AI with review" if cA < cH - 1e-9 else "by hand" if cA > cH + 1e-9 else
                "either: a tie")
        rows = [
            ("Costs", "By hand %s&middot;%s = %s; AI %s + %s&middot;%s = %s. Cheaper: %s."
             % (num(v["w"]), num(v["h"]), num(cH), num(v["f"]), num(v["w"]), num(v["t"]),
                num(cA), pick)),
            ("Review limit", "AI stays weakly cheaper while t &le; h &minus; f/w = %s hours."
             % num(st["tmax"]) if st["tmax"] >= 0 else
             "Even with no review the fee alone exceeds the hand-made cost."),
            ("Wage", "AI's advantage is w(h &minus; t) &minus; f. %s" % (
                "A higher wage helps AI here; it breaks even at w = f/(h &minus; t) = %s."
                % num(st["wstar"]) if math.isfinite(st["wstar"]) else
                "Review takes at least as long as the job, so no wage makes AI cheaper.")),
        ]
        if self.before:
            b = self.before
            bh, ba = fm.review_costs(b["w"], b["h"], b["f"], b["t"])
            rows.append(("Before &rarr; after", "by hand %s &rarr; %s, AI %s &rarr; %s"
                         % (num(bh), num(cH), num(ba), num(cA))))
        return table(rows)


# ======================================================================
# Lab 4: the tilted frontier
# ======================================================================

TEN = dict(L=10.0, aX=2.0, aY=3.0, piX=0.2, piY=0.0)


class TiltLab(Lab):
    TITLE = "Lab 4 &middot; The tilted frontier"
    INTRO = ("A fixed labor pool L moves between two sectors with constant output per worker "
             "a<sub>X</sub> and a<sub>Y</sub>. Technology cuts the labor needed per unit by &pi;, "
             "so output per worker becomes a/(1 &minus; &pi;).")
    SLIDERS = [
        ("L", 1.0, 30.0, 1.0, 10.0, ".0f"),
        ("aX", 0.5, 6.0, 0.1, 2.0, ".1f"),
        ("aY", 0.5, 6.0, 0.1, 3.0, ".1f"),
        ("piX", 0.0, 0.9, 0.01, 0.2, ".2f"),
        ("piY", 0.0, 0.9, 0.01, 0.0, ".2f"),
    ]
    FIGSIZE = (6.0, 4.6)
    PRESETS = [
        dict(label="Notes p. 15 ten workers", kind="notes", values=TEN),
        dict(label="Review Q6 π = 1/4", kind="notes", values=dict(TEN, piX=0.25)),
        dict(label="Only Y improves", kind="notes", values=dict(TEN, piX=0.0, piY=0.2)),
    ]

    def relabel(self):
        html_label(self.w["L"], "Workers L")
        html_label(self.w["aX"], "a<sub>X</sub>, output per worker")
        html_label(self.w["aY"], "a<sub>Y</sub>, output per worker")
        html_label(self.w["piX"], "&pi;<sub>X</sub>, labor saving")
        html_label(self.w["piY"], "&pi;<sub>Y</sub>, labor saving")

    def compute(self):
        v = self.values()
        aX2, aY2 = fm.improved(v["aX"], v["piX"]), fm.improved(v["aY"], v["piY"])
        st = dict(v=v, before=fm.frontier(v["aX"], v["aY"], v["L"]),
                  after=fm.frontier(aX2, aY2, v["L"]), aX2=aX2, aY2=aY2)
        st["top"] = self.stick("t", max(st["after"][0], st["after"][1]) * 1.1)
        return st

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        X0, Y0, _ = st["before"]
        X1, Y1, _ = st["after"]
        ax.plot([0, X0], [Y0, 0], color=LINE, lw=2, label="before")
        ax.plot([0, X1], [Y1, 0], color=NEW, lw=2, ls="--", label="after")
        ax.set_xlim(0, st["top"])
        ax.set_ylim(0, st["top"])
        ax.set_xlabel("X", color=INK, loc="right")
        ax.set_ylabel("Y", color=INK, loc="top")
        legend(ax)
        fig.tight_layout()

    def describe(self, st):
        v = st["v"]
        X0, Y0, s0 = st["before"]
        X1, Y1, s1 = st["after"]
        rows = [
            ("Output per worker", "X: %s &rarr; %s (factor %s); Y: %s &rarr; %s."
             % (num(v["aX"]), num(st["aX2"]), num(1 / (1 - v["piX"])), num(v["aY"]), num(st["aY2"]))),
            ("Intercepts", "X: %s &rarr; %s; Y: %s &rarr; %s." % (num(X0), num(X1), num(Y0), num(Y1))),
            ("Opportunity cost", "One more X costs %s &rarr; %s units of Y. If labor is mobile and "
                                 "both goods are produced, p<sub>X</sub>/p<sub>Y</sub> equals it."
             % (num(s0), num(s1))),
            ("What it doesn't say", "Demand, how labor reallocates, and who gains or loses all need "
                                    "further assumptions."),
        ]
        return table(rows)


substitution = SubstitutionLab()
tasks = TaskLab()
review = ReviewLab()
tilt = TiltLab()
