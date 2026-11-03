drc off
gds read pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD_ng.gds
load pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD_ng
select top cell
box 1.485um 3.160um 1.745um 3.480um
paint m2c
box 0.190um 3.160um 3.040um 3.480um
paint metal2
label S c metal2
box 0.195um 1.520um 0.455um 1.840um
paint m2c
box 2.775um 1.520um 3.035um 1.840um
paint m2c
box 0.190um 1.520um 3.040um 1.840um
paint metal2
label D c metal2
box 0.325um 4.705um 2.905um 4.935um
paint metal1
label G c metal1
box 0.050um 2.450um 0.150um 2.550um
paint nwell
label B c nwell
save pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD_ng
gds write pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD_ng
quit -noprompt
