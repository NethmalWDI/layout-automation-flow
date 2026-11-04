drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outD_ng.gds
load pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outD_ng
select top cell
box 1.485um 2.440um 1.745um 2.760um
paint m2c
box 0.190um 2.440um 3.040um 2.760um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.775um 0.360um 3.035um 0.680um
paint m2c
box 0.190um 0.360um 3.040um 0.680um
paint metal2
label D c metal2
box 0.325um 3.015um 2.905um 3.245um
paint metal1
label G c metal1
box 0.050um 1.605um 0.150um 1.705um
paint nwell
label B c nwell
save pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outD_ng
gds write pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outD_ng
quit -noprompt
