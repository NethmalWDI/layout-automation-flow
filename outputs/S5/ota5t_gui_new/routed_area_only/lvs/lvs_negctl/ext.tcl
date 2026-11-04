gds read /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/ota5t_gui_new_routed.gds
load ota5t_gui_new_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/lvs/lvs_negctl -o /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/lvs/lvs_negctl/extracted.spice
quit -noprompt
