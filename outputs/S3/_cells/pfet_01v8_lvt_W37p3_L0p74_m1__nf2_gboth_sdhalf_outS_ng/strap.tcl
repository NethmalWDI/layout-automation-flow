drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS_ng
select top cell
box 0.195um 14.150um 0.455um 14.470um
paint m2c
box 2.255um 14.150um 2.515um 14.470um
paint m2c
box 0.190um 14.150um 2.520um 14.470um
paint metal2
label S c metal2
box 1.225um 5.180um 1.485um 5.500um
paint m2c
box 0.190um 5.180um 2.520um 5.500um
paint metal2
label D c metal2
box 0.325um 19.355um 2.385um 19.585um
paint metal1
label G c metal1
box 0.050um 9.775um 0.150um 9.875um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS_ng
quit -noprompt
