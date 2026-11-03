drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
select top cell
box 0.210um 45.815um 0.440um 46.015um
paint metal1
label D c metal1
box 1.240um 45.815um 1.470um 46.015um
paint metal1
label S c metal1
box 0.490um 91.335um 1.190um 91.565um
paint metal1
label G c metal1
box 0.050um 45.765um 0.150um 45.865um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
quit -noprompt
