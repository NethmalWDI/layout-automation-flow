drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS
select top cell
box 0.440um 8.630um 0.700um 8.950um
paint m2c
box 2.500um 8.630um 2.760um 8.950um
paint m2c
box 4.560um 8.630um 4.820um 8.950um
paint m2c
box 6.620um 8.630um 6.880um 8.950um
paint m2c
box 8.680um 8.630um 8.940um 8.950um
paint m2c
box 0.435um 8.630um 8.945um 8.950um
paint metal2
label S c metal2
box 1.470um 3.330um 1.730um 3.650um
paint m2c
box 3.530um 3.330um 3.790um 3.650um
paint m2c
box 5.590um 3.330um 5.850um 3.650um
paint m2c
box 7.650um 3.330um 7.910um 3.650um
paint m2c
box 0.435um 3.330um 8.945um 3.650um
paint metal2
label D c metal2
box 0.570um 12.010um 8.810um 12.240um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdhalf_outS
quit -noprompt
