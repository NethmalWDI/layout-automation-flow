drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS.gds
load nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS
select top cell
box 0.440um 1.105um 0.700um 1.425um
paint m2c
box 9.020um 1.105um 9.280um 1.425um
paint m2c
box 17.600um 1.105um 17.860um 1.425um
paint m2c
box 0.435um 1.105um 17.865um 1.425um
paint metal2
label S c metal2
box 4.730um 0.525um 4.990um 0.845um
paint m2c
box 13.310um 0.525um 13.570um 0.845um
paint m2c
box 0.435um 0.525um 17.865um 0.845um
paint metal2
label D c metal2
box 0.570um 1.635um 17.730um 1.865um
paint metal1
label G c metal1
box 9.065um -0.085um 9.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS
gds write nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS
quit -noprompt
