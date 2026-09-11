#!/usr/bin/env Rscript
# Figure 8 - AI/analytics architecture stack for urban computational models.
# Icon-free block diagram with a content-driven compact layout: Nimbus Sans,
# explicit point sizes (<=3 tiers, 8-12 pt), minimal whitespace, vector PDF
# plus 600 dpi PNG. Box heights and the Federated-Learning panel are sized from
# the wrapped line count of their text, and each header and description are
# centred as one block within the box.
#
# Run:    Rscript Figure_08.R
# Out:    Figure_08.png (600 dpi), Figure_08.pdf (Nimbus Sans embedded)
# Needs:  ggplot2 >= 3.4 (size.unit="pt"), R >= 4.0.

suppressMessages({library(ggplot2); library(grid)})

FAM <- "Nimbus Sans"
stopifnot(packageVersion("ggplot2") >= "3.4.0")

## ---- typography (mandatory 3-tier scale, 8-12 pt) --------------------------
FS_HEAD   <- 11
FS_BODY   <- 9.5
FS_CREDIT <- 8

## ---- palette -----------------------------------------------------------
BLUE  <- list(fill = "#dbe6f2", edge = "#5f80a6", acc = "#2f4f73")
TAN   <- list(fill = "#f7ecc9", edge = "#c9a23a", acc = "#8a6d1e")
GREEN <- list(fill = "#d6e8cf", edge = "#5a8a4e", acc = "#356030")
PEACH <- list(fill = "#f7ded0", edge = "#c98a54", acc = "#8a5a2e")
FED   <- list(fill = "#f5cdb8", edge = "#b5583a", acc = "#7a3820")
OUTER <- list(fill = "#f2f2f2", edge = "#8a8a8a", acc = "#333333")

FLOW_DATA  <- "#5f80a6"
FLOW_TRAIN <- "#5a8a4e"
FLOW_PRIV  <- "#c9605a"

INK <- "#232323"; GREY <- "#555555"
ar1 <- arrow(length = unit(0.22, "cm"), type = "closed")
ar2 <- arrow(length = unit(0.22, "cm"), type = "closed", ends = "both")

## ---- geometry helpers -------------------------------------------------------
rrect <- function(xmin, xmax, ymin, ymax, r = 0.5, n = 8) {
  r <- min(r, (xmax - xmin) / 2, (ymax - ymin) / 2)
  a1 <- seq(pi, 3 * pi / 2, length.out = n); a2 <- seq(3 * pi / 2, 2 * pi, length.out = n)
  a3 <- seq(0, pi / 2, length.out = n);      a4 <- seq(pi / 2, pi, length.out = n)
  data.frame(
    x = c((xmin + r) + r * cos(a1), (xmax - r) + r * cos(a2),
          (xmax - r) + r * cos(a3), (xmin + r) + r * cos(a4)),
    y = c((ymin + r) + r * sin(a1), (ymin + r) + r * sin(a2),
          (ymax - r) + r * sin(a3), (ymax - r) + r * sin(a4)))
}

L <- list()
addbox <- function(x0, x1, y0, y1, fill = "white", col = INK, lwd = 0.4, lty = "solid", r = 0.5)
  L[[length(L) + 1]] <<- geom_polygon(data = rrect(x0, x1, y0, y1, r), aes(x, y),
      fill = fill, colour = col, linewidth = lwd, linetype = lty)
addtxt <- function(x, y, lab, size = FS_BODY, face = "plain", col = INK, h = 0.5, v = 0.5, ang = 0)
  L[[length(L) + 1]] <<- annotate("text", x = x, y = y, label = lab, size = size,
      size.unit = "pt", fontface = face, colour = col, hjust = h, vjust = v,
      family = FAM, lineheight = 0.92, angle = ang)
addseg <- function(x, xe, y, ye, col = INK, lwd = 0.5, lty = "solid", arw = NULL)
  L[[length(L) + 1]] <<- annotate("segment", x = x, xend = xe, y = y, yend = ye, colour = col,
      linewidth = lwd, linetype = lty, arrow = arw)

