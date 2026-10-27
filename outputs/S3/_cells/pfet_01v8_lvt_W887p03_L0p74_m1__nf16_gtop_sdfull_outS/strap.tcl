drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outS
select top cell
box 0.440um 55.545um 0.700um 55.865um
paint m2c
box 2.500um 55.545um 2.760um 55.865um
paint m2c
box 4.560um 55.545um 4.820um 55.865um
paint m2c
box 6.620um 55.545um 6.880um 55.865um
paint m2c
box 8.680um 55.545um 8.940um 55.865um
paint m2c
box 10.740um 55.545um 11.000um 55.865um
paint m2c
box 12.800um 55.545um 13.060um 55.865um
paint m2c
box 14.860um 55.545um 15.120um 55.865um
paint m2c
box 16.920um 55.545um 17.180um 55.865um
paint m2c
box 0.435um 55.545um 17.185um 55.865um
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
box 9.710um 0.525um 9.970um 0.845um
paint m2c
box 11.770um 0.525um 12.030um 0.845um
paint m2c
box 13.830um 0.525um 14.090um 0.845um
paint m2c
box 15.890um 0.525um 16.150um 0.845um
paint m2c
box 0.435um 0.525um 17.185um 0.845um
paint metal2
label D c metal2
box 0.570um 56.120um 17.050um 56.350um
paint metal1
label G c metal1
box 8.725um -0.085um 8.895um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outS
quit -noprompt
