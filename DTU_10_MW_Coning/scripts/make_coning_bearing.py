import numpy as np
from pathlib import Path
from lacbox.io import save_st



ROOT = Path(__file__).parents[1]  # root is main repo level, one level up


# ============================================================
# CREATE ROOT EXTENDER ST
# ============================================================

def create_bearing_st():
    """
    Create HAWC2 ST data for the selected root-extender material.

    Subset 1 = flexible
    Subset 2 = artificially stiff

    The geometry and mass properties are identical in both subsets.
    Only E and G are artificially increased in the stiff subset.
    """
    R_bearing = 1.000000000000000E-007 # Negligible lenght to not affect the results 

    # ========================================================
    # CALCULATE CROSS-SECTIONAL PROPERTIES
    # ========================================================

    

    # Two stations: beginning and end of extender
    s = np.array([0.0, R_bearing])

    # --------------------------------------------------------
    # CONSTANT SECTION PROPERTIES
    # --------------------------------------------------------

    m = np.zeros(2)

    A = np.zeros(2)

    I_x = np.zeros(2)
    I_y = np.zeros(2)
    I_p = np.zeros(2)

    ri_x = np.zeros(2)
    ri_y = np.zeros(2)

    # Symmetric circular cross-section
    x_cg = np.zeros(2)
    y_cg = np.zeros(2)

    x_sh = np.zeros(2)
    y_sh = np.zeros(2)

    x_e = np.zeros(2)
    y_e = np.zeros(2)

    pitch = np.zeros(2)

    # Timoshenko shear factors
    # Assumed value, not calculated by HAWC2
    k_x = np.full(2, 0.5)
    k_y = np.full(2, 0.5)

    # ========================================================
    # FLEXIBLE SUBSET
    # ========================================================

    flexible = {
        "s": s,

        "m": m,

        "x_cg": x_cg,
        "y_cg": y_cg,

        "ri_x": ri_x,
        "ri_y": ri_y,

        "x_sh": x_sh,
        "y_sh": y_sh,

        "E": np.full(2, 2.10e16),
        "G": np.full(2, 8.08e15),

        "I_x": I_x,
        "I_y": I_y,
        "I_p": I_p,

        "k_x": k_x,
        "k_y": k_y,

        "A": A,

        "pitch": pitch,

        "x_e": x_e,
        "y_e": y_e
    }

    # ========================================================
    # STIFF SUBSET
    # ========================================================

    stiff = {
        "s": s,

        # Same mass and geometry
        "m": m,

        "x_cg": x_cg,
        "y_cg": y_cg,

        "ri_x": ri_x,
        "ri_y": ri_y,

        "x_sh": x_sh,
        "y_sh": y_sh,

        # Artificially increased stiffness
        "E": np.full(2, 2.10e16),
        "G": np.full(2, 8.08e15),

        "I_x": I_x,
        "I_y": I_y,
        "I_p": I_p,

        "k_x": k_x,
        "k_y": k_y,

        "A": A,

        "pitch": pitch,

        "x_e": x_e,
        "y_e": y_e
    }

    # Set 1:
    # subset 1 = flexible
    # subset 2 = stiff
    return [[flexible, stiff]]


# -------- CREATE AND SAVE BEARING ---------
st_data = create_bearing_st()
TARGET_CONING_BEARING = (
    ROOT / "data" / "DTU_10MW_RWT_Bearing_st.dat"
) 

save_st(TARGET_CONING_BEARING, st_data)