elbow <- function(x0, y0, x1, y1, ymid, col, lwd = 1.0, lty = "solid") {
  if (abs(x0 - x1) < 1e-6) {
    addseg(x0, x1, y0, y1, col = col, lwd = lwd, lty = lty, arw = ar1)
  } else {
    addseg(x0, x0, y0, ymid, col = col, lwd = lwd, lty = lty)
    addseg(x0, x1, ymid, ymid, col = col, lwd = lwd, lty = lty)
    addseg(x1, x1, ymid, y1, col = col, lwd = lwd, lty = lty, arw = ar1)
  }
}
labelbreak <- function(x, y, lab, w = 12, h = 3.0, size = FS_BODY) {
  addbox(x - w / 2, x + w / 2, y - h / 2, y + h / 2, fill = "white", col = NA, lwd = 0, r = 0.2)
  addtxt(x, y, lab, size = size, col = INK)
}
wrapt <- function(s, w = 30) paste(strwrap(s, width = w), collapse = "\n")
nlines <- function(s, w) length(strwrap(s, width = w))

## ---- physical scale: 1 data-unit in points (x-range fixed at 88, width 15in)
SCALE_PT_PER_UNIT <- 15.0 * 72 / 88
LH_HEAD <- (FS_HEAD * 1.16) / SCALE_PT_PER_UNIT   # line height, header tier, data units
LH_BODY <- (FS_BODY * 1.16) / SCALE_PT_PER_UNIT   # line height, body tier, data units
GAP_HD  <- 0.16                                    # gap between header block and description

## content height needed for a header(+description) text block, data units
content_h <- function(header, desc, wrap, dwrap = wrap) {
  nh <- nlines(header, wrap)
  hh <- nh * LH_HEAD
  if (is.null(desc)) return(hh)
  nd <- nlines(desc, dwrap)
  hh + GAP_HD + nd * LH_BODY
}

## header (top) + description (below), the pair centred as ONE block in the box
PAD_INNER <- 0.30
hbox <- function(x0, x1, y0, y1, header, desc, S, fill = S$fill, wrap = 24, dwrap = 30) {
  addbox(x0, x1, y0, y1, fill = fill, col = S$edge, lwd = 0.55)
  cx <- (x0 + x1) / 2
  nh <- nlines(header, wrap)
  ch <- content_h(header, desc, wrap, dwrap)
  block_top <- (y0 + y1) / 2 + ch / 2
  addtxt(cx, block_top, wrapt(header, wrap), size = FS_HEAD, face = "bold", col = S$acc, v = 1)
  if (!is.null(desc)) {
    addtxt(cx, block_top - nh * LH_HEAD - GAP_HD, wrapt(desc, dwrap), size = FS_BODY, col = INK, v = 1)
  }
}

band <- function(x0, x1, y0, y1, title, tx) {
  addbox(x0, x1, y0, y1, fill = OUTER$fill, col = OUTER$edge, lwd = 0.6, r = 0.7)
  addtxt(tx, (y0 + y1) / 2, title, size = FS_HEAD, face = "bold", col = OUTER$acc, h = 0.5)
}

## =============================================================================
## column geometry (x only; y heights are computed below from content)
## =============================================================================
GAP_BOX <- 0.7
LABEL_W <- 13.5
X0 <- 1
CX0 <- X0 + LABEL_W
CX1 <- 68

w3 <- (CX1 - CX0 - 2 * GAP_BOX) / 3
b1x <- c(CX0, CX0 + w3); b2x <- c(b1x[2] + GAP_BOX, b1x[2] + GAP_BOX + w3)
b3x <- c(b2x[2] + GAP_BOX, CX1)
w2 <- (CX1 - CX0 - GAP_BOX) / 2
c1x <- c(CX0, CX0 + w2); c2x <- c(c1x[2] + GAP_BOX, CX1)

RX <- c(70, 87)
xB1 <- mean(b1x); xB2 <- mean(b2x); xB3 <- mean(b3x)
xCA <- mean(c1x); xCB <- mean(c2x)
xA1 <- mean(b1x); xA2 <- mean(b2x); xA3 <- mean(b3x)

