drc off
snap internal
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/nmos_differential_pair__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load example_ota_5t_placed_budget_aware -silent
box -4.0400um -15.2150um -4.0400um -15.2150um
getcell pmos_current_mirror_load__AB
box -4.2200um -37.5250um -4.2200um -37.5250um
getcell nmos_differential_pair__AB v
box -3.3600um -58.0350um -3.3600um -58.0350um
getcell nmos_current_mirror_bias__A v
tech unlock *
tech revert
save example_ota_5t_placed_budget_aware
gds write example_ota_5t_placed_budget_aware
quit -noprompt
