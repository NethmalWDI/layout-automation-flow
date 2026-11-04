gds read /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/iadc_ota_routed.gds
load iadc_ota_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/lvs/lvs -o /foss/designs/outputs/S5/iadc_ota/routed_budget_aware/lvs/lvs/extracted.spice
quit -noprompt
