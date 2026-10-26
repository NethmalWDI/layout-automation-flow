gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM33.gds
load XM33
set kids [cellname list children XM33]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/probe -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/probe/extracted.spice
quit -noprompt
