drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outD_ng
select top cell
box 1.225um 443.650um 1.485um 443.970um
paint m2c
box 0.190um 443.650um 2.520um 443.970um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.255um 0.550um 2.515um 0.870um
paint m2c
box 0.190um 0.550um 2.520um 0.870um
paint metal2
label D c metal2
box 0.325um 444.225um 2.385um 444.455um
paint metal1
label G c metal1
box 0.050um 222.210um 0.150um 222.310um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outD_ng
quit -noprompt
