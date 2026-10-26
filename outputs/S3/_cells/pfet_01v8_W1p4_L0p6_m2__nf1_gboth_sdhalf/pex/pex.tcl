gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdhalf/pfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdhalf.gds
load pfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdhalf
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdhalf/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdhalf/pex/pex.spice
quit -noprompt
