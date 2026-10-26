drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outS.gds
load nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outS
select top cell
box 0.440um 2.605um 0.700um 2.925um
paint m2c
box 3.020um 2.605um 3.280um 2.925um
paint m2c
box 5.600um 2.605um 5.860um 2.925um
paint m2c
box 0.420um 2.605um 5.880um 2.925um
paint metal2
label S c metal2
box 1.730um 0.525um 1.990um 0.845um
paint m2c
box 4.310um 0.525um 4.570um 0.845um
paint m2c
box 0.420um 0.525um 5.880um 0.845um
paint metal2
label D c metal2
box 0.570um 3.135um 5.730um 3.365um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outS
gds write nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outS
quit -noprompt
