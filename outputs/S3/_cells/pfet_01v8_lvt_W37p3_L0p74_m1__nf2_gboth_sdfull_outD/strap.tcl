drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdfull_outD
select top cell
box 1.470um 19.110um 1.730um 19.430um
paint m2c
box 0.435um 19.110um 2.765um 19.430um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 2.500um 0.880um 2.760um 1.200um
paint m2c
box 0.435um 0.880um 2.765um 1.200um
paint metal2
label D c metal2
box 0.570um 19.685um 2.630um 19.915um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdfull_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gboth_sdfull_outD
quit -noprompt
