drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outD_ng
select top cell
box 1.375um 7.050um 1.635um 7.370um
paint m2c
box 0.190um 7.050um 2.820um 7.370um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.555um 0.360um 2.815um 0.680um
paint m2c
box 0.190um 0.360um 2.820um 0.680um
paint metal2
label D c metal2
box 0.325um 7.625um 2.685um 7.855um
paint metal1
label G c metal1
box 0.050um 3.910um 0.150um 4.010um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outD_ng
quit -noprompt
