gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull/nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull
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
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdfull/rx/rx.spice
quit -noprompt
