#!/usr/bin/env bash
# Run every ALIGN-pdk-sky130 example unmodified, then DRC + PNG for each.  (inside layout-s0s3)
. /foss/designs/scripts/env.sh
cd /foss/designs
EX=external/ALIGN-pdk-sky130/examples
for d in $(ls $EX); do
  [ -f $EX/$d/$d.sp ] || { echo "SKIP $d (no $d.sp)"; continue; }
  W=runs/align/examples/$d; rm -rf $W
  echo "=== $d"; s=$(date +%s)
  bash scripts/run_align.sh $EX/$d $W -n 1 > runs/logs/align_ex_$d.log 2>&1; rc=$?
  g=$(ls $W/*_0.gds 2>/dev/null | grep -v python | head -1)
  echo "ALIGN_EXIT=$rc runtime=$(( $(date +%s)-s ))s gds=$g"
  if [ -n "$g" ]; then
    top=$(basename $g .gds)
    klayout -zz -rd gds=$g -rd png=${g%.gds}.png -r scripts/gds_to_png.py 2>&1 | tail -1
    timeout 300 bash scripts/magic_drc.sh $g $top $W/drc 2>&1 | grep -E "DRC_TOTAL|NEG_CONTROL" | head -2
  fi
done
echo ALL_DONE
