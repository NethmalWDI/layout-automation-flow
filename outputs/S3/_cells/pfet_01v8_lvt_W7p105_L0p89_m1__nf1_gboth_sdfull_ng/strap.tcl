drc off
gds read pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
select top cell
box 0.210um 4.055um 0.440um 4.255um
paint metal1
label D c metal1
box 1.390um 4.055um 1.620um 4.255um
paint metal1
label S c metal1
box 0.490um 7.815um 1.340um 8.045um
paint metal1
label G c metal1
box 0.050um 4.005um 0.150um 4.105um
paint nwell
label B c nwell
save pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
gds write pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
quit -noprompt
