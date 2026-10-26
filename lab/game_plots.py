"""
game_plots.py - drawing a payoff matrix and a game tree.

Used by the session 12 and 13 pages, guided and sandbox alike:

    import game_plots as gm
    gm.matrix(ax, game, "OpenAI", "Anthropic", nash=game.pure_nash())
    gm.tree(ax, root, names=("Anthropic", "OpenAI"), plan=plan)

Every function takes the Axes to draw on and a game from games.py, which does
the maths. Player 1 is blue and player 2 pink, as in the notes' figures, and
in a matrix each cell reads (player 1, player 2).
"""

from matplotlib.patches import Rectangle

from games import Leaf
from style import CURVE, GREEN, GREY, INK, LINE, MUTE

PLAYER = (LINE, CURVE)


def _num(x):
    # Payoffs print as the notes print them: 3, -2, 1.5, 2/3.
    if hasattr(x, "denominator") and x.denominator != 1:
        return "%d/%d" % (x.numerator, x.denominator)
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return "%d" % round(x)
    return ("%.2f" % x).rstrip("0").rstrip(".")


# ----------------------------------------------------------------- matrix ---

def matrix(ax, game, row_name, col_name, nash=(), struck_rows=(), struck_cols=(), best=False,
           mark=None, fontsize=11, title=None):
    """A payoff matrix drawn as a table.

    nash         cells (i, j) to shade green
    struck_rows  rows deleted by elimination: greyed and crossed out
    best         underline each player's best responses, the way you would
                 mark them by hand
    mark         one cell (i, j) to outline, e.g. a candidate being checked
    """
    nr, nc = len(game.rows), len(game.cols)
    ax.set_xlim(-1.25, nc + 0.05)
    ax.set_ylim(-0.05, nr + 1.25)
    ax.axis("off")
    if title:
        ax.set_title(title, loc="left", color=INK, fontsize=9.5)

    def y(i):                               # row i drawn from the top down
        return nr - 1 - i

    ax.text(nc / 2, nr + 0.85, col_name, ha="center", va="center", color=CURVE,
            fontsize=fontsize, weight="bold")
    ax.text(-1.2, nr + 0.85, row_name, ha="left", va="center", color=LINE,
            fontsize=fontsize, weight="bold")
    for j, name in enumerate(game.cols):
        gone = j in struck_cols
        ax.text(j + 0.5, nr + 0.35, str(name), ha="center", va="center",
                color=GREY if gone else CURVE, fontsize=fontsize)
    for i, name in enumerate(game.rows):
        gone = i in struck_rows
        ax.text(-0.15, y(i) + 0.5, str(name), ha="right", va="center",
                color=GREY if gone else LINE, fontsize=fontsize)

    # Best responses among the strategies still live, marked in live cells only.
    live_r = [i for i in range(nr) if i not in struck_rows]
    live_c = [j for j in range(nc) if j not in struck_cols]
    rb = {j: game.row_best(j, live_r) for j in live_c} if best else {}
    cb = {i: game.col_best(i, live_c) for i in live_r} if best else {}
    for i in range(nr):
        for j in range(nc):
            gone = i in struck_rows or j in struck_cols
            face = (GREEN if (i, j) in nash else "white")
            ax.add_patch(Rectangle((j, y(i)), 1, 1, facecolor=face,
                                   alpha=0.22 if (i, j) in nash else 1.0,
                                   edgecolor=MUTE, lw=0.8))
            u1, u2 = game.u[i][j]
            c1, c2 = (GREY, GREY) if gone else PLAYER
            ax.text(j + 0.47, y(i) + 0.5, _num(u1) + ",", ha="right", va="center", color=c1,
                    fontsize=fontsize, weight="bold" if i in rb.get(j, ()) else "normal")
            ax.text(j + 0.53, y(i) + 0.5, _num(u2), ha="left", va="center", color=c2,
                    fontsize=fontsize, weight="bold" if j in cb.get(i, ()) else "normal")
            if i in rb.get(j, ()):
                ax.plot([j + 0.18, j + 0.45], [y(i) + 0.3] * 2, color=LINE, lw=1.4)
            if j in cb.get(i, ()):
                ax.plot([j + 0.55, j + 0.82], [y(i) + 0.3] * 2, color=CURVE, lw=1.4)
    # Crossed out the way you would by hand: one light line through the label and the row.
    for i in struck_rows:
        ax.plot([-1.0, nc], [y(i) + 0.5] * 2, color=GREY, lw=1, alpha=0.7)
    for j in struck_cols:
        ax.plot([j + 0.5] * 2, [0, nr + 0.6], color=GREY, lw=1, alpha=0.7)
    if mark is not None:
        i, j = mark
        ax.add_patch(Rectangle((j + 0.03, y(i) + 0.03), 0.94, 0.94, fill=False,
                               edgecolor=INK, lw=2))


