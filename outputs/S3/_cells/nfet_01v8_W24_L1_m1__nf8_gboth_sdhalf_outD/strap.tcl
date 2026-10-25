drc off
gds read nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outD.gds
load nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outD
select top cell
box 1.730um 2.695um 1.990um 3.015um
paint m2c
box 4.310um 2.695um 4.570um 3.015um
paint m2c
box 6.890um 2.695um 7.150um 3.015um
paint m2c
box 9.470um 2.695um 9.730um 3.015um
paint m2c
box 0.435um 2.695um 11.025um 3.015um
paint metal2
label S c metal2
box 0.440um 1.555um 0.700um 1.875um
paint m2c
box 3.020um 1.555um 3.280um 1.875um
paint m2c
box 5.600um 1.555um 5.860um 1.875um
paint m2c
box 8.180um 1.555um 8.440um 1.875um
paint m2c
box 10.760um 1.555um 11.020um 1.875um
paint m2c
box 0.435um 1.555um 11.025um 1.875um
paint metal2
label D c metal2
box 0.570um 3.945um 10.890um 4.175um
paint metal1
label G c metal1
box 5.645um -0.085um 5.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outD
gds write nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outD
quit -noprompt
