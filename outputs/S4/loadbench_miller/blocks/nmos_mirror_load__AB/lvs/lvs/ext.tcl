gds read /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/nmos_mirror_load__AB.gds
load nmos_mirror_load__AB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/lvs/lvs -o /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/lvs/lvs/extracted.spice
quit -noprompt
