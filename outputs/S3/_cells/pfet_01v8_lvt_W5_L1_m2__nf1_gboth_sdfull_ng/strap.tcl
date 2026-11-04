drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull_ng
select top cell
box 0.210um 3.000um 0.440um 3.200um
paint metal1
label D c metal1
box 1.500um 3.000um 1.730um 3.200um
paint metal1
label S c metal1
box 0.490um 5.705um 1.450um 5.935um
paint metal1
label G c metal1
box 0.050um 2.950um 0.150um 3.050um
paint nwell
label B c nwell
save pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull_ng
gds write pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull_ng
quit -noprompt
