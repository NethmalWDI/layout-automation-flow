gds read /foss/designs/outputs/S5/loadbench_miller/routed_budget_aware/loadbench_miller_routed.gds
load loadbench_miller_routed
select top cell
flatten loadbench_miller_routed_flat
load loadbench_miller_routed_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/loadbench_miller/budget_aware
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/loadbench_miller/budget_aware/loadbench_miller_routed_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/loadbench_miller/budget_aware/loadbench_miller_routed_pex.spice

quit -noprompt
