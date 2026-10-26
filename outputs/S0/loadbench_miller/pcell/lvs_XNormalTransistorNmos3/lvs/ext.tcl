gds read /foss/designs/outputs/S0/loadbench_miller/pcell/XNormalTransistorNmos3.gds
load XNormalTransistorNmos3
set kids [cellname list children XNormalTransistorNmos3]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos3/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos3/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos3/lvs -o /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorNmos3/lvs/extracted.spice
quit -noprompt
