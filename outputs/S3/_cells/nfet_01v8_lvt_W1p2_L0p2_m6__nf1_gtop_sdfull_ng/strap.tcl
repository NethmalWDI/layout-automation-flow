drc off
gds read nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gtop_sdfull_ng.gds
load nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gtop_sdfull_ng
select top cell
box 0.030um 0.730um 0.260um 0.930um
paint metal1
label D c metal1
box 0.520um 0.730um 0.750um 0.930um
paint metal1
label S c metal1
box 0.205um 1.490um 0.575um 1.720um
paint metal1
box 0.205um 1.490um 0.575um 1.720um
paint metal1
label G c metal1
box 0.050um 0.680um 0.150um 0.780um
paint pwell
label B c pwell
save nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gtop_sdfull_ng
gds write nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gtop_sdfull_ng
quit -noprompt
