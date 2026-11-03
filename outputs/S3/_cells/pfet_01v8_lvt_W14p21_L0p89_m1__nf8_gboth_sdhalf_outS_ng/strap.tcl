drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS_ng
select top cell
box 0.195um 1.495um 0.455um 1.815um
paint m2c
box 2.555um 1.495um 2.815um 1.815um
paint m2c
box 4.915um 1.495um 5.175um 1.815um
paint m2c
box 7.275um 1.495um 7.535um 1.815um
paint m2c
box 9.635um 1.495um 9.895um 1.815um
paint m2c
box 0.190um 1.495um 9.900um 1.815um
paint metal2
label S c metal2
box 1.375um 0.965um 1.635um 1.285um
paint m2c
box 3.735um 0.965um 3.995um 1.285um
paint m2c
box 6.095um 0.965um 6.355um 1.285um
paint m2c
box 8.455um 0.965um 8.715um 1.285um
paint m2c
box 0.190um 0.965um 9.900um 1.285um
paint metal2
label D c metal2
box 0.325um 2.485um 9.765um 2.715um
paint metal1
label G c metal1
box 0.050um 1.340um 0.150um 1.440um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS_ng
quit -noprompt
