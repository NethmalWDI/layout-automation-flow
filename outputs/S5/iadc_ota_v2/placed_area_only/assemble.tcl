drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_b__cc3/x1_cm_bias_b__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_c__cc3/x1_cm_bias_c__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f2/x1_single_m5__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m3__f1/x1_single_m3__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f2/x1_diode_m2d__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_iref__cc2/x1_cm_iref__cc2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings1/x1_cc_cm__strings1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m4__f3/x1_single_m4__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_bias_b__f4/x1_diode_bias_b__f4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy__f1/pmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy_2__f1/pmos_dummy_2__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/nmos_dummy__f1/nmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC4__A/XC4__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_src__cc3/x2_cl_src__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_casc__cc2/x2_cl_casc__cc2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_diff__cc3/x2_diff__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/x2_cm_casc__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/x2_cm_tail__id6.gds
load iadc_ota_v2_placed_area_only -silent
box -40.6250um -29.5800um -40.6250um -29.5800um
getcell x1_cm_bias_b__cc3 v
box -19.4250um -29.5800um -19.4250um -29.5800um
getcell x1_cm_bias_c__cc3
box -42.3350um -45.0400um -42.3350um -45.0400um
getcell x1_single_m5__f2 v
box -15.7650um -45.0400um -15.7650um -45.0400um
getcell x1_single_m3__f1 v
box -42.2300um -58.8500um -42.2300um -58.8500um
getcell x1_diode_m2d__f2 v
box -39.2100um -74.1600um -39.2100um -74.1600um
getcell x1_cm_iref__cc2 v
box -42.3700um -83.8000um -42.3700um -83.8000um
getcell x1_cc_cm__strings1
box -42.1950um -105.9500um -42.1950um -105.9500um
getcell x1_single_m4__f3
box -25.3850um -105.9500um -25.3850um -105.9500um
getcell x1_diode_bias_b__f4 v
box 6.5950um -76.0900um 6.5950um -76.0900um
getcell pmos_dummy__f1
box 25.3950um -76.0900um 25.3950um -76.0900um
getcell pmos_dummy_2__f1
box 3.7700um -82.5500um 3.7700um -82.5500um
getcell nmos_dummy__f1
box 3.7400um -94.2500um 3.7400um -94.2500um
getcell XC3__A
box 3.7400um -105.9500um 3.7400um -105.9500um
getcell XC4__A
box -39.2800um -131.1300um -39.2800um -131.1300um
getcell x2_cl_src__cc3
box -2.4800um -131.1300um -2.4800um -131.1300um
getcell x2_cl_casc__cc2
box -29.7050um -159.0100um -29.7050um -159.0100um
getcell x2_diff__cc3 v
box -17.0550um -159.0100um -17.0550um -159.0100um
getcell x2_cm_casc__cc3
box -38.5550um -211.2500um -38.5550um -211.2500um
getcell x2_cm_tail__id6
tech unlock *
tech revert
save iadc_ota_v2_placed_area_only
gds write iadc_ota_v2_placed_area_only
quit -noprompt
