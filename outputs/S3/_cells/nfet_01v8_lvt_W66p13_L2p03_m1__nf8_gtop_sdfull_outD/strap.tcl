drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdfull_outD.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdfull_outD
select top cell
box 2.760um 8.375um 3.020um 8.695um
paint m2c
box 7.400um 8.375um 7.660um 8.695um
paint m2c
box 12.040um 8.375um 12.300um 8.695um
paint m2c
box 16.680um 8.375um 16.940um 8.695um
paint m2c
box 0.435um 8.375um 19.265um 8.695um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 5.080um 0.525um 5.340um 0.845um
paint m2c
box 9.720um 0.525um 9.980um 0.845um
paint m2c
box 14.360um 0.525um 14.620um 0.845um
paint m2c
box 19.000um 0.525um 19.260um 0.845um
paint m2c
box 0.435um 0.525um 19.265um 0.845um
paint metal2
label D c metal2
box 0.570um 8.905um 19.130um 9.135um
paint metal1
label G c metal1
box 9.765um -0.085um 9.935um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdfull_outD
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdfull_outD
quit -noprompt
