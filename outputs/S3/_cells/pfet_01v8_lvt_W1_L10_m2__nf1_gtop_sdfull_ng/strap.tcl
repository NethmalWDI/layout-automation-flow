drc off
gds read pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull_ng.gds
load pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull_ng
select top cell
box 0.210um 0.810um 0.440um 1.010um
paint metal1
label D c metal1
box 10.500um 0.810um 10.730um 1.010um
paint metal1
label S c metal1
box 0.490um 1.515um 10.450um 1.745um
paint metal1
label G c metal1
box 0.050um 0.855um 0.150um 0.955um
paint nwell
label B c nwell
save pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull_ng
gds write pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull_ng
quit -noprompt
