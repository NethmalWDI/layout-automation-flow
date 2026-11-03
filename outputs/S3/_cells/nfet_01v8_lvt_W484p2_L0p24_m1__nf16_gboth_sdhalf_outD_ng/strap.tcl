drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD_ng
select top cell
box 0.545um 22.795um 0.805um 23.115um
paint m2c
box 1.605um 22.795um 1.865um 23.115um
paint m2c
box 2.665um 22.795um 2.925um 23.115um
paint m2c
box 3.725um 22.795um 3.985um 23.115um
paint m2c
box 4.785um 22.795um 5.045um 23.115um
paint m2c
box 5.845um 22.795um 6.105um 23.115um
paint m2c
box 6.905um 22.795um 7.165um 23.115um
paint m2c
box 7.965um 22.795um 8.225um 23.115um
paint m2c
box 0.010um 22.795um 8.760um 23.115um
paint metal2
label S c metal2
box 0.015um 8.025um 0.275um 8.345um
paint m2c
box 1.075um 8.025um 1.335um 8.345um
paint m2c
box 2.135um 8.025um 2.395um 8.345um
paint m2c
box 3.195um 8.025um 3.455um 8.345um
paint m2c
box 4.255um 8.025um 4.515um 8.345um
paint m2c
box 5.315um 8.025um 5.575um 8.345um
paint m2c
box 6.375um 8.025um 6.635um 8.345um
paint m2c
box 7.435um 8.025um 7.695um 8.345um
paint m2c
box 8.495um 8.025um 8.755um 8.345um
paint m2c
box 0.010um 8.025um 8.760um 8.345um
paint metal2
label D c metal2
box 0.145um 30.860um 8.625um 31.090um
paint metal1
label G c metal1
box 0.050um 15.520um 0.150um 15.620um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdhalf_outD_ng
quit -noprompt
