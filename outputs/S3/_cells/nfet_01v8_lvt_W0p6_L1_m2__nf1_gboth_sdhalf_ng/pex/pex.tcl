gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p6_L1_m2__nf1_gboth_sdhalf_ng/nfet_01v8_lvt_W0p6_L1_m2__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_lvt_W0p6_L1_m2__nf1_gboth_sdhalf_ng
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p6_L1_m2__nf1_gboth_sdhalf_ng/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p6_L1_m2__nf1_gboth_sdhalf_ng/pex/pex.spice
quit -noprompt
