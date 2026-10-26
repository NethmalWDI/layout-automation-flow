gds read /foss/designs/outputs/S0/loadbench_miller/pcell/XNormalTransistorPmos5.gds
load XNormalTransistorPmos5
set kids [cellname list children XNormalTransistorPmos5]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos5/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos5/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos5/lvs_negctl -o /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_XNormalTransistorPmos5/lvs_negctl/extracted.spice
quit -noprompt
