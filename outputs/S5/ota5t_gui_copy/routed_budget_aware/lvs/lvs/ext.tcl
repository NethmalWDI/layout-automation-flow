gds read /foss/designs/outputs/S5/ota5t_gui_copy/routed_budget_aware/ota5t_gui_copy_routed.gds
load ota5t_gui_copy_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/ota5t_gui_copy/routed_budget_aware/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/ota5t_gui_copy/routed_budget_aware/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/ota5t_gui_copy/routed_budget_aware/lvs/lvs -o /foss/designs/outputs/S5/ota5t_gui_copy/routed_budget_aware/lvs/lvs/extracted.spice
quit -noprompt
