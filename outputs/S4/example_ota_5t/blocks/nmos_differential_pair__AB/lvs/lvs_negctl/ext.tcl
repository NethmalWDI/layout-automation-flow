gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/nmos_differential_pair__AB.gds
load nmos_differential_pair__AB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/lvs/lvs_negctl -o /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/lvs/lvs_negctl/extracted.spice
quit -noprompt
