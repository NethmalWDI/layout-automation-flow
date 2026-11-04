drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM3__A/XM3__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM4__A/XM4__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM1__A/XM1__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM2__A/XM2__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/XM5__A.gds
load ota5t_gui_new_placed_area_only -silent
box -3.1700um -14.5100um -3.1700um -14.5100um
getcell XM3__A
box -2.7700um -32.0200um -2.7700um -32.0200um
getcell XM4__A
box -2.8600um -52.8600um -2.8600um -52.8600um
getcell XM1__A
box -2.8600um -73.7000um -2.8600um -73.7000um
getcell XM2__A
box -2.7150um -106.5400um -2.7150um -106.5400um
getcell XM5__A
tech unlock *
tech revert
save ota5t_gui_new_placed_area_only
gds write ota5t_gui_new_placed_area_only
quit -noprompt
