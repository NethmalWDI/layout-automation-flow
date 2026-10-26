drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD
select top cell
box 4.730um 2.415um 4.990um 2.735um
paint m2c
box 0.435um 2.415um 9.285um 2.735um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 9.020um 0.835um 9.280um 1.155um
paint m2c
box 0.435um 0.835um 9.285um 1.155um
paint metal2
label D c metal2
box 0.570um 2.945um 9.150um 3.175um
paint metal1
label G c metal1
box 4.775um -0.085um 4.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD
gds write nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD
quit -noprompt
