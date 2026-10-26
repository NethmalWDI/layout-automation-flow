gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX1_M27.gds
load XX1_M27
set kids [cellname list children XX1_M27]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M27/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M27/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M27/lvs_negctl -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M27/lvs_negctl/extracted.spice
quit -noprompt
