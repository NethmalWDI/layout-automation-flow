gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XX1_M7.gds
load XX1_M7
set kids [cellname list children XX1_M7]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M7/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M7/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M7/lvs -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M7/lvs/extracted.spice
quit -noprompt
