gds read /foss/designs/outputs/S0/iadc_ota/pcell/XC3.gds
load XC3
set kids [cellname list children XC3]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC3/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC3/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC3/lvs_negctl -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XC3/lvs_negctl/extracted.spice
quit -noprompt
