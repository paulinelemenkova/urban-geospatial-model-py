#!/usr/bin/env python3
"""
Figure 9 - Layered communication architecture for urban geospatial model sensing,
transmission, and processing.

Four-stage horizontal architecture (sensing -> communication/gateways ->
messaging/network control -> urban geospatial model computational processing) drawn as a clean,
icon-free block diagram: Nimbus Sans typography, an Okabe-Ito colour-blind-safe
stage palette, non-overlapping text, and a compact, content-filled layout.
Citations are shown in the author-year form printed from references.bib.

Outputs:
    Figure_09.png  (600 dpi)   Figure_09.pdf  (vector)
Needs:  matplotlib (Nimbus Sans, with a system sans-serif fallback).
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.font_manager import findfont, FontProperties
from matplotlib.colors import to_rgb

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Nimbus Sans", "Helvetica", "Arial"],
    "pdf.fonttype": 42, "ps.fonttype": 42,
})
_fp = FontProperties(family=plt.rcParams["font.sans-serif"])
assert "dejavu" not in findfont(_fp).lower(), "Nimbus Sans missing (DejaVu fallback)"

BLUE = "#0072B2"; SKY = "#56B4E9"; SLATE = "#5f6b73"; GREEN = "#009E73"
INK = "#1c262c"; FLOW = "#333a3f"; FB = "#666666"

def mix(c, o, t):
    a, b = to_rgb(c), to_rgb(o)
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def tint(c, t):  return mix(c, "#ffffff", t)
def shade(c, t): return mix(c, "#000000", t)

# compressed height; x-extent kept fixed so the 4-column layout is unchanged
FW, FH = 13.4, 6.4
fig, ax = plt.subplots(figsize=(FW, FH))
XMAX = 191.42857
ax.set_xlim(0, XMAX); ax.set_ylim(0, 100); ax.axis("off")

C_EDGE  = "(Bonomi et al., 2014; Chen et al., 2018)"
C_MQTT  = "(Mohammadi & Taylor, 2017)"
C_SDN   = "(Wang et al., 2015)"
C_CLOUD = "(Chettri & Bera, 2020; Banerjee et al., 2024)"
C_ROAD  = "(Rudskoy et al., 2021)"

R = {}
def put(n, x, y, w, h): R[n] = (x, y, w, h); return R[n]
def L(n):  return R[n][0]
def Rt(n): return R[n][0] + R[n][2]
def B(n):  return R[n][1]
def T(n):  return R[n][1] + R[n][3]
def CX(n): return R[n][0] + R[n][2] / 2
def CY(n): return R[n][1] + R[n][3] / 2

def rbox(x, y, w, h, fc, ec, lw=1.3, rs=1.0, ls="-", z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={rs}",
                 fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=z))
def arrow(x0, y0, x1, y1, color=FLOW, lw=1.6, ls="-", ms=14, style="-|>", z=6):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style,
                 mutation_scale=ms, lw=lw, color=color, linestyle=ls,
                 zorder=z, shrinkA=0, shrinkB=0, joinstyle="miter", capstyle="butt"))
def ctext(cx, y, s, fs, color=INK, bold=False, style="normal", z=7):
    ax.text(cx, y, s, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", style=style,
            zorder=z, linespacing=1.03)
def sepline(x, w, y, color):
    ax.plot([x + 3, x + w - 3], [y, y], color=tint(color, 0.45), lw=0.7, zorder=5)

def titled(name, color, title, lines=None, cite=None, title_fs=9.3, body_fs=8.4,
           twrap=22, bwrap=24, cwrap=30, fill=None, seps=True):
    x, y, w, h = R[name]
    rbox(x, y, w, h, fill or tint(color, 0.9), shade(color, 0.1), lw=1.4, rs=0.9, z=4)
    cx = x + w / 2
    tt = "\n".join(textwrap.wrap(title, twrap)); ntl = tt.count("\n") + 1
    cite_cy = None; cite_top = y + 1.2
    if cite:
        ct = "\n".join(textwrap.wrap(cite, cwrap)); ncl = ct.count("\n") + 1
        cite_cy = y + 1.4 + (ncl - 1) * 1.0
        cite_top = cite_cy + (ncl - 1) * 1.0 + 1.7
    if lines:
        title_cy = y + h - 1.5 - (ntl - 1) * 1.25
        ctext(cx, title_cy, tt, title_fs, color=shade(color, 0.2), bold=True)
        region_top = title_cy - (ntl - 1) * 1.25 - 2.1
        region_bot = cite_top + 0.5
        n = len(lines); slot = (region_top - region_bot) / n
        for i, ln in enumerate(lines):
            wl = "\n".join(textwrap.wrap(ln, bwrap))
            ctext(cx, region_top - slot * (i + 0.5), wl, body_fs, color=INK)
            if seps and i > 0:
                sepline(x, w, region_top - slot * i, color)
    elif cite:
        ctext(cx, y + h * 0.55 + 1.2, tt, title_fs, color=shade(color, 0.2), bold=True)
    else:
        ctext(cx, y + h / 2, tt, title_fs, color=shade(color, 0.2), bold=True)
    if cite:
        ctext(cx, cite_cy, ct, 6.8, color=shade(color, 0.15), style="italic")

# ---- headers + panels ----
COLS = {
    "I":   (2.0, 40.0, BLUE,  "I.  Sensing Layer\n& Field Devices"),
    "II":  (45.0, 49.0, SKY,  "II.  Communication\nPathways & Gateways"),
    "III": (97.0, 52.0, SLATE, "III.  Messaging Protocols\n& Network Control"),
    "IV":  (152.0, 37.4, GREEN, "IV.  Urban Geospatial Model\nComputational Processing"),
}
HB, HH, PT, PB = 90.5, 7.5, 89.5, 12.5
for x0, w, col, title in COLS.values():
    rbox(x0, PB, w, PT - PB, tint(col, 0.96), tint(col, 0.55), lw=1.0, rs=1.4, z=1)
    rbox(x0, HB, w, HH, tint(col, 0.20), shade(col, 0.12), lw=1.3, rs=1.0, z=3)
    ctext(x0 + w / 2, HB + HH / 2, title, 11.0, color=shade(col, 0.28), bold=True)

# ---- Column I ----
xI, wI = 2.0, 40.0; cI = xI + wI / 2
for y0, lab in [(71, "Heterogeneous Sensor Data Streams"), (52, "5G Nodes"),
                (33, "Vehicular Communication (V2X)"), (14, "LPWAN Nodes (LoRaWAN / NB-IoT)")]:
    put("I" + str(y0), xI + 2, y0, wI - 4, 17)
    rbox(xI + 2, y0, wI - 4, 17, tint(BLUE, 0.82), shade(BLUE, 0.12), lw=1.4, rs=0.9, z=4)
    ctext(cI, y0 + 8.5, "\n".join(textwrap.wrap(lab, 20)), 9.4, color=shade(BLUE, 0.22), bold=True)

# ---- Column II ----
put("BB", 47.5, 55, 24, 33)
put("LP", 47.5, 14, 24, 37)
put("EG", 74.0, 23, 17.5, 47)
titled("BB", SKY, "High-Throughput, Ultra-Low-Latency Backbone (5G)",
       ["Real-time Transport", "Structural Health Monitoring"], C_EDGE,
       title_fs=9.0, body_fs=8.4, twrap=20, bwrap=20, cwrap=24)
titled("LP", SKY, "Low-Data-Rate, Energy-Constrained Sensors (LPWAN)",
       ["Remote Geological Monitoring", "Waste Management"], None,
       title_fs=9.0, body_fs=8.4, twrap=20, bwrap=20)
titled("EG", SKY, "Edge Gateways",
       ["Data Aggregation, Filtering, Pre-processing", "Latency-sensitive Local Inference"],
       C_EDGE, title_fs=9.3, body_fs=8.3, twrap=14, bwrap=17, cwrap=18, fill="white")

# ---- Column III ----
put("MQ", 99.5, 59, 27, 29)
put("LW", 99.5, 41.5, 27, 13.5)
put("MM", 99.5, 24.0, 27, 13.5)
put("SDN", 129.0, 19, 18, 55)
mqx, mqw = 99.5, 27
rbox(mqx, 59, mqw, 29, tint(SLATE, 0.9), shade(SLATE, 0.1), lw=1.4, rs=0.9, z=4)
ctext(mqx + mqw / 2, 85.6, "MQTT Protocol", 9.2, color=shade(SLATE, 0.25), bold=True)
ctext(mqx + mqw / 2, 82.6, "(Publish / Subscribe)", 8.1, color=shade(SLATE, 0.25))
sxa, rxa, ymid = mqx + 5.5, mqx + mqw - 5.5, 71.0; bxc = (sxa + rxa) / 2
for dy in (3.0, -3.0):
    ax.add_patch(Circle((sxa, ymid + dy), 1.1, fc=SKY, ec=shade(SKY, 0.2), lw=0.8, zorder=6))
    ax.add_patch(Circle((rxa, ymid + dy), 1.1, fc=GREEN, ec=shade(GREEN, 0.2), lw=0.8, zorder=6))
    arrow(sxa + 1.3, ymid + dy, bxc - 2.2, ymid + dy * 0.15, color=SLATE, lw=1.0, ms=8)
    arrow(bxc + 2.2, ymid + dy * 0.15, rxa - 1.3, ymid + dy, color=SLATE, lw=1.0, ms=8)
rbox(bxc - 2.1, ymid - 2.0, 4.2, 4.0, "white", shade(SLATE, 0.2), lw=1.0, rs=0.4, z=6)
ctext(bxc, ymid, "broker", 7.0, color=shade(SLATE, 0.3))
ctext(sxa, ymid - 5.0, "Senders", 7.6, color=INK); ctext(rxa, ymid - 5.0, "Receivers", 7.6, color=INK)
for nm, lab in [("LW", "Lightweight, Optimized for Constrained IoT"),
                ("MM", "Efficient Many-to-Many Routing")]:
    x, y, w, h = R[nm]
    rbox(x, y, w, h, tint(SLATE, 0.82), shade(SLATE, 0.12), lw=1.2, rs=0.7, z=4)
    ctext(x + w / 2, y + h / 2, "\n".join(textwrap.wrap(lab, 26)), 8.4, color=INK)
ctext(mqx + mqw / 2, 20.5, C_MQTT, 7.0, color=shade(SLATE, 0.2), style="italic")
titled("SDN", SLATE, "Software-Defined Networking (SDN)",
       ["Programmable, Centralised Network Control", "Dynamic Resource Reallocation"],
       C_SDN, title_fs=9.0, body_fs=8.2, twrap=13, bwrap=15, cwrap=18, fill="white")

# ---- Column IV ----
put("ING", 155.0, 79.0, 31.4, 9.5)
put("CLD", 155.0, 63.5, 31.4, 13.5)
put("CORE", 155.0, 44.0, 31.4, 17.0)
put("VC", 155.0, 31.0, 31.4, 10.0)
put("PRN", 155.0, 14.0, 31.4, 13.5)
cIV = 155.0 + 31.4 / 2
titled("ING", GREEN, "Urban Geospatial Model Data Ingestion Pipeline", None, None, title_fs=9.2, twrap=18, fill="white")
titled("CLD", GREEN, "Cloud Platforms", ["Processing large datasets"], C_CLOUD,
       title_fs=9.3, body_fs=8.3, twrap=18, bwrap=20, cwrap=30, fill="white")
titled("CORE", GREEN, "Core Urban Geospatial Model", ["Virtual representation, simulation models"],
       C_CLOUD, title_fs=9.3, body_fs=8.3, twrap=16, bwrap=20, cwrap=30, fill="white")
titled("VC", GREEN, "Virtual Counterpart", None, None, title_fs=9.3, twrap=18, fill="white")
titled("PRN", GREEN, "Physical Road Network", None, C_ROAD, title_fs=9.3, twrap=16,
       cwrap=24, fill=tint(GREEN, 0.82))
arrow(cIV, B("ING"), cIV, T("CLD"), color=GREEN, lw=1.7, ms=13)
arrow(cIV, B("CLD"), cIV, T("CORE"), color=GREEN, lw=1.7, ms=13)
arrow(cIV, B("CORE"), cIV, T("VC"), color=GREEN, lw=1.7, ms=13)
arrow(cIV, B("VC"), cIV, T("PRN"), color=GREEN, lw=1.7, ms=14, style="<|-|>")
ctext(cIV + 11.5, (B("VC") + T("PRN")) / 2, "Vehicular\nCommunication\n(V2X)", 7.6, color=shade(GREEN, 0.15))
fbx = 152.0 + 37.4 - 1.2
ax.add_patch(FancyArrowPatch((Rt("PRN") - 0.4, CY("PRN")), (fbx, CY("PRN")), arrowstyle="-",
             lw=1.4, color=FB, linestyle=(0, (5, 3)), zorder=3))
ax.add_patch(FancyArrowPatch((fbx, CY("PRN")), (fbx, T("ING") - 4.0), arrowstyle="-",
             lw=1.4, color=FB, linestyle=(0, (5, 3)), zorder=3))
arrow(fbx, T("ING") - 4.0, Rt("ING") - 0.4, T("ING") - 4.0, color=FB, lw=1.4, ls=(0, (5, 3)), ms=12)

# ---- inter-column flows ----
arrow(42, 79.5, L("BB"), 78, color=FLOW, lw=1.7, ms=15)
arrow(42, 60.5, L("BB"), 63, color=FLOW, lw=1.7, ms=15)
arrow(42, 41.5, L("LP"), 40, color=FLOW, lw=1.7, ms=15)
arrow(42, 22.5, L("LP"), 28, color=FLOW, lw=1.7, ms=15)
ax.text(43.5, 50, "Continuous Data Flow", rotation=90, ha="center", va="center",
        fontsize=8.2, color=shade(SKY, 0.25), fontweight="bold", zorder=7)
arrow(Rt("BB"), 63, L("EG"), 58, color=FLOW, lw=1.6, ms=14)
arrow(Rt("LP"), 33, L("EG"), 46, color=FLOW, lw=1.6, ms=14)
arrow(Rt("EG"), 47, L("MQ"), 66, color=FLOW, lw=1.7, ms=15, style="<|-|>")
arrow(Rt("MQ"), 60, L("SDN"), 60, color=FLOW, lw=1.6, ms=14)
arrow(Rt("SDN"), 52, L("CORE"), 52, color=FLOW, lw=1.7, ms=15, style="<|-|>")

# ---- legend ----
ly = 6.5
arrow(42.0, ly, 50.0, ly, color=FLOW, lw=2.0, ms=16); ctext(62.5, ly, "Data Flow", 9.2, color=INK)
arrow(82.0, ly, 90.0, ly, color=FB, lw=1.8, ls=(0, (5, 3)), ms=15)
ctext(107.5, ly, "Control / Feedback Loop", 9.2, color=INK)
arrow(135.0, ly, 143.0, ly, color=FLOW, lw=1.8, ms=15, style="<|-|>")
ctext(155.0, ly, "Connectivity", 9.2, color=INK)

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
fig.savefig("Figure_09.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("Figure_09.pdf", bbox_inches="tight", facecolor="white")
print("wrote Figure_09.png (600 dpi) + Figure_09.pdf")
