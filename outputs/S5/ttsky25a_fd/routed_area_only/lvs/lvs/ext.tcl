gds read /foss/designs/outputs/S5/ttsky25a_fd/routed_area_only/ttsky25a_fd_routed.gds
load ttsky25a_fd_routed
select top cell
port makeall
set f [open /foss/designs/outputs/S5/ttsky25a_fd/routed_area_only/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S5/ttsky25a_fd/routed_area_only/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S5/ttsky25a_fd/routed_area_only/lvs/lvs -o /foss/designs/outputs/S5/ttsky25a_fd/routed_area_only/lvs/lvs/extracted.spice
quit -noprompt
