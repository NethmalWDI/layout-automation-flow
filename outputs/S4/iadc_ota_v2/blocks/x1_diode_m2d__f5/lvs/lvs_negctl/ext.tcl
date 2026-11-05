gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/x1_diode_m2d__f5.gds
load x1_diode_m2d__f5
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/lvs/lvs_negctl -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/lvs/lvs_negctl/extracted.spice
quit -noprompt
