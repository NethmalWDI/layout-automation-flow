drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdfull_outD
select top cell
box 1.470um 18.755um 1.730um 19.075um
paint m2c
box 0.435um 18.755um 2.765um 19.075um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 2.500um 0.525um 2.760um 0.845um
paint m2c
box 0.435um 0.525um 2.765um 0.845um
paint metal2
label D c metal2
box 0.570um 19.330um 2.630um 19.560um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdfull_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdfull_outD
quit -noprompt
