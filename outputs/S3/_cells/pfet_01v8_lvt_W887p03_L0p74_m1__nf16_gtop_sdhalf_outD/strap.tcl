drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD
select top cell
box 1.470um 41.715um 1.730um 42.035um
paint m2c
box 3.530um 41.715um 3.790um 42.035um
paint m2c
box 5.590um 41.715um 5.850um 42.035um
paint m2c
box 7.650um 41.715um 7.910um 42.035um
paint m2c
box 9.710um 41.715um 9.970um 42.035um
paint m2c
box 11.770um 41.715um 12.030um 42.035um
paint m2c
box 13.830um 41.715um 14.090um 42.035um
paint m2c
box 15.890um 41.715um 16.150um 42.035um
paint m2c
box 0.435um 41.715um 17.185um 42.035um
paint metal2
label S c metal2
box 0.440um 14.355um 0.700um 14.675um
paint m2c
box 2.500um 14.355um 2.760um 14.675um
paint m2c
box 4.560um 14.355um 4.820um 14.675um
paint m2c
box 6.620um 14.355um 6.880um 14.675um
paint m2c
box 8.680um 14.355um 8.940um 14.675um
paint m2c
box 10.740um 14.355um 11.000um 14.675um
paint m2c
box 12.800um 14.355um 13.060um 14.675um
paint m2c
box 14.860um 14.355um 15.120um 14.675um
paint m2c
box 16.920um 14.355um 17.180um 14.675um
paint m2c
box 0.435um 14.355um 17.185um 14.675um
paint metal2
label D c metal2
box 0.570um 56.120um 17.050um 56.350um
paint metal1
label G c metal1
box 8.725um -0.085um 8.895um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD
quit -noprompt
