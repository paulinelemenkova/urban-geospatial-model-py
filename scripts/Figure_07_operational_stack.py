#!/usr/bin/env python3
"""
Figure 7 - Functional decomposition of the proposed virtual city model
operational stack.

Self-contained matplotlib reconstruction of the five-layer operational stack
used in the accompanying urban-informatics study. Each layer is a dashed
rounded panel holding a row of component cards (white body + coloured header
cap), dashed horizontal relays between adjacent cards and dashed vertical drops
between layers, a left-hand feedback/control loop, a right-hand open-data /
governance loop, and a line-style legend of the six flow types.

Colour scheme: ColorBrewer *Set2* qualitative palette (the "Set2 cpt"), one
hue per layer, with light tints derived for the panel backgrounds.

Run:    python Figure_07_operational_stack.py
Out:    Figure_07.png (300 dpi), Figure_07.pdf
Needs:  matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgb

plt.rcParams.update({"font.family": "DejaVu Sans"})

# --------------------------------------------------------------------------- #
# Set2 palette ("Set2 cpt")                                                    #
# --------------------------------------------------------------------------- #
SET2 = [tuple(matplotlib.colormaps["Set2"](i)[:3]) for i in range(8)]


def mix(c, other, t):
    """Linear blend of colour c toward `other` by fraction t in [0, 1]."""
    a, b = to_rgb(c), to_rgb(other)
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def tint(c, t):   # toward white  -> lighter
    return mix(c, "#ffffff", t)


def shade(c, t):  # toward black  -> darker
    return mix(c, "#000000", t)


# --------------------------------------------------------------------------- #
# Layer content (top = Layer 1, bottom = Layer 5)                              #
# --------------------------------------------------------------------------- #
# (layer_no, title, [(card_title, card_subtitle), ...], set2_index)
LAYERS = [
    (1, "Physical urban sensing", [
        ("IoT sensors",       "Temperature, humidity"),
        ("Traffic monitors",  "Flow, speed, density"),
        ("Remote sensing",    "Satellite, LiDAR, UAV"),
        ("Crowdsource data",  "Social, civic, mobility"),
        ("Smart meters",      "Energy, water, gas"),
        ("CCTV / vision",     "Video streams, events"),
    ], 0),
    (2, "Edge computing & stream ingestion", [
        ("Edge node A",   "Local preprocessing"),
        ("Edge node B",   "Real-time filtering"),
        ("Stream broker", "Kafka / MQTT pub-sub"),
        ("Edge node C",   "Anomaly detection"),
        ("Edge node D",   "Video analytics"),
    ], 1),
    (3, "Cloud data platform & storage", [
        ("Data lake",         "Raw multi-source store"),
        ("Spatial database",  "PostGIS, geospatial idx"),
        ("Time-series DB",    "InfluxDB, temporal data"),
        ("Object store",      "S3, point clouds, BIM"),
        ("Data warehouse",    "Aggregated analytics"),
        ("Blockchain ledger", "Data provenance, trust"),
    ], 2),
    (4, "AI analytics & big data processing", [
        ("ML / DL models",    "Prediction, forecasting"),
        ("Spark / Flink",     "Batch & stream analytics"),
        ("Simulation engine", "Agent-based, CFD, FEM"),
        ("GIS analytics",     "Spatial queries, mapping"),
        ("NLP / LLM",         "Citizen queries, reports"),
        ("Semantic fusion",   "Knowledge graph"),
    ], 3),
    (5, "Virtual city model core & immersive visualization", [
        ("3D city model",     "CityGML, IFC, BIM"),
        ("Scenario planner",  "What-if, interventions"),
        ("Real-time sync",    "virtual city model \u2194 physical coupling"),
        ("Dashboard / GIS UI","Decision support"),
        ("AR / VR / Metaverse","Immersive planning"),
        ("API gateway",       "Open data, REST"),
    ], 4),
]

FEEDBACK = SET2[7]   # neutral grey control accent (Set2 slot 8)

# --------------------------------------------------------------------------- #
# Canvas & geometry                                                            #
# --------------------------------------------------------------------------- #
fig, ax = plt.subplots(figsize=(16.2, 13.0))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

ax.text(50, 98.4,
        "Functional decomposition of the proposed virtual city model operational stack",
        ha="center", va="center", fontsize=16.5, fontweight="bold", color="#1c2833")

# horizontal extent reserved for the two side loops
STACK_L, STACK_R = 9.0, 96.0        # panel span
BAND_TOP = 94.0                      # top of first band
BAND_H = 13.6                        # band height
BAND_GAP = 1.7                       # gap between bands
CARD_H = 6.6                         # card height
CARD_GAP = 1.4                       # horizontal gap between cards
CAP_H = 1.15                         # coloured header cap height

band_bottoms = []
band_tops = []
card_centres = []                    # per-layer list of (cx, cy) card centres


def draw_card(cx, cy, w, h, title, sub, base):
    """White card with a rounded coloured header cap and coloured outline."""
    edge = shade(base, 0.10)
    # full coloured shape = cap + outline
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=0.55",
        fc=base, ec=edge, lw=1.4, zorder=3))
    # white body inset from top -> leaves coloured cap strip + thin border
    inset = 0.18
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2 + inset, cy - h / 2 + inset),
        w - 2 * inset, h - CAP_H - inset,
        boxstyle="round,pad=0,rounding_size=0.42",
        fc="white", ec="none", zorder=4))
    ax.text(cx, cy + 0.55, title, ha="center", va="center",
            fontsize=10.3, fontweight="bold", color="#20303a", zorder=5)
    ax.text(cx, cy - 1.55, sub, ha="center", va="center",
            fontsize=8.6, color="#4a5a63", zorder=5)


# ---- draw the five bands + cards ------------------------------------------ #
for k, (n, title, cards, ci) in enumerate(LAYERS):
    base = SET2[ci]
    band_top = BAND_TOP - k * (BAND_H + BAND_GAP)
    band_bot = band_top - BAND_H
    band_tops.append(band_top)
    band_bottoms.append(band_bot)

    # dashed rounded panel with a very light tint fill
    ax.add_patch(FancyBboxPatch(
        (STACK_L, band_bot), STACK_R - STACK_L, BAND_H,
        boxstyle="round,pad=0,rounding_size=1.0",
        fc=tint(base, 0.86), ec=shade(base, 0.05), lw=1.5,
        linestyle=(0, (6, 4)), zorder=1))

    ax.text(STACK_L + 1.6, band_top - 1.7,
            f"Layer {n} \u2014 {title}",
            ha="left", va="center", fontsize=11.5, fontweight="bold",
            color=shade(base, 0.35), zorder=2)

    # lay the cards in a centred row
    m = len(cards)
    inner_l, inner_r = STACK_L + 2.2, STACK_R - 2.2
    total_w = inner_r - inner_l
    card_w = (total_w - (m - 1) * CARD_GAP) / m
    cy = band_bot + 0.4 + CARD_H / 2 + 0.6
    row = []
    for j, (ct, cs) in enumerate(cards):
        cx = inner_l + card_w / 2 + j * (card_w + CARD_GAP)
        draw_card(cx, cy, card_w, CARD_H, ct, cs, base)
        row.append((cx, cy, card_w))
    card_centres.append(row)

    # dashed horizontal relay arrows between adjacent cards
    flow = shade(base, 0.05)
    for j in range(m - 1):
        x0 = row[j][0] + row[j][2] / 2
        x1 = row[j + 1][0] - row[j + 1][2] / 2
        ax.add_patch(FancyArrowPatch(
            (x0 + 0.15, cy), (x1 - 0.15, cy),
            arrowstyle="-|>", mutation_scale=11,
            lw=1.3, color=flow, linestyle=(0, (3, 2.5)), zorder=2))

# ---- dashed vertical drops between layers --------------------------------- #
for k in range(len(LAYERS) - 1):
    base = SET2[LAYERS[k][3]]
    flow = shade(base, 0.05)
    upper = card_centres[k]
    lower = card_centres[k + 1]
    n_drop = min(len(upper), len(lower))
    for j in range(n_drop):
        x = upper[j][0]
        y0 = band_bottoms[k] + 0.1
        y1 = band_tops[k + 1] - 0.1
        ax.add_patch(FancyArrowPatch(
            (x, y0), (x, y1),
            arrowstyle="-|>", mutation_scale=10,
            lw=1.2, color=flow, linestyle=(0, (3, 2.6)), zorder=1))

# --------------------------------------------------------------------------- #
# Left feedback & control loop  (Layer 5 -> Layer 2 first cards)              #
# --------------------------------------------------------------------------- #
loop_x = 4.3
y_top = card_centres[1][0][1]        # Edge node A centre (Layer 2)
y_bot = card_centres[4][0][1]        # 3D city model centre (Layer 5)
ax.add_patch(FancyArrowPatch(
    (loop_x, y_bot), (loop_x, y_top),
    arrowstyle="-", lw=1.7, color=FEEDBACK, linestyle=(0, (6, 4)), zorder=1))
# arrow into Edge node A
ax.add_patch(FancyArrowPatch(
    (loop_x, y_top), (STACK_L + 0.2, y_top),
    arrowstyle="-|>", mutation_scale=13, lw=1.7, color=FEEDBACK,
    linestyle=(0, (6, 4)), zorder=1))
# arrow into 3D city model
ax.add_patch(FancyArrowPatch(
    (loop_x, y_bot), (STACK_L + 0.2, y_bot),
    arrowstyle="-|>", mutation_scale=13, lw=1.7, color=FEEDBACK,
    linestyle=(0, (6, 4)), zorder=1))
ax.text(2.4, (y_top + y_bot) / 2, "Feedback & control loop",
        rotation=90, ha="center", va="center", fontsize=10.5,
        fontweight="bold", color=shade(FEEDBACK, 0.25))

# --------------------------------------------------------------------------- #
# Right open-data / governance loop  (into Layer 3 last card)                 #
# --------------------------------------------------------------------------- #
gov_x = 98.4
gov = shade(SET2[4], 0.05)
y_gov = card_centres[2][-1][1]       # Blockchain ledger centre (Layer 3)
ax.add_patch(FancyArrowPatch(
    (gov_x, band_bottoms[4] + 1.0), (gov_x, band_tops[2] - 1.0),
    arrowstyle="-", lw=1.7, color=gov, linestyle=(0, (6, 4)), zorder=1))
ax.add_patch(FancyArrowPatch(
    (gov_x, y_gov), (STACK_R - 0.2, y_gov),
    arrowstyle="-|>", mutation_scale=13, lw=1.7, color=gov,
    linestyle=(0, (6, 4)), zorder=1))
ax.text(99.6, (band_bottoms[4] + band_tops[2]) / 2, "Open data / governance",
        rotation=90, ha="center", va="center", fontsize=10.5,
        fontweight="bold", color=shade(gov, 0.25))

# --------------------------------------------------------------------------- #
# Legend of flow types                                                         #
# --------------------------------------------------------------------------- #
legend_specs = [
    ("Data ingest (L1\u2192L2)",  shade(SET2[0], 0.05)),
    ("Edge relay (L2\u2192L3)",   shade(SET2[1], 0.05)),
    ("Cloud pipeline (L3\u2192L4)", shade(SET2[2], 0.05)),
    ("AI processing (L4\u2192L5)", shade(SET2[3], 0.05)),
    ("virtual city model output / coupling",       shade(SET2[4], 0.05)),
    ("Feedback / control",         shade(FEEDBACK, 0.20)),
]
handles = [Line2D([0], [0], color=c, lw=2.0, linestyle=(0, (5, 3)), label=lab)
           for lab, c in legend_specs]

leg_bg = FancyBboxPatch(
    (STACK_L - 1.5, 3.2), (STACK_R + 1.5) - (STACK_L - 1.5), 6.0,
    boxstyle="round,pad=0,rounding_size=0.8",
    fc="#f4f6f8", ec="#c9d2d8", lw=1.2, zorder=1)
ax.add_patch(leg_bg)
ax.legend(handles=handles, loc="center", bbox_to_anchor=(0.5, 0.066),
          ncol=6, frameon=False, handlelength=2.4, columnspacing=1.6,
          handletextpad=0.6, fontsize=9.6)

ax.text(STACK_L, 3.9,
        "Fig. X. Functional decomposition of the proposed virtual city model operational stack",
        ha="left", va="center", fontsize=9.2, color="#8a97a0", style="italic")

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("Figure_07.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_07.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_07.png / .pdf")
