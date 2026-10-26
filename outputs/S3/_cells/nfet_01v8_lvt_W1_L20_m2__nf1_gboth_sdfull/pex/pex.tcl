gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdfull/nfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdfull
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdfull/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdfull/pex/pex.spice
quit -noprompt
