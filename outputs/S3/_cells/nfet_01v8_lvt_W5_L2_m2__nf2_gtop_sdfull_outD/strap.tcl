drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD
select top cell
box 2.730um 2.605um 2.990um 2.925um
paint m2c
box 0.435um 2.605um 5.285um 2.925um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 5.020um 0.525um 5.280um 0.845um
paint m2c
box 0.435um 0.525um 5.285um 0.845um
paint metal2
label D c metal2
box 0.570um 3.135um 5.150um 3.365um
paint metal1
label G c metal1
box 2.775um -0.085um 2.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD
gds write nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD
quit -noprompt
