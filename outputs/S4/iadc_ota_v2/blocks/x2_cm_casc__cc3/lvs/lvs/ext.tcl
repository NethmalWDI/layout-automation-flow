gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/x2_cm_casc__cc3.gds
load x2_cm_casc__cc3
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/lvs/lvs -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/lvs/lvs/extracted.spice
quit -noprompt
