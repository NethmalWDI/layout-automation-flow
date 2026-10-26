gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XX2_M10.gds
load XX2_M10
set kids [cellname list children XX2_M10]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M10/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M10/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M10/probe -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M10/probe/extracted.spice
quit -noprompt
