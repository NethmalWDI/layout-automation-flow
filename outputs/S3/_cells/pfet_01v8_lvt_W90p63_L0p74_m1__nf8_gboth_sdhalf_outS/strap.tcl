drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS
select top cell
box 0.440um 8.985um 0.700um 9.305um
paint m2c
box 2.500um 8.985um 2.760um 9.305um
paint m2c
box 4.560um 8.985um 4.820um 9.305um
paint m2c
box 6.620um 8.985um 6.880um 9.305um
paint m2c
box 8.680um 8.985um 8.940um 9.305um
paint m2c
box 0.435um 8.985um 8.945um 9.305um
paint metal2
label S c metal2
box 1.470um 3.685um 1.730um 4.005um
paint m2c
box 3.530um 3.685um 3.790um 4.005um
paint m2c
box 5.590um 3.685um 5.850um 4.005um
paint m2c
box 7.650um 3.685um 7.910um 4.005um
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
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS
quit -noprompt
