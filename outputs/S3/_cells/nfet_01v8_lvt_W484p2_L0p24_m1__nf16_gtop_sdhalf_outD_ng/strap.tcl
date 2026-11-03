drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD_ng
select top cell
box 0.545um 22.485um 0.805um 22.805um
paint m2c
box 1.605um 22.485um 1.865um 22.805um
paint m2c
box 2.665um 22.485um 2.925um 22.805um
paint m2c
box 3.725um 22.485um 3.985um 22.805um
paint m2c
box 4.785um 22.485um 5.045um 22.805um
paint m2c
box 5.845um 22.485um 6.105um 22.805um
paint m2c
box 6.905um 22.485um 7.165um 22.805um
paint m2c
box 7.965um 22.485um 8.225um 22.805um
paint m2c
box 0.010um 22.485um 8.760um 22.805um
paint metal2
label S c metal2
box 0.015um 7.715um 0.275um 8.035um
paint m2c
box 1.075um 7.715um 1.335um 8.035um
paint m2c
box 2.135um 7.715um 2.395um 8.035um
paint m2c
box 3.195um 7.715um 3.455um 8.035um
paint m2c
box 4.255um 7.715um 4.515um 8.035um
paint m2c
box 5.315um 7.715um 5.575um 8.035um
paint m2c
box 6.375um 7.715um 6.635um 8.035um
paint m2c
box 7.435um 7.715um 7.695um 8.035um
paint m2c
box 8.495um 7.715um 8.755um 8.035um
paint m2c
box 0.010um 7.715um 8.760um 8.035um
paint metal2
label D c metal2
box 0.145um 30.550um 8.625um 30.780um
paint metal1
label G c metal1
box 0.050um 15.210um 0.150um 15.310um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outD_ng
quit -noprompt
