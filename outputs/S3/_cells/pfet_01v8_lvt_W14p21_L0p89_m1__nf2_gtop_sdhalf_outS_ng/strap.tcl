drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outS_ng
select top cell
box 0.195um 5.300um 0.455um 5.620um
paint m2c
box 2.555um 5.300um 2.815um 5.620um
paint m2c
box 0.190um 5.300um 2.820um 5.620um
paint metal2
label S c metal2
box 1.375um 2.110um 1.635um 2.430um
paint m2c
box 0.190um 2.110um 2.820um 2.430um
paint metal2
label D c metal2
box 0.325um 7.625um 2.685um 7.855um
paint metal1
label G c metal1
box 0.050um 3.910um 0.150um 4.010um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outS_ng
quit -noprompt
