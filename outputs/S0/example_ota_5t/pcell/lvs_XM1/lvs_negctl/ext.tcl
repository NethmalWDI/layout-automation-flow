gds read /foss/designs/outputs/S0/example_ota_5t/pcell/XM1.gds
load XM1
set kids [cellname list children XM1]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM1/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM1/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM1/lvs_negctl -o /foss/designs/outputs/S0/example_ota_5t/pcell/lvs_XM1/lvs_negctl/extracted.spice
quit -noprompt
