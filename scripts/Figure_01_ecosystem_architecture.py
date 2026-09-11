#!/usr/bin/env python3
"""
Figure 1 - Virtual urban model ecosystem architecture.

Block diagram of the ecosystem architecture. Each box is sized from the
measured extent of its rendered text plus a small fixed pad, using a 3-tier
8-12 pt typography scale. Arrows use one consistent thin shaft weight and a
single closed arrowhead throughout. Font: Nimbus Sans (system sans-serif
fallback).

Run:    python Figure_01_ecosystem_architecture.py
Out:    Figure_01.png (600 dpi), Figure_01.pdf
Needs:  matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import findfont, FontProperties

# ---- font: Nimbus Sans only, verified present, no DejaVu fallback ----------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Nimbus Sans"]
_resolved = findfont(FontProperties(family=["Nimbus Sans"]), fallback_to_default=True)
assert "dejavu" not in _resolved.lower(), f"DejaVu fallback in use: {_resolved}"
assert "nimbus" in _resolved.lower(), f"Nimbus Sans not resolved: {_resolved}"

# ---- muted academic palette (unchanged) ------------------------------------
GREEN = dict(band="#eef4ee", edge="#4e8060", text="#33573f")
BLUE  = dict(band="#eef1f8", edge="#3f6395", text="#2c4a72")
OLIVE = dict(band="#f2f4e8", edge="#6f7f3d", text="#4c5828")
AMBER = dict(fill="#fbf1da", edge="#c08a2e", text="#8a5f18")
TEAL  = dict(fill="#e6f2ee", edge="#3f8f7c", text="#2c6357")
BOXED = "#ffffff"
INK, GREY, FLOW = "#2b2b2b", "#666666", "#3a3a3a"
FB_TEAL, FB_AMBER = "#3f8f7c", "#c08a2e"

# ---- typography: mandatory 3-tier scale, 8-12pt ----------------------------
FS_TITLE = 12   # main figure title (bold)
FS_BOX   = 9.5  # band labels, all box titles, virtual urban model header, captions, legend
FS_SMALL = 8    # small inline glosses (never smaller than the 8 pt floor)

# ---- line weights: one consistent shaft width per arrow class -------------
LW_BAND, LW_BOX, LW_HL = 0.9, 1.0, 1.3   # outlines
LW_FLOW = 1.0                              # solid data/processing-flow shafts
LW_FB   = 1.0                              # dashed feedback shafts (both colours)
ARROW_SCALE = 17                           # enlarged, distinct closed arrowhead

fig, ax = plt.subplots(figsize=(15.2, 8.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.canvas.draw()  # initialise a renderer so text extents can be measured

# =============================================================================
# content-driven measurement helpers
# =============================================================================
_p0 = ax.transData.transform((0, 0))
_px = ax.transData.transform((1, 0))
_py = ax.transData.transform((0, 1))
PPD_X = _px[0] - _p0[0]   # pixels per data-unit, x
PPD_Y = _py[1] - _p0[1]   # pixels per data-unit, y


def measure(s, fontsize, bold=True, linespacing=1.12):
    """Real rendered (width, height) of a text string, in data units."""
    t = ax.text(0, 0, s, fontsize=fontsize, fontweight="bold" if bold else "normal",
                ha="center", va="center", linespacing=linespacing, alpha=0)
    fig.canvas.draw()
    bbox = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    return bbox.width / PPD_X, bbox.height / PPD_Y


PAD_X, PAD_Y = 1.6, 1.5   # one consistent pad for every simple text box


def box_size(s, fontsize=FS_BOX, bold=True, pad_x=PAD_X, pad_y=PAD_Y):
    tw, th = measure(s, fontsize, bold)
    return tw + 2 * pad_x, th + 2 * pad_y


def row_size(specs, fontsize=FS_BOX, bold=True, pad_x=PAD_X, pad_y=PAD_Y):
    """Uniform (w, h) for a row of boxes: max over each box's own measured size."""
    sizes = [box_size(s, fontsize, bold, pad_x, pad_y) for s in specs]
    return max(w for w, h in sizes), max(h for w, h in sizes)


