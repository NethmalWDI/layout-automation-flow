gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf.gds
load nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/pex/pex.spice
quit -noprompt
