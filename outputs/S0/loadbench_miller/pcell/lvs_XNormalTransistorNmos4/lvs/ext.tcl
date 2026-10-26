gds read /foss/designs/outputs/S0/loadbench_miller/pcell/XNormalTransistorNmos4.gds
load XNormalTransistorNmos4
set kids [cellname list children XNormalTransistorNmos4]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos4/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos4/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos4/lvs -o /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos4/lvs/extracted.spice
quit -noprompt
