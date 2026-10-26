drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outD
select top cell
box 1.470um 332.775um 1.730um 333.095um
paint m2c
box 0.435um 332.775um 2.765um 333.095um
paint metal2
label S c metal2
box 0.440um 111.375um 0.700um 111.695um
paint m2c
box 2.500um 111.375um 2.760um 111.695um
paint m2c
box 0.435um 111.375um 2.765um 111.695um
paint metal2
label D c metal2
box 0.570um 444.200um 2.630um 444.430um
paint metal1
label G c metal1
box 1.515um -0.085um 1.685um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outD
quit -noprompt
