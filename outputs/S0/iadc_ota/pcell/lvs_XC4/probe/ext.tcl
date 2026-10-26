gds read /foss/designs/outputs/S0/iadc_ota/pcell/XC4.gds
load XC4
set kids [cellname list children XC4]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC4/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC4/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC4/probe -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC4/probe/extracted.spice
quit -noprompt
