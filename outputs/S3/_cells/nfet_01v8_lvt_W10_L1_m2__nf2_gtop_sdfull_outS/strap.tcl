drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdfull_outS.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdfull_outS
select top cell
box 0.440um 5.105um 0.700um 5.425um
paint m2c
box 3.020um 5.105um 3.280um 5.425um
paint m2c
box 0.435um 5.105um 3.285um 5.425um
paint metal2
label S c metal2
box 1.730um 0.525um 1.990um 0.845um
paint m2c
box 0.435um 0.525um 3.285um 0.845um
paint metal2
label D c metal2
box 0.570um 5.635um 3.150um 5.865um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdfull_outS
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdfull_outS
quit -noprompt
