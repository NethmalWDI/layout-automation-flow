drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS
select top cell
box 0.440um 17.130um 0.700um 17.450um
paint m2c
box 2.500um 17.130um 2.760um 17.450um
paint m2c
box 4.560um 17.130um 4.820um 17.450um
paint m2c
box 0.435um 17.130um 4.825um 17.450um
paint metal2
label S c metal2
box 1.470um 6.160um 1.730um 6.480um
paint m2c
box 3.530um 6.160um 3.790um 6.480um
paint m2c
box 0.435um 6.160um 4.825um 6.480um
paint metal2
label D c metal2
box 0.570um 23.340um 4.690um 23.570um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS
quit -noprompt
