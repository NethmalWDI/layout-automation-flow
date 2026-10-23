#!/usr/bin/env bash
# Run the full ALIGN flow inside layout-s0s3.
# usage: bash scripts/run_align.sh <netlist_dir> <work_dir> [extra schematic2layout args]
set -euo pipefail
. /foss/designs/scripts/env.sh
IN=$(realpath "$1"); WD=$2; shift 2
mkdir -p "$WD"; WD=$(realpath "$WD")
cd "$WD"
echo "ALIGN $(/opt/venv-align/bin/pip show align-analoglayout | grep Version)  pdk $(cat /foss/designs/runs/env/align_pdk_commit.txt)"
echo "input: $IN  work: $WD  args: $*"
start=$(date +%s)
/opt/venv-align/bin/schematic2layout.py "$IN" -p /foss/designs/external/ALIGN-pdk-sky130/SKY130_PDK -w "$WD" "$@"
rc=$?
echo "ALIGN_EXIT=$rc runtime_s=$(( $(date +%s) - start ))"
ls -la "$WD"
exit $rc
