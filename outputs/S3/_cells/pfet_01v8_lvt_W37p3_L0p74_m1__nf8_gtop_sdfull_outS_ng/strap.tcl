drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdfull_outS_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdfull_outS_ng
select top cell
box 0.195um 4.600um 0.455um 4.920um
paint m2c
box 2.255um 4.600um 2.515um 4.920um
paint m2c
box 4.315um 4.600um 4.575um 4.920um
paint m2c
box 6.375um 4.600um 6.635um 4.920um
paint m2c
box 8.435um 4.600um 8.695um 4.920um
paint m2c
box 0.190um 4.600um 8.700um 4.920um
paint metal2
label S c metal2
box 1.225um 0.360um 1.485um 0.680um
paint m2c
box 3.285um 0.360um 3.545um 0.680um
paint m2c
box 5.345um 0.360um 5.605um 0.680um
paint m2c
box 7.405um 0.360um 7.665um 0.680um
paint m2c
box 0.190um 0.360um 8.700um 0.680um
paint metal2
label D c metal2
box 0.325um 5.175um 8.565um 5.405um
paint metal1
label G c metal1
box 0.050um 2.685um 0.150um 2.785um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdfull_outS_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdfull_outS_ng
quit -noprompt
