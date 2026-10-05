"""
edgeworth_plots.py - drawing an Edgeworth box and what goes inside it.

Used by the session 6 and 7 pages, guided and sandbox alike:

    import edgeworth_plots as ed
    ed.ic_a(ax, e, 3, 9, color=LINE)

Every function takes the Axes to draw on and an Economy (equilibrium.py), which
does the maths. Points are always given in A's coordinates: A's corner is
bottom left, B's is top right, and B holds what A does not.
"""

import numpy as np

from style import CURVE, INK, LINE


def box(ax, X, Y):
    # The bare box of the guided pages: no ticks, each axis label at the far
    # end of its own axis with an arrow pointing away from its owner's corner.
    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(True)
        side.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    kw = dict(color=INK, fontsize=10)
    ax.text(X, -0.025 * Y, r"$x_A$ $\rightarrow$", ha="right", va="top", **kw)
    ax.text(-0.025 * X, Y, r"$y_A$ $\uparrow$", ha="right", va="top", **kw)
    ax.text(0, 1.025 * Y, r"$\leftarrow$ $x_B$", ha="left", va="bottom", **kw)
    ax.text(1.025 * X, 0, r"$y_B$ $\downarrow$", ha="left", va="bottom", **kw)
    # A blue, B pink, as in the notes' figures.
    ax.text(-0.025 * X, -0.025 * Y, "A", ha="right", va="top", color=LINE,
            fontsize=12, weight="bold")
    ax.text(1.025 * X, 1.025 * Y, "B", ha="left", va="bottom", color=CURVE,
            fontsize=12, weight="bold")


def grid(e, n=400):
    # x values across the box, stopping just short of the two edges where an
    # indifference curve runs off to infinity.
    return np.linspace(e.X * 0.004, e.X * 0.996, n)


def ic_a(ax, e, x, y, **kw):
    # A's indifference curve through (x, y).
    level = e.uA(x, y)
    xs = grid(e)
    ax.plot(xs, np.clip([e.icA(level, v) for v in xs], -1, e.Y + 1), **kw)


def ic_b(ax, e, x, y, **kw):
    # B's indifference curve through A's point (x, y): B holds what is left.
    level = e.uB(*e.b_bundle(x, y))
    xs = grid(e)
    ax.plot(xs, np.clip([e.icB(level, v) for v in xs], -1, e.Y + 1), **kw)


def lens(ax, e, x, y, **kw):
    # The area between the two curves through (x, y): both are better off.
    xs = grid(e)
    lo = np.clip([e.icA(e.uA(x, y), v) for v in xs], 0, e.Y)
    hi = np.clip([e.icB(e.uB(*e.b_bundle(x, y)), v) for v in xs], 0, e.Y)
    ax.fill_between(xs, lo, hi, where=lo < hi, lw=0, **kw)


def contract(ax, e, **kw):
    xs = np.linspace(0, e.X, 300)
    ax.plot(xs, [e.contract(v) for v in xs], **kw)


def price_line(ax, e, p, x0, y0, **kw):
    # The price line through (x0, y0), slope -p, across the box.
    xs = np.array([0, e.X])
    ax.plot(xs, y0 - p * (xs - x0), **kw)
