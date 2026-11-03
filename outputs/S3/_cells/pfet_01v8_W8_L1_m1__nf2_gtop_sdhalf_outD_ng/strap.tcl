drc off
gds read pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outD_ng.gds
load pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outD_ng
select top cell
box 1.485um 2.970um 1.745um 3.290um
paint m2c
box 0.190um 2.970um 3.040um 3.290um
paint metal2
label S c metal2
box 0.195um 1.330um 0.455um 1.650um
paint m2c
box 2.775um 1.330um 3.035um 1.650um
paint m2c
box 0.190um 1.330um 3.040um 1.650um
paint metal2
label D c metal2
box 0.325um 4.515um 2.905um 4.745um
paint metal1
label G c metal1
box 0.050um 2.355um 0.150um 2.455um
paint nwell
label B c nwell
save pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outD_ng
gds write pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outD_ng
quit -noprompt
