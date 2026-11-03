drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outD_ng
select top cell
box 1.225um 20.950um 1.485um 21.270um
paint m2c
box 3.285um 20.950um 3.545um 21.270um
paint m2c
box 5.345um 20.950um 5.605um 21.270um
paint m2c
box 7.405um 20.950um 7.665um 21.270um
paint m2c
box 9.465um 20.950um 9.725um 21.270um
paint m2c
box 11.525um 20.950um 11.785um 21.270um
paint m2c
box 13.585um 20.950um 13.845um 21.270um
paint m2c
box 15.645um 20.950um 15.905um 21.270um
paint m2c
box 17.705um 20.950um 17.965um 21.270um
paint m2c
box 19.765um 20.950um 20.025um 21.270um
paint m2c
box 21.825um 20.950um 22.085um 21.270um
paint m2c
box 23.885um 20.950um 24.145um 21.270um
paint m2c
box 25.945um 20.950um 26.205um 21.270um
paint m2c
box 28.005um 20.950um 28.265um 21.270um
paint m2c
box 30.065um 20.950um 30.325um 21.270um
paint m2c
box 32.125um 20.950um 32.385um 21.270um
paint m2c
box 0.190um 20.950um 33.420um 21.270um
paint metal2
label S c metal2
box 0.195um 7.450um 0.455um 7.770um
paint m2c
box 2.255um 7.450um 2.515um 7.770um
paint m2c
box 4.315um 7.450um 4.575um 7.770um
paint m2c
box 6.375um 7.450um 6.635um 7.770um
paint m2c
box 8.435um 7.450um 8.695um 7.770um
paint m2c
box 10.495um 7.450um 10.755um 7.770um
paint m2c
box 12.555um 7.450um 12.815um 7.770um
paint m2c
box 14.615um 7.450um 14.875um 7.770um
paint m2c
box 16.675um 7.450um 16.935um 7.770um
paint m2c
box 18.735um 7.450um 18.995um 7.770um
paint m2c
box 20.795um 7.450um 21.055um 7.770um
paint m2c
box 22.855um 7.450um 23.115um 7.770um
paint m2c
box 24.915um 7.450um 25.175um 7.770um
paint m2c
box 26.975um 7.450um 27.235um 7.770um
paint m2c
box 29.035um 7.450um 29.295um 7.770um
paint m2c
box 31.095um 7.450um 31.355um 7.770um
paint m2c
box 33.155um 7.450um 33.415um 7.770um
paint m2c
box 0.190um 7.450um 33.420um 7.770um
paint metal2
label D c metal2
box 0.325um 28.425um 33.285um 28.655um
paint metal1
label G c metal1
box 0.050um 14.310um 0.150um 14.410um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outD_ng
quit -noprompt
