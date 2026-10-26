drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outD
select top cell
box 1.470um 110.985um 1.730um 111.305um
paint m2c
box 3.530um 110.985um 3.790um 111.305um
paint m2c
box 5.590um 110.985um 5.850um 111.305um
paint m2c
box 7.650um 110.985um 7.910um 111.305um
paint m2c
box 0.435um 110.985um 8.945um 111.305um
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
box 0.570um 111.560um 8.810um 111.790um
paint metal1
label G c metal1
box 4.605um -0.085um 4.775um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outD
quit -noprompt
