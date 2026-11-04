drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf2_gtop_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W6_L1_m2__nf2_gtop_sdhalf_outD_ng
select top cell
box 1.485um 2.220um 1.745um 2.540um
paint m2c
box 0.190um 2.220um 3.040um 2.540um
paint metal2
label S c metal2
box 0.195um 1.080um 0.455um 1.400um
paint m2c
box 2.775um 1.080um 3.035um 1.400um
paint m2c
box 0.190um 1.080um 3.040um 1.400um
paint metal2
label D c metal2
box 0.325um 3.515um 2.905um 3.745um
paint metal1
label G c metal1
box 0.050um 1.855um 0.150um 1.955um
paint nwell
label B c nwell
save pfet_01v8_lvt_W6_L1_m2__nf2_gtop_sdhalf_outD_ng
gds write pfet_01v8_lvt_W6_L1_m2__nf2_gtop_sdhalf_outD_ng
quit -noprompt
