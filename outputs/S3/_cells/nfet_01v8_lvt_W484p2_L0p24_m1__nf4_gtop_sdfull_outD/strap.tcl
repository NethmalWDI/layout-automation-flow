drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outD
select top cell
box 0.970um 121.155um 1.230um 121.475um
paint m2c
box 2.030um 121.155um 2.290um 121.475um
paint m2c
box 0.435um 121.155um 2.825um 121.475um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 1.500um 0.525um 1.760um 0.845um
paint m2c
box 2.560um 0.525um 2.820um 0.845um
paint m2c
box 0.435um 0.525um 2.825um 0.845um
paint metal2
label D c metal2
box 0.570um 121.685um 2.690um 121.915um
paint metal1
label G c metal1
box 1.545um -0.085um 1.715um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outD
quit -noprompt
