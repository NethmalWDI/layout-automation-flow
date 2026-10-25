gds read /foss/designs/outputs/S0/ota5t_stress/pcell/XM3.gds
load XM3
set kids [cellname list children XM3]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM3/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM3/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM3/lvs -o /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM3/lvs/extracted.spice
quit -noprompt
