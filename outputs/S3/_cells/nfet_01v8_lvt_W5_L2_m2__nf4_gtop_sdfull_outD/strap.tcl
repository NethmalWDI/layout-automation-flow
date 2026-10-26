drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD
select top cell
box 2.730um 1.355um 2.990um 1.675um
paint m2c
box 7.310um 1.355um 7.570um 1.675um
paint m2c
box 0.435um 1.355um 9.865um 1.675um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 5.020um 0.525um 5.280um 0.845um
paint m2c
box 9.600um 0.525um 9.860um 0.845um
paint m2c
box 0.435um 0.525um 9.865um 0.845um
paint metal2
label D c metal2
box 0.570um 1.885um 9.730um 2.115um
paint metal1
label G c metal1
box 5.065um -0.085um 5.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD
gds write nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD
quit -noprompt