# =============================================================================
# drawing primitives
# =============================================================================
def box(cx, cy, w, h, title, edge, fill=BOXED, tfs=FS_BOX, bold=True, tcolor=INK,
        rounding=0.8, lw=LW_BOX, z=4):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                 boxstyle=f"round,pad=0,rounding_size={rounding}",
                 fc=fill, ec=edge, lw=lw, zorder=z))
    ax.text(cx, cy, title, ha="center", va="center", fontsize=tfs,
            fontweight="bold" if bold else "normal", color=tcolor,
            zorder=z + 1, linespacing=1.12)


def band(x0, x1, y0, y1, style, label):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                 boxstyle="round,pad=0,rounding_size=1.2",
                 fc=style["band"], ec=style["edge"], lw=LW_BAND, alpha=0.9, zorder=1))
    ax.text(7.0, (y0 + y1) / 2, label, ha="center", va="center", fontsize=FS_BOX,
            fontweight="bold", color=style["text"], zorder=2, linespacing=1.25)


def ortho(pts, color=FLOW, lw=LW_FLOW, dashed=False, z=3):
    """Draw an orthogonal (H/V only) connector through waypoints, arrow at end."""
    ls = (0, (4, 3)) if dashed else "-"
    if len(pts) > 2:
        ax.plot([p[0] for p in pts[:-1]], [p[1] for p in pts[:-1]],
                color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=z)
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>",
                 mutation_scale=ARROW_SCALE, color=color, lw=lw,
                 linestyle=ls, zorder=z))

# =============================================================================
# title + bands
# =============================================================================
ax.text(56, 96.5, "Virtual urban model Ecosystem Architecture",
        ha="center", va="center", fontsize=FS_TITLE, fontweight="bold", color="#24485f")

band(13, 85, 77, 93, GREEN, "Physical\ninfrastructure\n& IoT sensing")
band(13, 85, 50, 73, BLUE,  "Cloud-edge\ncomputing &\ncyber-physical\nsystems (CPS)")
band(13, 85, 8, 46, OLIVE,  "AI analytics,\ndecision support\n& governance")

# =============================================================================
# TIER 1 - physical infrastructure (content-driven uniform row size)
# =============================================================================
t1 = ["Smart City\nBuildings", "Autonomous\nVehicles", "Factory\nSystems",
      "Critical\nInfrastructure", "IoT & Sensor\nNetworks",
      "Environmental\nMonitoring", "Smart Energy\nGrid"]
t1_w, t1_h = row_size(t1, fontsize=FS_BOX, bold=False)
t1_xs = [19.5, 29.5, 39.5, 49.5, 59.5, 69.5, 79.5]
for x, name in zip(t1_xs, t1):
    box(x, 85, t1_w, t1_h, name, GREEN["edge"], bold=False, tcolor=GREEN["text"])

# =============================================================================
# TIER 2 - platform pipeline
# =============================================================================
w5g, h5g = box_size("5G /\nwireless", bold=False)
box(16.0, 61, w5g, h5g, "5G /\nwireless", BLUE["edge"], bold=False, tcolor=BLUE["text"])

pipe_names = ["Distributed\nStorage", "Edge Compute\nNodes",
              "Data Lake &\nIntegration", "Process\nPipelines"]
pipe_xs = [25.5, 38.0, 50.5, 63.0]
pipe_w, pipe_h = row_size(pipe_names, fontsize=FS_BOX, bold=True)
for name, x in zip(pipe_names, pipe_xs):
    box(x, 61, pipe_w, pipe_h, name, BLUE["edge"], tcolor=BLUE["text"])

wv, hv = box_size("Continuous\nValidation")
box(75.5, 61, wv, hv, "Continuous\nValidation", AMBER["edge"], fill=AMBER["fill"],
    tcolor=AMBER["text"], lw=LW_HL)
