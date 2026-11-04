gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror__interdigitated/nmos_current_mirror__interdigitated.gds
load nmos_current_mirror__interdigitated
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror__interdigitated/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror__interdigitated/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror__interdigitated/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_current_mirror__interdigitated/lvs/lvs/extracted.spice
quit -noprompt
