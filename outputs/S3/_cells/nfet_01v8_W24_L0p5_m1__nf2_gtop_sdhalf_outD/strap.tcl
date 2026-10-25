drc off
gds read nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD
select top cell
box 1.230um 9.135um 1.490um 9.455um
paint m2c
box 0.435um 9.135um 2.285um 9.455um
paint metal2
label S c metal2
box 0.440um 3.495um 0.700um 3.815um
paint m2c
box 2.020um 3.495um 2.280um 3.815um
paint m2c
box 0.435um 3.495um 2.285um 3.815um
paint metal2
label D c metal2
box 0.570um 12.635um 2.150um 12.865um
paint metal1
label G c metal1
box 1.275um -0.085um 1.445um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD
gds write nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD
quit -noprompt
