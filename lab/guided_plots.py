"""
guided_plots.py - small drawing helpers shared by the guided session files.

Every guided figure is built from the same few moves: a bare frame with no
ticks, a labelled dot, an arrow, a legend. They live here so that no session
has to borrow them from another session's file. Session files use them as

    import guided_plots as gp
    gp.frame(ax, 100, 150, "x1", "x2")

Like guided.py, this file knows nothing about economics.
"""

from style import CURVE, INK, MUTE


def frame(ax, xmax, ymax, xlabel, ylabel):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xlabel(xlabel, color=INK, fontsize=10, loc="right")
    ax.set_ylabel(ylabel, color=INK, fontsize=10, loc="top")


def legend(ax, loc="upper right"):
    if not ax.get_legend_handles_labels()[0]:
        return                          # early stages have nothing labelled yet
    leg = ax.legend(loc=loc, fontsize=9, frameon=False)
    for t in leg.get_texts():
        t.set_color(INK)


def dot(ax, x, y, label, dx=8, dy=4, colour=CURVE, ha="left"):
    ax.plot([x], [y], "o", color=colour, ms=7, zorder=6, clip_on=False)
    if label:
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(dx, dy),
                    color=colour, fontsize=10.5, ha=ha)


def arrow(ax, start, end, colour=INK):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.3, shrinkA=6, shrinkB=6))


def start(ax):
    # The empty figure a part opens with, before the first step is solved.
    ax.text(0.5, 0.5, "Answer step 1 to start drawing.", transform=ax.transAxes,
            ha="center", va="center", color=MUTE, fontsize=11)
