drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outD
select top cell
box 0.970um 60.945um 1.230um 61.265um
paint m2c
box 2.030um 60.945um 2.290um 61.265um
paint m2c
box 3.090um 60.945um 3.350um 61.265um
paint m2c
box 4.150um 60.945um 4.410um 61.265um
paint m2c
box 0.435um 60.945um 4.945um 61.265um
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
box 0.435um 0.835um 4.945um 1.155um
paint metal2
label D c metal2
box 0.570um 61.475um 4.810um 61.705um
paint metal1
label G c metal1
box 2.605um -0.085um 2.775um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outD
quit -noprompt
