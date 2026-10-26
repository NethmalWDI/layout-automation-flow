drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD
select top cell
box 1.470um 14.125um 1.730um 14.445um
paint m2c
box 0.435um 14.125um 2.765um 14.445um
paint metal2
label S c metal2
box 0.440um 5.155um 0.700um 5.475um
paint m2c
box 2.500um 5.155um 2.760um 5.475um
paint m2c
box 0.435um 5.155um 2.765um 5.475um
paint metal2
label D c metal2
box 0.570um 19.330um 2.630um 19.560um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD
quit -noprompt
