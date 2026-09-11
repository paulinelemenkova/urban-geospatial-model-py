#!/usr/bin/env python3
"""Run every listing and algorithm in sequence.

PyTorch examples (Listings 2 and 3) are skipped with a notice if torch is not
installed, so the NumPy-only examples still run on a minimal environment.
"""
import importlib.util
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS = [
    ("Listing 1  Kalman sensor fusion",        "src/listing1_kalman_sensor_fusion.py",   False),
    ("Listing 2  LSTM energy forecasting",     "src/listing2_lstm_energy_forecasting.py", True),
    ("Listing 3  Autoencoder anomaly",         "src/listing3_autoencoder_anomaly.py",     True),
    ("Listing 4  FedAvg federated learning",   "src/listing4_fedavg_federated.py",        False),
    ("Algorithm 1  dynamic urban model state synchronization",  "algorithms/algorithm1_state_sync.py",  False),
    ("Algorithm 2  Federated training",        "algorithms/algorithm2_federated_training.py", False),
]

has_torch = importlib.util.find_spec("torch") is not None

for title, rel, needs_torch in SCRIPTS:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    if needs_torch and not has_torch:
        print("[skipped] requires PyTorch (pip install torch)")
        continue
    sys.argv = [rel]
    try:
        runpy.run_path(str(ROOT / rel), run_name="__main__")
    except SystemExit:
        pass
