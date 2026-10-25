#!/usr/bin/env bash
# Extract with Magic (LVS mode) and compare with Netgen (sky130A setup).
# usage: magic_lvs.sh <gds> <topcell> <ref_spice> <ref_subckt> <outdir>
# LVS_MODE (env):
#   top     (default) extract the top cell; its labels become ports (port makeall)
#   subcell compare the first child cell instead (a single PDK PCell placed in a wrapper cell:
#           the PCell's own D/G/S/B labels become the ports; GDS does not carry port flags)
#   flat    flatten first (labels get instance prefixes; kept for diagnostics)
# The verdict is parsed from the report text, never from the exit code.
set -uo pipefail
. /foss/designs/scripts/env.sh
GDS=$(realpath "$1"); TOP=$2; REF=$(realpath "$3"); REFSUB=$4; OUT=$5; mkdir -p "$OUT"; OUT=$(realpath "$OUT")
MODE=${LVS_MODE:-top}; [ "${FLATTEN:-0}" = 1 ] && MODE=flat
case $MODE in
  top)     SEL="load $TOP";;
  flat)    SEL="load $TOP
flatten ${TOP}_flat
load ${TOP}_flat";;
  subcell) SEL="load $TOP
set kids [cellname list children $TOP]
load [lindex \$kids 0]";;
esac
cat > "$OUT/ext.tcl" <<TCL
gds read $GDS
$SEL
select top cell
port makeall
set f [open $OUT/cellname.txt w]; puts \$f [cellname list self]; close \$f
extract path $OUT
extract all
ext2spice lvs
ext2spice -p $OUT -o $OUT/extracted.spice
quit -noprompt
TCL
cd "$OUT"
rm -f extracted.spice cellname.txt lvs_report.txt
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc "$OUT/ext.tcl" > "$OUT/ext_magic.log" 2>&1
[ -s "$OUT/extracted.spice" ] || { echo "EXTRACT_FAILED"; tail -20 "$OUT/ext_magic.log"; exit 2; }
XTOP=$(tr -d '\n' < "$OUT/cellname.txt")
netgen -batch lvs "$OUT/extracted.spice $XTOP" "$REF $REFSUB" \
  $PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl "$OUT/lvs_report.txt" -json > "$OUT/netgen.log" 2>&1
if grep -q "Circuits match uniquely" "$OUT/lvs_report.txt" && ! grep -q -i "property errors\|mismatch\|failed pin matching" "$OUT/lvs_report.txt"; then
  echo "LVS_RESULT MATCH cell=$XTOP mode=$MODE"
else
  echo "LVS_RESULT FAIL cell=$XTOP mode=$MODE"
fi
grep -E "Number of devices|Number of nets|match|Mismatch|Property|failed" "$OUT/lvs_report.txt" | head -30
