"""
sandbox_s13.py - session 13 sandbox: dynamic games and credibility.

    entry      Lab 1  the entry game with editable payoffs, and an optional
                      exit after a fight: every Nash equilibrium of the
                      induced matrix against the one subgame-perfect profile
    leader     Lab 2  Stackelberg: the committed leader against Cournot and
                      Bertrand (session 12's duopoly lab, with a leader)
    deviation  Lab 3  the one-stage deviation check in a two-stage game

Released with the session 13 solutions. The maths is games.py, the drawing of
trees and matrices game_plots.py.
"""

import numpy as np

import game_plots as gm
import games as gs
from sandbox import Lab, legend, num, style_axes, table
from sandbox_s12 import BERTRAND, COURNOT, DuopolyLab
from style import BEFORE, CURVE, GREEN, GREY, INK, LINE, MUTE, NEW


# ======================================================================
# Lab 1: the entry game
# ======================================================================

def entry_values(out, fight, acc, ex=(0.0, 0.0), stay=(0.0, 0.0)):
    return dict(oE=out[0], oI=out[1], fE=fight[0], fI=fight[1], aE=acc[0], aI=acc[1],
                xE=ex[0], xI=ex[1], sE=stay[0], sI=stay[1])


NOTES = entry_values((0, 10), (-1, 1), (2, 4))
A132 = entry_values((0, 10), (-2, 1), (3, 4))
SHEET = entry_values((0, 12), (0, 0), (4, 6), ex=(-1, 7), stay=(-3, 3))
LAB_NAMES = ("Anthropic", "OpenAI", "Accommodate")


def failing(root, plan):
    """The nodes where a profile fails the one-stage deviation check.

    At each decision node, compare the mover's payoff from the profile's own
    action with every alternative, each followed by the profile's plan from
    there on. Returns (node, planned action, better action) triples.
    """
    out = []
    for node in gs.decision_nodes(root):
        mine = gs.path(node, plan)[1][node.player]
        for action, child in node.children:
            pay = child.payoffs if isinstance(child, gs.Leaf) else gs.path(child, plan)[1]
            if pay[node.player] > mine + 1e-9:
                out.append((node.name, plan[node.name], action))
                break
    return out


