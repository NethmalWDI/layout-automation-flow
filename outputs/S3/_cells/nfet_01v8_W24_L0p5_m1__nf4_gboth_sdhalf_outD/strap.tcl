drc off
gds read nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD.gds
load nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
select top cell
box 1.230um 4.945um 1.490um 5.265um
paint m2c
box 2.810um 4.945um 3.070um 5.265um
paint m2c
box 0.435um 4.945um 3.865um 5.265um
paint metal2
label S c metal2
box 0.440um 2.305um 0.700um 2.625um
paint m2c
box 2.020um 2.305um 2.280um 2.625um
paint m2c
box 3.600um 2.305um 3.860um 2.625um
paint m2c
box 0.435um 2.305um 3.865um 2.625um
paint metal2
label D c metal2
box 0.570um 6.945um 3.730um 7.175um
paint metal1
label G c metal1
box 2.065um -0.085um 2.235um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
gds write nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
quit -noprompt
