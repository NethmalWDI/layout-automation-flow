drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_b__cc3/x1_cm_bias_b__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_c__cc1/x1_cm_bias_c__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_bias_b__f4/x1_diode_bias_b__f4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_iref__cc3/x1_cm_iref__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m4__f1/x1_single_m4__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f1/x1_diode_m2d__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m3__f1/x1_single_m3__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings1/x1_cc_cm__strings1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f1/x1_single_m5__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy__f1/pmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy_2__f1/pmos_dummy_2__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/nmos_dummy__f1/nmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC4__A/XC4__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_src__cc3/x2_cl_src__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_casc__cc2/x2_cl_casc__cc2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_diff__cc1/x2_diff__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__cc6/x2_cm_tail__cc6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc6/x2_cm_casc__cc6.gds
load iadc_ota_v2_placed_budget_aware -silent
box -52.5975um -23.5800um -52.5975um -23.5800um
getcell x1_cm_bias_b__cc3
box -30.5975um -23.5800um -30.5975um -23.5800um
getcell x1_cm_bias_c__cc1
box -62.8925um -46.6800um -62.8925um -46.6800um
getcell x1_diode_bias_b__f4 v
box -34.6425um -46.6800um -34.6425um -46.6800um
getcell x1_cm_iref__cc3
box -5.7925um -46.6800um -5.7925um -46.6800um
getcell x1_single_m4__f1 v
box -70.8675um -55.6200um -70.8675um -55.6200um
getcell x1_diode_m2d__f1 v
box 10.0625um -55.6200um 10.0625um -55.6200um
getcell x1_single_m3__f1
box -68.2075um -66.0600um -68.2075um -66.0600um
getcell x1_cc_cm__strings1
box -22.7975um -66.0600um -22.7975um -66.0600um
getcell x1_single_m5__f1
box 34.6925um -33.8000um 34.6925um -33.8000um
getcell pmos_dummy__f1
box 54.2925um -33.8000um 54.2925um -33.8000um
getcell pmos_dummy_2__f1
box 32.2675um -41.0600um 32.2675um -41.0600um
getcell nmos_dummy__f1
box 32.2375um -53.5600um 32.2375um -53.5600um
getcell XC3__A
box 32.2375um -66.0600um 32.2375um -66.0600um
getcell XC4__A
box -14.2925um -92.0400um -14.2925um -92.0400um
getcell x2_cl_src__cc3
box 23.3075um -92.0400um 23.3075um -92.0400um
getcell x2_cl_casc__cc2
box 16.1625um -103.1800um 16.1625um -103.1800um
getcell x2_diff__cc1 v
box -65.0675um -156.2200um -65.0675um -156.2200um
getcell x2_cm_tail__cc6 v
box 14.4425um -156.2200um 14.4425um -156.2200um
getcell x2_cm_casc__cc6 v
tech unlock *
tech revert
save iadc_ota_v2_placed_budget_aware
gds write iadc_ota_v2_placed_budget_aware
quit -noprompt
