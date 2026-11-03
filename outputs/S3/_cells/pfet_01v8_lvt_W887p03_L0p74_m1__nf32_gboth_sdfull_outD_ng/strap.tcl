drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outD_ng
select top cell
box 1.225um 27.850um 1.485um 28.170um
paint m2c
box 3.285um 27.850um 3.545um 28.170um
paint m2c
box 5.345um 27.850um 5.605um 28.170um
paint m2c
box 7.405um 27.850um 7.665um 28.170um
paint m2c
box 9.465um 27.850um 9.725um 28.170um
paint m2c
box 11.525um 27.850um 11.785um 28.170um
paint m2c
box 13.585um 27.850um 13.845um 28.170um
paint m2c
box 15.645um 27.850um 15.905um 28.170um
paint m2c
box 17.705um 27.850um 17.965um 28.170um
paint m2c
box 19.765um 27.850um 20.025um 28.170um
paint m2c
box 21.825um 27.850um 22.085um 28.170um
paint m2c
box 23.885um 27.850um 24.145um 28.170um
paint m2c
box 25.945um 27.850um 26.205um 28.170um
paint m2c
box 28.005um 27.850um 28.265um 28.170um
paint m2c
box 30.065um 27.850um 30.325um 28.170um
paint m2c
box 32.125um 27.850um 32.385um 28.170um
paint m2c
box 0.190um 27.850um 33.420um 28.170um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.255um 0.550um 2.515um 0.870um
paint m2c
box 4.315um 0.550um 4.575um 0.870um
paint m2c
box 6.375um 0.550um 6.635um 0.870um
paint m2c
box 8.435um 0.550um 8.695um 0.870um
paint m2c
box 10.495um 0.550um 10.755um 0.870um
paint m2c
box 12.555um 0.550um 12.815um 0.870um
paint m2c
box 14.615um 0.550um 14.875um 0.870um
paint m2c
box 16.675um 0.550um 16.935um 0.870um
paint m2c
box 18.735um 0.550um 18.995um 0.870um
paint m2c
box 20.795um 0.550um 21.055um 0.870um
paint m2c
box 22.855um 0.550um 23.115um 0.870um
paint m2c
box 24.915um 0.550um 25.175um 0.870um
paint m2c
box 26.975um 0.550um 27.235um 0.870um
paint m2c
box 29.035um 0.550um 29.295um 0.870um
paint m2c
box 31.095um 0.550um 31.355um 0.870um
paint m2c
box 33.155um 0.550um 33.415um 0.870um
paint m2c
box 0.190um 0.550um 33.420um 0.870um
paint metal2
label D c metal2
box 0.325um 28.425um 33.285um 28.655um
paint metal1
label G c metal1
box 0.050um 14.310um 0.150um 14.410um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outD_ng
quit -noprompt
