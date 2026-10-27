drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD
select top cell
box 0.970um 23.140um 1.230um 23.460um
paint m2c
box 2.030um 23.140um 2.290um 23.460um
paint m2c
box 3.090um 23.140um 3.350um 23.460um
paint m2c
box 4.150um 23.140um 4.410um 23.460um
paint m2c
box 5.210um 23.140um 5.470um 23.460um
paint m2c
box 6.270um 23.140um 6.530um 23.460um
paint m2c
box 7.330um 23.140um 7.590um 23.460um
paint m2c
box 8.390um 23.140um 8.650um 23.460um
paint m2c
box 0.435um 23.140um 9.185um 23.460um
paint metal2
label S c metal2
box 0.440um 8.370um 0.700um 8.690um
paint m2c
box 1.500um 8.370um 1.760um 8.690um
paint m2c
box 2.560um 8.370um 2.820um 8.690um
paint m2c
box 3.620um 8.370um 3.880um 8.690um
paint m2c
box 4.680um 8.370um 4.940um 8.690um
paint m2c
box 5.740um 8.370um 6.000um 8.690um
paint m2c
box 6.800um 8.370um 7.060um 8.690um
paint m2c
box 7.860um 8.370um 8.120um 8.690um
paint m2c
box 8.920um 8.370um 9.180um 8.690um
paint m2c
box 0.435um 8.370um 9.185um 8.690um
paint metal2
label D c metal2
box 0.570um 31.205um 9.050um 31.435um
paint metal1
label G c metal1
box 4.725um -0.085um 4.895um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD
quit -noprompt
