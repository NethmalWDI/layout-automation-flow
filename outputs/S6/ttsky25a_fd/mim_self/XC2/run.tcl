gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/XC2__A/XC2__A.gds
load XC2__A
select top cell
flatten XC2__A_flat
load XC2__A_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC2
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC2/XC2__A_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC2/XC2__A_pex.spice

quit -noprompt
