gds read /foss/designs/outputs/S0/example_ota_5t/pcell/XM5.gds
load XM5
set kids [cellname list children XM5]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM5/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM5/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM5/lvs -o /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM5/lvs/extracted.spice
quit -noprompt
