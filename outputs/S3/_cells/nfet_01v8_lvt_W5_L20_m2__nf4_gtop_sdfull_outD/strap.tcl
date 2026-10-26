drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outD
select top cell
box 20.730um 1.355um 20.990um 1.675um
paint m2c
box 61.310um 1.355um 61.570um 1.675um
paint m2c
box 0.435um 1.355um 81.865um 1.675um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 41.020um 0.525um 41.280um 0.845um
paint m2c
box 81.600um 0.525um 81.860um 0.845um
paint m2c
box 0.435um 0.525um 81.865um 0.845um
paint metal2
label D c metal2
box 0.570um 1.885um 81.730um 2.115um
paint metal1
label G c metal1
box 41.065um -0.085um 41.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outD
gds write nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outD
quit -noprompt
