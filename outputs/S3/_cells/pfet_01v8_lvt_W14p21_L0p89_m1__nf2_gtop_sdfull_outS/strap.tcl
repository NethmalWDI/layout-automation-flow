drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outS
select top cell
box 0.440um 7.215um 0.700um 7.535um
paint m2c
box 2.800um 7.215um 3.060um 7.535um
paint m2c
box 0.435um 7.215um 3.065um 7.535um
paint metal2
label S c metal2
box 1.620um 0.525um 1.880um 0.845um
paint m2c
box 0.435um 0.525um 3.065um 0.845um
paint metal2
label D c metal2
box 0.570um 7.790um 2.930um 8.020um
paint metal1
label G c metal1
box 1.665um -0.085um 1.835um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outS
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdfull_outS
quit -noprompt
