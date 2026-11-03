drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng
select top cell
box 0.210um 444.015um 0.440um 444.215um
paint metal1
label D c metal1
box 1.240um 444.015um 1.470um 444.215um
paint metal1
label S c metal1
box 0.490um 887.735um 1.190um 887.965um
paint metal1
label G c metal1
box 0.050um 443.965um 0.150um 444.065um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdfull_ng
quit -noprompt
