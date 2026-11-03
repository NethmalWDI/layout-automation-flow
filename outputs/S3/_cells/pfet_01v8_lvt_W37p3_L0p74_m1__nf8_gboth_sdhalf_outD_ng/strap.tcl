drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gboth_sdhalf_outD_ng
select top cell
box 1.225um 3.655um 1.485um 3.975um
paint m2c
box 3.285um 3.655um 3.545um 3.975um
paint m2c
box 5.345um 3.655um 5.605um 3.975um
paint m2c
box 7.405um 3.655um 7.665um 3.975um
paint m2c
box 0.190um 3.655um 8.700um 3.975um
paint metal2
label S c metal2
box 0.195um 1.685um 0.455um 2.005um
paint m2c
box 2.255um 1.685um 2.515um 2.005um
paint m2c
box 4.315um 1.685um 4.575um 2.005um
paint m2c
box 6.375um 1.685um 6.635um 2.005um
paint m2c
box 8.435um 1.685um 8.695um 2.005um
paint m2c
box 0.190um 1.685um 8.700um 2.005um
paint metal2
label D c metal2
box 0.325um 5.365um 8.565um 5.595um
paint metal1
label G c metal1
box 0.050um 2.780um 0.150um 2.880um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gboth_sdhalf_outD_ng
quit -noprompt
