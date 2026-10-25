drc off
gds read nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outD.gds
load nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outD
select top cell
box 1.230um 9.445um 1.490um 9.765um
paint m2c
box 0.435um 9.445um 2.285um 9.765um
paint metal2
label S c metal2
box 0.440um 3.805um 0.700um 4.125um
paint m2c
box 2.020um 3.805um 2.280um 4.125um
paint m2c
box 0.435um 3.805um 2.285um 4.125um
paint metal2
label D c metal2
box 0.570um 12.945um 2.150um 13.175um
paint metal1
label G c metal1
box 1.275um -0.085um 1.445um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outD
gds write nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outD
quit -noprompt
