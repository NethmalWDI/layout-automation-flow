drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 7.485um 0.700um 7.805um
paint m2c
box 2.500um 7.485um 2.760um 7.805um
paint m2c
box 4.560um 7.485um 4.820um 7.805um
paint m2c
box 0.435um 7.485um 4.825um 7.805um
paint metal2
label S c metal2
box 1.470um 3.185um 1.730um 3.505um
paint m2c
box 3.530um 3.185um 3.790um 3.505um
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
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS
quit -noprompt
