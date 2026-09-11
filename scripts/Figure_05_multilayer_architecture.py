#!/usr/bin/env python3
"""
Figure 5 - Multilayer architecture of the proposed urban information model framework.

Reconstruction (self-contained matplotlib) of the seven-layer stack used in the
accompanying urban-informatics study: numbered layer panels (1 = physical at
the bottom, 7 = decision support at the top), each with an icon, title, subtitle
and a wrapped row of component pills, dashed contextual notes on the right, and
bidirectional data/control arrows between layers.

Run:    python Figure_05_multilayer_architecture.py
Out:    Figure_05.png (300 dpi), Figure_05.pdf
Needs:  matplotlib
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "DejaVu Sans"})

# each layer: number, title, subtitle, fill, edge, accent(dark), tags, note_title, note_text
LAYERS = [
    (7, "Decision support & visualisation",
     "Governance dashboards \u00b7 autonomous control \u00b7 citizen interfaces",
     "#d9e6f4", "#6f9fca", "#2f5f96",
     ["Urban dashboards", "AR / VR city explorer", "Autonomous control loops",
      "Scenario comparison", "Policy recommendation", "Stakeholder portals",
      "Alert & notification"],
     "Output layer",
     "Translates urban information model outputs into governance actions, real-time alerts, and immersive 3-D city visualisations"),
    (6, "AI & analytics layer",
     "Predictive modelling \u00b7 anomaly detection \u00b7 optimisation",
     "#e6def3", "#9b82c8", "#5a3f9c",
     ["Deep learning", "Reinforcement learning", "Federated learning",
      "Graph neural networks", "Time-series forecasting", "Anomaly detection",
      "Computer vision", "Explainable AI"],
     "Intelligence layer",
     "ML / DL models derive predictions, detect anomalies, and optimise urban operations continuously"),
    (5, "Urban information modelling layer",
     "Simulation engines \u00b7 physical\u2013virtual synchronisation \u00b7 scenario testing",
     "#d7efe6", "#5fb39c", "#2f7d68",
     ["Physics-based simulation", "Agent-based models", "Finite element analysis",
      "Data assimilation", "Semantic object models", "Multi-scale coupling",
      "Scenario generation", "State estimation"],
     "Model core",
     "Bidirectional physical\u2013virtual synchronisation; scenario and what-if simulation engine"),
    (4, "Geospatial modelling layer",
     "3-D city models \u00b7 terrain \u00b7 subsurface \u00b7 remote sensing integration",
     "#e4f2d7", "#8bc069", "#4a7a2f",
     ["CityGML / CityJSON", "BIM (IFC)", "Digital elevation model",
      "LiDAR point clouds", "InSAR deformation", "Satellite imagery",
      "3-D geological models", "GIS spatial databases"],
     "Spatial layer",
     "GIS, BIM, LiDAR and satellite data provide the georeferenced 3-D context for all models"),
    (3, "Edge\u2013cloud computing layer",
     "Distributed processing \u00b7 scalable storage \u00b7 real-time inference",
     "#fbeed5", "#d9a95a", "#9c6a1e",
     ["Edge nodes / fog", "Cloud microservices", "Stream processing", "Data lakes",
      "Containerisation", "GPU acceleration", "API gateways", "Cybersecurity layer"],
     "Processing layer",
     "Hybrid edge\u2013cloud architecture balances latency, bandwidth, and computational cost"),
    (2, "IoT sensing & communication layer",
     "Heterogeneous protocols \u00b7 data aggregation \u00b7 real-time streaming",
     "#f6e0da", "#c67c6f", "#9c3f38",
     ["5G / NB-IoT", "LoRaWAN / LPWAN", "MQTT / CoAP", "Wi-Fi 6", "Vehicular V2X",
      "Satellite (LEO)", "Edge gateways", "OGC SensorThings"],
     "Network layer",
     "Multi-protocol IoT fabric aggregates heterogeneous sensor streams at scale"),
    (1, "Physical infrastructure layer",
     "Urban assets \u00b7 sensors \u00b7 actuators \u00b7 embedded devices",
     "#ececec", "#9aa0a6", "#5a6169",
     ["Smart meters", "Environmental sensors", "Traffic detectors",
      "GPS / GNSS devices", "LiDAR scanners", "Smart cameras",
      "Geological sensors", "Actuators & controllers"],
     "Foundation layer",
     "Physical city assets and embedded sensing devices generate raw real-world data"),
]

fig, ax = plt.subplots(figsize=(15, 17.5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 120)
ax.axis("off")

ax.text(39, 117, "Multilayer architecture of the proposed urban information model framework",
        ha="center", va="center", fontsize=17, fontweight="bold", color="#1b3a5b")

# geometry
LX, LW = 8, 62          # layer box left, width
NX, NW = 73.5, 24.5     # note box left, width
LH = 13.5               # layer height
top_c = 106.0
step = 15.6             # centre-to-centre

def char_w(fs):
    return fs * 0.108     # rough x-units per character at this axes scale


def draw_pills(cx0, top_y, width, tags, fill, edge, accent):
    """Left-aligned wrapped pills; returns nothing."""
    fs = 7.8
    x = cx0
    y = top_y
    row_h = 3.0
    line_gap = 0.9
    maxx = cx0 + width
    for t in tags:
        w = 2.4 + 0.40 * len(t)              # width estimate in axes units
        if x + w > maxx + 0.2 and x > cx0:
            x = cx0
            y -= (row_h + line_gap)
        p = FancyBboxPatch((x, y - row_h), w, row_h,
                           boxstyle=f"round,pad=0,rounding_size={row_h / 2}",
                           fc="white", ec=edge, lw=1.1, zorder=5)
        ax.add_patch(p)
        ax.text(x + w / 2, y - row_h / 2, t, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=accent, zorder=6)
        x += w + 1.1
    return y - row_h


for i, (num, title, sub, fill, edge, accent, tags, ntitle, ntext) in enumerate(LAYERS):
    cy = top_c - i * step
    # layer panel
    panel = FancyBboxPatch((LX, cy - LH / 2), LW, LH,
                           boxstyle="round,pad=0,rounding_size=1.0",
                           fc=fill, ec=edge, lw=1.8, zorder=3)
    ax.add_patch(panel)
    # number badge
    ax.add_patch(plt.Circle((LX - 3.2, cy + LH / 2 - 2.0), 2.2, color=accent, zorder=6))
    ax.text(LX - 3.2, cy + LH / 2 - 2.0, str(num), ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=7)
    # icon square
    isz = 3.2
    ix, iy = LX + 2.4, cy + LH / 2 - 2.0
    ax.add_patch(FancyBboxPatch((ix - isz / 2, iy - isz / 2), isz, isz,
                                boxstyle="round,pad=0,rounding_size=0.6",
                                fc=accent, ec=accent, zorder=6))
    ax.add_patch(FancyBboxPatch((ix - isz / 2 + 0.9, iy - isz / 2 + 0.9),
                                isz - 1.8, isz - 1.8,
                                boxstyle="round,pad=0,rounding_size=0.3",
                                fc="white", ec="white", alpha=0.85, zorder=7))
    # title + subtitle
    ax.text(LX + 5.4, cy + LH / 2 - 1.3, title, ha="left", va="top",
            fontsize=12.5, fontweight="bold", color=accent, zorder=6)
    ax.text(LX + 5.4, cy + LH / 2 - 4.3, sub, ha="left", va="top",
            fontsize=9.0, color="#6a6a6a", zorder=6)
    # pills
    draw_pills(LX + 2.4, cy + LH / 2 - 6.0, LW - 4.8, tags, fill, edge, accent)

    # right dashed note
    note = FancyBboxPatch((NX, cy - LH / 2), NW, LH,
                          boxstyle="round,pad=0,rounding_size=1.0",
                          fc="white", ec=accent, lw=1.3,
                          linestyle=(0, (3, 2)), zorder=3)
    ax.add_patch(note)
    ax.add_patch(plt.Circle((NX + 2.0, cy + LH / 2 - 2.2), 0.7, color=accent, zorder=5))
    ax.text(NX + 3.4, cy + LH / 2 - 2.2, ntitle, ha="left", va="center",
            fontsize=10.5, fontweight="bold", color=accent, zorder=5)
    wrapped = textwrap.fill(ntext, width=34)
    ax.text(NX + 1.6, cy + LH / 2 - 4.4, wrapped, ha="left", va="top",
            fontsize=8.6, color="#555555", zorder=5, linespacing=1.28)

    # bidirectional arrow to layer below
    if i < len(LAYERS) - 1:
        ymid = cy - LH / 2 - (step - LH) / 2
        ax.annotate("", xy=(LX + LW / 2, cy - LH / 2 - 0.3),
                    xytext=(LX + LW / 2, cy - step + LH / 2 + 0.3),
                    arrowprops=dict(arrowstyle="<->", color="#9aa4b0", lw=1.4), zorder=1)

# ---- legend ----
ly = 2.5
ax.plot([9, 15], [ly, ly], color="#9aa4b0", lw=1.6)
ax.text(15.8, ly, ": Bidirectional data & control flow", ha="left", va="center",
        fontsize=9.5, color="#555555")
ax.plot([34, 40], [ly, ly], color="#888888", lw=1.4, linestyle=(0, (3, 2)))
ax.text(40.8, ly, "Annotation / contextual note", ha="left", va="center",
        fontsize=9.5, color="#555555")
ax.text(62, ly, "Layers 1\u20133: data acquisition  |  Layers 4\u20135: modelling  |  "
        "Layers 6\u20137: intelligence & output", ha="left", va="center",
        fontsize=9.5, color="#9aa4b0")

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("Figure_05.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_05.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_05.png / .pdf")
