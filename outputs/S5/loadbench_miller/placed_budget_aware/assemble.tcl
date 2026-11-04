drc off
snap internal
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/pmos_bias_bank__row/pmos_bias_bank__row.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/input_pair__AB.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/nmos_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/cs_stage__A.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/Capacitor2__A/Capacitor2__A.gds
load loadbench_miller_placed_budget_aware -silent
box -17.5500um -64.6500um -17.5500um -64.6500um
getcell pmos_bias_bank__row
box -5.1100um -83.0700um -5.1100um -83.0700um
getcell input_pair__AB
box -21.2000um -101.0800um -21.2000um -101.0800um
getcell nmos_mirror_load__AB
box -22.7600um -124.7700um -22.7600um -124.7700um
getcell cs_stage__A
box 1.3400um -124.7700um 1.3400um -124.7700um
getcell Capacitor2__A
tech unlock *
tech revert
save loadbench_miller_placed_budget_aware
gds write loadbench_miller_placed_budget_aware
quit -noprompt
