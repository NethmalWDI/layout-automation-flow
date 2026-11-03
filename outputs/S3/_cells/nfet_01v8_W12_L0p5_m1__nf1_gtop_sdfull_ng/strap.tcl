drc off
gds read nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng.gds
load nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng
select top cell
box 0.030um 6.130um 0.260um 6.330um
paint metal1
label D c metal1
box 0.820um 6.130um 1.050um 6.330um
paint metal1
label S c metal1
box 0.310um 12.290um 0.770um 12.520um
paint metal1
label G c metal1
box 0.050um 6.080um 0.150um 6.180um
paint pwell
label B c pwell
save nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng
gds write nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng
quit -noprompt
