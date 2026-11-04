gds read /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/input_pair__AB.gds
load input_pair__AB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/lvs/lvs -o /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/lvs/lvs/extracted.spice
quit -noprompt
