drc off
gds read nfet_01v8_W24_L0p5_m1__nf1_gtop_sdfull_ng.gds
load nfet_01v8_W24_L0p5_m1__nf1_gtop_sdfull_ng
select top cell
box 0.030um 12.130um 0.260um 12.330um
paint metal1
label D c metal1
box 0.820um 12.130um 1.050um 12.330um
paint metal1
label S c metal1
box 0.310um 24.290um 0.770um 24.520um
paint metal1
label G c metal1
box 0.050um 12.080um 0.150um 12.180um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf1_gtop_sdfull_ng
gds write nfet_01v8_W24_L0p5_m1__nf1_gtop_sdfull_ng
quit -noprompt
