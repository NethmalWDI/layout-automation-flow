drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy__f2/pmos_dummy__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_c__cc1/x1_cm_bias_c__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy_2__f2/pmos_dummy_2__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_casc__cc4/x2_cl_casc__cc4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_b__cc3/x1_cm_bias_b__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_src__cc4/x2_cl_src__cc4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC4__A/XC4__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m3__f1/x1_single_m3__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_bias_b__f2/x1_diode_bias_b__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_diff__cc3/x2_diff__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f3/x1_single_m5__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc3/x2_cm_casc__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m4__f1/x1_single_m4__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings1/x1_cc_cm__strings1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f1/x1_diode_m2d__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_iref__cc1/x1_cm_iref__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__id6/x2_cm_tail__id6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/nmos_dummy__f1/nmos_dummy__f1.gds
load iadc_ota_v2_placed_area_only -silent
box -30.4500um -10.5600um -30.4500um -10.5600um
getcell pmos_dummy__f2
box -18.6100um -10.5600um -18.6100um -10.5600um
getcell x1_cm_bias_c__cc1
box 20.9500um -10.5600um 20.9500um -10.5600um
getcell pmos_dummy_2__f2
box -34.8200um -44.4500um -34.8200um -44.4500um
getcell x2_cl_casc__cc4 v
box -10.7400um -44.4500um -10.7400um -44.4500um
getcell x1_cm_bias_b__cc3
box 9.6600um -44.4500um 9.6600um -44.4500um
getcell x2_cl_src__cc4 v
box -39.7800um -55.3500um -39.7800um -55.3500um
getcell XC3__A v
box 1.1500um -55.3500um 1.1500um -55.3500um
getcell XC4__A
box -33.3500um -68.3600um -33.3500um -68.3600um
getcell x1_single_m3__f1
box -16.1800um -68.3600um -16.1800um -68.3600um
getcell x1_diode_bias_b__f2
box -38.4900um -95.2900um -38.4900um -95.2900um
getcell x2_diff__cc3 v
box -26.6400um -95.2900um -26.6400um -95.2900um
getcell x1_single_m5__f3
box -8.2700um -95.2900um -8.2700um -95.2900um
getcell x2_cm_casc__cc3
box -38.9700um -104.1300um -38.9700um -104.1300um
getcell x1_single_m4__f1 v
box -4.0400um -104.1300um -4.0400um -104.1300um
getcell x1_cc_cm__strings1 v
box -39.2650um -110.7200um -39.2650um -110.7200um
getcell x1_diode_m2d__f1
box -36.1050um -118.8100um -36.1050um -118.8100um
getcell x1_cm_iref__cc1 v
box -38.5550um -170.2500um -38.5550um -170.2500um
getcell x2_cm_tail__id6
box -19.2850um -175.7600um -19.2850um -175.7600um
getcell nmos_dummy__f1
tech unlock *
tech revert
save iadc_ota_v2_placed_area_only
gds write iadc_ota_v2_placed_area_only
quit -noprompt
