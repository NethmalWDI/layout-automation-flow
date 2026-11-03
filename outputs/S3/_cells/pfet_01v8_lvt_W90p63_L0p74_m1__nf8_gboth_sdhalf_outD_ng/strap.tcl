drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD_ng
select top cell
box 1.225um 8.655um 1.485um 8.975um
paint m2c
box 3.285um 8.655um 3.545um 8.975um
paint m2c
box 5.345um 8.655um 5.605um 8.975um
paint m2c
box 7.405um 8.655um 7.665um 8.975um
paint m2c
box 0.190um 8.655um 8.700um 8.975um
paint metal2
label S c metal2
box 0.195um 3.355um 0.455um 3.675um
paint m2c
box 2.255um 3.355um 2.515um 3.675um
paint m2c
box 4.315um 3.355um 4.575um 3.675um
paint m2c
box 6.375um 3.355um 6.635um 3.675um
paint m2c
box 8.435um 3.355um 8.695um 3.675um
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
save pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdhalf_outD_ng
quit -noprompt
