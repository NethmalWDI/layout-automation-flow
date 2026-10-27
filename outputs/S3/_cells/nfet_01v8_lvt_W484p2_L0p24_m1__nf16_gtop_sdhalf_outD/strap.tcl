drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD
select top cell
box 0.970um 22.830um 1.230um 23.150um
paint m2c
box 2.030um 22.830um 2.290um 23.150um
paint m2c
box 3.090um 22.830um 3.350um 23.150um
paint m2c
box 4.150um 22.830um 4.410um 23.150um
paint m2c
box 5.210um 22.830um 5.470um 23.150um
paint m2c
box 6.270um 22.830um 6.530um 23.150um
paint m2c
box 7.330um 22.830um 7.590um 23.150um
paint m2c
box 8.390um 22.830um 8.650um 23.150um
paint m2c
box 0.435um 22.830um 9.185um 23.150um
paint metal2
label S c metal2
box 0.440um 8.060um 0.700um 8.380um
paint m2c
box 1.500um 8.060um 1.760um 8.380um
paint m2c
box 2.560um 8.060um 2.820um 8.380um
paint m2c
box 3.620um 8.060um 3.880um 8.380um
paint m2c
box 4.680um 8.060um 4.940um 8.380um
paint m2c
box 5.740um 8.060um 6.000um 8.380um
paint m2c
box 6.800um 8.060um 7.060um 8.380um
paint m2c
box 7.860um 8.060um 8.120um 8.380um
paint m2c
box 8.920um 8.060um 9.180um 8.380um
paint m2c
box 0.435um 8.060um 9.185um 8.380um
paint metal2
label D c metal2
box 0.570um 30.895um 9.050um 31.125um
paint metal1
label G c metal1
box 4.725um -0.085um 4.895um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD
quit -noprompt
