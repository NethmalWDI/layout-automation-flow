drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD
select top cell
box 1.470um 34.125um 1.730um 34.445um
paint m2c
box 0.435um 34.125um 2.765um 34.445um
paint metal2
label S c metal2
box 0.440um 11.825um 0.700um 12.145um
paint m2c
box 2.500um 11.825um 2.760um 12.145um
paint m2c
box 0.435um 11.825um 2.765um 12.145um
paint metal2
label D c metal2
box 0.570um 46.000um 2.630um 46.230um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD
quit -noprompt
