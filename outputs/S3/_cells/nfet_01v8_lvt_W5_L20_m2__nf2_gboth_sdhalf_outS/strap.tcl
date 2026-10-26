drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdhalf_outS
select top cell
box 0.440um 2.320um 0.700um 2.640um
paint m2c
box 41.020um 2.320um 41.280um 2.640um
paint m2c
box 0.435um 2.320um 41.285um 2.640um
paint metal2
label S c metal2
box 20.730um 1.430um 20.990um 1.750um
paint m2c
box 0.435um 1.430um 41.285um 1.750um
paint metal2
label D c metal2
box 0.570um 3.445um 41.150um 3.675um
paint metal1
label G c metal1
box 20.775um -0.085um 20.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdhalf_outS
quit -noprompt
