gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM42.gds
load XM42
set kids [cellname list children XM42]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM42/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM42/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM42/probe -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM42/probe/extracted.spice
quit -noprompt
