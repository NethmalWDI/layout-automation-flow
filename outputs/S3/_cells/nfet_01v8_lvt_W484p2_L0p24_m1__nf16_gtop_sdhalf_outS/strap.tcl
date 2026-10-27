drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS
select top cell
box 0.440um 22.830um 0.700um 23.150um
paint m2c
box 1.500um 22.830um 1.760um 23.150um
paint m2c
box 2.560um 22.830um 2.820um 23.150um
paint m2c
box 3.620um 22.830um 3.880um 23.150um
paint m2c
box 4.680um 22.830um 4.940um 23.150um
paint m2c
box 5.740um 22.830um 6.000um 23.150um
paint m2c
box 6.800um 22.830um 7.060um 23.150um
paint m2c
box 7.860um 22.830um 8.120um 23.150um
paint m2c
box 8.920um 22.830um 9.180um 23.150um
paint m2c
box 0.435um 22.830um 9.185um 23.150um
paint metal2
label S c metal2
box 0.970um 8.060um 1.230um 8.380um
paint m2c
box 2.030um 8.060um 2.290um 8.380um
paint m2c
box 3.090um 8.060um 3.350um 8.380um
paint m2c
box 4.150um 8.060um 4.410um 8.380um
paint m2c
box 5.210um 8.060um 5.470um 8.380um
paint m2c
box 6.270um 8.060um 6.530um 8.380um
paint m2c
box 7.330um 8.060um 7.590um 8.380um
paint m2c
box 8.390um 8.060um 8.650um 8.380um
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
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS
quit -noprompt
