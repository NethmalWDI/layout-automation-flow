gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings5/x1_cc_cm__strings5.gds
load x1_cc_cm__strings5
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings5/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings5/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings5/lvs/lvs -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings5/lvs/lvs/extracted.spice
quit -noprompt
