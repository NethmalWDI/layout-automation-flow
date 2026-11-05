gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/x1_single_m5__f1.gds
load x1_single_m5__f1
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/lvs/lvs_negctl -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/lvs/lvs_negctl/extracted.spice
quit -noprompt
