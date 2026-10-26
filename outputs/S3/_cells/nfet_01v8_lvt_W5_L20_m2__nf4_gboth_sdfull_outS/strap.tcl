drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS.gds
load nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS
select top cell
box 0.440um 1.665um 0.700um 1.985um
paint m2c
box 41.020um 1.665um 41.280um 1.985um
paint m2c
box 81.600um 1.665um 81.860um 1.985um
paint m2c
box 0.435um 1.665um 81.865um 1.985um
paint metal2
label S c metal2
box 20.730um 0.835um 20.990um 1.155um
paint m2c
box 61.310um 0.835um 61.570um 1.155um
paint m2c
box 0.435um 0.835um 81.865um 1.155um
paint metal2
label D c metal2
box 0.570um 2.195um 81.730um 2.425um
paint metal1
label G c metal1
box 41.065um -0.085um 41.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS
gds write nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS
quit -noprompt
