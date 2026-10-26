drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outS
select top cell
box 0.440um 111.340um 0.700um 111.660um
paint m2c
box 2.500um 111.340um 2.760um 111.660um
paint m2c
box 4.560um 111.340um 4.820um 111.660um
paint m2c
box 6.620um 111.340um 6.880um 111.660um
paint m2c
box 8.680um 111.340um 8.940um 111.660um
paint m2c
box 0.435um 111.340um 8.945um 111.660um
paint metal2
label S c metal2
box 1.470um 0.880um 1.730um 1.200um
paint m2c
box 3.530um 0.880um 3.790um 1.200um
paint m2c
box 5.590um 0.880um 5.850um 1.200um
paint m2c
box 7.650um 0.880um 7.910um 1.200um
paint m2c
box 0.435um 0.880um 8.945um 1.200um
paint metal2
label D c metal2
box 0.570um 111.915um 8.810um 112.145um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdfull_outS
quit -noprompt
