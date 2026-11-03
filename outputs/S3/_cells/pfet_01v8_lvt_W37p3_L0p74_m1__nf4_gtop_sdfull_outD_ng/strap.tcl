drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdfull_outD_ng
select top cell
box 1.225um 9.270um 1.485um 9.590um
paint m2c
box 3.285um 9.270um 3.545um 9.590um
paint m2c
box 0.190um 9.270um 4.580um 9.590um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.255um 0.360um 2.515um 0.680um
paint m2c
box 4.315um 0.360um 4.575um 0.680um
paint m2c
box 0.190um 0.360um 4.580um 0.680um
paint metal2
label D c metal2
box 0.325um 9.845um 4.445um 10.075um
paint metal1
label G c metal1
box 0.050um 5.020um 0.150um 5.120um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdfull_outD_ng
quit -noprompt
