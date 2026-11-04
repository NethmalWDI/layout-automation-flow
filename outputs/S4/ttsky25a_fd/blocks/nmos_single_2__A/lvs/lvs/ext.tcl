gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_single_2__A/nmos_single_2__A.gds
load nmos_single_2__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_single_2__A/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_single_2__A/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_single_2__A/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_single_2__A/lvs/lvs/extracted.spice
quit -noprompt
