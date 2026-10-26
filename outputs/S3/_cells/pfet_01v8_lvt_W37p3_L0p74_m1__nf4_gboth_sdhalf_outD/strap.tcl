drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD
select top cell
box 1.470um 7.485um 1.730um 7.805um
paint m2c
box 3.530um 7.485um 3.790um 7.805um
paint m2c
box 0.435um 7.485um 4.825um 7.805um
paint metal2
label S c metal2
box 0.440um 3.185um 0.700um 3.505um
paint m2c
box 2.500um 3.185um 2.760um 3.505um
paint m2c
box 4.560um 3.185um 4.820um 3.505um
paint m2c
box 0.435um 3.185um 4.825um 3.505um
paint metal2
label D c metal2
box 0.570um 10.365um 4.690um 10.595um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outD
quit -noprompt
