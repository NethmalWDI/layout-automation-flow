gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM54.gds
load XM54
set kids [cellname list children XM54]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM54/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM54/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM54/lvs -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM54/lvs/extracted.spice
quit -noprompt
