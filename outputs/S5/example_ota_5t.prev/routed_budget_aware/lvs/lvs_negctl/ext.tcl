gds read /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/example_ota_5t_routed.gds
load example_ota_5t_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/lvs/lvs_negctl -o /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/lvs/lvs_negctl/extracted.spice
quit -noprompt
