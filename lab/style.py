"""
style.py - what every figure in the course shares: the colours, and the way a
figure becomes a picture on the page.

Both kinds of page use this file, the guided pages (guided.py) and the
sandboxes (sandbox.py), so the two look like one course. A colour is changed
here and nowhere else.
"""

import io

# Light palette: Colab's notebook is white by default.
INK = "#1f2937"           # text and axes
MUTE = "#6b7280"          # secondary text, tick labels
GRID = "#e5e7eb"
LINE = "#2563eb"          # the budget line; consumer A
CURVE = "#db2777"         # indifference curves; consumer B
NEW = "#ea580c"           # the line after a price change, always dashed
HALF = "#7c3aed"          # the line after an income cut; the lens in the box
GREEN = "#059669"
GREY = "#9ca3af"
RED = "#dc2626"
FILL = LINE               # the shaded budget set

# The sandboxes name two of the colours by the job they do there.
BEFORE = GREY             # the frozen "before" state
DIRECT = GREEN            # a comparison budget (equal-revenue direct charge)


def render(draw, figsize, dpi=110):
    # A bare Figure with its own Agg canvas never touches pyplot, so the
    # notebook's inline backend cannot pick it up and show it a second time:
    # VS Code showed pyplot figures twice, once in the widget and once as
    # ordinary cell output. draw(fig) fills the figure in; the PNG bytes that
    # come back go straight into an Image widget.
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)
    draw(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    return buf.getvalue()