# ------------------------------------------------------------------- tree ---

def _layout(node, depth=0, out=None, leaves=None):
    # Leaves spread evenly from left to right; a decision node sits above the
    # middle of its children.
    out = {} if out is None else out
    leaves = [0] if leaves is None else leaves
    if isinstance(node, Leaf):
        out[id(node)] = (leaves[0], -depth)
        leaves[0] += 1
        return out
    xs = []
    for _, child in node.children:
        _layout(child, depth + 1, out, leaves)
        xs.append(out[id(child)][0])
    out[id(node)] = (sum(xs) / len(xs), -depth)
    return out


def tree(ax, root, names=("1", "2"), plan=None, struck=(), info=(), labels=True, hide=(),
         fontsize=10, title=None, leaf_text=None):
    """A game tree from games.Node, drawn top down.

    names     the players' names, for the node labels
    plan      {node name: action}: those branches are drawn thick, as in
              backward induction
    struck    (node name, action) pairs to cross out
    info      pairs of node names joined by a dashed line: one information set
    hide      node names whose subtrees are not drawn yet (a stage at a time)
    """
    pos = _layout(root)
    plan = plan or {}
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.7, max(xs) + 0.7)
    ax.set_ylim(min(ys) - 0.75, max(ys) + 0.45)
    ax.axis("off")
    if title:
        ax.set_title(title, loc="left", color=INK, fontsize=9.5)
    by_name = {}

    def draw(node):
        x, yv = pos[id(node)]
        if isinstance(node, Leaf):
            text = leaf_text(node) if leaf_text else "(%s)" % ", ".join(_num(u) for u in node.payoffs)
            ax.text(x, yv - 0.12, text, ha="center", va="top", color=INK, fontsize=fontsize - 0.5)
            return
        by_name[node.name] = (x, yv)
        colour = PLAYER[node.player]
        ax.plot([x], [yv], "o", color=colour, ms=8, zorder=5)
        if labels:
            ax.text(x, yv + 0.13, "%s (%s)" % (names[node.player], node.name), ha="center",
                    va="bottom", color=colour, fontsize=fontsize - 1)
        if node.name in hide:
            return
        for action, child in node.children:
            cx, cy = pos[id(child)]
            thick = plan.get(node.name) == action
            gone = (node.name, action) in struck
            ax.plot([x, cx], [yv, cy], color=GREY if gone else colour,
                    lw=3.2 if thick else 1.2, zorder=3, ls=":" if gone else "-")
            mx, my = (x + cx) / 2, (yv + cy) / 2
            ax.text(mx + (0.08 if cx >= x else -0.08), my, action, ha="left" if cx >= x else "right",
                    va="center", color=GREY if gone else colour, fontsize=fontsize - 0.5,
                    weight="bold" if thick else "normal")
            draw(child)

    draw(root)
    for a, b in info:
        (x1, y1), (x2, y2) = by_name[a], by_name[b]
        ax.plot([x1, x2], [y1, y2], color=MUTE, lw=1.3, ls="--", zorder=2)
