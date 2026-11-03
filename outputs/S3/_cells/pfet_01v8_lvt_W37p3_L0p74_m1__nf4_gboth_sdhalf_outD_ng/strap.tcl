drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD_ng
select top cell
box 1.225um 7.155um 1.485um 7.475um
paint m2c
box 3.285um 7.155um 3.545um 7.475um
paint m2c
box 0.190um 7.155um 4.580um 7.475um
paint metal2
label S c metal2
box 0.195um 2.855um 0.455um 3.175um
paint m2c
box 2.255um 2.855um 2.515um 3.175um
paint m2c
box 4.315um 2.855um 4.575um 3.175um
paint m2c
box 0.190um 2.855um 4.580um 3.175um
paint metal2
label D c metal2
box 0.325um 10.035um 4.445um 10.265um
paint metal1
label G c metal1
box 0.050um 5.115um 0.150um 5.215um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD_ng
quit -noprompt
