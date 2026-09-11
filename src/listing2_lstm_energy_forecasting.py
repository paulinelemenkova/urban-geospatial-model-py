"""
Listing 2 - LSTM network for urban energy-demand forecasting.

Expanded, runnable version of Listing 2 for the accompanying urban-informatics study. Implements the LSTM forecaster used by the AI/analytics layer for
spatial-temporal prediction (Section "Mathematical Foundations": LSTM cell
equations for the forget/input/output gates and cell/hidden state updates).

Note: the compact excerpt in the study is condensed for print. This version fixes a
subtlety so the example actually trains the model it evaluates: the optimiser is
attached to ``model.parameters()`` (in the paper snippet a throwaway
``LSTMForecaster()`` instance was passed to the optimiser), and a train/validation
split with per-epoch reporting is added.

Run:
    python listing2_lstm_energy_forecasting.py
Requires:
    torch, numpy
"""
from __future__ import annotations

import argparse
import numpy as np
import torch
import torch.nn as nn


class LSTMForecaster(nn.Module):
    """Minimal LSTM regressor: sequence -> next-step scalar demand."""

    def __init__(self, inp: int = 1, hid: int = 64, lay: int = 2, hor: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(inp, hid, lay, batch_first=True)
        self.fc = nn.Linear(hid, hor)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])          # last time step -> horizon


def make_windows(series: np.ndarray, window: int):
    """Turn a 1-D series into (samples, window, 1) inputs and next-step targets."""
    X = np.stack([series[i:i + window] for i in range(len(series) - window)])
    y = series[window:]
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(-1)
    return X, y


def synthetic_load(n: int, seed: int = 42) -> np.ndarray:
    """Diurnal-like load curve with noise, standardised for stable training."""
    rng = np.random.default_rng(seed)
    load = 50.0 + 20.0 * np.sin(np.linspace(0, 12 * np.pi, n)) + rng.standard_normal(n)
    return (load - load.mean()) / load.std()


def main() -> None:
    ap = argparse.ArgumentParser(description="LSTM energy forecasting (Listing 2).")
    ap.add_argument("--n", type=int, default=2000, help="series length")
    ap.add_argument("--window", type=int, default=24, help="input window (hours)")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    series = synthetic_load(args.n, seed=args.seed)
    X, y = make_windows(series, args.window)

    split = int(0.8 * len(X))
    X_tr, y_tr, X_va, y_va = X[:split], y[:split], X[split:], y[split:]

    model = LSTMForecaster()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)   # fixed: train THIS model
    loss_fn = nn.MSELoss()

    for epoch in range(1, args.epochs + 1):
        model.train()
        opt.zero_grad()
        loss = loss_fn(model(X_tr), y_tr)
        loss.backward()
        opt.step()
        if epoch % 5 == 0 or epoch == 1:
            model.eval()
            with torch.no_grad():
                val = loss_fn(model(X_va), y_va).item()
            print(f"epoch {epoch:3d} | train MSE {loss.item():.4f} | val MSE {val:.4f}")

    model.eval()
    with torch.no_grad():
        val_rmse = torch.sqrt(loss_fn(model(X_va), y_va)).item()
    print(f"final validation RMSE (standardised units): {val_rmse:.4f}")


if __name__ == "__main__":
    main()
