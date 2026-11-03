drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD_ng
select top cell
box 1.375um 5.490um 1.635um 5.810um
paint m2c
box 0.190um 5.490um 2.820um 5.810um
paint metal2
label S c metal2
box 0.195um 2.300um 0.455um 2.620um
paint m2c
box 2.555um 2.300um 2.815um 2.620um
paint m2c
box 0.190um 2.300um 2.820um 2.620um
paint metal2
label D c metal2
box 0.325um 7.815um 2.685um 8.045um
paint metal1
label G c metal1
box 0.050um 4.005um 0.150um 4.105um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD_ng
quit -noprompt
