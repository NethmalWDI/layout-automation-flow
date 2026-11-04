gds read /foss/designs/outputs/S5/loadbench_miller/routed_area_only/loadbench_miller_routed.gds
load loadbench_miller_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/loadbench_miller/routed_area_only/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/loadbench_miller/routed_area_only/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/loadbench_miller/routed_area_only/lvs/lvs_negctl -o /foss/designs/outputs/S5/loadbench_miller/routed_area_only/lvs/lvs_negctl/extracted.spice
quit -noprompt
