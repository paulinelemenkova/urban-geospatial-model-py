"""
Algorithm 1 - Real-time dynamic urban model state synchronization loop.

Runnable implementation of Algorithm 1 for the accompanying urban-informatics study. The loop ingests a sensor stream, maintains the dynamic urban model state with a
(vector) Kalman filter, screens each innovation for anomalies against a
threshold, and pushes the updated state to a model sink.

Pseudocode -> code mapping (paper, Algorithm 1):
  Step 1  initialise x_hat = 0, P = I, F = {}          -> StateSynchronizer.__init__
  Step 2  for each (t_k, z_k): predict / gain / update -> .step()
          anomaly A_k = ||z_k - H x_pred||^2, flag if > tau
          push x_hat_k to model M
  Step 3  return x_hat, F                              -> .run()

Run:
    python algorithm1_dt_state_sync.py
Requires:
    numpy
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import numpy as np


@dataclass
class StateSynchronizer:
    """Vector Kalman-filter dynamic urban model synchroniser with anomaly screening."""

    F: np.ndarray
    H: np.ndarray
    Q: np.ndarray
    R: np.ndarray
    tau: float
    x_hat: np.ndarray = field(init=False)
    P: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        n = self.F.shape[0]
        self.x_hat = np.zeros(n)          # Step 1: x_hat_0 <- 0
        self.P = np.eye(n)                # Step 1: P_0 <- I

    def step(self, z: np.ndarray):
        """One synchronisation cycle; returns (state, anomaly_score, is_anomaly)."""
        # Predict
        x_pred = self.F @ self.x_hat
        P_pred = self.F @ self.P @ self.F.T + self.Q
        # Innovation + anomaly score (before correction)
        innov = z - self.H @ x_pred
        score = float(innov @ innov)                       # ||z - H x_pred||^2
        # Gain + update
        S = self.H @ P_pred @ self.H.T + self.R
        K = P_pred @ self.H.T @ np.linalg.inv(S)
        self.x_hat = x_pred + K @ innov
        self.P = (np.eye(self.F.shape[0]) - K @ self.H) @ P_pred
        return self.x_hat.copy(), score, score > self.tau

    def run(self, stream):
        """Consume a stream of (t_k, z_k); return state history and flags."""
        states, flags = [], []
        for t_k, z_k in stream:
            x_hat, score, is_anom = self.step(np.asarray(z_k, dtype=float))
            states.append(x_hat)
            if is_anom:
                flags.append((t_k, score))    # add to anomaly set F; trigger alert
        return np.array(states), flags


def synthetic_stream(n: int, dim: int, seed: int = 0):
    """Random-walk ground truth + noise, with a few injected spikes (anomalies)."""
    rng = np.random.default_rng(seed)
    x = np.zeros(dim)
    for k in range(n):
        x = x + rng.normal(0, 0.05, dim)              # slow drift
        z = x + rng.normal(0, 0.1, dim)               # measurement noise
        if k in (n // 3, 2 * n // 3):                 # injected faults
            z = z + rng.normal(6, 1, dim)
        yield k, z


def main() -> None:
    ap = argparse.ArgumentParser(description="dynamic urban model state synchronization loop (Algorithm 1).")
    ap.add_argument("--n", type=int, default=300, help="stream length")
    ap.add_argument("--dim", type=int, default=3, help="state/observation dim")
    ap.add_argument("--tau", type=float, default=2.0, help="anomaly threshold")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    dim = args.dim
    sync = StateSynchronizer(
        F=np.eye(dim), H=np.eye(dim),
        Q=1e-3 * np.eye(dim), R=1e-1 * np.eye(dim),
        tau=args.tau,
    )
    states, flags = sync.run(synthetic_stream(args.n, dim, seed=args.seed))

    print(f"processed {len(states)} samples")
    print(f"final dynamic urban model state : {states[-1].round(3)}")
    print(f"anomalies flagged: {len(flags)} at steps {[t for t, _ in flags]}")


if __name__ == "__main__":
    main()
