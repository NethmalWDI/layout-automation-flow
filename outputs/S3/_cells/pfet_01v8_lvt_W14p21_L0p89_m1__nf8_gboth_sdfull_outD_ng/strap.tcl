drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outD_ng
select top cell
box 1.375um 1.910um 1.635um 2.230um
paint m2c
box 3.735um 1.910um 3.995um 2.230um
paint m2c
box 6.095um 1.910um 6.355um 2.230um
paint m2c
box 8.455um 1.910um 8.715um 2.230um
paint m2c
box 0.190um 1.910um 9.900um 2.230um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.555um 0.550um 2.815um 0.870um
paint m2c
box 4.915um 0.550um 5.175um 0.870um
paint m2c
box 7.275um 0.550um 7.535um 0.870um
paint m2c
box 9.635um 0.550um 9.895um 0.870um
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
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdfull_outD_ng
quit -noprompt
