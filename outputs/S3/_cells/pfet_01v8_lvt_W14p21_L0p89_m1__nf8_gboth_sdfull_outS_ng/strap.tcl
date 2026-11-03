drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outS_ng
select top cell
box 0.195um 1.910um 0.455um 2.230um
paint m2c
box 2.555um 1.910um 2.815um 2.230um
paint m2c
box 4.915um 1.910um 5.175um 2.230um
paint m2c
box 7.275um 1.910um 7.535um 2.230um
paint m2c
box 9.635um 1.910um 9.895um 2.230um
paint m2c
box 0.190um 1.910um 9.900um 2.230um
paint metal2
label S c metal2
box 1.375um 0.550um 1.635um 0.870um
paint m2c
box 3.735um 0.550um 3.995um 0.870um
paint m2c
box 6.095um 0.550um 6.355um 0.870um
paint m2c
box 8.455um 0.550um 8.715um 0.870um
paint m2c
box 0.190um 0.550um 9.900um 0.870um
paint metal2
label D c metal2
box 0.325um 2.485um 9.765um 2.715um
paint metal1
label G c metal1
box 0.050um 1.340um 0.150um 1.440um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outS_ng
quit -noprompt
