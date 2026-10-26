# Launcher for the layout-automation flow (Windows PowerShell, Docker Desktop).
# Runs `python3 -m src.flow <args>` inside the pinned EDA image with this repository mounted at /foss/designs.
#
#   .\flow.ps1 list
#   .\flow.ps1 run example_ota_5t
#   .\flow.ps1 run example_ota_5t --stage S2
#   .\flow.ps1 status all
#   .\flow.ps1 test
#
# $env:FLOW_IMAGE      override the image (default hpretl/iic-osic-tools:2026.10)
# $env:FLOW_CONTAINER  reuse a running container that already mounts this repo at /foss/designs
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$FlowArgs)
$Image = if ($env:FLOW_IMAGE) { $env:FLOW_IMAGE } else { "hpretl/iic-osic-tools:2026.10" }
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Inner = "source scripts/env.sh && python3 -m src.flow " + ($FlowArgs -join ' ')
if ($env:FLOW_CONTAINER) {
    docker exec -i $env:FLOW_CONTAINER bash -lc "cd /foss/designs && $Inner"
} else {
    docker run --rm -i -e IIC_OSIC_TOOLS_QUIET=1 -v "${Here}:/foss/designs" -w /foss/designs $Image --skip bash -lc $Inner
}
exit $LASTEXITCODE
