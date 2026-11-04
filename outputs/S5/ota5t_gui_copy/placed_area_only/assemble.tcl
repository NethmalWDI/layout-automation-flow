drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/nmos_differential_pair__ABBA.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load ota5t_gui_copy_placed_area_only -silent
box -6.5800um -16.1150um -6.5800um -16.1150um
getcell pmos_current_mirror_load__AB
box -7.2900um -40.2250um -7.2900um -40.2250um
getcell nmos_differential_pair__ABBA
box -3.3600um -60.7350um -3.3600um -60.7350um
getcell nmos_current_mirror_bias__A
tech unlock *
tech revert
save ota5t_gui_copy_placed_area_only
gds write ota5t_gui_copy_placed_area_only
quit -noprompt