class EntryLab(Lab):
    TITLE = "Lab 1 &middot; Entry, threats and credibility"
    INTRO = ("The entrant moves first: Out ends the game, In hands the move to the incumbent, "
             "who fights or accommodates. Tick the box to let the entrant exit or stay after a "
             "fight. The thick branches are backward induction; the matrix on the right is the "
             "induced normal form, with every pure Nash equilibrium shaded and the "
             "subgame-perfect one outlined.")
    SLIDERS = [(k, -10.0, 20.0, 0.5, 0.0, ".1f") for k in
               ("oE", "oI", "fE", "fI", "aE", "aI", "xE", "xI", "sE", "sI")]
    CHECKS = [("exit", "After a fight the entrant can exit or stay")]
    FIGSIZE = (9.4, 4.2)
    PRESETS = [
        dict(label="Notes p. 2 the entry game", kind="notes", values=NOTES, names=LAB_NAMES),
        dict(label="Fighting pays OpenAI 5", kind="extra", before=NOTES,
             values=dict(NOTES, fI=5.0), names=LAB_NAMES),
        dict(label="A13.2 entrant and incumbent", kind="problem", values=A132,
             names=("Entrant", "Incumbent", "Accommodate")),
        dict(label="Worksheet: entry with an exit", kind="notes", values=SHEET,
             names=("Challenger", "Incumbent", "Share"), flags=dict(exit=True)),
        dict(label="Worksheet: staying pays -0.5", kind="extra", before=SHEET,
             values=dict(SHEET, sE=-0.5), names=("Challenger", "Incumbent", "Share"),
             flags=dict(exit=True)),
    ]

    def __init__(self):
        super().__init__()
        self.names = LAB_NAMES

    def show(self):
        super().show()
        self.apply(self.PRESETS[0])

    def on_preset(self, preset):
        self.names = preset.get("names", LAB_NAMES)

    def relabel(self):
        e, i, acc = self.names
        ex = self.flag("exit")
        for key, text in (("oE", "%s if Out" % e), ("oI", "%s if Out" % i),
                          ("fE", "%s if Fight" % e), ("fI", "%s if Fight" % i),
                          ("aE", "%s if %s" % (e, acc)), ("aI", "%s if %s" % (i, acc)),
                          ("xE", "%s if Exit" % e), ("xI", "%s if Exit" % i),
                          ("sE", "%s if Stay" % e), ("sI", "%s if Stay" % i)):
            self.w[key].description = text
        for key in ("fE", "fI"):
            self.w[key].disabled = ex
        for key in ("xE", "xI", "sE", "sI"):
            self.w[key].disabled = not ex

    def tree(self, v, ex):
        acc = self.names[2]
        if ex:
            fight = gs.Node(0, "x2", [("Exit", gs.Leaf(v["xE"], v["xI"])),
                                      ("Stay", gs.Leaf(v["sE"], v["sI"]))])
        else:
            fight = gs.Leaf(v["fE"], v["fI"])
        return gs.Node(0, "x0", [("Out", gs.Leaf(v["oE"], v["oI"])),
                                 ("In", gs.Node(1, "x1", [("Fight", fight),
                                                          (acc, gs.Leaf(v["aE"], v["aI"]))]))])

    def induced(self, root, ex):
        # The normal form: the entrant's plan at each of its nodes against the
        # incumbent's choice, each pair played out to a leaf.
        acc = self.names[2]
        rows = ([("In", "Exit"), ("In", "Stay"), ("Out", "Exit"), ("Out", "Stay")] if ex
                else [("In",), ("Out",)])
        cols = ["Fight", acc]
        cells = []
        for r in rows:
            line = []
            for c in cols:
                plan = {"x0": r[0], "x1": c}
                if ex:
                    plan["x2"] = r[1]
                line.append(gs.path(root, plan)[1])
            cells.append(line)
        labels = [" & ".join(r) for r in rows]
        return gs.Matrix(labels, cols, cells), rows, cols

    def state(self, v, ex):
        root = self.tree(v, ex)
        value, plan = gs.solve(root)
        game, rows, cols = self.induced(root, ex)
        spe = (rows.index(tuple([plan["x0"]] + ([plan["x2"]] if ex else []))),
               cols.index(plan["x1"]))
        return dict(root=root, plan=plan, value=value, game=game, nash=game.pure_nash(), spe=spe,
                    path=gs.path(root, plan)[0], ex=ex)

    def compute(self):
        st = dict(v=self.values(), live=self.state(self.values(), self.flag("exit")))
        st["before"] = self.state(self.before, self.flag("exit")) if self.before else None
        return st

    def figure(self, fig, st):
        s = st["live"]
        e, i, acc = self.names
        tree, mat = fig.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.2, 1]))
        struck = [(n.name, a) for n in gs.decision_nodes(s["root"]) for a, _ in n.children
                  if s["plan"].get(n.name) != a]
        gm.tree(tree, s["root"], names=(e, i), plan=s["plan"], struck=struck, fontsize=9,
                title="Backward induction")
        gm.matrix(mat, s["game"], e, i, nash=s["nash"], mark=s["spe"], fontsize=9,
                  title="Induced matrix")
        fig.subplots_adjust(left=0.02, right=0.99, top=0.9, bottom=0.04, wspace=0.08)

    def describe(self, st):
        s, v = st["live"], st["v"]
        e, i, acc = self.names
        g = s["game"]
        spe_row, spe_col = s["spe"]
        rows = [("Subgame perfect", "%s plays %s, %s plays %s: the path %s, paying (%s, %s)."
                 % (e, g.rows[spe_row], i, g.cols[spe_col], " then ".join(s["path"]),
                    num(s["value"][0]), num(s["value"][1])))]
        other = [(r, c) for r, c in s["nash"] if (r, c) != s["spe"]]
        if other:
            texts = []
            for r, c in other:
                plan = {"x0": g.rows[r].split(" & ")[0], "x1": g.cols[c]}
                if s["ex"]:
                    plan["x2"] = g.rows[r].split(" & ")[1]
                bad = failing(s["root"], plan)
                if not bad:
                    why = "it differs from the subgame-perfect profile only where a player is indifferent"
                elif bad[0][0] == "x1":
                    why = ("at its own node %s would rather %s, so its threat to %s is not credible"
                           % (i, bad[0][2].lower(), bad[0][1].lower()))
                else:
                    why = ("%s's plan to %s after a fight is not credible: at that node it would "
                           "rather %s" % (e, bad[0][1].lower(), bad[0][2].lower()))
                texts.append("(%s; %s): Nash, because the plan is never put to the test, but %s"
                             % (g.rows[r], g.cols[c], why))
            rows.append(("Nash, not perfect", "<br>".join(texts) + "."))
        else:
            rows.append(("Nash", "The subgame-perfect profile is the only pure Nash equilibrium."))
        if not s["ex"]:
            rows.append(("Credibility", "Fighting pays %s %s and accommodating %s. The threat "
                                        "becomes credible once fighting pays more than %s, and "
                                        "it deters only if %s then prefers Out: %s against %s."
                         % (i, num(v["fI"]), num(v["aI"]), num(v["aI"]), e, num(v["oE"]),
                            num(v["fE"]))))
        else:
            after = s["plan"]["x2"]
            fight_pay = v["xI"] if after == "Exit" else v["sI"]
            rows.append(("Credibility", "After a fight %s would %s, so fighting pays %s %s against "
                                        "%s from %s: the threat is %s."
                         % (e, after.lower(), i, num(fight_pay), num(v["aI"]), acc.lower(),
                            "credible" if fight_pay > v["aI"] else "not credible")))
        if st["before"] is not None:
            b = st["before"]
            rows.append(("Before &rarr; after", "Path %s &rarr; %s."
                         % (" then ".join(b["path"]), " then ".join(s["path"]))))
        return table(rows)


