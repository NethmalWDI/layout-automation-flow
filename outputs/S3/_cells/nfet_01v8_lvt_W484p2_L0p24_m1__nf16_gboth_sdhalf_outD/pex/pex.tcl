gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD/nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD
select top cell
port makeall
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD/pex
extract all
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD/pex/pex.spice
quit -noprompt