## =============================================================================
## content-driven row heights (max over each row's boxes, + small pad)
## =============================================================================
INPUT_WRAP <- 18; INPUT_DWRAP <- 20
input_h_needed <- max(
  content_h("INFRASTRUCTURE SENSOR DATA", "(Spatial-Temporal Dependencies)", INPUT_WRAP, INPUT_DWRAP),
  content_h("IMAGERY & LIDAR DATA", NULL, 16),
  content_h("HISTORICAL & REAL-TIME URBAN DATA", NULL, 16)
)
INPUT_H <- input_h_needed + 2 * PAD_INNER

core_h_needed <- max(
  content_h("CLASSICAL ML METHODS", "(Classification, Regression, Clustering, interpretable baseline)", 26, 32),
  content_h("DEEP LEARNING ARCHITECTURES", "(Convolutional, Recurrent, complex dependency capture)", 26, 30)
)
CORE_H <- core_h_needed + 2 * PAD_INNER

adv_h_needed <- max(
  content_h("REINFORCEMENT LEARNING AGENTS", "Adaptive Policies for Closed-Loop Control", 16, 17),
  content_h("COMPUTER VISION TECHNIQUES", "Object Detection, Semantic Segmentation, Change Monitoring", 16, 17),
  content_h("PREDICTIVE ANALYTICS ENGINE",
            "Probabilistic Forecasts (Energy Demand, Flood Risk, Failure, Congestion)", 16, 18)
)
ADV_H <- adv_h_needed + 2 * PAD_INNER

## Application band: header line + two pill rows, tightly
PILL_H <- 1.35; PILL_GAP <- 0.22
APP_HEAD_H <- LH_HEAD + 0.30
APP_H <- APP_HEAD_H + 0.20 + 2 * PILL_H + PILL_GAP + 2 * PAD_INNER

GAP1 <- 1.7; GAP2 <- 2.5; GAP3 <- 1.6

y0 <- 0.4
OB1 <- c(y0, y0 + INPUT_H + 2 * PAD_INNER)
OB2 <- c(OB1[2] + GAP1, OB1[2] + GAP1 + CORE_H + 2 * PAD_INNER)
OB3 <- c(OB2[2] + GAP2, OB2[2] + GAP2 + ADV_H + 2 * PAD_INNER)
OB4 <- c(OB3[2] + GAP3, OB3[2] + GAP3 + APP_H)

RP <- c(OB2[1], OB4[2])
TOPY <- OB4[2] + 0.4

## ---- Federated Learning panel content sizing (computed early so the inner
## box can be vertically centred within the full-height outer peach panel,
## which must still span Core-bottom..Application-top for the cross-band
## connector arrows to land inside it)
fed_header_h <- 2 * LH_HEAD + 0.15
fed_sections <- list(
  "Distributed Model Training (Multi-stakeholder Environments)",
  "Train across institutions/sensor networks",
  "No centralized raw data"
)
SEC_WRAP <- 22
sec_lines <- sapply(fed_sections, nlines, w = SEC_WRAP)
DIV_GAP <- 0.55   # space either side of each divider rule
fed_body_h <- sum(sec_lines * LH_BODY) + 2 * DIV_GAP * 2 + 0.3 * 2
fed_content_h <- fed_header_h + 0.35 + fed_body_h + 2 * PAD_INNER

fed_margin <- 0.8             # gap from the outer peach panel border
avail_top <- RP[2] - 2.4      # leave room for the "Data Privacy & Governance" title
avail_bot <- RP[1] + fed_margin
fed_center <- (avail_top + avail_bot) / 2
fedTop <- min(avail_top, fed_center + fed_content_h / 2)
fedBot <- fedTop - fed_content_h

