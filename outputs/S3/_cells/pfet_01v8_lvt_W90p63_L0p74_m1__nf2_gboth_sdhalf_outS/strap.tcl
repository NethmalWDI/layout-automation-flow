drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS
select top cell
box 0.440um 34.480um 0.700um 34.800um
paint m2c
box 2.500um 34.480um 2.760um 34.800um
paint m2c
box 0.435um 34.480um 2.765um 34.800um
paint metal2
label S c metal2
box 1.470um 12.180um 1.730um 12.500um
paint m2c
box 0.435um 12.180um 2.765um 12.500um
paint metal2
label D c metal2
box 0.570um 46.355um 2.630um 46.585um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS
quit -noprompt
