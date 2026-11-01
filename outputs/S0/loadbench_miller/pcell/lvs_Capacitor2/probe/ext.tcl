gds read /foss/designs/outputs/S0/loadbench_miller/pcell/Capacitor2.gds
load Capacitor2
set kids [cellname list children Capacitor2]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_Capacitor2/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_Capacitor2/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_Capacitor2/probe -o /foss/designs/outputs/S0/loadbench_miller/pcell/lvs_Capacitor2/probe/extracted.spice
quit -noprompt
