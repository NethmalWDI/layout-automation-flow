gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS/nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS.gds
load nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS/pex/pex.spice
quit -noprompt
