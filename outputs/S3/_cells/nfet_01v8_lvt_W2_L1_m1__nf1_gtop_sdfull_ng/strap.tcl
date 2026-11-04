drc off
gds read nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng.gds
load nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng
select top cell
box 0.030um 1.130um 0.260um 1.330um
paint metal1
label D c metal1
box 1.320um 1.130um 1.550um 1.330um
paint metal1
label S c metal1
box 0.310um 2.290um 1.270um 2.520um
paint metal1
label G c metal1
box 0.050um 1.080um 0.150um 1.180um
paint pwell
label B c pwell
save nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng
gds write nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng
quit -noprompt
