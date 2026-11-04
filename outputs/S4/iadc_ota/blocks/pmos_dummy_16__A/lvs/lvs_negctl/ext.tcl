gds read /foss/designs/outputs/S4/iadc_ota/blocks/pmos_dummy_16__A/pmos_dummy_16__A.gds
load pmos_dummy_16__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota/blocks/pmos_dummy_16__A/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota/blocks/pmos_dummy_16__A/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota/blocks/pmos_dummy_16__A/lvs/lvs_negctl -o /foss/designs/outputs/S4/iadc_ota/blocks/pmos_dummy_16__A/lvs/lvs_negctl/extracted.spice
quit -noprompt
