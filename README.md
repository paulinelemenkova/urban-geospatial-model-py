# Urban sensing, simulation & monitoring — reference code

Python (with two R figure scripts) reference implementations that accompany a
study in **urban informatics** on the sensing, simulation, and monitoring of
city-scale systems. The code expands the compact excerpts printed in the study
into self-contained, runnable examples, and reproduces the study's figures.

The study builds a **city-scale digital representation** — an integrated urban
model kept continuously in step with live sensor feeds — and this repository
provides the underlying computational pieces. The examples cover the recurring
building blocks of an urban sensing-and-simulation workflow: fusing noisy sensor
streams into a single state estimate, forecasting demand from time series,
detecting anomalies in monitoring data, and training models across distributed
edge nodes without moving raw data.

Throughout the code and figures the same class of model is referred to with
several interchangeable terms — *urban digital model*, *virtual urban model*,
*dynamic urban model*, *integrated urban model*, and others (see **Keywords**
below).

These scripts are **self-contained reference implementations** of the proposed
architecture. Each is seeded for reproducibility, runs on synthetic data, and
prints a short result so the mechanism can be verified end to end. They expand
the compact code excerpts to a complete working form.

## Contents

| File | Item | What it does |
|------|------|--------------|
| `src/listing1_kalman_sensor_fusion.py` | Listing 1 | Scalar Kalman filter fusing a noisy IoT stream into one synchronised urban digital model state estimate. |
| `src/listing2_lstm_energy_forecasting.py` | Listing 2 | PyTorch LSTM for urban energy-demand forecasting (train/validation split). |
| `src/listing3_autoencoder_anomaly.py` | Listing 3 | Autoencoder anomaly detection via reconstruction error and a percentile threshold. |
| `src/listing4_fedavg_federated.py` | Listing 4 | FedAvg aggregation across simulated edge nodes (NumPy only). |
| `algorithms/algorithm1_state_sync.py` | Algorithm 1 | Real-time dynamic urban model state-synchronization loop: vector Kalman filter + anomaly screening. |
| `algorithms/algorithm2_federated_training.py` | Algorithm 2 | Full FedAvg training loop with R rounds, E local steps, and early stopping. |

Each file's docstring maps its code back to the corresponding equations in the
study's methods section.

## Figures

The `scripts/` folder holds the scripts that generate the study's figures. Each
is self-contained and writes a 300–600 dpi PNG plus a vector PDF alongside
itself; text is set in Nimbus Sans (any system sans-serif is used as a
fallback).

| File | Figure | Engine |
|------|--------|--------|
| `scripts/Figure_01_ecosystem_architecture.py` | Fig. 1 | Python / Matplotlib |
| `scripts/Figure_02_evolution_timeline.py` | Fig. 2 | Python / Matplotlib |
| `scripts/Figure_03_PRISMA.tex` | Fig. 3 | LaTeX (TikZ, standalone) |
| `scripts/Figure_04_application_domains.py` | Fig. 4 | Python / Matplotlib |
| `scripts/Figure_05_multilayer_architecture.py` | Fig. 5 | Python / Matplotlib |
| `scripts/Figure_06.R` | Fig. 6 | R / ggplot2 |
| `scripts/Figure_07_operational_stack.py` | Fig. 7 | Python / Matplotlib |
| `scripts/Figure_08.R` | Fig. 8 | R / ggplot2 |
| `scripts/Figure_09_comm_architecture.py` | Fig. 9 | Python / Matplotlib |

`scripts/qual-light-06.cpt` is the shared qualitative colour palette.
Dependencies: the Python figures need `matplotlib`; the R figures need
`ggplot2` (R ≥ 4.0); the PRISMA diagram compiles with any modern LaTeX
distribution.

```bash
python scripts/Figure_09_comm_architecture.py     # -> Figure_09.png + Figure_09.pdf
Rscript scripts/Figure_06.R                        # -> Figure_06.png + Figure_06.pdf
pdflatex scripts/Figure_03_PRISMA.tex              # -> Figure_03_PRISMA.pdf
```

## Requirements

- Python 3.9+
- `numpy` (all listings/algorithms), `torch` (only Listings 2 and 3)
- `matplotlib` (Python figure scripts); `ggplot2` on R ≥ 4.0 (R figure scripts)

```bash
pip install -r requirements.txt
```

## Usage

Run any script directly; all accept `--help` for parameters (sample counts,
seeds, learning rates, thresholds, etc.):

```bash
python src/listing1_kalman_sensor_fusion.py
python src/listing4_fedavg_federated.py --nodes 5 --rounds 20
python algorithms/algorithm1_state_sync.py --tau 2.0
python algorithms/algorithm2_federated_training.py --rounds 50 --eta 0.05
```

Run everything at once (PyTorch examples are skipped if `torch` is absent):

```bash
python run_all.py
```

## Notes on the implementations

- The scripts reproduce the logic of the compact code excerpts; where the
  compact form omitted glue code (data generation, training loop, thresholding),
  the minimum needed to run is added and documented.
- Listing 2 fixes one issue in the compact excerpt: the optimiser is now bound
  to the trained model's parameters (the excerpt passed a throwaway model
  instance to the optimiser), so the reported loss reflects actual training.
- Results depend on fixed random seeds and synthetic data; they demonstrate the
  computational mechanism, not empirical performance of any deployed system.

## Reproducibility of the review

This repository holds the **code** referenced by the study. The **review
apparatus** — full per-database search strings and dates, the PRISMA record log
(identification → screening → eligibility → inclusion), and the
extraction/classification tables behind the comparative tables and the PRISMA
flow diagram — accompanies it in the same archived release so the study
selection can be reproduced. The code and the review apparatus are archived
together in a single citable Zenodo release, mirrored on GitHub.

## Keywords

Repository topics / keywords:

`urban-informatics` · `urban-digital-model` · `virtual-urban-model` ·
`urban-information-model` · `urban-computational-model` · `urban-system-model` ·
`urban-spatial-model` · `urban-geospatial-model` · `urban-cyber-physical-model` ·
`virtual-city-model` · `city-scale-digital-representation` · `dynamic-urban-model` ·
`integrated-urban-model` · `simulation` · `monitoring` · `sensor-fusion` ·
`kalman-filter` · `anomaly-detection` · `federated-learning` · `python`

## License

Code released under the MIT License (see `LICENSE`).
