drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD
select top cell
box 2.760um 12.535um 3.020um 12.855um
paint m2c
box 7.400um 12.535um 7.660um 12.855um
paint m2c
box 0.435um 12.535um 9.985um 12.855um
paint metal2
label S c metal2
box 0.440um 4.625um 0.700um 4.945um
paint m2c
box 5.080um 4.625um 5.340um 4.945um
paint m2c
box 9.720um 4.625um 9.980um 4.945um
paint m2c
box 0.435um 4.625um 9.985um 4.945um
paint metal2
label D c metal2
box 0.570um 17.165um 9.850um 17.395um
paint metal1
label G c metal1
box 5.125um -0.085um 5.295um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD
quit -noprompt
