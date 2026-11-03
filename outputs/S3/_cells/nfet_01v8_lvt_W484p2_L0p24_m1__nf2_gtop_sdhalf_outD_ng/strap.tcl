drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outD_ng
select top cell
box 0.545um 181.365um 0.805um 181.685um
paint m2c
box 0.010um 181.365um 1.340um 181.685um
paint metal2
label S c metal2
box 0.015um 60.675um 0.275um 60.995um
paint m2c
box 1.075um 60.675um 1.335um 60.995um
paint m2c
box 0.010um 60.675um 1.340um 60.995um
paint metal2
label D c metal2
box 0.145um 242.390um 1.205um 242.620um
paint metal1
label G c metal1
box 0.050um 121.130um 0.150um 121.230um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outD_ng
quit -noprompt
