drc off
gds read pfet_01v8_lvt_W2_L5_m4__nf1_gboth_sdhalf_ng.gds
load pfet_01v8_lvt_W2_L5_m4__nf1_gboth_sdhalf_ng
select top cell
box 0.210um 1.500um 0.440um 1.700um
paint metal1
label D c metal1
box 5.500um 1.500um 5.730um 1.700um
paint metal1
label S c metal1
box 0.490um 2.705um 5.450um 2.935um
paint metal1
label G c metal1
box 0.050um 1.450um 0.150um 1.550um
paint nwell
label B c nwell
save pfet_01v8_lvt_W2_L5_m4__nf1_gboth_sdhalf_ng
gds write pfet_01v8_lvt_W2_L5_m4__nf1_gboth_sdhalf_ng
quit -noprompt
