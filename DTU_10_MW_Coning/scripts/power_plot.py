import numpy as np

from pathlib import Path
import matplotlib.pyplot as plt
from lacbox.io import load_pwr

ROOT = Path.cwd()


# ============================================================
# LOAD HAWC2S CONING CASES
# ============================================================

cone_angles = [0.0, 0.5, 1.0, 1.5, 2.0]

results = {}

for cone in cone_angles:

    pwr_path = (
        ROOT
        / "res_hawc2s"
        / f"DTU_10MW_RWT_cone_hawc2s_hawc2s_{cone}.pwr"
    )

    pwr = load_pwr(pwr_path)

    results[cone] = {
        "wsp":    pwr["V_ms"],
        "pitch":  pwr["Pitch_deg"],
        "rot":    pwr["Speed_rpm"],
        "power":  pwr["P_kW"],
        "thrust": pwr["T_kN"],
        "cp":     pwr["Cp"],
        "ct":     pwr["Ct"],
    }


# ============================================================
# FIGURE 1: AERODYNAMIC PERFORMANCE
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(11, 8), sharex=True)

for cone, data in results.items():

    label = f"{cone:g}°"

    # Power
    axs[0, 0].plot(
        data["wsp"],
        data["power"] / 1e3,
        label=label
    )

    # Cp
    axs[0, 1].plot(
        data["wsp"],
        data["cp"]
    )

    # Thrust
    axs[1, 0].plot(
        data["wsp"],
        data["thrust"] / 1e3
    )

    # Ct
    axs[1, 1].plot(
        data["wsp"],
        data["ct"]
    )


# ------------------------------------------------------------
# Plot formatting
# ------------------------------------------------------------

axs[0, 0].set_ylabel("Aerodynamic Power [MW]")
axs[0, 0].set_title("Aerodynamic Power")
axs[0, 0].grid(True)
axs[0, 0].legend(title="Cone angle")

axs[0, 1].set_ylabel("Cp [-]")
axs[0, 1].set_title("Power Coefficient")
axs[0, 1].grid(True)

axs[1, 0].set_xlabel("Wind Speed [m/s]")
axs[1, 0].set_ylabel("Aerodynamic Thrust [MN]")
axs[1, 0].set_title("Aerodynamic Thrust")
axs[1, 0].grid(True)

axs[1, 1].set_xlabel("Wind Speed [m/s]")
axs[1, 1].set_ylabel("Ct [-]")
axs[1, 1].set_title("Thrust Coefficient")
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()


# ============================================================
# FIGURE 2: OPERATING CONDITIONS
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))

for cone, data in results.items():

    label = f"{cone:g}°"

    # Rotor speed
    axs[0].plot(
        data["wsp"],
        data["rot"],
        label=label
    )

    # Pitch
    axs[1].plot(
        data["wsp"],
        data["pitch"],
        label=label
    )


axs[0].set_xlabel("Wind Speed [m/s]")
axs[0].set_ylabel("Rotor Speed [rpm]")
axs[0].set_title("Rotor Speed")
axs[0].grid(True)
axs[0].legend(title="Cone angle")

axs[1].set_xlabel("Wind Speed [m/s]")
axs[1].set_ylabel("Pitch Angle [deg]")
axs[1].set_title("Pitch Angle")
axs[1].grid(True)

plt.tight_layout()
plt.show()



# ============================================================
# LOAD HAWC2S CONING CASES --- 8M/S WIND SPEED
# ============================================================

HOURS_YEAR = 8760

results_1wsp = {}

for cone in cone_angles:

    pwr_path = (
        ROOT
        / "res_hawc2s"
        / f"DTU_10MW_RWT_cone_hawc2s_1wsp_{cone}.pwr"
    )

    pwr = load_pwr(pwr_path)

    results_1wsp[cone] = {
        "wsp":    pwr["V_ms"],
        "pitch":  pwr["Pitch_deg"],
        "rot":    pwr["Speed_rpm"],
        "power":  pwr["P_kW"],
        "thrust": pwr["T_kN"],
        "cp":     pwr["Cp"],
        "ct":     pwr["Ct"],
        "flap_m": pwr["Flap_M_kNm"],   # check exact key
        "edge_m": pwr["Edge_M_kNm"],   # check exact key
        "aep":    pwr["P_kW"] * HOURS_YEAR,
    }

