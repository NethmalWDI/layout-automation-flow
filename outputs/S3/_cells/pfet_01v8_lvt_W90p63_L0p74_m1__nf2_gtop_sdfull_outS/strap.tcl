drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdfull_outS
select top cell
box 0.440um 45.425um 0.700um 45.745um
paint m2c
box 2.500um 45.425um 2.760um 45.745um
paint m2c
box 0.435um 45.425um 2.765um 45.745um
paint metal2
label S c metal2
box 1.470um 0.525um 1.730um 0.845um
paint m2c
box 0.435um 0.525um 2.765um 0.845um
paint metal2
label D c metal2
box 0.570um 46.000um 2.630um 46.230um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdfull_outS
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdfull_outS
quit -noprompt
