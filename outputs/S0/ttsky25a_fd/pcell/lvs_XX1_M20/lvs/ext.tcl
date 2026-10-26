gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XX1_M20.gds
load XX1_M20
set kids [cellname list children XX1_M20]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M20/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M20/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M20/lvs -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX1_M20/lvs/extracted.spice
quit -noprompt
