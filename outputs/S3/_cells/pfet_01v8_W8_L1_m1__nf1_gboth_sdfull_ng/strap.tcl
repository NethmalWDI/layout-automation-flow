drc off
gds read pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng.gds
load pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng
select top cell
box 0.210um 4.500um 0.440um 4.700um
paint metal1
label D c metal1
box 1.500um 4.500um 1.730um 4.700um
paint metal1
label S c metal1
box 0.490um 8.705um 1.450um 8.935um
paint metal1
label G c metal1
box 0.050um 4.450um 0.150um 4.550um
paint nwell
label B c nwell
save pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng
gds write pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng
quit -noprompt
