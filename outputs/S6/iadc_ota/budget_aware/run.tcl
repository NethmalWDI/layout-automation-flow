gds read /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/iadc_ota_routed.gds
load iadc_ota_routed
select top cell
flatten iadc_ota_routed_flat
load iadc_ota_routed_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/iadc_ota/budget_aware
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/iadc_ota/budget_aware/iadc_ota_routed_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/iadc_ota/budget_aware/iadc_ota_routed_pex.spice

quit -noprompt
