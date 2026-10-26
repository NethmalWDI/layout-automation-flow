drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdfull_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdfull_outS
select top cell
box 0.440um 33.175um 0.700um 33.495um
paint m2c
box 5.080um 33.175um 5.340um 33.495um
paint m2c
box 0.435um 33.175um 5.345um 33.495um
paint metal2
label S c metal2
box 2.760um 0.525um 3.020um 0.845um
paint m2c
box 0.435um 0.525um 5.345um 0.845um
paint metal2
label D c metal2
box 0.570um 33.705um 5.210um 33.935um
paint metal1
label G c metal1
box 2.805um -0.085um 2.975um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdfull_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdfull_outS
quit -noprompt
