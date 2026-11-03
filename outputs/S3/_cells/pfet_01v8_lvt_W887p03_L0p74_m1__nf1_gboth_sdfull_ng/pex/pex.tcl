gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng/pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng/pex/pex.spice
quit -noprompt
