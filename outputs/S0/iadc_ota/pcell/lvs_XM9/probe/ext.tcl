gds read /foss/designs/outputs/S0/iadc_ota/pcell/XM9.gds
load XM9
set kids [cellname list children XM9]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM9/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM9/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM9/probe -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XM9/probe/extracted.spice
quit -noprompt
