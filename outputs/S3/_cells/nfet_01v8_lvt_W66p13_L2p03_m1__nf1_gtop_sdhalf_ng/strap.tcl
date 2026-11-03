drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gtop_sdhalf_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gtop_sdhalf_ng
select top cell
box 0.030um 33.195um 0.260um 33.395um
paint metal1
label D c metal1
box 2.350um 33.195um 2.580um 33.395um
paint metal1
label S c metal1
box 0.310um 66.420um 2.300um 66.650um
paint metal1
label G c metal1
box 0.050um 33.145um 0.150um 33.245um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gtop_sdhalf_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gtop_sdhalf_ng
quit -noprompt
