drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdfull_outD_ng
select top cell
box 1.225um 221.700um 1.485um 222.020um
paint m2c
box 3.285um 221.700um 3.545um 222.020um
paint m2c
box 0.190um 221.700um 4.580um 222.020um
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
box 0.325um 222.275um 4.445um 222.505um
paint metal1
label G c metal1
box 0.050um 111.235um 0.150um 111.335um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdfull_outD_ng
quit -noprompt
