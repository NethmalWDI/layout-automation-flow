gds read /foss/designs/outputs/S5/iadc_ota_v2/routed_area_only/iadc_ota_v2_routed.gds
load iadc_ota_v2_routed
select top cell
flatten iadc_ota_v2_routed_flat
load iadc_ota_v2_routed_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/iadc_ota_v2/area_only
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/iadc_ota_v2/area_only/iadc_ota_v2_routed_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/iadc_ota_v2/area_only/iadc_ota_v2_routed_pex.spice

quit -noprompt
