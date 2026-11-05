gds read /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/iadc_ota_v2_routed.gds
load iadc_ota_v2_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/lvs/lvs -o /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/lvs/lvs/extracted.spice
quit -noprompt
