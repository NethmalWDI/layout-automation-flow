gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated.gds
load mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/mirror_XX1_M1_XX1_M2_XX1_M7_XX1_M9__interdigitated/lvs/lvs/extracted.spice
quit -noprompt
