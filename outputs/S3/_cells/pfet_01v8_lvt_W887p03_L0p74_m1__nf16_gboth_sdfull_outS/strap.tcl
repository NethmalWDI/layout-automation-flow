drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS
select top cell
box 0.440um 55.900um 0.700um 56.220um
paint m2c
box 2.500um 55.900um 2.760um 56.220um
paint m2c
box 4.560um 55.900um 4.820um 56.220um
paint m2c
box 6.620um 55.900um 6.880um 56.220um
paint m2c
box 8.680um 55.900um 8.940um 56.220um
paint m2c
box 10.740um 55.900um 11.000um 56.220um
paint m2c
box 12.800um 55.900um 13.060um 56.220um
paint m2c
box 14.860um 55.900um 15.120um 56.220um
paint m2c
box 16.920um 55.900um 17.180um 56.220um
paint m2c
box 0.435um 55.900um 17.185um 56.220um
paint metal2
label S c metal2
box 1.470um 0.880um 1.730um 1.200um
paint m2c
box 3.530um 0.880um 3.790um 1.200um
paint m2c
box 5.590um 0.880um 5.850um 1.200um
paint m2c
box 7.650um 0.880um 7.910um 1.200um
paint m2c
box 9.710um 0.880um 9.970um 1.200um
paint m2c
box 11.770um 0.880um 12.030um 1.200um
paint m2c
box 13.830um 0.880um 14.090um 1.200um
paint m2c
box 15.890um 0.880um 16.150um 1.200um
paint m2c
box 0.435um 0.880um 17.185um 1.200um
paint metal2
label D c metal2
box 0.570um 56.475um 17.050um 56.705um
paint metal1
label G c metal1
box 8.725um -0.085um 8.895um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outS
quit -noprompt
