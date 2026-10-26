drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 91.235um 0.700um 91.555um
paint m2c
box 1.500um 91.235um 1.760um 91.555um
paint m2c
box 2.560um 91.235um 2.820um 91.555um
paint m2c
box 0.435um 91.235um 2.825um 91.555um
paint metal2
label S c metal2
box 0.970um 31.065um 1.230um 31.385um
paint m2c
box 2.030um 31.065um 2.290um 31.385um
paint m2c
box 0.435um 31.065um 2.825um 31.385um
paint metal2
label D c metal2
box 0.570um 121.995um 2.690um 122.225um
paint metal1
label G c metal1
box 1.545um -0.085um 1.715um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdhalf_outS
quit -noprompt
