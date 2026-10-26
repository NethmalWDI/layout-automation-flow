gds read /foss/designs/outputs/S0/iadc_ota/pcell/XM45.gds
load XM45
set kids [cellname list children XM45]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM45/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM45/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM45/probe -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM45/probe/extracted.spice
quit -noprompt