wp, hp = box_size("Public Data\nServices")
box(92.5, 61, wp, hp, "Public Data\nServices", BLUE["edge"], tcolor=BLUE["text"])

# horizontal connectors between adjacent Tier-2 boxes (edges recomputed from
# the measured widths above)
t2_edges = [
    (16.0 + w5g / 2, 25.5 - pipe_w / 2),
    (25.5 + pipe_w / 2, 38.0 - pipe_w / 2),
    (38.0 + pipe_w / 2, 50.5 - pipe_w / 2),
    (50.5 + pipe_w / 2, 63.0 - pipe_w / 2),
    (63.0 + pipe_w / 2, 75.5 - wv / 2),
    (75.5 + wv / 2, 92.5 - wp / 2),
]
for xa, xb in t2_edges:
    ortho([(xa, 61), (xb, 61)])
ax.text(44.2, 61 + pipe_h / 2 + 1.3, "cloud\nconn.", ha="center", va="center",
        fontsize=FS_SMALL, color=GREY, style="italic")

# =============================================================================
# TIER 3 - analytics / virtual urban model / decision support / governance
# =============================================================================
wa, ha = box_size("Analytics &\nAI Models")
box(24.0, 30, wa, ha, "Analytics &\nAI Models", OLIVE["edge"], tcolor=OLIVE["text"])

# --- virtual urban model composite container: height built from its own
# stacked content (header, loop annotation, sub-model row, caption) rather
# than a guessed constant.
vr_sub = ["Hydrology\nModel", "Traffic\nSimulation Model", "Energy Use\nModel"]
sub_w, sub_h = row_size(vr_sub, fontsize=FS_BOX, bold=False, pad_x=1.2, pad_y=1.1)

hdr_w, hdr_h = measure("VIRTUAL URBAN MODELS", FS_BOX, bold=True)
loop_w, loop_h = measure("Continuous readiness & loop", FS_SMALL, bold=False)
cap_w, cap_h = measure("Simulation environment (real-time and future-predictive)",
                        FS_BOX, bold=True)

GAP = 0.9        # fixed small gap between internal elements
OUTER_PAD = 1.3  # container edge padding
vr_h = hdr_h + GAP + loop_h + GAP + sub_h + GAP + cap_h + 2 * OUTER_PAD
vr_w = max(3 * sub_w + 2 * 0.8, hdr_w, cap_w) + 2 * OUTER_PAD

vr_cx, vr_cy = 50.5, 26.0
vr_x0, vr_x1 = vr_cx - vr_w / 2, vr_cx + vr_w / 2
vr_y0, vr_y1 = vr_cy - vr_h / 2, vr_cy + vr_h / 2

ax.add_patch(FancyBboxPatch((vr_x0, vr_y0), vr_w, vr_h,
             boxstyle="round,pad=0,rounding_size=1.2",
             fc=TEAL["fill"], ec=TEAL["edge"], lw=LW_HL, zorder=3))

y_cursor = vr_y1 - OUTER_PAD - hdr_h / 2
ax.text(vr_cx, y_cursor, "VIRTUAL URBAN MODELS", ha="center", va="center",
        fontsize=FS_BOX, fontweight="bold", color=TEAL["text"], zorder=5)
y_cursor -= hdr_h / 2 + GAP + loop_h / 2
ax.text(vr_cx, y_cursor, "Continuous readiness & loop", ha="center", va="center",
        fontsize=FS_SMALL, color=TEAL["edge"], style="italic", zorder=5)

sub_cy = y_cursor - loop_h / 2 - GAP - sub_h / 2
sub_xs = [vr_cx - sub_w - 0.8, vr_cx, vr_cx + sub_w + 0.8]
for name, x in zip(vr_sub, sub_xs):
    box(x, sub_cy, sub_w, sub_h, name, TEAL["edge"], bold=False, tcolor=TEAL["text"],
        tfs=FS_BOX)

