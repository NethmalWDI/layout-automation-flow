drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD
select top cell
box 1.470um 8.985um 1.730um 9.305um
paint m2c
box 3.530um 8.985um 3.790um 9.305um
paint m2c
box 5.590um 8.985um 5.850um 9.305um
paint m2c
box 7.650um 8.985um 7.910um 9.305um
paint m2c
box 0.435um 8.985um 8.945um 9.305um
paint metal2
label S c metal2
box 0.440um 3.685um 0.700um 4.005um
paint m2c
box 2.500um 3.685um 2.760um 4.005um
paint m2c
box 4.560um 3.685um 4.820um 4.005um
paint m2c
box 6.620um 3.685um 6.880um 4.005um
paint m2c
box 8.680um 3.685um 8.940um 4.005um
paint m2c
box 0.435um 3.685um 8.945um 4.005um
paint metal2
label D c metal2
box 0.570um 12.365um 8.810um 12.595um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD
quit -noprompt
