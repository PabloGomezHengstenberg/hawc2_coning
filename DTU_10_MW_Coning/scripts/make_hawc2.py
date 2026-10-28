"""Make HAWC2S files from a master htc file.

This file should create the following htc files:
 * _hawc2s_1wsp.htc
 * _hawc2s_multitsr.htc
 * _hawc2s_rigid.htc
 * _hawc2s_flex.htc
 * _hawc2s_ctrltune_fX_dY_C[T/P].htc (7 files)
 * ...and more?

We recommend saving the HAWC2S files in a dedicated subfolder. If you
do this, note that you will need to move the htc before running HAWCStab2.

Requires myteampack (which requires lacbox).
"""

from pathlib import Path

from mypack import MyHTC

# file names and paths
DESIGN_NAME = "dtu_10mw"
ROOT = Path(__file__).parents[1]  # root is one level up
MASTER_FILE = ROOT / "_master_htc" / "DTU_10MW_RWT_cone.htc"  # your master htc file
TARGET_DIR = ROOT / "htc_hawc2"  # where to save the htc files this script will make

GENSPEED = (0, 480)  # minimum and maximum generator speed [rpm]

# make rigid hawc2s file for single-wsp opt file
htc = MyHTC(MASTER_FILE)

htc.make_hawc2(
    TARGET_DIR,
    wsp=8.0,
    append="_8wsp_0.0",
    cone_angle=0.0,
    wind_type="constant",
    rigid=True,
    time_stop=500,
)


# Create wind steps file
htc = MyHTC(MASTER_FILE)

htc.make_hawc2(
    save_dir=TARGET_DIR,
    wsp=6.0,
    append="_steps_0.0",
    cone_angle=0.0,
    wind_type="step",
    wind_steps=[
        (100, 101, 2.0),
        (200, 201, 2.0),
        (300, 301, 2.0),
    ],
    rigid=True,
    time_stop=400,
)