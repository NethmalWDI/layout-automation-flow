gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdfull/pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdfull
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdfull/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdfull/pex/pex.spice
quit -noprompt
