drc off
gds read nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull_ng.gds
load nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull_ng
select top cell
box 0.030um 0.830um 0.260um 1.030um
paint metal1
label D c metal1
box 0.920um 0.830um 1.150um 1.030um
paint metal1
label S c metal1
box 0.310um 1.690um 0.870um 1.920um
paint metal1
label G c metal1
box 0.050um 0.780um 0.150um 0.880um
paint pwell
label B c pwell
save nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull_ng
gds write nfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull_ng
quit -noprompt
