drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outD
select top cell
box 1.470um 83.650um 1.730um 83.970um
paint m2c
box 3.530um 83.650um 3.790um 83.970um
paint m2c
box 5.590um 83.650um 5.850um 83.970um
paint m2c
box 7.650um 83.650um 7.910um 83.970um
paint m2c
box 0.435um 83.650um 8.945um 83.970um
paint metal2
label S c metal2
box 0.440um 28.570um 0.700um 28.890um
paint m2c
box 2.500um 28.570um 2.760um 28.890um
paint m2c
box 4.560um 28.570um 4.820um 28.890um
paint m2c
box 6.620um 28.570um 6.880um 28.890um
paint m2c
box 8.680um 28.570um 8.940um 28.890um
paint m2c
box 0.435um 28.570um 8.945um 28.890um
paint metal2
label D c metal2
box 0.570um 111.915um 8.810um 112.145um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gboth_sdhalf_outD
quit -noprompt
