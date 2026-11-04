gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull_ng/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull_ng
select top cell
port makeall
extract do resistance
extract all
ext2sim labels on
ext2sim
extresist tolerance 1
extresist all
ext2spice extresist on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull_ng/rx/rx.spice
quit -noprompt
