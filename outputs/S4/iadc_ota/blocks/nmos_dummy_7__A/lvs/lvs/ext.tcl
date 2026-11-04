gds read /foss/designs/outputs/S4/iadc_ota/blocks/nmos_dummy_7__A/nmos_dummy_7__A.gds
load nmos_dummy_7__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota/blocks/nmos_dummy_7__A/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota/blocks/nmos_dummy_7__A/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota/blocks/nmos_dummy_7__A/lvs/lvs -o /foss/designs/outputs/S4/iadc_ota/blocks/nmos_dummy_7__A/lvs/lvs/extracted.spice
quit -noprompt
