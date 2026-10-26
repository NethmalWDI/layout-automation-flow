drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outD.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outD
select top cell
box 2.760um 6.645um 3.020um 6.965um
paint m2c
box 7.400um 6.645um 7.660um 6.965um
paint m2c
box 12.040um 6.645um 12.300um 6.965um
paint m2c
box 16.680um 6.645um 16.940um 6.965um
paint m2c
box 0.435um 6.645um 19.265um 6.965um
paint metal2
label S c metal2
box 0.440um 2.875um 0.700um 3.195um
paint m2c
box 5.080um 2.875um 5.340um 3.195um
paint m2c
box 9.720um 2.875um 9.980um 3.195um
paint m2c
box 14.360um 2.875um 14.620um 3.195um
paint m2c
box 19.000um 2.875um 19.260um 3.195um
paint m2c
box 0.435um 2.875um 19.265um 3.195um
paint metal2
label D c metal2
box 0.570um 9.215um 19.130um 9.445um
paint metal1
label G c metal1
box 9.765um -0.085um 9.935um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outD
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outD
quit -noprompt
