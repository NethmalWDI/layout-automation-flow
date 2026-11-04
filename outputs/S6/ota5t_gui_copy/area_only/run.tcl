gds read /foss/designs/outputs/S5/ota5t_gui_copy/routed_area_only/ota5t_gui_copy_routed.gds
load ota5t_gui_copy_routed
select top cell
flatten ota5t_gui_copy_routed_flat
load ota5t_gui_copy_routed_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/ota5t_gui_copy/area_only
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/ota5t_gui_copy/area_only/ota5t_gui_copy_routed_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/ota5t_gui_copy/area_only/ota5t_gui_copy_routed_pex.spice

quit -noprompt
