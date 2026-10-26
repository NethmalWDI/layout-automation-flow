drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD
select top cell
box 0.970um 30.675um 1.230um 30.995um
paint m2c
box 2.030um 30.675um 2.290um 30.995um
paint m2c
box 3.090um 30.675um 3.350um 30.995um
paint m2c
box 4.150um 30.675um 4.410um 30.995um
paint m2c
box 5.210um 30.675um 5.470um 30.995um
paint m2c
box 6.270um 30.675um 6.530um 30.995um
paint m2c
box 7.330um 30.675um 7.590um 30.995um
paint m2c
box 8.390um 30.675um 8.650um 30.995um
paint m2c
box 0.435um 30.675um 9.185um 30.995um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 1.500um 0.835um 1.760um 1.155um
paint m2c
box 2.560um 0.835um 2.820um 1.155um
paint m2c
box 3.620um 0.835um 3.880um 1.155um
paint m2c
box 4.680um 0.835um 4.940um 1.155um
paint m2c
box 5.740um 0.835um 6.000um 1.155um
paint m2c
box 6.800um 0.835um 7.060um 1.155um
paint m2c
box 7.860um 0.835um 8.120um 1.155um
paint m2c
box 8.920um 0.835um 9.180um 1.155um
paint m2c
box 0.435um 0.835um 9.185um 1.155um
paint metal2
label D c metal2
box 0.570um 31.205um 9.050um 31.435um
paint metal1
label G c metal1
box 4.725um -0.085um 4.895um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD
quit -noprompt
