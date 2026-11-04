gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M22_XX1_M15__ABBA/mirror_XX1_M22_XX1_M15__ABBA.gds
load mirror_XX1_M22_XX1_M15__ABBA
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M22_XX1_M15__ABBA/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M22_XX1_M15__ABBA/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M22_XX1_M15__ABBA/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M22_XX1_M15__ABBA/lvs/lvs/extracted.spice
quit -noprompt
