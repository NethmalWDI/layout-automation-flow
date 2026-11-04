drc off
gds read pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdhalf_ng.gds
load pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdhalf_ng
select top cell
box 0.210um 1.200um 0.440um 1.400um
paint metal1
label D c metal1
box 1.100um 1.200um 1.330um 1.400um
paint metal1
label S c metal1
box 0.490um 2.105um 1.050um 2.335um
paint metal1
label G c metal1
box 0.050um 1.150um 0.150um 1.250um
paint nwell
label B c nwell
save pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdhalf_ng
gds write pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gboth_sdhalf_ng
quit -noprompt
