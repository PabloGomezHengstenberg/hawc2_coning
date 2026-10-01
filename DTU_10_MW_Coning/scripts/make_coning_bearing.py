
import numpy as np
from pathlib import Path
from lacbox.io import save_st


ROOT = Path(__file__).parents[1]  # Main repository level


# ============================================================
# CREATE CONING BEARING ST
# ============================================================

def create_bearing_st():
    """
    Create HAWC2 ST data for the intermediate coning-bearing body.

    The body is intended to be:
        - Very short
        - Nearly massless
        - Structurally stiff

    Its purpose is to connect the coning and pitch bearings
    without introducing significant additional deformation,
    mass or inertia.

    Set 1:
        Subset 1 = stiff
        Subset 2 = stiff

    Both subsets have identical properties for now.
    """

    # ========================================================
    # GEOMETRY
    # ========================================================

    L_bearing = 1e-4  # [m]

    # Two stations: beginning and end
    s = np.array([0.0, L_bearing])

    # ========================================================
    # MASS AND CROSS-SECTIONAL PROPERTIES
    # ========================================================

    # Small but nonzero mass per unit length [kg/m]
    m = np.full(2, 1e-3)

    # Artificial cross-sectional area [m^2]
    A = np.full(2, 1.0)

    # Second moments of area [m^4]
    I_x = np.full(2, 1.0)
    I_y = np.full(2, 1.0)

    # Polar moment of area [m^4]
    I_p = np.full(2, 2.0)

    # Radii of gyration [m]
    ri_x = np.full(2, 1.0)
    ri_y = np.full(2, 1.0)

    # ========================================================
    # SECTION OFFSETS
    # ========================================================

    # Centre of gravity
    x_cg = np.zeros(2)
    y_cg = np.zeros(2)

    # Shear centre
    x_sh = np.zeros(2)
    y_sh = np.zeros(2)

    # Elastic centre
    x_e = np.zeros(2)
    y_e = np.zeros(2)

    # Structural pitch [deg]
    pitch = np.zeros(2)

    # ========================================================
    # MATERIAL PROPERTIES
    # ========================================================

    # Young's modulus [Pa]
    E = np.full(2, 2.10e11)

    # Shear modulus [Pa]
    G = np.full(2, 8.08e10)

    # ========================================================
    # TIMOSHENKO SHEAR FACTORS
    # ========================================================

    k_x = np.full(2, 0.5)
    k_y = np.full(2, 0.5)

    # ========================================================
    # STRUCTURAL SUBSET
    # ========================================================

    stiff = {
        "s": s,

        "m": m,

        "x_cg": x_cg,
        "y_cg": y_cg,

        "ri_x": ri_x,
        "ri_y": ri_y,

        "x_sh": x_sh,
        "y_sh": y_sh,

        "E": E,
        "G": G,

        "I_x": I_x,
        "I_y": I_y,
        "I_p": I_p,

        "k_x": k_x,
        "k_y": k_y,

        "A": A,

        "pitch": pitch,

        "x_e": x_e,
        "y_e": y_e,
    }

    # ========================================================
    # RETURN HAWC2 ST STRUCTURE
    # ========================================================

    # Set 1:
    #   Subset 1 = stiff
    #   Subset 2 = stiff

    return [[stiff, stiff.copy()]]


# ============================================================
# CREATE AND SAVE BEARING FILE
# ============================================================

if __name__ == "__main__":

    st_data = create_bearing_st()

    TARGET_CONING_BEARING = (
        ROOT / "data" / "DTU_10MW_RWT_Bearing_st.dat"
    )

    TARGET_CONING_BEARING.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    save_st(TARGET_CONING_BEARING, st_data)

    print(
        f"Coning bearing ST file saved to: "
        f"{TARGET_CONING_BEARING}"
    )
