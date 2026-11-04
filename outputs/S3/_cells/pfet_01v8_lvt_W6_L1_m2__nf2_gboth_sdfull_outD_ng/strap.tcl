drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdfull_outD_ng.gds
load pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdfull_outD_ng
select top cell
box 1.485um 3.130um 1.745um 3.450um
paint m2c
box 0.190um 3.130um 3.040um 3.450um
paint metal2
label S c metal2
box 0.195um 0.550um 0.455um 0.870um
paint m2c
box 2.775um 0.550um 3.035um 0.870um
paint m2c
box 0.190um 0.550um 3.040um 0.870um
paint metal2
label D c metal2
box 0.325um 3.705um 2.905um 3.935um
paint metal1
label G c metal1
box 0.050um 1.950um 0.150um 2.050um
paint nwell
label B c nwell
save pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdfull_outD_ng
gds write pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdfull_outD_ng
quit -noprompt