# ============================================================
# CALCULATE AEP LOSS, THRUST REDUCTION AND FLAP MOMENT REDUCTION
# ============================================================

# Reference case: 0° additional coning
aep_ref = results_1wsp[0.0]["aep"]
thrust_ref = results_1wsp[0.0]["thrust"]
flap_m_ref = np.abs(results_1wsp[0.0]["flap_m"])

for cone in cone_angles:

    # AEP loss [%]
    results_1wsp[cone]["aep_loss"] = (
        (aep_ref - results_1wsp[cone]["aep"])
        / aep_ref * 100
    )

    # Thrust reduction [%]
    results_1wsp[cone]["thrust_reduction"] = (
        (thrust_ref - results_1wsp[cone]["thrust"])
        / thrust_ref * 100
    )

    # Flapwise root bending moment reduction [%]
    results_1wsp[cone]["flap_m_reduction"] = (
        (flap_m_ref - np.abs(results_1wsp[cone]["flap_m"]))
        / flap_m_ref * 100
    )


# ============================================================
# PREPARE PLOTTING DATA
# ============================================================

aep_loss = [
    float(np.squeeze(results_1wsp[cone]["aep_loss"]))
    for cone in cone_angles
]

thrust_reduction = [
    float(np.squeeze(results_1wsp[cone]["thrust_reduction"]))
    for cone in cone_angles
]

flap_m_reduction = [
    float(np.squeeze(results_1wsp[cone]["flap_m_reduction"]))
    for cone in cone_angles
]


# ============================================================
# PLOTS
# ============================================================

fig, axs = plt.subplots(1, 3, figsize=(16, 5))


# ------------------------------------------------------------
# AEP LOSS
# ------------------------------------------------------------

bars = axs[0].bar(
    cone_angles,
    aep_loss,
    width=0.35
)

for bar, loss in zip(bars, aep_loss):
    axs[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{loss:.2f}%",
        ha="center",
        va="bottom"
    )

axs[0].set_xlabel("Additional Cone Angle [deg]")
axs[0].set_ylabel("AEP Loss [%]")
axs[0].set_title("AEP Loss due to Coning")
axs[0].set_xticks(cone_angles)
axs[0].grid(axis="y", alpha=0.3)
axs[0].set_ylim(0, max(aep_loss) * 1.15)


# ------------------------------------------------------------
# THRUST REDUCTION
# ------------------------------------------------------------

bars = axs[1].bar(
    cone_angles,
    thrust_reduction,
    width=0.35
)

for bar, reduction in zip(bars, thrust_reduction):
    axs[1].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{reduction:.2f}%",
        ha="center",
        va="bottom"
    )

axs[1].set_xlabel("Additional Cone Angle [deg]")
axs[1].set_ylabel("Thrust Reduction [%]")
axs[1].set_title("Thrust Reduction due to Coning")
axs[1].set_xticks(cone_angles)
axs[1].grid(axis="y", alpha=0.3)
axs[1].set_ylim(0, max(thrust_reduction) * 1.15)


# ------------------------------------------------------------
# FLAPWISE ROOT BENDING MOMENT REDUCTION
# ------------------------------------------------------------

bars = axs[2].bar(
    cone_angles,
    flap_m_reduction,
    width=0.35
)

for bar, reduction in zip(bars, flap_m_reduction):
    axs[2].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{reduction:.2f}%",
        ha="center",
        va="bottom"
    )

axs[2].set_xlabel("Additional Cone Angle [deg]")
axs[2].set_ylabel("Flapwise Root Moment Reduction [%]")
axs[2].set_title("Flapwise Root Moment Reduction due to Coning")
axs[2].set_xticks(cone_angles)
axs[2].grid(axis="y", alpha=0.3)
axs[2].set_ylim(0, max(flap_m_reduction) * 1.15)


plt.tight_layout()
plt.show()