gds read /foss/designs/outputs/S0/ota5t_stress/pcell/XM2.gds
load XM2
set kids [cellname list children XM2]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM2/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM2/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM2/lvs -o /foss/designs/outputs/S0/ota5t_stress/pcell/lvs_XM2/lvs/extracted.spice
quit -noprompt
