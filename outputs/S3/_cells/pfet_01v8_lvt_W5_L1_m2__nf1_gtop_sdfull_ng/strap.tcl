drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull_ng.gds
load pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull_ng
select top cell
box 0.210um 2.810um 0.440um 3.010um
paint metal1
label D c metal1
box 1.500um 2.810um 1.730um 3.010um
paint metal1
label S c metal1
box 0.490um 5.515um 1.450um 5.745um
paint metal1
label G c metal1
box 0.050um 2.855um 0.150um 2.955um
paint nwell
label B c nwell
save pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull_ng
gds write pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull_ng
quit -noprompt
