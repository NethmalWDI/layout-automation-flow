drc off
gds read nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS.gds
load nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS
select top cell
box 0.440um 12.105um 0.700um 12.425um
paint m2c
box 2.020um 12.105um 2.280um 12.425um
paint m2c
box 0.435um 12.105um 2.285um 12.425um
paint metal2
label S c metal2
box 1.230um 0.525um 1.490um 0.845um
paint m2c
box 0.435um 0.525um 2.285um 0.845um
paint metal2
label D c metal2
box 0.570um 12.635um 2.150um 12.865um
paint metal1
label G c metal1
box 1.275um -0.085um 1.445um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS
gds write nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS
quit -noprompt
