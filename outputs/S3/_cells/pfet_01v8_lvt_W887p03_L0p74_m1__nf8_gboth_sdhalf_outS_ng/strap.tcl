drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outS_ng
select top cell
box 0.195um 83.320um 0.455um 83.640um
paint m2c
box 2.255um 83.320um 2.515um 83.640um
paint m2c
box 4.315um 83.320um 4.575um 83.640um
paint m2c
box 6.375um 83.320um 6.635um 83.640um
paint m2c
box 8.435um 83.320um 8.695um 83.640um
paint m2c
box 0.190um 83.320um 8.700um 83.640um
paint metal2
label S c metal2
box 1.225um 28.240um 1.485um 28.560um
paint m2c
box 3.285um 28.240um 3.545um 28.560um
paint m2c
box 5.345um 28.240um 5.605um 28.560um
paint m2c
box 7.405um 28.240um 7.665um 28.560um
paint m2c
box 0.190um 28.240um 8.700um 28.560um
paint metal2
label D c metal2
box 0.325um 111.585um 8.565um 111.815um
paint metal1
label G c metal1
box 0.050um 55.890um 0.150um 55.990um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outS_ng
quit -noprompt
