drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outS_ng
select top cell
box 0.195um 27.850um 0.455um 28.170um
paint m2c
box 2.255um 27.850um 2.515um 28.170um
paint m2c
box 4.315um 27.850um 4.575um 28.170um
paint m2c
box 6.375um 27.850um 6.635um 28.170um
paint m2c
box 8.435um 27.850um 8.695um 28.170um
paint m2c
box 10.495um 27.850um 10.755um 28.170um
paint m2c
box 12.555um 27.850um 12.815um 28.170um
paint m2c
box 14.615um 27.850um 14.875um 28.170um
paint m2c
box 16.675um 27.850um 16.935um 28.170um
paint m2c
box 18.735um 27.850um 18.995um 28.170um
paint m2c
box 20.795um 27.850um 21.055um 28.170um
paint m2c
box 22.855um 27.850um 23.115um 28.170um
paint m2c
box 24.915um 27.850um 25.175um 28.170um
paint m2c
box 26.975um 27.850um 27.235um 28.170um
paint m2c
box 29.035um 27.850um 29.295um 28.170um
paint m2c
box 31.095um 27.850um 31.355um 28.170um
paint m2c
box 33.155um 27.850um 33.415um 28.170um
paint m2c
box 0.190um 27.850um 33.420um 28.170um
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
box 17.705um 0.550um 17.965um 0.870um
paint m2c
box 19.765um 0.550um 20.025um 0.870um
paint m2c
box 21.825um 0.550um 22.085um 0.870um
paint m2c
box 23.885um 0.550um 24.145um 0.870um
paint m2c
box 25.945um 0.550um 26.205um 0.870um
paint m2c
box 28.005um 0.550um 28.265um 0.870um
paint m2c
box 30.065um 0.550um 30.325um 0.870um
paint m2c
box 32.125um 0.550um 32.385um 0.870um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdfull_outS_ng
quit -noprompt
