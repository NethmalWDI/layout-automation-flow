#!/usr/bin/env bash
# Magic DRC (sky130A, drc(full)) on a GDS. usage: magic_drc.sh <gds> <topcell> <outdir>
set -uo pipefail
. /foss/designs/scripts/env.sh
GDS=$(realpath "$1"); TOP=$2; OUT=$3; mkdir -p "$OUT"; OUT=$(realpath "$OUT")
cat > "$OUT/drc.tcl" <<TCL
gds read $GDS
load $TOP
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children $TOP]]"
flatten ${TOP}_flat
load ${TOP}_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL \$n"
set f [open $OUT/drc_report.txt w]
puts \$f "top $TOP (flattened) gds $GDS"
puts \$f "DRC_TOTAL \$n"
foreach {why boxes} [drc listall why] { puts \$f "[llength \$boxes]\t\$why" }
close \$f
# negative control: a 0.05 um wide met1 sliver must be flagged
box 0um 0um 0.05um 1um
paint metal1
drc check
drc catchup
puts "NEG_CONTROL_TOTAL [drc list count total]"
quit -noprompt
TCL
cd "$OUT"
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc "$OUT/drc.tcl" > "$OUT/drc_magic.log" 2>&1
grep -E "CELL_BBOX|FLAT_BBOX|SUBCELLS|DRC_TOTAL|NEG_CONTROL|Unknown layer" "$OUT/drc_magic.log" || { echo "DRC_RUN_FAILED"; tail -20 "$OUT/drc_magic.log"; exit 2; }
sort -t$'\t' -k1,1nr "$OUT/drc_report.txt" | head -25
