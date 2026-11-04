gds read /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__ABBA/input_pair__ABBA.gds
load input_pair__ABBA
select top cell
port makeall
set f [open /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__ABBA/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__ABBA/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__ABBA/lvs/lvs_negctl -o /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__ABBA/lvs/lvs_negctl/extracted.spice
quit -noprompt
