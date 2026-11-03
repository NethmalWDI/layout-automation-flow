drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdhalf_ng
select top cell
box 0.030um 33.505um 0.260um 33.705um
paint metal1
label D c metal1
box 2.350um 33.505um 2.580um 33.705um
paint metal1
label S c metal1
box 0.310um 66.730um 2.300um 66.960um
paint metal1
label G c metal1
box 0.050um 33.455um 0.150um 33.555um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdhalf_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdhalf_ng
quit -noprompt
