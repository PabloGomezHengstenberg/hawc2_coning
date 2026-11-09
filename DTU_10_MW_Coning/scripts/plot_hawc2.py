
from pathlib import Path
import re

import h5py
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Configuration
# ============================================================

RESULT_FILE = Path("res/DTU_10MW_RWT_cone_hawc2s_8wsp_0.0.hdf5")
DT = 0.01  # HAWC2 output sampling interval [s]


# ============================================================
# Load HAWC2 results
# ============================================================

def load_hawc2_hdf5(path, dt=DT):
    """Load HAWC2 HDF5 results and channel metadata."""

    with h5py.File(path, "r") as h5:

        names = [
            v.decode().strip() if isinstance(v, bytes) else str(v)
            for v in h5["attribute_names"][:]
        ]

        descriptions = [
            v.decode().strip() if isinstance(v, bytes) else str(v)
            for v in h5["attribute_descriptions"][:]
        ]

        units = [
            v.decode().strip() if isinstance(v, bytes) else str(v)
            for v in h5["attribute_units"][:]
        ]

        block_keys = sorted(
            (k for k in h5 if re.fullmatch(r"block\d+", k)),
            key=lambda k: int(k[5:]),
        )

        if not block_keys:
            raise ValueError("No HAWC2 data blocks found.")

        data = np.vstack([
            h5[k]["data"][:].astype(float)
            * h5[k]["gains"][:]
            + h5[k]["offsets"][:]
            for k in block_keys
        ])

    time = np.arange(len(data)) * dt

    return {
        "time": time,
        "data": data,
        "names": names,
        "descriptions": descriptions,
        "units": units,
    }


# ============================================================
# Extract signals
# ============================================================

def get_signal(result, description):
    """Extract a channel by matching its description."""

    matches = [
        i for i, d in enumerate(result["descriptions"])
        if description.lower() in d.lower()
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected one channel for '{description}', "
            f"found {len(matches)}."
        )

    i = matches[0]

    return result["data"][:, i], result["units"][i]


# ============================================================
# Plot results
# ============================================================

def plot_signal(result, description, title=None):
    """Plot one HAWC2 output channel against time."""

    signal, unit = get_signal(result, description)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(result["time"], signal, linewidth=1)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel(f"{description} [{unit}]")
    ax.set_title(title or description)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    plt.show()

    return fig, ax


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    result = load_hawc2_hdf5(RESULT_FILE)

    for i, (name, description, unit) in enumerate(
    zip(result["names"], result["descriptions"], result["units"])
    ):
        print(f"{i}: {name} | {description} [{unit}]")

    plot_signal(result, "Rotor speed")
    plot_signal(result, "Aero rotor power")
    plot_signal(result, "pitch1 angle")
