"""
Listing 3 - Autoencoder anomaly detection for urban cyber-physical model sensor streams.

Expanded, runnable version of Listing 3 for the accompanying urban-informatics study. A small autoencoder learns the manifold of nominal sensor vectors; the
reconstruction error is the anomaly score and a high percentile of the training
error is used as the decision threshold (Section "Mathematical Foundations":
anomaly detection via reconstruction error).

Run:
    python listing3_autoencoder_anomaly.py
Requires:
    torch, numpy
"""
from __future__ import annotations

import argparse
import numpy as np
import torch
import torch.nn as nn


class AE(nn.Module):
    """Undercomplete autoencoder: d -> 8 -> lat -> 8 -> d."""

    def __init__(self, d: int = 16, lat: int = 4):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(d, 8), nn.ReLU(), nn.Linear(8, lat))
        self.dec = nn.Sequential(nn.Linear(lat, 8), nn.ReLU(), nn.Linear(8, d))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dec(self.enc(x))


def reconstruction_error(model: nn.Module, x: torch.Tensor) -> torch.Tensor:
    with torch.no_grad():
        return ((x - model(x)) ** 2).mean(dim=1)


def train(model: nn.Module, X: torch.Tensor, epochs: int, lr: float = 1e-3) -> None:
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    for epoch in range(1, epochs + 1):
        opt.zero_grad()
        loss = loss_fn(model(X), X)
        loss.backward()
        opt.step()
        if epoch % 5 == 0 or epoch == 1:
            print(f"epoch {epoch:3d} | train MSE {loss.item():.4f}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Autoencoder anomaly detection (Listing 3).")
    ap.add_argument("--d", type=int, default=16, help="sensor vector dimension")
    ap.add_argument("--n", type=int, default=1000, help="nominal training samples")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--pct", type=float, default=99.0, help="threshold percentile")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)

    # Nominal data: unit-Gaussian sensor vectors.
    X = torch.tensor(rng.standard_normal((args.n, args.d)), dtype=torch.float32)

    model = AE(d=args.d)
    train(model, X, epochs=args.epochs)

    # Threshold from the training reconstruction-error distribution.
    err = reconstruction_error(model, X).numpy()
    tau = float(np.percentile(err, args.pct))
    print(f"anomaly threshold (p{args.pct:.0f}) = {tau:.4f}")

    # Evaluate one nominal and one clearly out-of-distribution sample.
    for label, scale in [("nominal", 1.0), ("faulty", 5.0)]:
        test = torch.tensor(rng.standard_normal((1, args.d)) * scale, dtype=torch.float32)
        score = float(reconstruction_error(model, test).item())
        verdict = "Anomaly" if score > tau else "Normal"
        print(f"{label:8s} sample -> {verdict:7s} (score={score:.3f})")


if __name__ == "__main__":
    main()
