drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD_ng
select top cell
box 1.225um 55.380um 1.485um 55.700um
paint m2c
box 3.285um 55.380um 3.545um 55.700um
paint m2c
box 5.345um 55.380um 5.605um 55.700um
paint m2c
box 7.405um 55.380um 7.665um 55.700um
paint m2c
box 9.465um 55.380um 9.725um 55.700um
paint m2c
box 11.525um 55.380um 11.785um 55.700um
paint m2c
box 13.585um 55.380um 13.845um 55.700um
paint m2c
box 15.645um 55.380um 15.905um 55.700um
paint m2c
box 0.190um 55.380um 16.940um 55.700um
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
box 10.495um 0.360um 10.755um 0.680um
paint m2c
box 12.555um 0.360um 12.815um 0.680um
paint m2c
box 14.615um 0.360um 14.875um 0.680um
paint m2c
box 16.675um 0.360um 16.935um 0.680um
paint m2c
box 0.190um 0.360um 16.940um 0.680um
paint metal2
label D c metal2
box 0.325um 55.955um 16.805um 56.185um
paint metal1
label G c metal1
box 0.050um 28.075um 0.150um 28.175um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD_ng
quit -noprompt
