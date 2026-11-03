drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD_ng
select top cell
box 1.375um 2.635um 1.635um 2.955um
paint m2c
box 3.735um 2.635um 3.995um 2.955um
paint m2c
box 0.190um 2.635um 5.180um 2.955um
paint metal2
label S c metal2
box 0.195um 1.215um 0.455um 1.535um
paint m2c
box 2.555um 1.215um 2.815um 1.535um
paint m2c
box 4.915um 1.215um 5.175um 1.535um
paint m2c
box 0.190um 1.215um 5.180um 1.535um
paint metal2
label D c metal2
box 0.325um 4.065um 5.045um 4.295um
paint metal1
label G c metal1
box 0.050um 2.130um 0.150um 2.230um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD_ng
quit -noprompt
