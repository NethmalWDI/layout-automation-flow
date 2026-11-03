drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gtop_sdfull_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gtop_sdfull_ng
select top cell
box 0.210um 18.960um 0.440um 19.160um
paint metal1
label D c metal1
box 1.240um 18.960um 1.470um 19.160um
paint metal1
label S c metal1
box 0.490um 37.815um 1.190um 38.045um
paint metal1
label G c metal1
box 0.050um 19.005um 0.150um 19.105um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gtop_sdfull_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gtop_sdfull_ng
quit -noprompt
