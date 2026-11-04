drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf1_gboth_sdhalf_ng.gds
load pfet_01v8_lvt_W6_L1_m2__nf1_gboth_sdhalf_ng
select top cell
box 0.210um 3.500um 0.440um 3.700um
paint metal1
label D c metal1
box 1.500um 3.500um 1.730um 3.700um
paint metal1
label S c metal1
box 0.490um 6.705um 1.450um 6.935um
paint metal1
label G c metal1
box 0.050um 3.450um 0.150um 3.550um
paint nwell
label B c nwell
save pfet_01v8_lvt_W6_L1_m2__nf1_gboth_sdhalf_ng
gds write pfet_01v8_lvt_W6_L1_m2__nf1_gboth_sdhalf_ng
quit -noprompt
