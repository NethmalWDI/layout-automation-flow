gds read /foss/designs/outputs/S0/example_ota_5t/pcell/XM4.gds
load XM4
set kids [cellname list children XM4]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM4/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM4/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM4/lvs -o /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM4/lvs/extracted.spice
quit -noprompt
