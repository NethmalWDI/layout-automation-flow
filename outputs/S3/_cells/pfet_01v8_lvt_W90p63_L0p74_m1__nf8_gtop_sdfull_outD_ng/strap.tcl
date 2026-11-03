drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD_ng
select top cell
box 1.225um 11.270um 1.485um 11.590um
paint m2c
box 3.285um 11.270um 3.545um 11.590um
paint m2c
box 5.345um 11.270um 5.605um 11.590um
paint m2c
box 7.405um 11.270um 7.665um 11.590um
paint m2c
box 0.190um 11.270um 8.700um 11.590um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.255um 0.360um 2.515um 0.680um
paint m2c
box 4.315um 0.360um 4.575um 0.680um
paint m2c
box 6.375um 0.360um 6.635um 0.680um
paint m2c
box 8.435um 0.360um 8.695um 0.680um
paint m2c
box 0.190um 0.360um 8.700um 0.680um
paint metal2
label D c metal2
box 0.325um 11.845um 8.565um 12.075um
paint metal1
label G c metal1
box 0.050um 6.020um 0.150um 6.120um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD_ng
quit -noprompt