## =============================================================================
## band outlines + labels
## =============================================================================
band(X0, 87, OB1[1], OB1[2], "Multimodal Data\nIngestion (Input)", tx = (X0 + CX0 - 0.6) / 2)
band(X0, 87, OB2[1], OB2[2], "Core Learning\nArchitectures", tx = (X0 + CX0 - 0.6) / 2)
band(X0, 87, OB3[1], OB3[2], "Advanced Learning\nParadigms &\nSpecialized Analytics", tx = (X0 + CX0 - 0.6) / 2)
band(X0, 87, OB4[1], OB4[2], "urban computational model\nApplication Services", tx = (X0 + CX0 - 0.6) / 2)

## right panel outline -- spans the full left-stack height (needed so the
## Core/Advanced/Input connector arrows all land inside it); inner content
## is centred within it rather than stretched, so it stays visually compact
addbox(RX[1], RX[2], RP[1], RP[2], fill = PEACH$fill, col = PEACH$edge, lwd = 0.7, r = 0.7)
addtxt((RX[1] + RX[2]) / 2, RP[2] - 0.85, "Data Privacy &\nGovernance",
       size = FS_HEAD, face = "bold", col = PEACH$acc, v = 1)
addbox(RX[1], RX[2], OB1[1], OB1[2], fill = "white", col = OUTER$edge, lwd = 0.5, r = 0.6)

## =============================================================================
## INPUT band content
## =============================================================================
iy <- c(OB1[1] + PAD_INNER, OB1[2] - PAD_INNER)
hbox(b1x[1], b1x[2], iy[1], iy[2], "INFRASTRUCTURE SENSOR DATA", "(Spatial-Temporal Dependencies)",
     BLUE, wrap = INPUT_WRAP, dwrap = INPUT_DWRAP)
hbox(b2x[1], b2x[2], iy[1], iy[2], "IMAGERY & LIDAR DATA", NULL, BLUE, wrap = 16)
hbox(b3x[1], b3x[2], iy[1], iy[2], "HISTORICAL & REAL-TIME URBAN DATA", NULL, BLUE, wrap = 16)

## =============================================================================
## CORE band content
## =============================================================================
cy <- c(OB2[1] + PAD_INNER, OB2[2] - PAD_INNER)
hbox(c1x[1], c1x[2], cy[1], cy[2], "CLASSICAL ML METHODS",
     "(Classification, Regression, Clustering, interpretable baseline)", TAN, wrap = 26, dwrap = 32)
hbox(c2x[1], c2x[2], cy[1], cy[2], "DEEP LEARNING ARCHITECTURES",
     "(Convolutional, Recurrent, complex dependency capture)", TAN, wrap = 26, dwrap = 30)

## =============================================================================
## ADVANCED band content
## =============================================================================
ay <- c(OB3[1] + PAD_INNER, OB3[2] - PAD_INNER)
hbox(b1x[1], b1x[2], ay[1], ay[2], "REINFORCEMENT LEARNING AGENTS",
     "Adaptive Policies for Closed-Loop Control", GREEN, wrap = 16, dwrap = 17)
hbox(b2x[1], b2x[2], ay[1], ay[2], "COMPUTER VISION TECHNIQUES",
     "Object Detection, Semantic Segmentation, Change Monitoring", GREEN, wrap = 16, dwrap = 17)
hbox(b3x[1], b3x[2], ay[1], ay[2], "PREDICTIVE ANALYTICS ENGINE",
     "Probabilistic Forecasts (Energy Demand, Flood Risk, Failure, Congestion)",
     GREEN, wrap = 16, dwrap = 18)

midY <- mean(ay)
addseg(b1x[2] + 0.08, b2x[1] - 0.08, midY, midY, col = FLOW_TRAIN, lwd = 0.65, arw = ar1)
addseg(b2x[2] + 0.08, b3x[1] - 0.08, midY, midY, col = FLOW_TRAIN, lwd = 0.65, arw = ar1)

## =============================================================================
## APPLICATION band content (tight: header + 2 pill rows only)
## =============================================================================
addbox(b1x[1], b3x[2], OB4[1] + PAD_INNER, OB4[2] - PAD_INNER, fill = PEACH$fill, col = PEACH$edge, lwd = 0.6)
appHeadY <- OB4[2] - PAD_INNER - 0.30
addtxt(mean(c(b1x[1], b3x[2])), appHeadY, "URBAN COMPUTATIONAL MODEL SERVICES",
       size = FS_HEAD, face = "bold", col = PEACH$acc, v = 1)
