gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX1_M34.gds
load XX1_M34
set kids [cellname list children XX1_M34]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M34/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M34/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M34/lvs -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M34/lvs/extracted.spice
quit -noprompt
