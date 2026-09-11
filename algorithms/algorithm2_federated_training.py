"""
Algorithm 2 - Federated learning for distributed integrated urban model intelligence.

Runnable implementation of Algorithm 2 for the accompanying urban-informatics study: the full FedAvg training loop with R communication rounds, E local steps,
learning rate eta, and an early-stopping tolerance epsilon. Raw data stay on the
edge nodes; only model weights are exchanged.

Pseudocode -> code mapping (paper, Algorithm 2):
  Step 1  initialise w^0 on server                          -> federated_train (w0)
  Step 2  for r in 0..R-1: broadcast w^r; local E-step SGD  -> local_update()
          FedAvg: w^{r+1} = sum_k (|D_k|/|D|) w_k           -> fedavg()
          if ||w^{r+1}-w^r|| < eps: break                   -> early stop
  Step 3  return w^R                                        -> return

Run:
    python algorithm2_federated_training.py
Requires:
    numpy
"""
from __future__ import annotations

import argparse
import numpy as np


def local_update(w: np.ndarray, X: np.ndarray, y: np.ndarray,
                 eta: float, steps: int, batch: int, rng) -> np.ndarray:
    """E steps of mini-batch SGD on a local linear/MSE objective."""
    w = w.copy()
    n = len(y)
    for _ in range(steps):
        idx = rng.choice(n, size=min(batch, n), replace=False)   # sample B_k subset
        Xb, yb = X[idx], y[idx]
        grad = Xb.T @ (Xb @ w - yb) / len(yb)
        w -= eta * grad
    return w


def fedavg(node_weights, node_sizes) -> np.ndarray:
    """Size-weighted aggregation of local models."""
    total = float(sum(node_sizes))
    return sum((nk / total) * wk for nk, wk in zip(node_sizes, node_weights))


def federated_train(datasets, dim: int, rounds: int, local_steps: int,
                    eta: float, batch: int, eps: float, seed: int = 0):
    """Server-side FedAvg loop. Returns (final_weights, per_round_history)."""
    rng = np.random.default_rng(seed)
    w = np.zeros(dim)                                   # Step 1
    history = []
    for r in range(rounds):                             # Step 2
        local_w, sizes = [], []
        for (Xk, yk) in datasets:                       # each node in parallel
            local_w.append(local_update(w, Xk, yk, eta, local_steps, batch, rng))
            sizes.append(len(yk))
        w_new = fedavg(local_w, sizes)                  # FedAvg
        delta = float(np.linalg.norm(w_new - w))
        history.append(delta)
        w = w_new
        if delta < eps:                                 # early stop
            print(f"converged at round {r + 1} (||dw|| = {delta:.2e} < {eps})")
            break
    return w, history                                   # Step 3


def build_nodes(n_nodes: int, dim: int, n_per: int, seed: int = 7):
    rng = np.random.default_rng(seed)
    true_w = rng.standard_normal(dim)
    datasets = []
    for _ in range(n_nodes):
        Xk = rng.standard_normal((n_per, dim))
        yk = Xk @ true_w + rng.standard_normal(n_per) * 0.1
        datasets.append((Xk, yk))
    return datasets, true_w


def main() -> None:
    ap = argparse.ArgumentParser(description="Federated training (Algorithm 2).")
    ap.add_argument("--nodes", type=int, default=6, help="number of edge nodes K")
    ap.add_argument("--dim", type=int, default=8, help="feature dimension")
    ap.add_argument("--n", type=int, default=200, help="samples per node")
    ap.add_argument("--rounds", type=int, default=50, help="max rounds R")
    ap.add_argument("--local-steps", type=int, default=5, help="local steps E")
    ap.add_argument("--eta", type=float, default=0.05, help="learning rate")
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--eps", type=float, default=1e-4, help="early-stop tolerance")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    datasets, true_w = build_nodes(args.nodes, args.dim, args.n, seed=args.seed + 7)
    w, history = federated_train(
        datasets, dim=args.dim, rounds=args.rounds, local_steps=args.local_steps,
        eta=args.eta, batch=args.batch, eps=args.eps, seed=args.seed,
    )
    print(f"rounds run       : {len(history)}")
    print(f"recovery error   : {np.linalg.norm(w - true_w):.4f}")
    print(f"global w (first4): {w[:4].round(4)}")


if __name__ == "__main__":
    main()
