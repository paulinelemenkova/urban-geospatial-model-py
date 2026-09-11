#!/usr/bin/env Rscript
# Figure 6 - IoT-to-urban-system-model data pipeline.
#
# Three-stage pipeline for the accompanying urban-informatics study:
#   1) Data & IoT Foundation      (collect, integrate & store)
#   2) Big Data Processing & Analytics (process, analyze & learn)
#   3) urban system model construction & operation (model, simulate & synchronise)
# plus four right-hand annotation notes and a closed-loop feedback path from
# stage 3 back into stage 3's geospatial modelling layer.
#
# Run:    Rscript Figure_06.R
# Out:    Figure_06.png (300 dpi), Figure_06.pdf
# Needs:  ggplot2 (R >= 4.0). Font: Nimbus Sans (falls back to system sans).

suppressMessages({library(ggplot2); library(grid)})

FAM <- "Nimbus Sans"                                   # Arial-like free font
ar  <- arrow(length = unit(0.16, "cm"), type = "closed")

## ---- palette --------------------------------------------------------------
S1 <- list(band = "#eaf0f8", edge = "#3f6395", acc = "#284a72", badge = "#3f6395")  # blue
S2 <- list(band = "#e7f3ef", edge = "#2f8f7c", acc = "#215d51", badge = "#2f8f7c")  # teal
S3 <- list(band = "#efeaf6", edge = "#6a4f9c", acc = "#4a3878", badge = "#6a4f9c")  # purple
INK  <- "#2b2b2b"; GREY <- "#5f5f5f"; FLOW <- "#3a3a3a"

