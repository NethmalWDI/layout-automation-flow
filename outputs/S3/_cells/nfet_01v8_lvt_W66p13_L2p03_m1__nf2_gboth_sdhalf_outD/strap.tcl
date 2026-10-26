drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outD.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outD
select top cell
box 2.760um 25.245um 3.020um 25.565um
paint m2c
box 0.435um 25.245um 5.345um 25.565um
paint metal2
label S c metal2
box 0.440um 9.075um 0.700um 9.395um
paint m2c
box 5.080um 9.075um 5.340um 9.395um
paint m2c
box 0.435um 9.075um 5.345um 9.395um
paint metal2
label D c metal2
box 0.570um 34.015um 5.210um 34.245um
paint metal1
label G c metal1
box 2.805um -0.085um 2.975um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outD
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outD
quit -noprompt
