drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdfull_outD
select top cell
box 2.730um 2.915um 2.990um 3.235um
paint m2c
box 0.435um 2.915um 5.285um 3.235um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 5.020um 0.835um 5.280um 1.155um
paint m2c
box 0.435um 0.835um 5.285um 1.155um
paint metal2
label D c metal2
box 0.570um 3.445um 5.150um 3.675um
paint metal1
label G c metal1
box 2.775um -0.085um 2.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdfull_outD
gds write nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdfull_outD
quit -noprompt
