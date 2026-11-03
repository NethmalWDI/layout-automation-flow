drc off
gds read pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng.gds
load pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
select top cell
box 1.485um 1.660um 1.745um 1.980um
paint m2c
box 4.065um 1.660um 4.325um 1.980um
paint m2c
box 0.190um 1.660um 5.620um 1.980um
paint metal2
label S c metal2
box 0.195um 1.020um 0.455um 1.340um
paint m2c
box 2.775um 1.020um 3.035um 1.340um
paint m2c
box 5.355um 1.020um 5.615um 1.340um
paint m2c
box 0.190um 1.020um 5.620um 1.340um
paint metal2
label D c metal2
box 0.325um 2.705um 5.485um 2.935um
paint metal1
label G c metal1
box 0.050um 1.450um 0.150um 1.550um
paint nwell
label B c nwell
save pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
gds write pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
quit -noprompt
