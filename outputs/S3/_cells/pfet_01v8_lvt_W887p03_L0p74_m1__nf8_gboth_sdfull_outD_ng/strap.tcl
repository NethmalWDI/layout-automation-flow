drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outD_ng
select top cell
box 1.225um 111.010um 1.485um 111.330um
paint m2c
box 3.285um 111.010um 3.545um 111.330um
paint m2c
box 5.345um 111.010um 5.605um 111.330um
paint m2c
box 7.405um 111.010um 7.665um 111.330um
paint m2c
box 0.190um 111.010um 8.700um 111.330um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.255um 0.550um 2.515um 0.870um
paint m2c
box 4.315um 0.550um 4.575um 0.870um
paint m2c
box 6.375um 0.550um 6.635um 0.870um
paint m2c
box 8.435um 0.550um 8.695um 0.870um
paint m2c
box 0.190um 0.550um 8.700um 0.870um
paint metal2
label D c metal2
box 0.325um 111.585um 8.565um 111.815um
paint metal1
label G c metal1
box 0.050um 55.890um 0.150um 55.990um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outD_ng
quit -noprompt
