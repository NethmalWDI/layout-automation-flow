gds read /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
load pmos_current_mirror_load__AB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/lvs/lvs -o /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/lvs/lvs/extracted.spice
quit -noprompt
