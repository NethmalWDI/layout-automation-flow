drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS_ng
select top cell
box 0.195um 55.570um 0.455um 55.890um
paint m2c
box 2.255um 55.570um 2.515um 55.890um
paint m2c
box 4.315um 55.570um 4.575um 55.890um
paint m2c
box 6.375um 55.570um 6.635um 55.890um
paint m2c
box 8.435um 55.570um 8.695um 55.890um
paint m2c
box 10.495um 55.570um 10.755um 55.890um
paint m2c
box 12.555um 55.570um 12.815um 55.890um
paint m2c
box 14.615um 55.570um 14.875um 55.890um
paint m2c
box 16.675um 55.570um 16.935um 55.890um
paint m2c
box 0.190um 55.570um 16.940um 55.890um
paint metal2
label S c metal2
box 1.225um 0.550um 1.485um 0.870um
paint m2c
box 3.285um 0.550um 3.545um 0.870um
paint m2c
box 5.345um 0.550um 5.605um 0.870um
paint m2c
box 7.405um 0.550um 7.665um 0.870um
paint m2c
box 9.465um 0.550um 9.725um 0.870um
paint m2c
box 11.525um 0.550um 11.785um 0.870um
paint m2c
box 13.585um 0.550um 13.845um 0.870um
paint m2c
box 15.645um 0.550um 15.905um 0.870um
paint m2c
box 0.190um 0.550um 16.940um 0.870um
paint metal2
label D c metal2
box 0.325um 56.145um 16.805um 56.375um
paint metal1
label G c metal1
box 0.050um 28.170um 0.150um 28.270um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS_ng
quit -noprompt