pill <- function(x0, x1, y0, y1, lab) {
  addbox(x0, x1, y0, y1, fill = "#fbeec2", col = TAN$edge, lwd = 0.45, r = 0.3)
  addtxt((x0 + x1) / 2, (y0 + y1) / 2, lab, size = FS_HEAD, face = "bold", col = "#5a4a1e")
}
pw  <- (b3x[2] - b1x[1] - 0.7) / 2
p1x <- c(b1x[1] + 0.25, b1x[1] + 0.25 + pw); p2x <- c(p1x[2] + 0.7, b3x[2] - 0.25)
py2 <- appHeadY - LH_HEAD - 0.25 - PILL_H
py1 <- py2 - PILL_GAP - PILL_H
pill(p1x[1], p1x[2], py2, py2 + PILL_H, "Autonomous Analysis")
pill(p2x[1], p2x[2], py2, py2 + PILL_H, "Enhanced System Awareness")
pill(p1x[1], p1x[2], py1, py1 + PILL_H, "Optimal Policy Implementation")
pill(p2x[1], p2x[2], py1, py1 + PILL_H, "Adaptive Control")

## =============================================================================
## FEDERATED LEARNING inner panel (sizing already computed above)
## =============================================================================
addbox(RX[1] + 0.6, RX[2] - 0.6, fedBot, fedTop, fill = FED$fill, col = FED$edge, lwd = 0.65)
addtxt((RX[1] + RX[2]) / 2, fedTop - 0.35, "FEDERATED LEARNING\nPARADIGM",
       size = FS_HEAD, face = "bold", col = FED$acc, v = 1)

yc <- fedTop - fed_header_h - 0.35
for (i in seq_along(fed_sections)) {
  th <- sec_lines[i] * LH_BODY
  addtxt((RX[1] + RX[2]) / 2, yc, wrapt(fed_sections[[i]], SEC_WRAP), size = FS_BODY, col = FED$acc, v = 1)
  yc <- yc - th
  if (i < length(fed_sections)) {
    yc <- yc - DIV_GAP
    addseg(RX[1] + 1.6, RX[2] - 1.6, yc, yc, col = FED$edge, lwd = 0.4)
    yc <- yc - DIV_GAP
  }
}

## =============================================================================
## LEGEND (bottom right, aligned with OB1)
## =============================================================================
lx0 <- RX[1] + 1.2
ly1 <- OB1[2] - 1.3; ly2 <- (OB1[1] + OB1[2]) / 2; ly3 <- OB1[1] + 1.3
addseg(lx0, lx0 + 3.2, ly1, ly1, col = FLOW_DATA, lwd = 0.65, arw = ar1)
addtxt(lx0 + 3.8, ly1, "Data Flow", size = FS_BODY, h = 0, col = INK)
addseg(lx0, lx0 + 3.2, ly2, ly2, col = FLOW_TRAIN, lwd = 0.65, arw = ar1)
addtxt(lx0 + 3.8, ly2, wrapt("Model Training/\nPolicy Loop", 30), size = FS_BODY, h = 0, col = INK)
addseg(lx0, lx0 + 3.2, ly3, ly3, col = FLOW_PRIV, lwd = 0.65, lty = "22", arw = ar1)
addtxt(lx0 + 3.8, ly3, "Privacy\nPreservation", size = FS_BODY, h = 0, col = INK)

## =============================================================================
## ARROWS -- Input -> Core (blue, Data Flow)
## =============================================================================
ymidA <- (iy[2] + cy[1]) / 2
elbow(xB1, iy[2], xCA, cy[1], ymidA, FLOW_DATA, 0.65)
elbow(xB2, iy[2], c2x[1] + 4, cy[1], ymidA, FLOW_DATA, 0.65)
elbow(xB3, iy[2], c2x[2] - 4, cy[1], ymidA, FLOW_DATA, 0.65)

