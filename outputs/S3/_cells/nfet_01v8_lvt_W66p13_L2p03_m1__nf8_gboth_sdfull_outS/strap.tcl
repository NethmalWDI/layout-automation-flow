drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS
select top cell
box 0.440um 8.685um 0.700um 9.005um
paint m2c
box 5.080um 8.685um 5.340um 9.005um
paint m2c
box 9.720um 8.685um 9.980um 9.005um
paint m2c
box 14.360um 8.685um 14.620um 9.005um
paint m2c
box 19.000um 8.685um 19.260um 9.005um
paint m2c
box 0.435um 8.685um 19.265um 9.005um
paint metal2
label S c metal2
box 2.760um 0.835um 3.020um 1.155um
paint m2c
box 7.400um 0.835um 7.660um 1.155um
paint m2c
box 12.040um 0.835um 12.300um 1.155um
paint m2c
box 16.680um 0.835um 16.940um 1.155um
paint m2c
box 0.435um 0.835um 19.265um 1.155um
paint metal2
label D c metal2
box 0.570um 9.215um 19.130um 9.445um
paint metal1
label G c metal1
box 9.765um -0.085um 9.935um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS
quit -noprompt
