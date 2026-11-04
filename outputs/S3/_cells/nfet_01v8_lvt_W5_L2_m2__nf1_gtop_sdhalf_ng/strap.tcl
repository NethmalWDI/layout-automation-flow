drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf_ng.gds
load nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf_ng
select top cell
box 0.030um 2.630um 0.260um 2.830um
paint metal1
label D c metal1
box 2.320um 2.630um 2.550um 2.830um
paint metal1
label S c metal1
box 0.310um 5.290um 2.270um 5.520um
paint metal1
label G c metal1
box 0.050um 2.580um 0.150um 2.680um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf_ng
gds write nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf_ng
quit -noprompt
