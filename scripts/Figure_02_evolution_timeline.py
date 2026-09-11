#!/usr/bin/env python3
"""
Figure 2 - Evolution of urban digital model technologies (timeline).

Reconstruction of the figure used in the accompanying urban-informatics study.
Self-contained matplotlib script: draws an era-banded horizontal timeline with
milestone cards above and below the axis and a converging-summary box.

Run:
    python Figure_02_evolution_timeline.py
Outputs:
    Figure_02.png (300 dpi) and Figure_02.pdf
Requires:
    matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

# ----------------------------------------------------------------------
# palette (fill, edge, dark-text) per era family
# ----------------------------------------------------------------------
TEAL   = dict(fill="#c9e7db", edge="#3f9d86", text="#2f6b5c")
PURPLE = dict(fill="#dcd7ee", edge="#8079bf", text="#4a447a")
BLUE   = dict(fill="#cfe0ee", edge="#5f92b8", text="#2f5a7a")
RED    = dict(fill="#f5cfca", edge="#cf6b62", text="#9c3f38")
YELLOW = dict(fill="#fbf6c6", edge="#c9b83f", text="#8a7d1e")
GREY_TXT = "#555555"

plt.rcParams.update({"font.family": "DejaVu Sans"})

fig, ax = plt.subplots(figsize=(11.6, 12.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 118)
ax.axis("off")

# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def rbox(cx, cy, w, h, style, rounding=0.9, lw=1.6, dashed=False, alpha=1.0):
    """Rounded box centred on (cx, cy)."""
    p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle=f"round,pad=0,rounding_size={rounding}",
                       fc=style["fill"], ec=style["edge"], lw=lw,
                       linestyle="--" if dashed else "-", alpha=alpha, zorder=3)
    ax.add_patch(p)


def card(cx, cy, w, h, style, title, desc, dashed=False):
    rbox(cx, cy, w, h, style, rounding=1.0, lw=1.6, dashed=dashed)
    ax.text(cx, cy + h / 2 - 1.9, title, ha="center", va="top",
            fontsize=12.5, fontweight="bold", color=style["text"], zorder=4)
    ax.text(cx, cy + h / 2 - 5.2, desc, ha="center", va="top",
            fontsize=9.2, color=GREY_TXT, zorder=4, linespacing=1.25)


def pill(cx, cy, w, h, style, label, fontsize=10.5, bold=False, dashed=False):
    rbox(cx, cy, w, h, style, rounding=h / 2, lw=1.5, dashed=dashed)
    ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize,
            fontweight="bold" if bold else "normal", color=style["text"], zorder=4)


def stem(x, y0, y1, color, lw=2.2):
    ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=1, solid_capstyle="round")

# ----------------------------------------------------------------------
# titles
# ----------------------------------------------------------------------
ax.text(50, 116, "From industrial systems toward intelligent urban ecosystems",
        ha="center", va="center", fontsize=13, color=GREY_TXT)
ax.text(50, 111, "Evolution of urban digital model technologies",
        ha="center", va="center", fontsize=20)

# ----------------------------------------------------------------------
# timeline geometry: 10 evenly spaced points
# ----------------------------------------------------------------------
TL_Y = 55                      # timeline y
xs = [6 + i * (88 / 9) for i in range(10)]      # 10 x positions across the axis
years = ["1991", "2002", "1999", "2006", "2010", "2013", "2014", "2018", "2020", "2030+"]
fam = [TEAL, TEAL, PURPLE, PURPLE, PURPLE, BLUE, BLUE, RED, RED, YELLOW]

# axis line with arrow
ax.annotate("", xy=(99, TL_Y), xytext=(3, TL_Y),
            arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.6), zorder=1)
# minor ticks
for i in range(10):
    ax.plot([xs[i], xs[i]], [TL_Y - 0.8, TL_Y + 0.8], color="#888888", lw=1.0, zorder=1)
for i in range(9):
    xm = (xs[i] + xs[i + 1]) / 2
    ax.plot([xm, xm], [TL_Y - 0.5, TL_Y + 0.5], color="#aaaaaa", lw=0.7, zorder=1)

# markers + year labels
for i, (x, yr, st) in enumerate(zip(xs, years, fam)):
    if yr == "2030+":
        ax.plot(x, TL_Y, marker="D", ms=11, mfc="white", mec=st["edge"],
                mew=1.8, zorder=4)
        # dashed forward arrow
        ax.annotate("", xy=(x + 5.5, TL_Y), xytext=(x, TL_Y),
                    arrowprops=dict(arrowstyle="-|>", color=st["edge"],
                                    lw=1.6, linestyle=(0, (4, 3))), zorder=1)
    else:
        ax.plot(x, TL_Y, marker="o", ms=9, color=st["edge"], zorder=4)
    ax.text(x, TL_Y - 3.6, yr, ha="center", va="top", fontsize=11.5,
            fontweight="bold", color=st["edge"])

# era-boundary triangles on the axis
for xb in [(xs[1] + xs[2]) / 2, (xs[4] + xs[5]) / 2, (xs[6] + xs[7]) / 2]:
    ax.plot(xb, TL_Y, marker="^", ms=7, color="#9aa0a6", zorder=3)

# ----------------------------------------------------------------------
# era bands (top)
# ----------------------------------------------------------------------
band_y = 101
bands = [
    ("Industrial origins 1991-2002", TEAL,   xs[0] - 3, xs[1] + 3),
    ("GIS & spatial 2003-2010",      PURPLE, xs[2] - 3, xs[4] + 3),
    ("Big data & cloud 2011-17",     BLUE,   xs[5] - 3, xs[6] + 3),
    ("AI urban ecosystems 2018-2030+", RED,  xs[7] - 3, xs[9] + 3),
]
for label, st, x0, x1 in bands:
    cx = (x0 + x1) / 2
    pill(cx, band_y, x1 - x0, 4.2, st, label, fontsize=10.5)
    # faint droppers from band to axis at its edges
    for xe in (x0 + 2, x1 - 2):
        ax.plot([xe, xe], [band_y - 2.2, TL_Y + 1], color="#cccccc",
                lw=0.8, linestyle=(0, (2, 2)), zorder=0)

# ----------------------------------------------------------------------
# category pills just above the axis
# ----------------------------------------------------------------------
pill((xs[1] + xs[2]) / 2, TL_Y + 8, 15, 4.0, PURPLE, "GIS / spatial", 10)
pill(xs[4], TL_Y + 8, 17, 4.0, BLUE, "big data / cloud", 10)
pill(xs[6], TL_Y + 8, 15, 4.0, RED, "AI / ML / RL", 10)

# ----------------------------------------------------------------------
# cards ABOVE the axis  (cx, top-card center-y, width, height, style, title, desc, timeline-x)
# ----------------------------------------------------------------------
above = [
    (xs[0], 88, 18, 14, TEAL,   "digital model concept",         "Grieves / NASA-USAF\naerospace lifecycle model"),
    (xs[2], 74, 19, 14, PURPLE, "GIS integration",    "Esri 3-D spatial data\nmerged with digital models"),
    (xs[4], 88, 19, 14, PURPLE, "IoT sensor nets",    "Real-time sensor fusion\nembedded in city grids"),
    (xs[5] + 3, 74, 20, 14, BLUE, "Cloud virtual model platforms", "Hadoop/Spark pipelines\nfeed industrial models"),
    (xs[8], 88, 19, 14, RED,    "AI virtual urban model",        "Deep-learning city simulators\nSingapore, Zurich, Helsinki"),
]
for cx, cy, w, h, st, title, desc in above:
    stem(cx, TL_Y + 1, cy - h / 2, st["edge"])
    card(cx, cy, w, h, st, title, desc)

# ----------------------------------------------------------------------
# cards BELOW the axis
# ----------------------------------------------------------------------
below = [
    (xs[1], 40, 19, 14, TEAL,   "Manufacturing digital model", "NASA formalises the digital model for\nF-35 fleet lifecycle", False),
    (xs[3], 26, 19, 14, PURPLE, "CityGML 1.0",      "OGC 3-D city objects\nsemantic geospatial standard", False),
    (xs[5], 40, 19, 14, BLUE,   "BIM-GIS merge",    "IFC + CityGML pipeline\nsmart-building models", False),
    (xs[7], 26, 19, 14, RED,    "Autonomous CPS",   "Federated learning, edge AI\nacross cyber-physical grids", False),
    (xs[9], 40, 19, 14, YELLOW, "Planetary digital model",     "EU DestinE earth-system\nclimate-adaptive simulation", True),
]
for cx, cy, w, h, st, title, desc, dashed in below:
    stem(cx, cy + h / 2, TL_Y - 1, st["edge"])
    card(cx, cy, w, h, st, title, desc, dashed=dashed)

# ----------------------------------------------------------------------
# bottom converging-summary box
# ----------------------------------------------------------------------
box = FancyBboxPatch((5, 3.5), 90, 12,
                     boxstyle="round,pad=0,rounding_size=1.2",
                     fc="#fbf9d6", ec="#cdbf46", lw=1.8, zorder=3)
ax.add_patch(box)
ax.text(50, 13.0, "Converging into: intelligent dynamic urban model ecosystems",
        ha="center", va="center", fontsize=13.5, color="#7d7020")
ax.text(50, 9.0,
        "IoT sensing  \u2192  3-D GIS city models  \u2192  big-data pipelines  \u2192  "
        "AI/ML simulation  \u2192  autonomous city governance",
        ha="center", va="center", fontsize=10.5, color="#7d7020")
ax.text(50, 5.8,
        "Smart energy grids  \u00b7  geological-hazard urban spatial model  \u00b7  climate resilience  \u00b7  "
        "transportation  \u00b7  water networks",
        ha="center", va="center", fontsize=10.5, color="#7d7020")

ax.text(99, 0.6, "Source: author", ha="right", va="bottom",
        fontsize=9, style="italic", color="#999999")

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("Figure_02.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_02.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_02.png / .pdf")
