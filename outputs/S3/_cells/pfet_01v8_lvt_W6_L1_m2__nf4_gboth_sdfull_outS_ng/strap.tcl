drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS_ng
select top cell
box 0.195um 1.630um 0.455um 1.950um
paint m2c
box 2.775um 1.630um 3.035um 1.950um
paint m2c
box 5.355um 1.630um 5.615um 1.950um
paint m2c
box 0.190um 1.630um 5.620um 1.950um
paint metal2
label S c metal2
box 1.485um 0.550um 1.745um 0.870um
paint m2c
box 4.065um 0.550um 4.325um 0.870um
paint m2c
box 0.190um 0.550um 5.620um 0.870um
paint metal2
label D c metal2
box 0.325um 2.205um 5.485um 2.435um
paint metal1
label G c metal1
box 0.050um 1.200um 0.150um 1.300um
paint nwell
label B c nwell
save pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS_ng
quit -noprompt
