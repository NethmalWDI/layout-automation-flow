gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM41.gds
load XM41
set kids [cellname list children XM41]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM41/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM41/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM41/probe -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM41/probe/extracted.spice
quit -noprompt
