drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outS
select top cell
box 0.440um 23.140um 0.700um 23.460um
paint m2c
box 1.500um 23.140um 1.760um 23.460um
paint m2c
box 2.560um 23.140um 2.820um 23.460um
paint m2c
box 3.620um 23.140um 3.880um 23.460um
paint m2c
box 4.680um 23.140um 4.940um 23.460um
paint m2c
box 5.740um 23.140um 6.000um 23.460um
paint m2c
box 6.800um 23.140um 7.060um 23.460um
paint m2c
box 7.860um 23.140um 8.120um 23.460um
paint m2c
box 8.920um 23.140um 9.180um 23.460um
paint m2c
box 0.435um 23.140um 9.185um 23.460um
paint metal2
label S c metal2
box 0.970um 8.370um 1.230um 8.690um
paint m2c
box 2.030um 8.370um 2.290um 8.690um
paint m2c
box 3.090um 8.370um 3.350um 8.690um
paint m2c
box 4.150um 8.370um 4.410um 8.690um
paint m2c
box 5.210um 8.370um 5.470um 8.690um
paint m2c
box 6.270um 8.370um 6.530um 8.690um
paint m2c
box 7.330um 8.370um 7.590um 8.690um
paint m2c
box 8.390um 8.370um 8.650um 8.690um
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
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outS
quit -noprompt
