gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX2_M39.gds
load XX2_M39
set kids [cellname list children XX2_M39]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M39/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M39/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M39/lvs_negctl -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M39/lvs_negctl/extracted.spice
quit -noprompt
