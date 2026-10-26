drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdfull_outD
select top cell
box 1.470um 9.790um 1.730um 10.110um
paint m2c
box 3.530um 9.790um 3.790um 10.110um
paint m2c
box 0.435um 9.790um 4.825um 10.110um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 2.500um 0.880um 2.760um 1.200um
paint m2c
box 4.560um 0.880um 4.820um 1.200um
paint m2c
box 0.435um 0.880um 4.825um 1.200um
paint metal2
label D c metal2
box 0.570um 10.365um 4.690um 10.595um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdfull_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdfull_outD
quit -noprompt
