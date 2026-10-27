drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS
select top cell
box 0.440um 41.715um 0.700um 42.035um
paint m2c
box 2.500um 41.715um 2.760um 42.035um
paint m2c
box 4.560um 41.715um 4.820um 42.035um
paint m2c
box 6.620um 41.715um 6.880um 42.035um
paint m2c
box 8.680um 41.715um 8.940um 42.035um
paint m2c
box 10.740um 41.715um 11.000um 42.035um
paint m2c
box 12.800um 41.715um 13.060um 42.035um
paint m2c
box 14.860um 41.715um 15.120um 42.035um
paint m2c
box 16.920um 41.715um 17.180um 42.035um
paint m2c
box 0.435um 41.715um 17.185um 42.035um
paint metal2
label S c metal2
box 1.470um 14.355um 1.730um 14.675um
paint m2c
box 3.530um 14.355um 3.790um 14.675um
paint m2c
box 5.590um 14.355um 5.850um 14.675um
paint m2c
box 7.650um 14.355um 7.910um 14.675um
paint m2c
box 9.710um 14.355um 9.970um 14.675um
paint m2c
box 11.770um 14.355um 12.030um 14.675um
paint m2c
box 13.830um 14.355um 14.090um 14.675um
paint m2c
box 15.890um 14.355um 16.150um 14.675um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS
quit -noprompt
