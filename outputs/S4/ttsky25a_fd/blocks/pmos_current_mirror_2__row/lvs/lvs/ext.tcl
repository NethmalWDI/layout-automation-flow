gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_current_mirror_2__row/pmos_current_mirror_2__row.gds
load pmos_current_mirror_2__row
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_current_mirror_2__row/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_current_mirror_2__row/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_current_mirror_2__row/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_current_mirror_2__row/lvs/lvs/extracted.spice
quit -noprompt
