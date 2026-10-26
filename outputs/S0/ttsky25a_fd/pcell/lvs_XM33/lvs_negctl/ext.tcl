gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM33.gds
load XM33
set kids [cellname list children XM33]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/lvs_negctl -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM33/lvs_negctl/extracted.spice
quit -noprompt
