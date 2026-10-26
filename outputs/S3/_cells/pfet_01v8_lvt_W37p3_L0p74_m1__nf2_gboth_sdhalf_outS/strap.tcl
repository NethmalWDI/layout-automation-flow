drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS
select top cell
box 0.440um 14.480um 0.700um 14.800um
paint m2c
box 2.500um 14.480um 2.760um 14.800um
paint m2c
box 0.435um 14.480um 2.765um 14.800um
paint metal2
label S c metal2
box 1.470um 5.510um 1.730um 5.830um
paint m2c
box 0.435um 5.510um 2.765um 5.830um
paint metal2
label D c metal2
box 0.570um 19.685um 2.630um 19.915um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdhalf_outS
quit -noprompt
