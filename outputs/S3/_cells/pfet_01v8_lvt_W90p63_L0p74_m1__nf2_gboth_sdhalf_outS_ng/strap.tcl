drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS_ng
select top cell
box 0.195um 34.150um 0.455um 34.470um
paint m2c
box 2.255um 34.150um 2.515um 34.470um
paint m2c
box 0.190um 34.150um 2.520um 34.470um
paint metal2
label S c metal2
box 1.225um 11.850um 1.485um 12.170um
paint m2c
box 0.190um 11.850um 2.520um 12.170um
paint metal2
label D c metal2
box 0.325um 46.025um 2.385um 46.255um
paint metal1
label G c metal1
box 0.050um 23.110um 0.150um 23.210um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS_ng
quit -noprompt
