drc off
gds read pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull_ng.gds
load pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull_ng
select top cell
box 0.210um 1.310um 0.440um 1.510um
paint metal1
label D c metal1
box 5.500um 1.310um 5.730um 1.510um
paint metal1
label S c metal1
box 0.490um 2.515um 5.450um 2.745um
paint metal1
label G c metal1
box 0.050um 1.355um 0.150um 1.455um
paint nwell
label B c nwell
save pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull_ng
gds write pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull_ng
quit -noprompt
