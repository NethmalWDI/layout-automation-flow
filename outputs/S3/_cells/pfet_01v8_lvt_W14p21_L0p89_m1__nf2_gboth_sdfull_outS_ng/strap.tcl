drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng
select top cell
box 0.195um 7.240um 0.455um 7.560um
paint m2c
box 2.555um 7.240um 2.815um 7.560um
paint m2c
box 0.190um 7.240um 2.820um 7.560um
paint metal2
label S c metal2
box 1.375um 0.550um 1.635um 0.870um
paint m2c
box 0.190um 0.550um 2.820um 0.870um
paint metal2
label D c metal2
box 0.325um 7.815um 2.685um 8.045um
paint metal1
label G c metal1
box 0.050um 4.005um 0.150um 4.105um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng
quit -noprompt