# ======================================================================
# Lab 2: Stackelberg
# ======================================================================

STACKELBERG = "Stackelberg: firm 1 commits first"
API = dict(a=100.0, c1=10.0, c2=10.0)
TSMC = dict(a=104.0, c1=20.0, c2=20.0)


class LeaderLab(DuopolyLab):
    TITLE = "Lab 2 &middot; Commitment: Stackelberg against Cournot"
    INTRO = ("Session 12's market with a first mover. The leader commits its quantity, the "
             "follower sees it and best-responds, q<sub>2</sub> = (a &minus; c<sub>2</sub> "
             "&minus; q<sub>1</sub>)/2, and the leader picks the best point on that line: S. "
             "Cournot's crossing C is shown for comparison, and the dotted point is what the "
             "leader itself would do if it could revise after seeing q<sub>2</sub>.")
    DROPDOWNS = [("mode", "Competition", [STACKELBERG, COURNOT, BERTRAND])]
    PRESETS = [
        dict(label="Notes p. 10 API market", kind="notes", values=dict(API, mode=STACKELBERG),
             before=dict(API, mode=COURNOT)),
        dict(label="Notes p. 11 Try it: TSMC", kind="notes", values=dict(TSMC, mode=STACKELBERG),
             before=dict(TSMC, mode=COURNOT)),
        dict(label="Try it (b) TSMC commits 36", kind="notes",
             values=dict(TSMC, c1=32.0, c2=32.0, mode=STACKELBERG)),
        dict(label="Worksheet: the server market", kind="notes",
             values=dict(a=60.0, c1=12.0, c2=12.0, mode=STACKELBERG)),
        dict(label="Review Q4: salmon", kind="notes",
             values=dict(a=36.0, c1=0.0, c2=0.0, mode=STACKELBERG)),
        dict(label="A13.1 P = 24 − Q", kind="problem",
             values=dict(a=24.0, c1=0.0, c2=0.0, mode=STACKELBERG),
             before=dict(a=24.0, c1=0.0, c2=0.0, mode=COURNOT)),
    ]

    def outcomes(self, v):
        out = super().outcomes(v)
        out["stackelberg"] = gs.stackelberg(v["a"], v["c1"], v["c2"])
        return out

    def chosen(self, v, out):
        if v["mode"] == STACKELBERG:
            return out["stackelberg"]
        return super().chosen(v, out)

    def draw_br(self, ax, st):
        super().draw_br(ax, st)
        v, s = st["v"], st["out"]["stackelberg"]
        ax.plot([s["q2"]], [s["q1"]], "o", color=NEW, ms=8, zorder=6, label="Stackelberg S")
        q1 = gs.cournot_br(v["a"], v["c1"], s["q2"])
        ax.plot([s["q2"], s["q2"]], [s["q1"], q1], color=MUTE, lw=1, ls=":")
        ax.plot([s["q2"]], [q1], "o", mfc="white", mec=MUTE, mew=1.4, ms=7)

    def draw_bars(self, ax, st):
        style_axes(ax)
        out = st["out"]
        c, s = out["cournot"], out["stackelberg"]
        xs = np.arange(3)
        ax.bar(xs - 0.18, [c["pi1"], c["pi2"], c["pi1"] + c["pi2"]], width=0.34, color=GREY,
               label="Cournot")
        ax.bar(xs + 0.18, [s["pi1"], s["pi2"], s["pi1"] + s["pi2"]], width=0.34,
               color=[GREEN, CURVE, LINE], label="Stackelberg")
        ax.set_xticks(xs)
        ax.set_xticklabels(["leader", "follower", "industry"], fontsize=9)
        ax.set_ylim(0, self.stick("pi", max(c["pi1"] + c["pi2"], 1.0) * 1.15))
        ax.set_title("Profits", loc="left", color=INK, fontsize=9.5)
        legend(ax, loc="upper left")

    def describe(self, st):
        v, out = st["v"], st["out"]
        s, c = out["stackelberg"], out["cournot"]
        q1_revise = gs.cournot_br(v["a"], v["c1"], s["q2"])
        rows = [
            ("Stackelberg", "Leader %s, follower %s, Q = %s, P = %s; profits %s and %s."
             % (num(s["q1"]), num(s["q2"]), num(s["Q"]), num(s["P"]), num(s["pi1"]), num(s["pi2"]))),
            ("Cournot", "%s and %s, Q = %s, P = %s; profits %s and %s."
             % (num(c["q1"]), num(c["q2"]), num(c["Q"]), num(c["P"]), num(c["pi1"]), num(c["pi2"]))),
            ("Who pays", "The leader gains %s, the follower loses %s, industry profit changes by "
                         "%s. Output %s and the price %s: consumers %s."
             % (num(s["pi1"] - c["pi1"]), num(c["pi2"] - s["pi2"]),
                num(s["pi1"] + s["pi2"] - c["pi1"] - c["pi2"]),
                "rises" if s["Q"] > c["Q"] else "falls", "falls" if s["P"] < c["P"] else "rises",
                "gain" if s["P"] < c["P"] else "lose")),
            ("Commitment", "Could the leader revise after seeing q<sub>2</sub> = %s, it would "
                           "move to %s, not %s. Only an irreversible commitment makes %s "
                           "credible: without it the game falls back to Cournot."
             % (num(s["q2"]), num(q1_revise), num(s["q1"]), num(s["q1"]))),
        ]
        if v["c1"] == v["c2"]:
            rows.append(("Read the cost", "With equal costs the leader's rule is q<sub>1</sub> = "
                                          "(a &minus; c)/2, so a commitment of %s reveals c = %s."
                         % (num(s["q1"]), num(gs.leader_cost(v["a"], s["q1"])))))
        if st["before"] is not None:
            bf, lv = st["before"], st["live"]
            rows.append(("Before &rarr; after", "Price %s &rarr; %s, output %s &rarr; %s."
                         % (num(bf["P"]), num(lv["P"]), num(bf["Q"]), num(lv["Q"]))))
        return table(rows)


