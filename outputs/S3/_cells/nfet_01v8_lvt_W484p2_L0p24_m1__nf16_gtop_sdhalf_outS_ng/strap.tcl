drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS_ng
select top cell
box 0.015um 22.485um 0.275um 22.805um
paint m2c
box 1.075um 22.485um 1.335um 22.805um
paint m2c
box 2.135um 22.485um 2.395um 22.805um
paint m2c
box 3.195um 22.485um 3.455um 22.805um
paint m2c
box 4.255um 22.485um 4.515um 22.805um
paint m2c
box 5.315um 22.485um 5.575um 22.805um
paint m2c
box 6.375um 22.485um 6.635um 22.805um
paint m2c
box 7.435um 22.485um 7.695um 22.805um
paint m2c
box 8.495um 22.485um 8.755um 22.805um
paint m2c
box 0.010um 22.485um 8.760um 22.805um
paint metal2
label S c metal2
box 0.545um 7.715um 0.805um 8.035um
paint m2c
box 1.605um 7.715um 1.865um 8.035um
paint m2c
box 2.665um 7.715um 2.925um 8.035um
paint m2c
box 3.725um 7.715um 3.985um 8.035um
paint m2c
box 4.785um 7.715um 5.045um 8.035um
paint m2c
box 5.845um 7.715um 6.105um 8.035um
paint m2c
box 6.905um 7.715um 7.165um 8.035um
paint m2c
box 7.965um 7.715um 8.225um 8.035um
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
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gtop_sdhalf_outS_ng
quit -noprompt
