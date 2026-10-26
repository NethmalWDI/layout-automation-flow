drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD
select top cell
box 0.970um 60.635um 1.230um 60.955um
paint m2c
box 2.030um 60.635um 2.290um 60.955um
paint m2c
box 3.090um 60.635um 3.350um 60.955um
paint m2c
box 4.150um 60.635um 4.410um 60.955um
paint m2c
box 0.435um 60.635um 4.945um 60.955um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 1.500um 0.525um 1.760um 0.845um
paint m2c
box 2.560um 0.525um 2.820um 0.845um
paint m2c
box 3.620um 0.525um 3.880um 0.845um
paint m2c
box 4.680um 0.525um 4.940um 0.845um
paint m2c
box 0.435um 0.525um 4.945um 0.845um
paint metal2
label D c metal2
box 0.570um 61.165um 4.810um 61.395um
paint metal1
label G c metal1
box 2.605um -0.085um 2.775um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD
quit -noprompt
