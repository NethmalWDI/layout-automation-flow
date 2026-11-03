drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS_ng
select top cell
box 0.195um 110.820um 0.455um 111.140um
paint m2c
box 2.255um 110.820um 2.515um 111.140um
paint m2c
box 4.315um 110.820um 4.575um 111.140um
paint m2c
box 6.375um 110.820um 6.635um 111.140um
paint m2c
box 8.435um 110.820um 8.695um 111.140um
paint m2c
box 0.190um 110.820um 8.700um 111.140um
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
box 0.325um 111.395um 8.565um 111.625um
paint metal1
label G c metal1
box 0.050um 55.795um 0.150um 55.895um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS_ng
quit -noprompt
