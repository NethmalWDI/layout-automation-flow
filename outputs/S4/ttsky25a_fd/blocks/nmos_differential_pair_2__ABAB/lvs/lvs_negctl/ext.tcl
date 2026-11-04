gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_differential_pair_2__ABAB/nmos_differential_pair_2__ABAB.gds
load nmos_differential_pair_2__ABAB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_differential_pair_2__ABAB/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_differential_pair_2__ABAB/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_differential_pair_2__ABAB/lvs/lvs_negctl -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_differential_pair_2__ABAB/lvs/lvs_negctl/extracted.spice
quit -noprompt
