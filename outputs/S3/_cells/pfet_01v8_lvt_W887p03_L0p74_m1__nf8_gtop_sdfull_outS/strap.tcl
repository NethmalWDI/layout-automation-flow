drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS
select top cell
box 0.440um 110.985um 0.700um 111.305um
paint m2c
box 2.500um 110.985um 2.760um 111.305um
paint m2c
box 4.560um 110.985um 4.820um 111.305um
paint m2c
box 6.620um 110.985um 6.880um 111.305um
paint m2c
box 8.680um 110.985um 8.940um 111.305um
paint m2c
box 0.435um 110.985um 8.945um 111.305um
paint metal2
label S c metal2
box 1.470um 0.525um 1.730um 0.845um
paint m2c
box 3.530um 0.525um 3.790um 0.845um
paint m2c
box 5.590um 0.525um 5.850um 0.845um
paint m2c
box 7.650um 0.525um 7.910um 0.845um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf8_gtop_sdfull_outS
quit -noprompt
