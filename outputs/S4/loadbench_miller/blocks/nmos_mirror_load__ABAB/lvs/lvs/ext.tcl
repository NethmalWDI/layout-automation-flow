gds read /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__ABAB/nmos_mirror_load__ABAB.gds
load nmos_mirror_load__ABAB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__ABAB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__ABAB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__ABAB/lvs/lvs -o /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__ABAB/lvs/lvs/extracted.spice
quit -noprompt
