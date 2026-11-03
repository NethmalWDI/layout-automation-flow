drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outD_ng
select top cell
box 1.375um 3.490um 1.635um 3.810um
paint m2c
box 3.735um 3.490um 3.995um 3.810um
paint m2c
box 0.190um 3.490um 5.180um 3.810um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.555um 0.360um 2.815um 0.680um
paint m2c
box 4.915um 0.360um 5.175um 0.680um
paint m2c
box 0.190um 0.360um 5.180um 0.680um
paint metal2
label D c metal2
box 0.325um 4.065um 5.045um 4.295um
paint metal1
label G c metal1
box 0.050um 2.130um 0.150um 2.230um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outD_ng
quit -noprompt
