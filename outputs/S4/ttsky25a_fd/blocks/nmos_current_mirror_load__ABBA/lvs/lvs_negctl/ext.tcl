gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror_load__ABBA/nmos_current_mirror_load__ABBA.gds
load nmos_current_mirror_load__ABBA
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror_load__ABBA/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror_load__ABBA/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror_load__ABBA/lvs/lvs_negctl -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror_load__ABBA/lvs/lvs_negctl/extracted.spice
quit -noprompt