# ======================================================================
# Lab 3: the one-stage deviation check
# ======================================================================

TRY = dict(hn=3.0, hl=6.0, dn=5.0, dl=3.0, delta=0.5)


class DeviationLab(Lab):
    TITLE = "Lab 3 &middot; The one-stage deviation check"
    INTRO = ("A two-stage game. Holding to the candidate profile pays h<sub>1</sub> now and "
             "h<sub>2</sub> next stage; deviating once pays d<sub>1</sub> now and triggers a "
             "continuation worth d<sub>2</sub>. Next stage is discounted by &delta;. The "
             "profile survives the check at this information set when h<sub>1</sub> + "
             "&delta;h<sub>2</sub> &ge; d<sub>1</sub> + &delta;d<sub>2</sub>.")
    SLIDERS = [
        ("hn", -10.0, 20.0, 0.5, 3.0, ".1f"),
        ("hl", -10.0, 20.0, 0.5, 6.0, ".1f"),
        ("dn", -10.0, 20.0, 0.5, 5.0, ".1f"),
        ("dl", -10.0, 20.0, 0.5, 3.0, ".1f"),
        ("delta", 0.0, 1.0, 0.01, 0.5, ".2f"),
    ]
    FIGSIZE = (6.4, 4.4)
    PRESETS = [
        dict(label="Notes p. 14 Try it (a)", kind="notes", values=TRY),
        dict(label="Try it (b) a harsher war, z = 2", kind="notes", before=TRY,
             values=dict(TRY, dl=2.0)),
        dict(label="Try it (c) a grab of 7", kind="notes", before=TRY, values=dict(TRY, dn=7.0)),
        dict(label="Review Q5", kind="notes",
             values=dict(hn=-1.0, hl=0.0, dn=2.0, dl=-4.0, delta=0.8)),
    ]

    def relabel(self):
        self.w["hn"].description = "Hold: now"
        self.w["hl"].description = "Hold: next stage"
        self.w["dn"].description = "Deviate: now"
        self.w["dl"].description = "Deviate: next stage"
        self.w["delta"].description = "Discount factor δ"

    def compute(self):
        v = self.values()
        return dict(v=v, star=gs.deviation_threshold(v["hn"], v["hl"], v["dn"], v["dl"]))

    def figure(self, fig, st):
        ax = fig.add_subplot()
        style_axes(ax)
        v = st["v"]
        d = np.array([0.0, 1.0])
        if self.before:
            b = self.before
            ax.plot(d, b["hn"] + d * b["hl"], color=BEFORE, lw=1.2, ls="--")
            ax.plot(d, b["dn"] + d * b["dl"], color=BEFORE, lw=1.2, ls="--", label="before")
        ax.plot(d, v["hn"] + d * v["hl"], color=LINE, lw=2, label="hold")
        ax.plot(d, v["dn"] + d * v["dl"], color=NEW, lw=2, label="deviate once")
        ax.axvline(v["delta"], color=MUTE, lw=1, ls=":")
        if st["star"] is not None and 0 <= st["star"] <= 1:
            ax.plot([st["star"]], [v["hn"] + st["star"] * v["hl"]], "o", color=GREEN, ms=8,
                    zorder=6)
        ax.set_xlim(0, 1)
        ax.set_xlabel("discount factor δ", color=INK, fontsize=9, loc="right")
        ax.set_ylabel("payoff", color=INK, fontsize=9, loc="top")
        legend(ax, loc="upper left")
        fig.tight_layout()

    def describe(self, st):
        v, star = st["v"], st["star"]
        hold = v["hn"] + v["delta"] * v["hl"]
        dev = v["dn"] + v["delta"] * v["dl"]
        rows = [("At δ = %s" % num(v["delta"]),
                 "Hold %s against deviate %s: the profile %s the check here."
                 % (num(hold, 3), num(dev, 3), "passes" if hold >= dev - 1e-9 else "fails"))]
        if star is None:
            rows.append(("Threshold", "The future does not punish the deviation, so no discount "
                                      "factor deters it." if v["dn"] > v["hn"] else
                         "Deviating does not even pay today: holding passes for every δ."))
        else:
            verdict = ("above one: no discount factor sustains it, however patient the players"
                       if star > 1 else "every δ passes" if star <= 0 else
                       "patient enough players hold")
            rows.append(("Threshold", "δ* = (%s &minus; %s)/(%s &minus; %s) = %s: %s."
                         % (num(v["dn"]), num(v["hn"]), num(v["hl"]), num(v["dl"]),
                            num(star, 3), verdict)))
        if v["delta"] > 0:
            z = gs.continuation_for(v["delta"], v["hn"], v["hl"], v["dn"])
            rows.append(("Indifference", "At this δ the players are just willing to hold when "
                                         "the punishment continuation is z = %s." % num(z, 3)))
        rows.append(("Why one stage", "If no single change at one information set helps, no "
                                      "combination of changes does: the one-stage deviation "
                                      "principle."))
        return table(rows)


entry = EntryLab()
leader = LeaderLab()
deviation = DeviationLab()
