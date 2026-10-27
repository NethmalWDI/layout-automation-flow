drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outD
select top cell
box 1.470um 55.900um 1.730um 56.220um
paint m2c
box 3.530um 55.900um 3.790um 56.220um
paint m2c
box 5.590um 55.900um 5.850um 56.220um
paint m2c
box 7.650um 55.900um 7.910um 56.220um
paint m2c
box 9.710um 55.900um 9.970um 56.220um
paint m2c
box 11.770um 55.900um 12.030um 56.220um
paint m2c
box 13.830um 55.900um 14.090um 56.220um
paint m2c
box 15.890um 55.900um 16.150um 56.220um
paint m2c
box 0.435um 55.900um 17.185um 56.220um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 2.500um 0.880um 2.760um 1.200um
paint m2c
box 4.560um 0.880um 4.820um 1.200um
paint m2c
box 6.620um 0.880um 6.880um 1.200um
paint m2c
box 8.680um 0.880um 8.940um 1.200um
paint m2c
box 10.740um 0.880um 11.000um 1.200um
paint m2c
box 12.800um 0.880um 13.060um 1.200um
paint m2c
box 14.860um 0.880um 15.120um 1.200um
paint m2c
box 16.920um 0.880um 17.180um 1.200um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdfull_outD
quit -noprompt
