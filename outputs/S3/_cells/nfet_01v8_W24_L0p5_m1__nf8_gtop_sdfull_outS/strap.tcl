drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS.gds
load nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS
select top cell
box 0.440um 3.105um 0.700um 3.425um
paint m2c
box 2.020um 3.105um 2.280um 3.425um
paint m2c
box 3.600um 3.105um 3.860um 3.425um
paint m2c
box 5.180um 3.105um 5.440um 3.425um
paint m2c
box 6.760um 3.105um 7.020um 3.425um
paint m2c
box 0.435um 3.105um 7.025um 3.425um
paint metal2
label S c metal2
box 1.230um 0.525um 1.490um 0.845um
paint m2c
box 2.810um 0.525um 3.070um 0.845um
paint m2c
box 4.390um 0.525um 4.650um 0.845um
paint m2c
box 5.970um 0.525um 6.230um 0.845um
paint m2c
box 0.435um 0.525um 7.025um 0.845um
paint metal2
label D c metal2
box 0.570um 3.635um 6.890um 3.865um
paint metal1
label G c metal1
box 3.645um -0.085um 3.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS
gds write nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS
quit -noprompt