## ---- rounded-rectangle polygon helper -------------------------------------
rrect <- function(xmin, xmax, ymin, ymax, r = 0.9, n = 8) {
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
addbox <- function(x0, x1, y0, y1, fill = "white", col = INK, lwd = 0.4, lty = "solid", r = 0.9)
  L[[length(L) + 1]] <<- geom_polygon(data = rrect(x0, x1, y0, y1, r), aes(x, y),
      fill = fill, colour = col, linewidth = lwd, linetype = lty)
addtxt <- function(x, y, lab, size = 2.75, face = "plain", col = INK, h = 0.5, v = 0.5, ang = 0)
  L[[length(L) + 1]] <<- annotate("text", x = x, y = y, label = lab, size = size, fontface = face,
      colour = col, hjust = h, vjust = v, family = FAM, lineheight = 0.95, angle = ang)
addseg <- function(x, xe, y, ye, col = FLOW, lwd = 0.5, lty = "solid", arw = TRUE)
  L[[length(L) + 1]] <<- annotate("segment", x = x, xend = xe, y = y, yend = ye, colour = col,
      linewidth = lwd, linetype = lty, arrow = if (arw) ar else NULL)

## ---- content box: header + bullet items (+ optional caption) --------------
cbox <- function(x0, x1, y0, y1, header, items, S, fill = "white", cap = NULL) {
  addbox(x0, x1, y0, y1, fill = fill, col = S$edge, lwd = 0.45)
  addtxt((x0 + x1) / 2, y1 - 1.5, header, size = 3.0, face = "bold", col = S$acc)
  n <- length(items); top <- y1 - 3.5; bot <- y0 + if (!is.null(cap)) 3.0 else 1.1
  ys <- if (n == 1) (top + bot) / 2 else top - (0:(n - 1)) * ((top - bot) / (n - 1))
  for (i in seq_len(n)) addtxt(x0 + 1.3, ys[i], paste0("\u2022 ", items[i]), size = 2.7, col = INK, h = 0)
  if (!is.null(cap)) addtxt((x0 + x1) / 2, y0 + 1.4, cap, size = 2.45, face = "italic", col = GREY)
}

## ---- stage panel (numbered badge + title + subtitle) -----------------------
stage <- function(x0, x1, S, num, title, sub) {
  addbox(x0, x1, 4, 60.5, fill = S$band, col = S$edge, lwd = 0.6, r = 1.3)
  addbox(x0 + 0.8, x0 + 3.4, 57.4, 60.0, fill = S$badge, col = S$badge, lwd = 0, r = 0.6)
  addtxt(x0 + 2.1, 58.7, num, size = 3.8, face = "bold", col = "white")
  addtxt(x0 + 4.0, 59.0, title, size = 3.5, face = "bold", col = S$acc, h = 0)
  addtxt(x0 + 4.0, 57.0, sub, size = 2.7, face = "italic", col = GREY, h = 0)
}

X1 <- c(1.2, 26.2); X2 <- c(27.7, 52.7); X3 <- c(54.2, 79.2)      # stage columns
YB <- c(43.5, 55.0, 31.0, 42.0, 18.5, 29.5, 5.2, 17.0)            # 4 box slots (y0,y1) x 4
slot <- function(i) YB[c(2 * i - 1, 2 * i)]

stage(X1[1], X1[2], S1, "1", "Data & IoT Foundation", "Collect, integrate & store")
stage(X2[1], X2[2], S2, "2", "Big Data Processing & Analytics", "Process, analyze & learn")
stage(X3[1], X3[2], S3, "3", "urban system model construction & operation", "Model, simulate & synchronise")

## ---- Stage 1 boxes ----
s <- slot(1); cbox(X1[1] + 0.9, X1[2] - 0.9, s[1], s[2], "Heterogeneous IoT data sources",
  c("Geological monitoring sensors", "Smart utility meters (energy, gas, water)",
    "GPS-enabled vehicles & mobile assets", "LiDAR scanners", "Air-quality sensors",
    "Smart cameras & vision sensors", "Satellite remote sensing"), S1)
s <- slot(2); cbox(X1[1] + 0.9, X1[2] - 0.9, s[1], s[2], "Data ingestion",
  c("Gateways & IoT protocols", "LPWAN \u00b7 5G \u00b7 Wi-Fi \u00b7 MQTT"), S1)
s <- slot(3); cbox(X1[1] + 0.9, X1[2] - 0.9, s[1], s[2], "Raw IoT data lake",
  c("Distributed storage"), S1)
s <- slot(4); cbox(X1[1] + 0.9, X1[2] - 0.9, s[1], s[2], "Edge\u2013cloud computing layer",
  c("Edge devices (filter \u00b7 compress \u00b7 detect)", "Edge servers (low-latency inference)",
    "Cloud infrastructure (storage & compute)"), S1,
  cap = "Workload distribution to minimise latency")

## ---- Stage 2 boxes ----
s <- slot(1); cbox(X2[1] + 0.9, X2[2] - 0.9, s[1], s[2], "Big data platform (Apache Spark)",
  c("Distributed processing", "In-memory analytics", "Stream processing", "Fault tolerant"),
  S2, fill = "#dcefe9")
s <- slot(2); cbox(X2[1] + 0.9, X2[2] - 0.9, s[1], s[2], "Data management layer",
  c("Structured data", "Time-series data", "Spatial data", "Unstructured data"), S2)
s <- slot(3); cbox(X2[1] + 0.9, X2[2] - 0.9, s[1], s[2], "Analytics & machine learning",
  c("Feature engineering", "Predictive modelling", "Anomaly detection", "Deep learning"), S2)
s <- slot(4); cbox(X2[1] + 0.9, X2[2] - 0.9, s[1], s[2], "Knowledge & model repository",
  c("Trained models", "Rules & knowledge", "Geospatial indexes", "Metadata catalog"), S2)

## ---- Stage 3 boxes ----
s <- slot(1); cbox(X3[1] + 0.9, X3[2] - 0.9, s[1], s[2], "Geospatial modeling layer",
  c("GIS databases", "3D BIM models", "CityGML city objects", "Digital elevation models (DEM)",
    "InSAR-derived deformation maps"), S3)
s <- slot(2); cbox(X3[1] + 0.9, X3[2] - 0.9, s[1], s[2], "urban system modeling layer",
  c("Physics-based simulation models", "Agent-based systems", "Finite element analysis",
    "Continuously updated from IoT data"), S3)
s <- slot(3); cbox(X3[1] + 0.9, X3[2] - 0.9, s[1], s[2], "Virtual city model platform",
  c("Real-time visualization", "Scenario simulation", "Decision support",
    "Alerts & notifications", "API & service interfaces"), S3)
s <- slot(4); cbox(X3[1] + 0.9, X3[2] - 0.9, s[1], s[2], "Applications & use cases",
  c("Early warning (geohazards)", "Urban traffic management", "Energy & utilities optimization",
    "Environmental monitoring", "Urban planning & resilience"), S3, fill = "#e7dff2")

## ---- within-stage vertical flow arrows ----
for (X in list(X1, X2, X3)) {
  cx <- mean(X)
  for (g in list(c(43.5, 42.0), c(31.0, 29.5), c(18.5, 17.0)))
    addseg(cx, cx, g[1], g[2], col = FLOW, lwd = 0.5)
}

## ---- inter-stage horizontal arrows ----
addseg(X1[2], X2[1], 31, 31, col = FLOW, lwd = 0.7)
addseg(X2[2], X3[1], 31, 31, col = FLOW, lwd = 0.7)

## ---- stage-1 workload feedback (dashed, up left gutter) ----
addseg(X1[1] + 0.3, X1[1] + 0.3, 7.5, 49.0, col = S1$edge, lwd = 0.4, lty = "22")

## ---- stage-3 closed-loop feedback (dashed elbow, vertical label) ----
gx <- 82.4
addseg(X3[2] - 0.9, gx, 24.0, 24.0, col = S3$edge, lwd = 0.45, lty = "22", arw = FALSE)
addseg(gx, gx, 24.0, 49.0, col = S3$edge, lwd = 0.45, lty = "22", arw = FALSE)
addseg(gx, X3[2] - 0.9, 49.0, 49.0, col = S3$edge, lwd = 0.45, lty = "22")
addtxt(gx + 1.0, 36.5, "closed-loop feedback", size = 2.35, face = "italic",
       col = S3$edge, h = 0.5, v = 0.5, ang = 90)

## ---- right annotation column (dashed notes) ----
NX <- c(84.6, 99.5)
wrapt <- function(s, w = 34) paste(strwrap(s, width = w), collapse = "\n")
note <- function(y0, y1, S, title, body) {
  addbox(NX[1], NX[2], y0, y1, fill = "white", col = S$edge, lwd = 0.4, lty = "22", r = 1.0)
  addtxt(NX[1] + 1.0, y1 - 1.6, title, size = 2.95, face = "bold", col = S$acc, h = 0)
  addtxt(NX[1] + 1.0, y1 - 3.6, wrapt(body), size = 2.5, col = GREY, h = 0, v = 1)
}
note(46.0, 59.5, S1, "Edge\u2013Cloud Computing Layer",
  "Distributes computational workloads to minimise latency and improve real-time responsiveness; edge intelligence is critical for geological early-warning and autonomous urban traffic management [28, 22].")
note(31.5, 44.5, S3, "Geospatial Modeling Layer",
  "Provides the spatial reference framework integrating GIS databases, 3D BIM models, CityGML city objects, digital elevation models (DEM), and InSAR-derived surface deformation maps [143, 130].")
note(17.0, 30.0, S3, "urban system modeling layer",
  "Instantiates physics-based simulation models, agent-based systems, and finite element analyses continuously updated from real-world sensor inputs to keep physical and virtual environments synchronised.")
note(4.0, 15.5, S2, "Big Data & Analytics",
  "Using Apache Spark and Python, massive heterogeneous IoT data are processed, analysed, and learned to extract insights and train models that drive the urban system model.")

## ---- credit line ----
gv <- as.character(packageVersion("ggplot2"))
addtxt(99.5, 1.4, paste0("Software: R ", getRversion(), " + ggplot2 ", gv, ".  Source: authors."),
       size = 2.4, col = "#9a9a9a", h = 1)

## ---- assemble and export ----
p <- Reduce(`+`, L, ggplot()) +
  coord_cartesian(xlim = c(0, 101), ylim = c(0, 62), expand = FALSE) +
  theme_void()

ggsave("Figure_06.png", p, width = 13.9, height = 8.5, dpi = 300, bg = "white", limitsize = FALSE)
ggsave("Figure_06.pdf", p, width = 13.9, height = 8.5, bg = "white", device = cairo_pdf, limitsize = FALSE)
cat("wrote Figure_06.png / .pdf\n")
