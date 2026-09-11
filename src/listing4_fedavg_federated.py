"""
Listing 4 - FedAvg aggregation for privacy-preserving distributed urban system model training.

Expanded, runnable version of Listing 4 for the accompanying urban-informatics study. Each simulated edge node trains a local linear model on data that never
leaves the node; the server averages the local weights, weighted by local
dataset size (Section "Mathematical Foundations": FedAvg aggregation). This is a
NumPy-only reference implementation of the federated update.

Run:
    python listing4_fedavg_federated.py
Requires:
    numpy
"""
from __future__ import annotations

import argparse
import numpy as np


def local_sgd(w: np.ndarray, X: np.ndarray, y: np.ndarray,
              lr: float = 0.01, steps: int = 5) -> np.ndarray:
    """Local gradient descent for a linear model with squared loss."""
    w = w.copy()
    for _ in range(steps):
        grad = X.T @ (X @ w - y) / len(y)
        w -= lr * grad
    return w


def fedavg(global_w: np.ndarray, node_weights, node_sizes) -> np.ndarray:
    """Size-weighted average of local models (the FedAvg step)."""
    total = float(sum(node_sizes))
    return sum((nk / total) * wk for nk, wk in zip(node_sizes, node_weights))


def main() -> None:
    ap = argparse.ArgumentParser(description="FedAvg federated learning (Listing 4).")
    ap.add_argument("--nodes", type=int, default=5, help="number of edge nodes K")
    ap.add_argument("--dim", type=int, default=8, help="feature dimension d")
    ap.add_argument("--n", type=int, default=100, help="samples per node")
    ap.add_argument("--rounds", type=int, default=10, help="communication rounds")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    true_w = np.ones(args.dim)                       # shared ground truth

    # Fixed per-node datasets (kept local; only weights are shared).
    datasets = []
    for _ in range(args.nodes):
        Xk = rng.standard_normal((args.n, args.dim))
        yk = Xk @ true_w + rng.standard_normal(args.n) * 0.1
        datasets.append((Xk, yk))

    global_w = np.zeros(args.dim)
    for r in range(1, args.rounds + 1):
        weights, sizes = [], []
        for (Xk, yk) in datasets:
            weights.append(local_sgd(global_w, Xk, yk))
            sizes.append(len(yk))
        global_w = fedavg(global_w, weights, sizes)
        err = float(np.linalg.norm(global_w - true_w))
        if r % 2 == 0 or r == 1:
            print(f"round {r:2d} | ||w - w*|| = {err:.4f}")

    print("global weights (first 4):", global_w[:4].round(4))
    print("recovery error          :", round(float(np.linalg.norm(global_w - true_w)), 4))


if __name__ == "__main__":
    main()
