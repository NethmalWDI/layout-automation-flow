gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/x2_cm_tail__id6.gds
load x2_cm_tail__id6
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/lvs/lvs_negctl -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/lvs/lvs_negctl/extracted.spice
quit -noprompt
