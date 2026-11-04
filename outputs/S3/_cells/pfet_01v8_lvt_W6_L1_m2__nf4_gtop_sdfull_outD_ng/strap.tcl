drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD_ng
select top cell
box 1.485um 1.440um 1.745um 1.760um
paint m2c
box 4.065um 1.440um 4.325um 1.760um
paint m2c
box 0.190um 1.440um 5.620um 1.760um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.775um 0.360um 3.035um 0.680um
paint m2c
box 5.355um 0.360um 5.615um 0.680um
paint m2c
box 0.190um 0.360um 5.620um 0.680um
paint metal2
label D c metal2
box 0.325um 2.015um 5.485um 2.245um
paint metal1
label G c metal1
box 0.050um 1.105um 0.150um 1.205um
paint nwell
label B c nwell
save pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD_ng
quit -noprompt
