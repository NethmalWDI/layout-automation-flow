gds read /foss/designs/outputs/S4/loadbench_miller/blocks/Capacitor2__A/Capacitor2__A.gds
load Capacitor2__A
select top cell
flatten Capacitor2__A_flat
load Capacitor2__A_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/loadbench_miller/mim_self/Capacitor2
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/loadbench_miller/mim_self/Capacitor2/Capacitor2__A_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/loadbench_miller/mim_self/Capacitor2/Capacitor2__A_pex.spice

quit -noprompt
