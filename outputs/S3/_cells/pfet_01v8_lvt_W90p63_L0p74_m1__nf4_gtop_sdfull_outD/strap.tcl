drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdfull_outD
select top cell
box 1.470um 22.765um 1.730um 23.085um
paint m2c
box 3.530um 22.765um 3.790um 23.085um
paint m2c
box 0.435um 22.765um 4.825um 23.085um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 2.500um 0.525um 2.760um 0.845um
paint m2c
box 4.560um 0.525um 4.820um 0.845um
paint m2c
box 0.435um 0.525um 4.825um 0.845um
paint metal2
label D c metal2
box 0.570um 23.340um 4.690um 23.570um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdfull_outD
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdfull_outD
quit -noprompt
