drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD
select top cell
box 4.730um 1.415um 4.990um 1.735um
paint m2c
box 13.310um 1.415um 13.570um 1.735um
paint m2c
box 0.435um 1.415um 17.865um 1.735um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 9.020um 0.835um 9.280um 1.155um
paint m2c
box 17.600um 0.835um 17.860um 1.155um
paint m2c
box 0.435um 0.835um 17.865um 1.155um
paint metal2
label D c metal2
box 0.570um 1.945um 17.730um 2.175um
paint metal1
label G c metal1
box 9.065um -0.085um 9.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD
gds write nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD
quit -noprompt
