drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outS.gds
load nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outS
select top cell
box 0.440um 2.385um 0.700um 2.705um
paint m2c
box 2.020um 2.385um 2.280um 2.705um
paint m2c
box 3.600um 2.385um 3.860um 2.705um
paint m2c
box 5.180um 2.385um 5.440um 2.705um
paint m2c
box 6.760um 2.385um 7.020um 2.705um
paint m2c
box 0.435um 2.385um 7.025um 2.705um
paint metal2
label S c metal2
box 1.230um 1.245um 1.490um 1.565um
paint m2c
box 2.810um 1.245um 3.070um 1.565um
paint m2c
box 4.390um 1.245um 4.650um 1.565um
paint m2c
box 5.970um 1.245um 6.230um 1.565um
paint m2c
box 0.435um 1.245um 7.025um 1.565um
paint metal2
label D c metal2
box 0.570um 3.635um 6.890um 3.865um
paint metal1
label G c metal1
box 3.645um -0.085um 3.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outS
gds write nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outS
quit -noprompt
