drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outS
select top cell
box 0.440um 443.980um 0.700um 444.300um
paint m2c
box 2.500um 443.980um 2.760um 444.300um
paint m2c
box 0.435um 443.980um 2.765um 444.300um
paint metal2
label S c metal2
box 1.470um 0.880um 1.730um 1.200um
paint m2c
box 0.435um 0.880um 2.765um 1.200um
paint metal2
label D c metal2
box 0.570um 444.555um 2.630um 444.785um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gboth_sdfull_outS
quit -noprompt
