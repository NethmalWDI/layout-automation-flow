drc off
gds read nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS.gds
load nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS
select top cell
box 0.440um 6.105um 0.700um 6.425um
paint m2c
box 3.020um 6.105um 3.280um 6.425um
paint m2c
box 5.600um 6.105um 5.860um 6.425um
paint m2c
box 0.435um 6.105um 5.865um 6.425um
paint metal2
label S c metal2
box 1.730um 0.525um 1.990um 0.845um
paint m2c
box 4.310um 0.525um 4.570um 0.845um
paint m2c
box 0.435um 0.525um 5.865um 0.845um
paint metal2
label D c metal2
box 0.570um 6.635um 5.730um 6.865um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS
gds write nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS
quit -noprompt
