drc off
gds read pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outS.gds
load pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outS
select top cell
box 0.440um 3.135um 0.700um 3.455um
paint m2c
box 3.020um 3.135um 3.280um 3.455um
paint m2c
box 0.435um 3.135um 3.285um 3.455um
paint metal2
label S c metal2
box 1.730um 1.495um 1.990um 1.815um
paint m2c
box 0.435um 1.495um 3.285um 1.815um
paint metal2
label D c metal2
box 0.570um 4.680um 3.150um 4.910um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outS
gds write pfet_01v8_W8_L1_m1__nf2_gtop_sdhalf_outS
quit -noprompt
