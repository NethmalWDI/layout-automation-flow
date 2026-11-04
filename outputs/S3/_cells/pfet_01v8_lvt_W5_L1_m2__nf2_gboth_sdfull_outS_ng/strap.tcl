drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS_ng
select top cell
box 0.195um 2.630um 0.455um 2.950um
paint m2c
box 2.775um 2.630um 3.035um 2.950um
paint m2c
box 0.190um 2.630um 3.040um 2.950um
paint metal2
label S c metal2
box 1.485um 0.550um 1.745um 0.870um
paint m2c
box 0.190um 0.550um 3.040um 0.870um
paint metal2
label D c metal2
box 0.325um 3.205um 2.905um 3.435um
paint metal1
label G c metal1
box 0.050um 1.700um 0.150um 1.800um
paint nwell
label B c nwell
save pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS_ng
quit -noprompt
