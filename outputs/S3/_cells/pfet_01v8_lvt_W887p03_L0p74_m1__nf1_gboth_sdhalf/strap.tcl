drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdhalf.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdhalf
select top cell
box 0.455um 444.345um 0.685um 444.545um
paint metal1
label D c metal1
box 1.485um 444.345um 1.715um 444.545um
paint metal1
label S c metal1
box 0.735um 888.065um 1.435um 888.295um
paint metal1
label G c metal1
box 1.000um -0.085um 1.170um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdhalf
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf1_gboth_sdhalf
quit -noprompt
