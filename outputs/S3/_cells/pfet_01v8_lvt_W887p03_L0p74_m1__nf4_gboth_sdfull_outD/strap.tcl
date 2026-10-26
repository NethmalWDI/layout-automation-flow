drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outD
select top cell
box 1.470um 222.220um 1.730um 222.540um
paint m2c
box 3.530um 222.220um 3.790um 222.540um
paint m2c
box 0.435um 222.220um 4.825um 222.540um
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
box 0.570um 222.795um 4.690um 223.025um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outD
quit -noprompt
