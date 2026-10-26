drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outS
select top cell
box 0.440um 6.645um 0.700um 6.965um
paint m2c
box 5.080um 6.645um 5.340um 6.965um
paint m2c
box 9.720um 6.645um 9.980um 6.965um
paint m2c
box 14.360um 6.645um 14.620um 6.965um
paint m2c
box 19.000um 6.645um 19.260um 6.965um
paint m2c
box 0.435um 6.645um 19.265um 6.965um
paint metal2
label S c metal2
box 2.760um 2.875um 3.020um 3.195um
paint m2c
box 7.400um 2.875um 7.660um 3.195um
paint m2c
box 12.040um 2.875um 12.300um 3.195um
paint m2c
box 16.680um 2.875um 16.940um 3.195um
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
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdhalf_outS
quit -noprompt