cap_cy = sub_cy - sub_h / 2 - GAP - cap_h / 2
ax.text(vr_cx, cap_cy, "Simulation environment (real-time and future-predictive)",
        ha="center", va="center", fontsize=FS_BOX, fontweight="bold",
        color=TEAL["edge"], zorder=5)

wds, hds = box_size("Decision Support\nSystems")
box(75.5, 33, wds, hds, "Decision Support\nSystems", OLIVE["edge"], tcolor=OLIVE["text"])
wg, hg = box_size("Governance\n& Policy")
box(75.5, 21.5, wg, hg, "Governance\n& Policy", AMBER["edge"], fill=AMBER["fill"],
    tcolor=AMBER["text"], lw=LW_HL)
wc, hc = box_size("City\nManagement")
box(92.5, 30, wc, hc, "City\nManagement", OLIVE["edge"], tcolor=OLIVE["text"])

ortho([(24.0 + wa / 2, 30), (vr_x0, 30)])              # analytics -> virtual urban model models
vr_side_y = vr_y1 - 2.6                                 # clear of the top rounding
ortho([(vr_x1, vr_side_y), (75.5 - wds / 2, vr_side_y)])  # virtual urban model models -> decision support
ortho([(75.5 + wds / 2, 32), (92.5 - wc / 2, 32)])     # decision support -> city mgmt

# =============================================================================
# cross-tier couplings + feedback loops  (all orthogonal)
# =============================================================================
ortho([(50.5, 77), (50.5, 61 + pipe_h / 2)], lw=1.0)             # physical -> data lake
ax.text(53.4, 74.2, "network\ndevices", ha="left", va="center", fontsize=FS_SMALL,
        color=GREY, style="italic")
ortho([(24.0, 50), (24.0, 30 + ha / 2)])                          # platform -> analytics

ortho([(50.5, vr_y1), (50.5, 61 - pipe_h / 2)], color=FB_TEAL, lw=LW_FB, dashed=True)
ortho([(75.5, 33 + hds / 2), (75.5, 61 - hv / 2)], color=FB_TEAL, lw=LW_FB, dashed=True)
ortho([(92.5, 61 + hp / 2), (92.5, 75.0), (30.0, 75.0), (30.0, 77.0)],
      color=FB_TEAL, lw=LW_FB, dashed=True)
ax.text(61.0, 76.3, "governance & data feedback", ha="center", va="center",
        fontsize=FS_SMALL, color=FB_TEAL, style="italic")

ortho([(75.5, 61 - hv / 2), (75.5, 58.5), (63.0, 58.5), (63.0, 61 - pipe_h / 2)],
      color=FB_AMBER, lw=LW_FB, dashed=True)                     # validation -> pipelines
ortho([(75.5 + wg / 2, 21.5), (92.5, 21.5), (92.5, 30 - hc / 2)],
      color=FB_AMBER, lw=LW_FB, dashed=True)                     # governance -> city mgmt

# =============================================================================
# legend
# =============================================================================
lx, ly = 15.0, 3.2
ortho([(lx, ly), (lx + 4, ly)])
ax.text(lx + 4.8, ly, "Data & processing flow", ha="left", va="center", fontsize=FS_BOX, color=INK)
ortho([(lx + 33, ly), (lx + 37, ly)], color=FB_TEAL, dashed=True)
ax.text(lx + 37.8, ly, "Readiness / governance feedback", ha="left", va="center", fontsize=FS_BOX, color=INK)
ortho([(lx + 70, ly), (lx + 74, ly)], color=FB_AMBER, dashed=True)
ax.text(lx + 74.8, ly, "Validation / policy loop", ha="left", va="center", fontsize=FS_BOX, color=INK)

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("Figure_01.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_01.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_01.png / .pdf")
print(f"t1 box: {t1_w:.2f}x{t1_h:.2f}  pipe box: {pipe_w:.2f}x{pipe_h:.2f}  "
      f"virtual urban model container: {vr_w:.2f}x{vr_h:.2f}  sub box: {sub_w:.2f}x{sub_h:.2f}")
