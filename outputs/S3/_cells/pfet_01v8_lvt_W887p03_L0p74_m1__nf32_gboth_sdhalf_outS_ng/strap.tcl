drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outS_ng
select top cell
box 0.195um 20.950um 0.455um 21.270um
paint m2c
box 2.255um 20.950um 2.515um 21.270um
paint m2c
box 4.315um 20.950um 4.575um 21.270um
paint m2c
box 6.375um 20.950um 6.635um 21.270um
paint m2c
box 8.435um 20.950um 8.695um 21.270um
paint m2c
box 10.495um 20.950um 10.755um 21.270um
paint m2c
box 12.555um 20.950um 12.815um 21.270um
paint m2c
box 14.615um 20.950um 14.875um 21.270um
paint m2c
box 16.675um 20.950um 16.935um 21.270um
paint m2c
box 18.735um 20.950um 18.995um 21.270um
paint m2c
box 20.795um 20.950um 21.055um 21.270um
paint m2c
box 22.855um 20.950um 23.115um 21.270um
paint m2c
box 24.915um 20.950um 25.175um 21.270um
paint m2c
box 26.975um 20.950um 27.235um 21.270um
paint m2c
box 29.035um 20.950um 29.295um 21.270um
paint m2c
box 31.095um 20.950um 31.355um 21.270um
paint m2c
box 33.155um 20.950um 33.415um 21.270um
paint m2c
box 0.190um 20.950um 33.420um 21.270um
paint metal2
label S c metal2
box 1.225um 7.450um 1.485um 7.770um
paint m2c
box 3.285um 7.450um 3.545um 7.770um
paint m2c
box 5.345um 7.450um 5.605um 7.770um
paint m2c
box 7.405um 7.450um 7.665um 7.770um
paint m2c
box 9.465um 7.450um 9.725um 7.770um
paint m2c
box 11.525um 7.450um 11.785um 7.770um
paint m2c
box 13.585um 7.450um 13.845um 7.770um
paint m2c
box 15.645um 7.450um 15.905um 7.770um
paint m2c
box 17.705um 7.450um 17.965um 7.770um
paint m2c
box 19.765um 7.450um 20.025um 7.770um
paint m2c
box 21.825um 7.450um 22.085um 7.770um
paint m2c
box 23.885um 7.450um 24.145um 7.770um
paint m2c
box 25.945um 7.450um 26.205um 7.770um
paint m2c
box 28.005um 7.450um 28.265um 7.770um
paint m2c
box 30.065um 7.450um 30.325um 7.770um
paint m2c
box 32.125um 7.450um 32.385um 7.770um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gboth_sdhalf_outS_ng
quit -noprompt
