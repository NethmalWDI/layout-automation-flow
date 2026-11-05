gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
load XC3__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/lvs/lvs_negctl -o /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/lvs/lvs_negctl/extracted.spice
quit -noprompt
