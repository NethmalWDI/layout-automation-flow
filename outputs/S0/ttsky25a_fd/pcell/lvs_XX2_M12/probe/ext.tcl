gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XX2_M12.gds
load XX2_M12
set kids [cellname list children XX2_M12]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M12/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M12/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M12/probe -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XX2_M12/probe/extracted.spice
quit -noprompt
