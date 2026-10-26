gds read /foss/designs/outputs/S0/loadbench_miller/pcell/XNormalTransistorPmos8.gds
load XNormalTransistorPmos8
set kids [cellname list children XNormalTransistorPmos8]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos8/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos8/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos8/lvs -o /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos8/lvs/extracted.spice
quit -noprompt
