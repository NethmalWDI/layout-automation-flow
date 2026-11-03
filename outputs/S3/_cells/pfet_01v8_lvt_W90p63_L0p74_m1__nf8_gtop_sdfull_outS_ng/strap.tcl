drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outS_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outS_ng
select top cell
box 0.195um 11.270um 0.455um 11.590um
paint m2c
box 2.255um 11.270um 2.515um 11.590um
paint m2c
box 4.315um 11.270um 4.575um 11.590um
paint m2c
box 6.375um 11.270um 6.635um 11.590um
paint m2c
box 8.435um 11.270um 8.695um 11.590um
paint m2c
box 0.190um 11.270um 8.700um 11.590um
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
box 0.325um 11.845um 8.565um 12.075um
paint metal1
label G c metal1
box 0.050um 6.020um 0.150um 6.120um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outS_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outS_ng
quit -noprompt
