drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_c__cc1/x1_cm_bias_c__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_b__cc3/x1_cm_bias_b__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy_2__f3/pmos_dummy_2__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy__f1/pmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_src__id4/x2_cl_src__id4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_casc__cc1/x2_cl_casc__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings1/x1_cc_cm__strings1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_diff__cc1/x2_diff__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_bias_b__f2/x1_diode_bias_b__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_iref__cc1/x1_cm_iref__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC4__A/XC4__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/nmos_dummy__f1/nmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/x1_diode_m2d__f5.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc6/x2_cm_casc__cc6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__cc6/x2_cm_tail__cc6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m3__f1/x1_single_m3__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f3/x1_single_m5__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m4__f1/x1_single_m4__f1.gds
load iadc_ota_v2_placed_budget_aware -silent
box -43.9975um -23.5800um -43.9975um -23.5800um
getcell x1_cm_bias_c__cc1
box -2.8375um -23.5800um -2.8375um -23.5800um
getcell x1_cm_bias_b__cc3
box -80.2375um -53.0700um -80.2375um -53.0700um
getcell pmos_dummy_2__f3 v
box -69.8775um -53.0700um -69.8775um -53.0700um
getcell pmos_dummy__f1 v
box -50.2775um -53.0700um -50.2775um -53.0700um
getcell x2_cl_src__id4
box -22.7175um -53.0700um -22.7175um -53.0700um
getcell x2_cl_casc__cc1 v
box -68.2525um -66.3300um -68.2525um -66.3300um
getcell x1_cc_cm__strings1
box -22.8425um -66.3300um -22.8425um -66.3300um
getcell x2_diff__cc1
box -0.9925um -66.3300um -0.9925um -66.3300um
getcell x1_diode_bias_b__f2
box -49.7225um -76.0200um -49.7225um -76.0200um
getcell x1_cm_iref__cc1
box -75.4325um -88.5200um -75.4325um -88.5200um
getcell XC4__A v
box -32.9025um -88.5200um -32.9025um -88.5200um
getcell nmos_dummy__f1 v
box 9.5675um -88.5200um 9.5675um -88.5200um
getcell XC3__A v
box -47.4925um -143.0600um -47.4925um -143.0600um
getcell x1_diode_m2d__f5
box -24.5625um -143.0600um -24.5625um -143.0600um
getcell x2_cm_casc__cc6 v
box 3.1275um -143.0600um 3.1275um -143.0600um
getcell x2_cm_tail__cc6 v
box -21.8025um -152.0000um -21.8025um -152.0000um
getcell x1_single_m3__f1
box -22.4025um -174.5300um -22.4025um -174.5300um
getcell x1_single_m5__f3
box -30.6825um -183.4700um -30.6825um -183.4700um
getcell x1_single_m4__f1
tech unlock *
tech revert
save iadc_ota_v2_placed_budget_aware
gds write iadc_ota_v2_placed_budget_aware
quit -noprompt
