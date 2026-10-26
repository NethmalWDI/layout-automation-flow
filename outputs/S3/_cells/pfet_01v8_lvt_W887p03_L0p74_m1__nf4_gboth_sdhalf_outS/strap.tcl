drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 166.810um 0.700um 167.130um
paint m2c
box 2.500um 166.810um 2.760um 167.130um
paint m2c
box 4.560um 166.810um 4.820um 167.130um
paint m2c
box 0.435um 166.810um 4.825um 167.130um
paint metal2
label S c metal2
box 1.470um 56.290um 1.730um 56.610um
paint m2c
box 3.530um 56.290um 3.790um 56.610um
paint m2c
box 0.435um 56.290um 4.825um 56.610um
paint metal2
label D c metal2
box 0.570um 222.795um 4.690um 223.025um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outS
quit -noprompt
