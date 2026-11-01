# Source inside the layout-s0s3 container: tool paths + PDK selection
export PATH=/foss/tools/bin:/foss/tools/sak:/foss/tools/klayout:$PATH
export PDK_ROOT=/foss/pdks
export REPO=/foss/designs
# The image's login profile selects IHP-SG13G2 by default (PDK, SPICE_USERINIT_DIR, KLAYOUT_PATH, ...): ngspice then
# reads IHP's init and not sky130's (ngbehavior=hsa, enable_noisy_r). Switch with the image's own command, sak-pdk
# (an alias of this script). Its last line returns 1 for every PDK except GF180, so the check below decides.
source /foss/tools/sak/sak-pdk-script.sh sky130A > /dev/null
if [ "$PDK" != sky130A ] || [ "$SPICE_USERINIT_DIR" != "$PDK_ROOT/sky130A/libs.tech/ngspice" ]; then
    echo "[ERROR] scripts/env.sh: could not select the sky130A PDK (PDK=$PDK)" >&2
    return 1 2> /dev/null || exit 1
fi
