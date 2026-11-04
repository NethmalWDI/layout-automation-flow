gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/XC1__A/XC1__A.gds
load XC1__A
select top cell
flatten XC1__A_flat
load XC1__A_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC1
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC1/XC1__A_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/mim_self/XC1/XC1__A_pex.spice

quit -noprompt
