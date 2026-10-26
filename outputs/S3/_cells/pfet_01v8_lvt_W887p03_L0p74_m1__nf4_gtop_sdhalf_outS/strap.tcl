drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdhalf_outS
select top cell
box 0.440um 166.455um 0.700um 166.775um
paint m2c
box 2.500um 166.455um 2.760um 166.775um
paint m2c
box 4.560um 166.455um 4.820um 166.775um
paint m2c
box 0.435um 166.455um 4.825um 166.775um
paint metal2
label S c metal2
box 1.470um 55.935um 1.730um 56.255um
paint m2c
box 3.530um 55.935um 3.790um 56.255um
paint m2c
box 0.435um 55.935um 4.825um 56.255um
paint metal2
label D c metal2
box 0.570um 222.440um 4.690um 222.670um
paint metal1
label G c metal1
box 2.545um -0.085um 2.715um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdhalf_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gtop_sdhalf_outS
quit -noprompt
