drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdfull_outD_ng
select top cell
box 1.225um 45.450um 1.485um 45.770um
paint m2c
box 0.190um 45.450um 2.520um 45.770um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.255um 0.550um 2.515um 0.870um
paint m2c
box 0.190um 0.550um 2.520um 0.870um
paint metal2
label D c metal2
box 0.325um 46.025um 2.385um 46.255um
paint metal1
label G c metal1
box 0.050um 23.110um 0.150um 23.210um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdfull_outD_ng
quit -noprompt
