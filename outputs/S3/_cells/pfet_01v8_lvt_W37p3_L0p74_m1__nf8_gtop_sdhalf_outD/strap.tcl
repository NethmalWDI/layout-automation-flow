drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outD
select top cell
box 1.470um 3.630um 1.730um 3.950um
paint m2c
box 3.530um 3.630um 3.790um 3.950um
paint m2c
box 5.590um 3.630um 5.850um 3.950um
paint m2c
box 7.650um 3.630um 7.910um 3.950um
paint m2c
box 0.435um 3.630um 8.945um 3.950um
paint metal2
label S c metal2
box 0.440um 1.660um 0.700um 1.980um
paint m2c
box 2.500um 1.660um 2.760um 1.980um
paint m2c
box 4.560um 1.660um 4.820um 1.980um
paint m2c
box 6.620um 1.660um 6.880um 1.980um
paint m2c
box 8.680um 1.660um 8.940um 1.980um
paint m2c
box 0.435um 1.660um 8.945um 1.980um
paint metal2
label D c metal2
box 0.570um 5.340um 8.810um 5.570um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outD
quit -noprompt
