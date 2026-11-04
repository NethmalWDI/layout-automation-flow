gds read /foss/designs/outputs/S5/ota5t_gui_new/routed_area_only/ota5t_gui_new_routed.gds
load ota5t_gui_new_routed
select top cell
flatten ota5t_gui_new_routed_flat
load ota5t_gui_new_routed_flat
select top cell
port makeall
extract do local
extract all
ext2sim labels on
ext2sim
extresist tolerance 100
extresist all
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist on
ext2spice -o /foss/designs/outputs/S6/ota5t_gui_new/area_only/ota5t_gui_new_routed_pexrc.spice

quit -noprompt
