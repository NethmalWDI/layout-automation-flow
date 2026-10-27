drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outD
select top cell
box 1.470um 42.070um 1.730um 42.390um
paint m2c
box 3.530um 42.070um 3.790um 42.390um
paint m2c
box 5.590um 42.070um 5.850um 42.390um
paint m2c
box 7.650um 42.070um 7.910um 42.390um
paint m2c
box 9.710um 42.070um 9.970um 42.390um
paint m2c
box 11.770um 42.070um 12.030um 42.390um
paint m2c
box 13.830um 42.070um 14.090um 42.390um
paint m2c
box 15.890um 42.070um 16.150um 42.390um
paint m2c
box 0.435um 42.070um 17.185um 42.390um
paint metal2
label S c metal2
box 0.440um 14.710um 0.700um 15.030um
paint m2c
box 2.500um 14.710um 2.760um 15.030um
paint m2c
box 4.560um 14.710um 4.820um 15.030um
paint m2c
box 6.620um 14.710um 6.880um 15.030um
paint m2c
box 8.680um 14.710um 8.940um 15.030um
paint m2c
box 10.740um 14.710um 11.000um 15.030um
paint m2c
box 12.800um 14.710um 13.060um 15.030um
paint m2c
box 14.860um 14.710um 15.120um 15.030um
paint m2c
box 16.920um 14.710um 17.180um 15.030um
paint m2c
box 0.435um 14.710um 17.185um 15.030um
paint metal2
label D c metal2
box 0.570um 56.475um 17.050um 56.705um
paint metal1
label G c metal1
box 8.725um -0.085um 8.895um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outD
quit -noprompt
