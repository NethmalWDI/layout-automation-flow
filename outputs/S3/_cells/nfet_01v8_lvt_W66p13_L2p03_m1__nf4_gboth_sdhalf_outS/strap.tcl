drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 12.845um 0.700um 13.165um
paint m2c
box 5.080um 12.845um 5.340um 13.165um
paint m2c
box 9.720um 12.845um 9.980um 13.165um
paint m2c
box 0.435um 12.845um 9.985um 13.165um
paint metal2
label S c metal2
box 2.760um 4.935um 3.020um 5.255um
paint m2c
box 7.400um 4.935um 7.660um 5.255um
paint m2c
box 0.435um 4.935um 9.985um 5.255um
paint metal2
label D c metal2
box 0.570um 17.475um 9.850um 17.705um
paint metal1
label G c metal1
box 5.125um -0.085um 5.295um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outS
quit -noprompt
