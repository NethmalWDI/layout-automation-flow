drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD
select top cell
box 1.470um 11.435um 1.730um 11.755um
paint m2c
box 3.530um 11.435um 3.790um 11.755um
paint m2c
box 5.590um 11.435um 5.850um 11.755um
paint m2c
box 7.650um 11.435um 7.910um 11.755um
paint m2c
box 0.435um 11.435um 8.945um 11.755um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 2.500um 0.525um 2.760um 0.845um
paint m2c
box 4.560um 0.525um 4.820um 0.845um
paint m2c
box 6.620um 0.525um 6.880um 0.845um
paint m2c
box 8.680um 0.525um 8.940um 0.845um
paint m2c
box 0.435um 0.525um 8.945um 0.845um
paint metal2
label D c metal2
box 0.570um 12.010um 8.810um 12.240um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gtop_sdfull_outD
quit -noprompt
