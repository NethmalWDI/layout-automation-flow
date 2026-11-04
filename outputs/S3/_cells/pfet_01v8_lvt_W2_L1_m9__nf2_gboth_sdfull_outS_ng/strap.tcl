drc off
gds read pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS_ng
select top cell
box 0.195um 1.130um 0.455um 1.450um
paint m2c
box 2.775um 1.130um 3.035um 1.450um
paint m2c
box 0.190um 1.130um 3.040um 1.450um
paint metal2
label S c metal2
box 1.485um 0.550um 1.745um 0.870um
paint m2c
box 0.190um 0.550um 3.040um 0.870um
paint metal2
label D c metal2
box 0.325um 1.705um 2.905um 1.935um
paint metal1
label G c metal1
box 0.050um 0.950um 0.150um 1.050um
paint nwell
label B c nwell
save pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS_ng
quit -noprompt
