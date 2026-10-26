gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS/pex/pex.spice
quit -noprompt
