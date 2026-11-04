drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM3__A/XM3__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM4__A/XM4__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM1__A/XM1__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM2__A/XM2__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/XM5__A.gds
load ota5t_gui_new_placed_budget_aware -silent
box -7.4400um -14.5100um -7.4400um -14.5100um
getcell XM3__A
box 1.9000um -14.5100um 1.9000um -14.5100um
getcell XM4__A
box -7.2200um -35.3500um -7.2200um -35.3500um
getcell XM1__A v
box 1.5000um -35.3500um 1.5000um -35.3500um
getcell XM2__A v
box -2.7150um -68.1900um -2.7150um -68.1900um
getcell XM5__A v
tech unlock *
tech revert
save ota5t_gui_new_placed_budget_aware
gds write ota5t_gui_new_placed_budget_aware
quit -noprompt
