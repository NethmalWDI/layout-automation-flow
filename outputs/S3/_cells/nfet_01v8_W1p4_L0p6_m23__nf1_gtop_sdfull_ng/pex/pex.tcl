gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m23__nf1_gtop_sdfull_ng/nfet_01v8_W1p4_L0p6_m23__nf1_gtop_sdfull_ng.gds
load nfet_01v8_W1p4_L0p6_m23__nf1_gtop_sdfull_ng
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m23__nf1_gtop_sdfull_ng/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m23__nf1_gtop_sdfull_ng/pex/pex.spice
quit -noprompt
