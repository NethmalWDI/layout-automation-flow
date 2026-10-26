drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outD
select top cell
box 0.970um 242.515um 1.230um 242.835um
paint m2c
box 0.435um 242.515um 1.765um 242.835um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 1.500um 0.835um 1.760um 1.155um
paint m2c
box 0.435um 0.835um 1.765um 1.155um
paint metal2
label D c metal2
box 0.570um 243.045um 1.630um 243.275um
paint metal1
label G c metal1
box 1.015um -0.085um 1.185um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outD
quit -noprompt
