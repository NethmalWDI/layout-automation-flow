gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX2_M1A.gds
load XX2_M1A
set kids [cellname list children XX2_M1A]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M1A/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M1A/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M1A/lvs_negctl -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX2_M1A/lvs_negctl/extracted.spice
quit -noprompt
