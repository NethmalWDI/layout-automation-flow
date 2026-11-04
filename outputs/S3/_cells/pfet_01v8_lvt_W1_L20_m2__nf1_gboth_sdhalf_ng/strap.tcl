drc off
gds read pfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdhalf_ng.gds
load pfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdhalf_ng
select top cell
box 0.210um 1.000um 0.440um 1.200um
paint metal1
label D c metal1
box 20.500um 1.000um 20.730um 1.200um
paint metal1
label S c metal1
box 0.490um 1.705um 20.450um 1.935um
paint metal1
label G c metal1
box 0.050um 0.950um 0.150um 1.050um
paint nwell
label B c nwell
save pfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdhalf_ng
gds write pfet_01v8_lvt_W1_L20_m2__nf1_gboth_sdhalf_ng
quit -noprompt
