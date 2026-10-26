gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM36.gds
load XM36
set kids [cellname list children XM36]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM36/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM36/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM36/lvs -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM36/lvs/extracted.spice
quit -noprompt
