drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS.gds
load nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
select top cell
box 0.440um 2.695um 0.700um 3.015um
paint m2c
box 2.020um 2.695um 2.280um 3.015um
paint m2c
box 3.600um 2.695um 3.860um 3.015um
paint m2c
box 5.180um 2.695um 5.440um 3.015um
paint m2c
box 6.760um 2.695um 7.020um 3.015um
paint m2c
box 0.435um 2.695um 7.025um 3.015um
paint metal2
label S c metal2
box 1.230um 1.555um 1.490um 1.875um
paint m2c
box 2.810um 1.555um 3.070um 1.875um
paint m2c
box 4.390um 1.555um 4.650um 1.875um
paint m2c
box 5.970um 1.555um 6.230um 1.875um
paint m2c
box 0.435um 1.555um 7.025um 1.875um
paint metal2
label D c metal2
box 0.570um 3.945um 6.890um 4.175um
paint metal1
label G c metal1
box 3.645um -0.085um 3.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
gds write nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
quit -noprompt
