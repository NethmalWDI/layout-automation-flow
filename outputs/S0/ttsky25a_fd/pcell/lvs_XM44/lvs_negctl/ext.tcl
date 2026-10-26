gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM44.gds
load XM44
set kids [cellname list children XM44]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM44/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM44/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM44/lvs_negctl -o /foss/designs/outputs/S0/ttsky25a_fd/pcell/lvs_XM44/lvs_negctl/extracted.spice
quit -noprompt
