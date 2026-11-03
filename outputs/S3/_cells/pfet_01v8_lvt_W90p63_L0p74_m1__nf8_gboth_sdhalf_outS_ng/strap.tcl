drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS_ng
select top cell
box 0.195um 8.655um 0.455um 8.975um
paint m2c
box 2.255um 8.655um 2.515um 8.975um
paint m2c
box 4.315um 8.655um 4.575um 8.975um
paint m2c
box 6.375um 8.655um 6.635um 8.975um
paint m2c
box 8.435um 8.655um 8.695um 8.975um
paint m2c
box 0.190um 8.655um 8.700um 8.975um
paint metal2
label S c metal2
box 1.225um 3.355um 1.485um 3.675um
paint m2c
box 3.285um 3.355um 3.545um 3.675um
paint m2c
box 5.345um 3.355um 5.605um 3.675um
paint m2c
box 7.405um 3.355um 7.665um 3.675um
paint m2c
box 0.190um 3.355um 8.700um 3.675um
paint metal2
label D c metal2
box 0.325um 12.035um 8.565um 12.265um
paint metal1
label G c metal1
box 0.050um 6.115um 0.150um 6.215um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outS_ng
quit -noprompt
