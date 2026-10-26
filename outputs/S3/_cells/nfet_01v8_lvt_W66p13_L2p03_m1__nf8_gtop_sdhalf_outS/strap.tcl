drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outS
select top cell
box 0.440um 6.335um 0.700um 6.655um
paint m2c
box 5.080um 6.335um 5.340um 6.655um
paint m2c
box 9.720um 6.335um 9.980um 6.655um
paint m2c
box 14.360um 6.335um 14.620um 6.655um
paint m2c
box 19.000um 6.335um 19.260um 6.655um
paint m2c
box 0.435um 6.335um 19.265um 6.655um
paint metal2
label S c metal2
box 2.760um 2.565um 3.020um 2.885um
paint m2c
box 7.400um 2.565um 7.660um 2.885um
paint m2c
box 12.040um 2.565um 12.300um 2.885um
paint m2c
box 16.680um 2.565um 16.940um 2.885um
paint m2c
box 0.435um 2.565um 19.265um 2.885um
paint metal2
label D c metal2
box 0.570um 8.905um 19.130um 9.135um
paint metal1
label G c metal1
box 9.765um -0.085um 9.935um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outS
quit -noprompt
