gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XX2_X1_R15.gds
load XX2_X1_R15
set kids [cellname list children XX2_X1_R15]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_X1_R15/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_X1_R15/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_X1_R15/lvs -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_X1_R15/lvs/extracted.spice
quit -noprompt
