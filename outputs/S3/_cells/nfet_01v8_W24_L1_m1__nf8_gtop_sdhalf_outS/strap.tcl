drc off
gds read nfet_01v8_W24_L1_m1__nf8_gtop_sdhalf_outS.gds
load nfet_01v8_W24_L1_m1__nf8_gtop_sdhalf_outS
select top cell
box 0.440um 2.385um 0.700um 2.705um
paint m2c
box 3.020um 2.385um 3.280um 2.705um
paint m2c
box 5.600um 2.385um 5.860um 2.705um
paint m2c
box 8.180um 2.385um 8.440um 2.705um
paint m2c
box 10.760um 2.385um 11.020um 2.705um
paint m2c
box 0.435um 2.385um 11.025um 2.705um
paint metal2
label S c metal2
box 1.730um 1.245um 1.990um 1.565um
paint m2c
box 4.310um 1.245um 4.570um 1.565um
paint m2c
box 6.890um 1.245um 7.150um 1.565um
paint m2c
box 9.470um 1.245um 9.730um 1.565um
paint m2c
box 0.435um 1.245um 11.025um 1.565um
paint metal2
label D c metal2
box 0.570um 3.635um 10.890um 3.865um
paint metal1
label G c metal1
box 5.645um -0.085um 5.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf8_gtop_sdhalf_outS
gds write nfet_01v8_W24_L1_m1__nf8_gtop_sdhalf_outS
quit -noprompt
