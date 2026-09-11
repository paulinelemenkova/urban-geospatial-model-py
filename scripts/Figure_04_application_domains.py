#!/usr/bin/env python3
"""
Figure 4 - Major application domains of urban spatial model technologies.

Reconstruction (self-contained matplotlib) of the eight-branch domain tree used
in the accompanying urban-informatics study: a title bar feeding a horizontal
bus, with eight coloured domain columns, each a dark header over a spine of
light rounded item boxes.

Run:    python Figure_04_application_domains.py
Out:    Figure_04.png (300 dpi), Figure_04.pdf
Needs:  matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "DejaVu Sans"})

# domain: (title, header_fill, item_fill, item_edge, [items])
DOMAINS = [
    ("Urban planning &\ndesign", "#2e5f8a", "#dce7f4", "#7ba0cc",
     ["Land-use simulation", "3-D city modelling", "Zoning & density\nanalysis",
      "Participatory planning", "Heritage preservation", "Infrastructure lifecycle",
      "Decision support"]),
    ("Smart energy\nmanagement", "#b3651c", "#f6e6d2", "#d6a566",
     ["Grid optimisation", "Renewable integration", "Demand forecasting",
      "Building energy model", "Microgrid control", "Fault detection", "Carbon accounting"]),
    ("Transport & mobility", "#1f7a6b", "#d3ece5", "#66b0a1",
     ["Traffic flow modelling", "Adaptive signal control", "Multimodal routing",
      "Autonomous vehicles", "Pedestrian simulation", "Incident prediction",
      "Logistics optimisation"]),
    ("Environment &\nclimate", "#2f6f2f", "#dcedcf", "#83b568",
     ["Air quality monitoring", "Urban heat island", "Flood risk modelling",
      "Green infrastructure", "Noise mapping", "Climate adaptation",
      "Biodiversity tracking"]),
    ("Public health & safety", "#69409e", "#e5def2", "#a98fd0",
     ["Epidemic surveillance", "Emergency response", "Hospital resource model",
      "Crime pattern analysis", "Crowd management", "Disaster simulation",
      "Mental health mapping"]),
    ("Water & waste\nsystems", "#1f7a92", "#d4eaf0", "#63aabf",
     ["Pipe network\nmonitoring", "Leak detection", "Stormwater modelling",
      "Water quality sensing", "Waste route\noptimisation", "Recycling analytics",
      "Demand forecasting"]),
    ("Governance &\ninfrastructure", "#3f4a5a", "#e0e3e9", "#9aa2ae",
     ["Policy simulation", "Smart procurement", "Asset management",
      "BIM-GIS integration", "Citizen engagement", "Open data platforms",
      "Interoperability"]),
    ("Geoscience &\nsubsurface", "#9c3b2c", "#f4dad3", "#d59183",
     ["Subsurface 3-D\nmodels", "Geological hazard model", "Landslide monitoring",
      "InSAR deformation", "Groundwater sensing", "Seismic risk mapping",
      "Coastal erosion model"]),
]

fig, ax = plt.subplots(figsize=(17, 6.7))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# ---- title bar ----
tb = FancyBboxPatch((27, 91), 46, 6.5, boxstyle="round,pad=0,rounding_size=0.8",
                    fc="#1f4e79", ec="#1f4e79", zorder=3)
ax.add_patch(tb)
ax.text(50, 94.25, "Major application domains of urban spatial model technologies",
        ha="center", va="center", fontsize=15, fontweight="bold", color="white", zorder=4)

n = len(DOMAINS)
xs = [6.5 + i * (88 / (n - 1)) for i in range(n)]
col_w = 11.0
header_y = 82
header_h = 6.0
bus_y = 88

# title -> bus
ax.plot([50, 50], [91, bus_y], color="#9aa8bf", lw=1.4, zorder=1)
ax.plot([xs[0], xs[-1]], [bus_y, bus_y], color="#9aa8bf", lw=1.4, zorder=1)

item_h = 6.4
gap = 2.0
top_item = header_y - header_h / 2 - 3.0

for x, (title, hfill, ifill, iedge, items) in zip(xs, DOMAINS):
    # dropper from bus to header
    ax.plot([x, x], [bus_y, header_y + header_h / 2], color=iedge, lw=1.6, zorder=1)
    # header
    h = FancyBboxPatch((x - col_w / 2, header_y - header_h / 2), col_w, header_h,
                       boxstyle="round,pad=0,rounding_size=0.7",
                       fc=hfill, ec=hfill, zorder=3)
    ax.add_patch(h)
    ax.text(x, header_y, title, ha="center", va="center", fontsize=10.3,
            fontweight="bold", color="white", zorder=4, linespacing=1.05)

    # left spine
    spine_x = x - col_w / 2 + 0.4
    y_first = top_item
    y_last = top_item - (len(items) - 1) * (item_h + gap)
    ax.plot([spine_x, spine_x], [header_y - header_h / 2, y_last - item_h / 2],
            color=iedge, lw=1.4, zorder=1)

    # items
    y = top_item
    for it in items:
        ax.plot([spine_x, x - col_w / 2 + 1.4], [y, y], color=iedge, lw=1.4, zorder=1)
        b = FancyBboxPatch((x - col_w / 2 + 1.4, y - item_h / 2), col_w - 1.8, item_h,
                           boxstyle="round,pad=0,rounding_size=0.7",
                           fc=ifill, ec=iedge, lw=1.3, zorder=3)
        ax.add_patch(b)
        ax.text(x + 0.5, y, it, ha="center", va="center", fontsize=8.6,
                fontweight="bold", color="#333333", zorder=4, linespacing=1.0)
        y -= (item_h + gap)

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("Figure_04.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_04.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_04.png / .pdf")
