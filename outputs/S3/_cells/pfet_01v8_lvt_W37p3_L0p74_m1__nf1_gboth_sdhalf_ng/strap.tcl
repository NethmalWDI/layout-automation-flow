drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng
select top cell
box 0.210um 19.150um 0.440um 19.350um
paint metal1
label D c metal1
box 1.240um 19.150um 1.470um 19.350um
paint metal1
label S c metal1
box 0.490um 38.005um 1.190um 38.235um
paint metal1
label G c metal1
box 0.050um 19.100um 0.150um 19.200um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng
quit -noprompt
