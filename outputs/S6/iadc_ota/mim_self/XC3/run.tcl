gds read /foss/designs/outputs/S4/iadc_ota/blocks/XC3__A/XC3__A.gds
load XC3__A
select top cell
flatten XC3__A_flat
load XC3__A_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/iadc_ota/mim_self/XC3
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/iadc_ota/mim_self/XC3/XC3__A_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/iadc_ota/mim_self/XC3/XC3__A_pex.spice

quit -noprompt