## =============================================================================
## ARROWS -- Core -> Advanced (green) + captions (captions drawn first)
## =============================================================================
ymidB <- ay[1] - 0.5
capY  <- cy[2] + 0.40 * (ay[1] - cy[2])

labelbreak(xA1, capY, "Traffic Signals,\nSmart Grids", w = 13, h = 2.1)
elbow(xCA, cy[2], xA1, ay[1], ymidB, FLOW_TRAIN, 0.65)

labelbreak(xA2, capY, "Ground-level,\nAerial platforms", w = 13, h = 2.1)
elbow(c2x[1] + 4, cy[2], xA2, ay[1], ymidB - 0.3, FLOW_TRAIN, 0.65)

labelbreak(xA3, capY, "Synthesis of\npatterns & inputs", w = 14, h = 2.1)
elbow(c2x[2] - 4, cy[2], xA3, ay[1], ymidB + 0.3, FLOW_TRAIN, 0.65)

elbow(CX0 - 1.0, cy[1], b1x[1], midY, midY, FLOW_TRAIN, 0.65)

## =============================================================================
## ARROWS -- Advanced -> Application (blue)
## =============================================================================
appY0 <- OB4[1] + PAD_INNER
ymidC <- (ay[2] + appY0) / 2
elbow(xA1, ay[2], xA1, appY0, ymidC, FLOW_DATA, 0.65)
elbow(xA2, ay[2], xA2, appY0, ymidC, FLOW_DATA, 0.65)

## =============================================================================
## ARROWS -- Privacy / Federated connections
## =============================================================================
addseg(b3x[2], RX[1], midY, midY, col = FLOW_PRIV, lwd = 0.65, lty = "22", arw = ar1)
addseg(c2x[2], RX[1], mean(cy), mean(cy), col = FLOW_TRAIN, lwd = 0.65, arw = ar2)

svcY <- min(fedTop + 0.5, appHeadY - 0.6)
addseg((RX[1] + RX[2]) / 2, (RX[1] + RX[2]) / 2, fedTop, svcY, col = FLOW_PRIV, lwd = 0.65, lty = "22")
addseg((RX[1] + RX[2]) / 2, b3x[2], svcY, svcY, col = FLOW_PRIV, lwd = 0.65, lty = "22", arw = ar1)

xr <- RX[1] - 1.0
addseg(RX[1], xr, fedBot + 0.35, fedBot + 0.35, col = FLOW_PRIV, lwd = 0.65, lty = "22")
addseg(xr, xr, fedBot + 0.35, mean(iy), col = FLOW_PRIV, lwd = 0.65, lty = "22")
addseg(xr, b3x[2], mean(iy), mean(iy), col = FLOW_PRIV, lwd = 0.65, lty = "22", arw = ar1)

## =============================================================================
## credit line + assemble
## =============================================================================
gv <- as.character(packageVersion("ggplot2"))
addtxt(RX[2], -0.9, paste0("Software: R ", getRversion(), " + ggplot2 ", gv, ".  Source: authors."),
       size = FS_CREDIT, col = "#9a9a9a", h = 1)

p <- Reduce(`+`, L, ggplot()) +
  coord_cartesian(xlim = c(0, 88), ylim = c(-1.6, TOPY), expand = FALSE) +
  theme_void()

ggsave("Figure_08.png", p, width = 15.0, height = 15.0 * (TOPY + 1.6) / 88,
       dpi = 600, bg = "white", limitsize = FALSE)
pdf_dev <- if (capabilities("cairo")) grDevices::cairo_pdf else grDevices::pdf
ggsave("Figure_08.pdf", p, width = 15.0, height = 15.0 * (TOPY + 1.6) / 88,
       bg = "white", device = pdf_dev, limitsize = FALSE)
cat("wrote Figure_08.png / .pdf\n")
cat("canvas:", 88, "x", TOPY + 1.6, "\n")
cat("row heights -- INPUT_H:", INPUT_H, " CORE_H:", CORE_H, " ADV_H:", ADV_H, " APP_H:", APP_H, "\n")
cat("fed content_h:", fed_content_h, " fedTop:", fedTop, " fedBot:", fedBot, "\n")
