"""
Listing 1 - IoT sensor fusion with a Kalman filter for urban digital model state estimation.

Expanded, runnable version of Listing 1 from the accompanying urban-informatics
study (manuscript under review).

Implements the scalar discrete Kalman filter used by the sensing layer to fuse a
noisy IoT stream into a single synchronised urban digital model state estimate
(Section "Mathematical Foundations": urban digital model state synchronisation and the Kalman
predict/gain/update equations).

Run:
    python listing1_kalman_sensor_fusion.py
Requires:
    numpy
"""
from __future__ import annotations

import argparse
import numpy as np


def kalman_step(z: float, x: float, P: float,
                F: float, H: float, Q: float, R: float) -> tuple[float, float]:
    """One predict/update cycle of the scalar Kalman filter.

    Returns the updated state estimate and its error covariance.
    """
    # Predict
    x_pred = F * x
    P_pred = F * P * F + Q
    # Update
    K = P_pred * H / (H * P_pred * H + R)          # Kalman gain
    x_upd = x_pred + K * (z - H * x_pred)          # innovation-corrected state
    P_upd = (1.0 - K * H) * P_pred
    return x_upd, P_upd


def run_filter(observations: np.ndarray,
               F: float = 1.0, H: float = 1.0, Q: float = 1e-4, R: float = 0.1,
               x0: float = 20.0, P0: float = 1.0) -> np.ndarray:
    """Run the Kalman filter over a stream of observations.

    Returns the array of successive state estimates (one per observation).
    """
    x_est, P_est = x0, P0
    estimates = np.empty(len(observations), dtype=float)
    for k, z in enumerate(observations):
        x_est, P_est = kalman_step(z, x_est, P_est, F, H, Q, R)
        estimates[k] = x_est
    return estimates


def main() -> None:
    ap = argparse.ArgumentParser(description="Kalman sensor fusion (Listing 1).")
    ap.add_argument("--n", type=int, default=50, help="number of samples")
    ap.add_argument("--true", type=float, default=22.0, help="true temperature")
    ap.add_argument("--R", type=float, default=0.1, help="measurement noise var")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    observations = args.true + rng.normal(0.0, np.sqrt(args.R), args.n)

    estimates = run_filter(observations, R=args.R)
    final = estimates[-1]
    rmse_raw = float(np.sqrt(np.mean((observations - args.true) ** 2)))
    rmse_est = float(np.sqrt(np.mean((estimates - args.true) ** 2)))

    print(f"urban digital model state estimate : {final:.4f} deg C   (true = {args.true})")
    print(f"RMSE raw sensors  : {rmse_raw:.4f}")
    print(f"RMSE filtered urban digital model  : {rmse_est:.4f}  "
          f"({100 * (1 - rmse_est / rmse_raw):.1f}% reduction)")


if __name__ == "__main__":
    main()
