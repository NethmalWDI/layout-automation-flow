drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outS
select top cell
box 0.440um 45.840um 0.700um 46.160um
paint m2c
box 1.500um 45.840um 1.760um 46.160um
paint m2c
box 2.560um 45.840um 2.820um 46.160um
paint m2c
box 3.620um 45.840um 3.880um 46.160um
paint m2c
box 4.680um 45.840um 4.940um 46.160um
paint m2c
box 0.435um 45.840um 4.945um 46.160um
paint metal2
label S c metal2
box 0.970um 15.940um 1.230um 16.260um
paint m2c
box 2.030um 15.940um 2.290um 16.260um
paint m2c
box 3.090um 15.940um 3.350um 16.260um
paint m2c
box 4.150um 15.940um 4.410um 16.260um
paint m2c
box 0.435um 15.940um 4.945um 16.260um
paint metal2
label D c metal2
box 0.570um 61.475um 4.810um 61.705um
paint metal1
label G c metal1
box 2.605um -0.085um 2.775um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outS
quit -noprompt
