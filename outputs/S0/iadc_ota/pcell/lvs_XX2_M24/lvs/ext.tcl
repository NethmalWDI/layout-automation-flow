gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX2_M24.gds
load XX2_M24
set kids [cellname list children XX2_M24]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M24/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M24/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M24/lvs -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M24/lvs/extracted.spice
quit -noprompt
