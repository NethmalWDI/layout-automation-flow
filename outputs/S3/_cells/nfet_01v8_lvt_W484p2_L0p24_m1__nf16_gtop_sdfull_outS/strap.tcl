drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdfull_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdfull_outS
select top cell
box 0.440um 30.365um 0.700um 30.685um
paint m2c
box 1.500um 30.365um 1.760um 30.685um
paint m2c
box 2.560um 30.365um 2.820um 30.685um
paint m2c
box 3.620um 30.365um 3.880um 30.685um
paint m2c
box 4.680um 30.365um 4.940um 30.685um
paint m2c
box 5.740um 30.365um 6.000um 30.685um
paint m2c
box 6.800um 30.365um 7.060um 30.685um
paint m2c
box 7.860um 30.365um 8.120um 30.685um
paint m2c
box 8.920um 30.365um 9.180um 30.685um
paint m2c
box 0.435um 30.365um 9.185um 30.685um
paint metal2
label S c metal2
box 0.970um 0.525um 1.230um 0.845um
paint m2c
box 2.030um 0.525um 2.290um 0.845um
paint m2c
box 3.090um 0.525um 3.350um 0.845um
paint m2c
box 4.150um 0.525um 4.410um 0.845um
paint m2c
box 5.210um 0.525um 5.470um 0.845um
paint m2c
box 6.270um 0.525um 6.530um 0.845um
paint m2c
box 7.330um 0.525um 7.590um 0.845um
paint m2c
box 8.390um 0.525um 8.650um 0.845um
paint m2c
box 0.435um 0.525um 9.185um 0.845um
paint metal2
label D c metal2
box 0.570um 30.895um 9.050um 31.125um
paint metal1
label G c metal1
box 4.725um -0.085um 4.895um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdfull_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdfull_outS
quit -noprompt
