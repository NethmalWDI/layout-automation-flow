#!/usr/bin/env bash
# Extract with Magic (LVS mode) and compare with Netgen (sky130A setup).
# usage: magic_lvs.sh <gds> <topcell> <ref_spice> <ref_subckt> <outdir>
set -uo pipefail
. /foss/designs/scripts/env.sh
GDS=$(realpath "$1"); TOP=$2; REF=$(realpath "$3"); REFSUB=$4; OUT=$5; mkdir -p "$OUT"; OUT=$(realpath "$OUT")
cat > "$OUT/ext.tcl" <<TCL
gds read $GDS
load $TOP
$( [ "${FLATTEN:-0}" = 1 ] && echo "flatten ${TOP}_flat
load ${TOP}_flat" )
select top cell
port makeall
extract path $OUT
extract all
ext2spice lvs
ext2spice -p $OUT -o $OUT/${TOP}_extracted.spice
quit -noprompt
TCL
cd "$OUT"
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc "$OUT/ext.tcl" > "$OUT/ext_magic.log" 2>&1
[ -s "$OUT/${TOP}_extracted.spice" ] || { echo "EXTRACT_FAILED"; tail -20 "$OUT/ext_magic.log"; exit 2; }
XTOP=$TOP; [ "${FLATTEN:-0}" = 1 ] && XTOP=${TOP}_flat
netgen -batch lvs "$OUT/${TOP}_extracted.spice $XTOP" "$REF $REFSUB" \
  $PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl "$OUT/lvs_report.txt" -json > "$OUT/netgen.log" 2>&1
if grep -q "Circuits match uniquely" "$OUT/lvs_report.txt" && ! grep -q -i "property errors\|mismatch" "$OUT/lvs_report.txt"; then
  echo "LVS_RESULT MATCH"
else
  echo "LVS_RESULT FAIL"
fi
grep -E "Number of devices|Number of nets|match|Mismatch|Property" "$OUT/lvs_report.txt" | head -30
