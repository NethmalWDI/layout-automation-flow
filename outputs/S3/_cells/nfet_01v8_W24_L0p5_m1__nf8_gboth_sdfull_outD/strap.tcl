drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gboth_sdfull_outD.gds
load nfet_01v8_W24_L0p5_m1__nf8_gboth_sdfull_outD
select top cell
box 1.230um 3.415um 1.490um 3.735um
paint m2c
box 2.810um 3.415um 3.070um 3.735um
paint m2c
box 4.390um 3.415um 4.650um 3.735um
paint m2c
box 5.970um 3.415um 6.230um 3.735um
paint m2c
box 0.435um 3.415um 7.025um 3.735um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 2.020um 0.835um 2.280um 1.155um
paint m2c
box 3.600um 0.835um 3.860um 1.155um
paint m2c
box 5.180um 0.835um 5.440um 1.155um
paint m2c
box 6.760um 0.835um 7.020um 1.155um
paint m2c
box 0.435um 0.835um 7.025um 1.155um
paint metal2
label D c metal2
box 0.570um 3.945um 6.890um 4.175um
paint metal1
label G c metal1
box 3.645um -0.085um 3.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf8_gboth_sdfull_outD
gds write nfet_01v8_W24_L0p5_m1__nf8_gboth_sdfull_outD
quit -noprompt
