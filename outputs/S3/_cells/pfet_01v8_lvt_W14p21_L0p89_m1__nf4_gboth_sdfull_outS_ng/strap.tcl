drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outS_ng
select top cell
box 0.195um 3.680um 0.455um 4.000um
paint m2c
box 2.555um 3.680um 2.815um 4.000um
paint m2c
box 4.915um 3.680um 5.175um 4.000um
paint m2c
box 0.190um 3.680um 5.180um 4.000um
paint metal2
label S c metal2
box 1.375um 0.550um 1.635um 0.870um
paint m2c
box 3.735um 0.550um 3.995um 0.870um
paint m2c
box 0.190um 0.550um 5.180um 0.870um
paint metal2
label D c metal2
box 0.325um 4.255um 5.045um 4.485um
paint metal1
label G c metal1
box 0.050um 2.225um 0.150um 2.325um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outS_ng
quit -noprompt
