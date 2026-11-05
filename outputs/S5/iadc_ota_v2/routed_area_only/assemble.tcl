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
load iadc_ota_v2_routed -silent
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
box -22.6000um -30.6000um -18.2000um -30.2000um
paint metal3
box -22.6000um -30.6000um -22.2000um -27.0000um
paint metal4
box -18.6000um -30.6000um -18.2000um -28.6000um
paint metal4
box -22.6000um -30.6000um -22.2000um -30.2000um
paint via3
box -18.6000um -30.6000um -18.2000um -30.2000um
paint via3
box -18.6000um -29.1100um -18.2000um -28.1700um
paint metal4
box -18.6000um -28.6800um -18.2000um -28.2800um
paint via3
box -22.6000um -27.6900um -22.2000um -26.8900um
paint metal4
box -22.6000um -27.5800um -22.2000um -27.1800um
paint via3
box -19.4000um -34.6000um -17.4000um -34.2000um
paint metal3
box -22.6000um -12.2000um -19.0000um -11.8000um
paint metal3
box -22.6000um -12.2000um -22.2000um -9.4000um
paint metal4
box -19.4000um -34.6000um -19.0000um -11.8000um
paint metal4
box -17.8000um -34.6000um -17.4000um -25.4000um
paint metal4
box -19.4000um -12.2000um -19.0000um -11.8000um
paint via3
box -19.4000um -34.6000um -19.0000um -34.2000um
paint via3
box -17.8000um -34.6000um -17.4000um -34.2000um
paint via3
box -22.6000um -12.2000um -22.2000um -11.8000um
paint via3
box -17.8000um -25.9100um -17.4000um -25.1700um
paint metal4
box -17.8000um -25.6800um -17.4000um -25.2800um
paint via3
box -22.6000um -9.9100um -22.2000um -9.0400um
paint metal4
box -22.6000um -9.5500um -22.2000um -9.1500um
paint via3
box -22.6000um 0.6000um -5.4000um 1.0000um
paint metal3
box -22.6000um -7.4000um -22.2000um 1.0000um
paint metal4
box -5.8000um -27.4000um -5.4000um 1.0000um
paint metal4
box -5.8000um 0.6000um -5.4000um 1.0000um
paint via3
box -22.6000um 0.6000um -22.2000um 1.0000um
paint via3
box -5.8000um -27.5100um -5.4000um -26.6700um
paint metal4
box -5.8000um -27.1800um -5.4000um -26.7800um
paint via3
box -22.6000um -8.1600um -22.2000um -6.8900um
paint metal4
box -22.6000um -8.0500um -22.2000um -7.6500um
paint via3
box -5.0000um -132.2000um -1.4000um -131.8000um
paint metal3
box -29.0000um -137.8000um -28.6000um -128.6000um
paint metal4
box -5.0000um -132.2000um -4.6000um -128.6000um
paint metal4
box -1.8000um -132.2000um -1.4000um -130.2000um
paint metal4
box -5.0000um -132.2000um -4.6000um -131.8000um
paint via3
box -1.8000um -132.2000um -1.4000um -131.8000um
paint via3
box -29.0000um -137.9100um -28.6000um -137.1800um
paint metal4
box -29.0000um -137.6900um -28.6000um -137.2900um
paint via3
box -29.0000um -129.1100um -28.6000um -128.2200um
paint metal4
box -29.0000um -128.7300um -28.6000um -128.3300um
paint via3
box -5.0000um -129.1100um -4.6000um -128.2200um
paint metal4
box -5.0000um -128.7300um -4.6000um -128.3300um
paint via3
box -1.8000um -130.7100um -1.4000um -129.7200um
paint metal4
box -1.8000um -130.2300um -1.4000um -129.8300um
paint via3
box -5.8000um -113.8000um 36.2000um -113.4000um
paint metal3
box -28.2000um -139.4000um -27.8000um -130.2000um
paint metal4
box -5.8000um -130.6000um -5.4000um -113.4000um
paint metal4
box 35.8000um -129.8000um 36.2000um -113.4000um
paint metal4
box -5.8000um -113.8000um -5.4000um -113.4000um
paint via3
box 35.8000um -113.8000um 36.2000um -113.4000um
paint via3
box -28.2000um -139.5100um -27.8000um -138.6800um
paint metal4
box -28.2000um -139.1900um -27.8000um -138.7900um
paint via3
box -28.2000um -130.7100um -27.8000um -129.7200um
paint metal4
box -28.2000um -130.2300um -27.8000um -129.8300um
paint via3
box -5.8000um -130.7100um -5.4000um -129.7200um
paint metal4
box -5.8000um -130.2300um -5.4000um -129.8300um
paint via3
box 35.8000um -129.9100um 36.2000um -128.9700um
paint metal4
box 35.8000um -129.4800um 36.2000um -129.0800um
paint via3
box 34.2000um -107.4000um 37.0000um -107.0000um
paint metal3
box 26.2000um -156.2000um 26.6000um -128.6000um
paint metal4
box 34.2000um -107.4000um 34.6000um -97.4000um
paint metal4
box 36.6000um -129.0000um 37.0000um -107.0000um
paint metal4
box 34.2000um -107.4000um 34.6000um -107.0000um
paint via3
box 36.6000um -107.4000um 37.0000um -107.0000um
paint via3
box 26.2000um -156.3100um 26.6000um -155.4400um
paint metal4
box 26.2000um -155.9500um 26.6000um -155.5500um
paint via3
box 26.2000um -129.1100um 26.6000um -128.2200um
paint metal4
box 26.2000um -128.7300um 26.6000um -128.3300um
paint via3
box 36.6000um -129.1100um 37.0000um -128.2200um
paint metal4
box 36.6000um -128.7300um 37.0000um -128.3300um
paint via3
box 34.2000um -97.9100um 34.6000um -97.2400um
paint metal4
box 34.2000um -97.7500um 34.6000um -97.3500um
paint via3
box 26.3500um -156.0500um 26.4500um -155.9500um
label on c metal4
box 33.4000um -108.2000um 37.8000um -107.8000um
paint metal3
box 27.0000um -155.4000um 27.4000um -127.0000um
paint metal4
box 33.4000um -108.2000um 33.8000um -85.4000um
paint metal4
box 37.4000um -127.4000um 37.8000um -107.8000um
paint metal4
box 33.4000um -108.2000um 33.8000um -107.8000um
paint via3
box 37.4000um -108.2000um 37.8000um -107.8000um
paint via3
box 27.0000um -155.5100um 27.4000um -154.6900um
paint metal4
box 27.0000um -155.2000um 27.4000um -154.8000um
paint via3
box 27.0000um -127.5100um 27.4000um -126.7200um
paint metal4
box 27.0000um -127.2300um 27.4000um -126.8300um
paint via3
box 37.4000um -127.5100um 37.8000um -126.7200um
paint metal4
box 37.4000um -127.2300um 37.8000um -126.8300um
paint via3
box 33.4000um -86.1600um 33.8000um -85.2900um
paint metal4
box 33.4000um -86.0500um 33.8000um -85.6500um
paint via3
box 27.1500um -155.2500um 27.2500um -155.1500um
label op c metal4
box 28.6000um -160.2000um 35.4000um -159.8000um
paint metal3
box 28.6000um -160.2000um 29.0000um -157.4000um
paint metal4
box 35.0000um -209.0000um 35.4000um -159.8000um
paint metal4
box 28.6000um -160.2000um 29.0000um -159.8000um
paint via3
box 35.0000um -160.2000um 35.4000um -159.8000um
paint via3
box 35.0000um -209.1100um 35.4000um -208.4300um
paint metal4
box 35.0000um -208.9400um 35.4000um -208.5400um
paint via3
box 28.6000um -158.3100um 29.0000um -157.2900um
paint metal4
box 28.6000um -158.2000um 29.0000um -157.8000um
paint via3
box 27.8000um -153.8000um 36.2000um -153.4000um
paint metal3
box 27.8000um -157.8000um 28.2000um -153.4000um
paint metal4
box 35.8000um -210.6000um 36.2000um -153.4000um
paint metal4
box 27.8000um -153.8000um 28.2000um -153.4000um
paint via3
box 35.8000um -153.8000um 36.2000um -153.4000um
paint via3
box 35.8000um -210.7100um 36.2000um -209.9300um
paint metal4
box 35.8000um -210.4400um 36.2000um -210.0400um
paint via3
box 27.8000um -157.9100um 28.2000um -156.9400um
paint metal4
box 27.8000um -157.4500um 28.2000um -157.0500um
paint via3
box -1.0000um -80.2000um 0.2000um -79.8000um
paint metal3
box -1.8000um -74.6000um 0.2000um -74.2000um
paint metal3
box -2.6000um -2.6000um 0.2000um -2.2000um
paint metal3
box -2.6000um -2.6000um -2.2000um -0.6000um
paint metal4
box -1.8000um -74.6000um -1.4000um -72.6000um
paint metal4
box -1.0000um -114.6000um -0.6000um -79.8000um
paint metal4
box -0.2000um -80.2000um 0.2000um -2.2000um
paint metal4
box -0.2000um -74.6000um 0.2000um -74.2000um
paint via3
box -0.2000um -80.2000um 0.2000um -79.8000um
paint via3
box -2.6000um -2.6000um -2.2000um -2.2000um
paint via3
box -1.8000um -74.6000um -1.4000um -74.2000um
paint via3
box -1.0000um -80.2000um -0.6000um -79.8000um
paint via3
box -0.2000um -2.6000um 0.2000um -2.2000um
paint via3
box -1.0000um -115.0700um -0.6000um -114.0900um
paint metal4
box -1.0000um -114.9600um -0.6000um -114.5600um
paint via3
box -1.0000um -86.7200um -0.6000um -86.0900um
paint metal4
box -1.0000um -86.6100um -0.6000um -86.2100um
paint via3
box -1.8000um -73.1100um -1.4000um -72.4900um
paint metal4
box -1.8000um -73.0000um -1.4000um -72.6000um
paint via3
box -2.6000um -1.1100um -2.2000um -0.3900um
paint metal4
box -2.6000um -0.9000um -2.2000um -0.5000um
paint via3
box -17.0000um -48.2000um -16.6000um -26.2000um
paint metal4
box -14.6000um -48.2000um -14.2000um -44.6000um
paint metal4
box -14.6000um -48.7100um -14.2000um -47.6900um
paint metal4
box -14.6000um -48.6000um -14.2000um -48.2000um
paint via3
box -14.6000um -45.1100um -14.2000um -44.1200um
paint metal4
box -14.6000um -44.6300um -14.2000um -44.2300um
paint via3
box -17.0000um -48.7100um -16.6000um -47.6900um
paint metal4
box -17.0000um -48.6000um -16.6000um -48.2000um
paint via3
box -17.0000um -26.7100um -16.6000um -25.9200um
paint metal4
box -17.0000um -26.4300um -16.6000um -26.0300um
paint via3
box -28.2000um -107.4000um -6.2000um -107.0000um
paint metal3
box -42.6000um -80.2000um -40.6000um -79.8000um
paint metal3
box -42.6000um -45.8000um -41.4000um -45.4000um
paint metal3
box -42.6000um -80.2000um -42.2000um -45.4000um
paint metal4
box -41.8000um -48.2000um -41.4000um -45.4000um
paint metal4
box -41.0000um -88.2000um -40.6000um -79.8000um
paint metal4
box -28.2000um -107.4000um -27.8000um -87.8000um
paint metal4
box -13.8000um -48.2000um -13.4000um -43.8000um
paint metal4
box -6.6000um -133.8000um -6.2000um -107.0000um
paint metal4
box -41.8000um -45.8000um -41.4000um -45.4000um
paint via3
box -6.6000um -107.4000um -6.2000um -107.0000um
paint via3
box -41.0000um -80.2000um -40.6000um -79.8000um
paint via3
box -42.6000um -80.2000um -42.2000um -79.8000um
paint via3
box -28.2000um -107.4000um -27.8000um -107.0000um
paint via3
box -42.6000um -45.8000um -42.2000um -45.4000um
paint via3
box -6.6000um -133.9100um -6.2000um -133.1800um
paint metal4
box -6.6000um -133.6900um -6.2000um -133.2900um
paint via3
box -28.2000um -88.3100um -27.8000um -87.6200um
paint metal4
box -28.2000um -88.1300um -27.8000um -87.7300um
paint via3
box -41.0000um -88.3100um -40.6000um -87.6200um
paint metal4
box -41.0000um -88.1300um -40.6000um -87.7300um
paint via3
box -41.8000um -48.3100um -41.4000um -47.3400um
paint metal4
box -41.8000um -47.8500um -41.4000um -47.4500um
paint via3
box -13.8000um -48.3100um -13.4000um -47.3400um
paint metal4
box -13.8000um -47.8500um -13.4000um -47.4500um
paint via3
box -13.8000um -44.3100um -13.4000um -43.3700um
paint metal4
box -13.8000um -43.8800um -13.4000um -43.4800um
paint via3
box -39.4000um -132.2000um -37.4000um -131.8000um
paint metal3
box -29.0000um -85.0000um 1.0000um -84.6000um
paint metal3
box -18.6000um -41.8000um -15.8000um -41.4000um
paint metal3
box -16.2000um -37.8000um -14.2000um -37.4000um
paint metal3
box -1.0000um -37.8000um 1.0000um -37.4000um
paint metal3
box -39.4000um -132.2000um -39.0000um -103.8000um
paint metal4
box -37.8000um -161.8000um -37.4000um -131.8000um
paint metal4
box -29.0000um -104.2000um -28.6000um -84.6000um
paint metal4
box -18.6000um -45.0000um -18.2000um -41.4000um
paint metal4
box -16.2000um -41.8000um -15.8000um -37.4000um
paint metal4
box -14.6000um -39.4000um -14.2000um -37.4000um
paint metal4
box -1.0000um -39.4000um -0.6000um -37.4000um
paint metal4
box 0.6000um -85.0000um 1.0000um -37.4000um
paint metal4
box -29.0000um -85.0000um -28.6000um -84.6000um
paint via3
box 0.6000um -85.0000um 1.0000um -84.6000um
paint via3
box -37.8000um -132.2000um -37.4000um -131.8000um
paint via3
box -1.0000um -37.8000um -0.6000um -37.4000um
paint via3
box -14.6000um -37.8000um -14.2000um -37.4000um
paint via3
box 0.6000um -37.8000um 1.0000um -37.4000um
paint via3
box -18.6000um -41.8000um -18.2000um -41.4000um
paint via3
box -16.2000um -37.8000um -15.8000um -37.4000um
paint via3
box -16.2000um -41.8000um -15.8000um -41.4000um
paint via3
box -39.4000um -132.2000um -39.0000um -131.8000um
paint via3
box -37.8000um -162.2800um -37.4000um -161.2900um
paint metal4
box -37.8000um -162.1700um -37.4000um -161.7700um
paint via3
box -39.4000um -104.5000um -39.0000um -103.6900um
paint metal4
box -39.4000um -104.3900um -39.0000um -103.9900um
paint via3
box -29.0000um -104.5000um -28.6000um -103.6900um
paint metal4
box -29.0000um -104.3900um -28.6000um -103.9900um
paint via3
box -1.0000um -39.8200um -0.6000um -38.8900um
paint metal4
box -1.0000um -39.7100um -0.6000um -39.3100um
paint via3
box -14.6000um -39.8200um -14.2000um -38.8900um
paint metal4
box -14.6000um -39.7100um -14.2000um -39.3100um
paint via3
box -18.6000um -45.1100um -18.2000um -44.1200um
paint metal4
box -18.6000um -44.6300um -18.2000um -44.2300um
paint via3
box -37.6500um -161.6500um -37.5500um -161.5500um
label bias_a c metal4
box -25.8000um -81.0000um -23.8000um -80.6000um
paint metal3
box -1.8000um -81.0000um 1.8000um -80.6000um
paint metal3
box -2.6000um -30.6000um 1.8000um -30.2000um
paint metal3
box -23.4000um 1.4000um -4.6000um 1.8000um
paint metal3
box -25.8000um -109.8000um -25.4000um -80.6000um
paint metal4
box -24.2000um -87.4000um -23.8000um -80.6000um
paint metal4
box -23.4000um -29.0000um -23.0000um 1.8000um
paint metal4
box -5.0000um -24.2000um -4.6000um 1.8000um
paint metal4
box -2.6000um -30.6000um -2.2000um -23.8000um
paint metal4
box -1.8000um -87.4000um -1.4000um -80.6000um
paint metal4
box 1.4000um -81.0000um 1.8000um -30.2000um
paint metal4
box -5.0000um 1.4000um -4.6000um 1.8000um
paint via3
box 1.4000um -30.6000um 1.8000um -30.2000um
paint via3
box -24.2000um -81.0000um -23.8000um -80.6000um
paint via3
box 1.4000um -81.0000um 1.8000um -80.6000um
paint via3
box -25.8000um -81.0000um -25.4000um -80.6000um
paint via3
box -2.6000um -30.6000um -2.2000um -30.2000um
paint via3
box -1.8000um -81.0000um -1.4000um -80.6000um
paint via3
box -23.4000um 1.4000um -23.0000um 1.8000um
paint via3
box -25.8000um -110.0600um -25.4000um -109.2900um
paint metal4
box -25.8000um -109.9500um -25.4000um -109.5500um
paint via3
box -24.2000um -87.5100um -23.8000um -86.8500um
paint metal4
box -24.2000um -87.3600um -23.8000um -86.9600um
paint via3
box -1.8000um -87.5100um -1.4000um -86.8500um
paint metal4
box -1.8000um -87.3600um -1.4000um -86.9600um
paint via3
box -2.6000um -24.3100um -2.2000um -23.6700um
paint metal4
box -2.6000um -24.1800um -2.2000um -23.7800um
paint via3
box -5.0000um -24.3100um -4.6000um -23.6700um
paint metal4
box -5.0000um -24.1800um -4.6000um -23.7800um
paint via3
box -23.4000um -29.1900um -23.0000um -28.4900um
paint metal4
box -23.4000um -29.0800um -23.0000um -28.6800um
paint via3
box -1.0000um -45.8000um 2.6000um -45.4000um
paint metal3
box -3.4000um -31.4000um 2.6000um -31.0000um
paint metal3
box -3.4000um -31.4000um -3.0000um -27.8000um
paint metal4
box -1.0000um -76.2000um -0.6000um -45.4000um
paint metal4
box 2.2000um -45.8000um 2.6000um -31.0000um
paint metal4
box 2.2000um -45.8000um 2.6000um -45.4000um
paint via3
box 2.2000um -31.4000um 2.6000um -31.0000um
paint via3
box -3.4000um -31.4000um -3.0000um -31.0000um
paint via3
box -1.0000um -45.8000um -0.6000um -45.4000um
paint via3
box -1.0000um -76.6800um -0.6000um -75.6900um
paint metal4
box -1.0000um -76.5700um -0.6000um -76.1700um
paint via3
box -3.4000um -28.3100um -3.0000um -27.4200um
paint metal4
box -3.4000um -27.9300um -3.0000um -27.5300um
paint via3
box -0.8500um -76.0500um -0.7500um -75.9500um
label cm c metal4
box -29.8000um -108.2000um 3.4000um -107.8000um
paint metal3
box -19.4000um -35.4000um 3.4000um -35.0000um
paint metal3
box -29.8000um -108.2000um -29.4000um -104.6000um
paint metal4
box -19.4000um -43.4000um -19.0000um -35.0000um
paint metal4
box 3.0000um -108.2000um 3.4000um -35.0000um
paint metal4
box -29.8000um -108.2000um -29.4000um -107.8000um
paint via3
box -19.4000um -35.4000um -19.0000um -35.0000um
paint via3
box 3.0000um -108.2000um 3.4000um -107.8000um
paint via3
box 3.0000um -35.4000um 3.4000um -35.0000um
paint via3
box -29.8000um -105.2500um -29.4000um -104.4900um
paint metal4
box -29.8000um -105.1400um -29.4000um -104.7400um
paint via3
box -19.4000um -43.5100um -19.0000um -42.6200um
paint metal4
box -19.4000um -43.1300um -19.0000um -42.7300um
paint via3
box -38.6500um -73.8500um -38.1500um -73.3500um
paint metal4
box -38.6000um -73.9100um -38.2000um -73.2400um
paint metal4
box -38.6000um -73.7500um -38.2000um -73.3500um
paint via3
box -38.4500um -73.6500um -38.3500um -73.5500um
label IBIAS c metal4
box -38.6000um -212.2000um -37.4000um -211.8000um
paint metal3
box -38.6000um -159.4000um -22.2000um -159.0000um
paint metal3
box -38.6000um -212.2000um -38.2000um -159.0000um
paint metal4
box -37.8000um -212.2000um -37.4000um -207.8000um
paint metal4
box -22.6000um -159.4000um -22.2000um -138.2000um
paint metal4
box -38.6000um -212.2000um -38.2000um -211.8000um
paint via3
box -38.6000um -159.4000um -38.2000um -159.0000um
paint via3
box -37.8000um -212.2000um -37.4000um -211.8000um
paint via3
box -22.6000um -159.4000um -22.2000um -159.0000um
paint via3
box -37.8000um -208.3100um -37.4000um -207.6800um
paint metal4
box -37.8000um -208.1900um -37.4000um -207.7900um
paint via3
box -22.6000um -138.7100um -22.2000um -137.9300um
paint metal4
box -22.6000um -138.4400um -22.2000um -138.0400um
paint via3
box -40.2000um -133.0000um -36.6000um -132.6000um
paint metal3
box 37.4000um -132.2000um 38.6000um -131.8000um
paint metal3
box -5.0000um -113.0000um -1.4000um -112.6000um
paint metal3
box -40.2000um -109.0000um -38.2000um -108.6000um
paint metal3
box 2.2000um -77.0000um 8.2000um -76.6000um
paint metal3
box 22.2000um -77.0000um 26.6000um -76.6000um
paint metal3
box -4.2000um -32.2000um 4.2000um -31.8000um
paint metal3
box -24.2000um 2.2000um -3.8000um 2.6000um
paint metal3
box -40.2000um -133.0000um -39.8000um -108.6000um
paint metal4
box -38.6000um -111.4000um -38.2000um -108.6000um
paint metal4
box -37.0000um -133.0000um -36.6000um -131.0000um
paint metal4
box -24.2000um -28.2000um -23.8000um 2.6000um
paint metal4
box -16.2000um -29.8000um -15.8000um -24.6000um
paint metal4
box -5.0000um -113.0000um -4.6000um -111.0000um
paint metal4
box -4.2000um -32.2000um -3.8000um -29.4000um
paint metal4
box -4.2000um -25.0000um -3.8000um 2.6000um
paint metal4
box -1.8000um -115.4000um -1.4000um -112.6000um
paint metal4
box 2.2000um -115.4000um 2.6000um -76.6000um
paint metal4
box 3.8000um -77.0000um 4.2000um -31.8000um
paint metal4
box 7.8000um -77.0000um 8.2000um -75.0000um
paint metal4
box 22.2000um -77.0000um 22.6000um -75.8000um
paint metal4
box 26.2000um -77.0000um 26.6000um -75.0000um
paint metal4
box 37.4000um -132.2000um 37.8000um -131.0000um
paint metal4
box 38.2000um -132.2000um 38.6000um -115.0000um
paint metal4
box 7.8000um -77.0000um 8.2000um -76.6000um
paint via3
box -40.2000um -133.0000um -39.8000um -132.6000um
paint via3
box -4.2000um 2.2000um -3.8000um 2.6000um
paint via3
box 3.8000um -77.0000um 4.2000um -76.6000um
paint via3
box -1.8000um -113.0000um -1.4000um -112.6000um
paint via3
box -38.6000um -109.0000um -38.2000um -108.6000um
paint via3
box 3.8000um -32.2000um 4.2000um -31.8000um
paint via3
box 37.4000um -132.2000um 37.8000um -131.8000um
paint via3
box 2.2000um -77.0000um 2.6000um -76.6000um
paint via3
box 26.2000um -77.0000um 26.6000um -76.6000um
paint via3
box -40.2000um -109.0000um -39.8000um -108.6000um
paint via3
box -37.0000um -133.0000um -36.6000um -132.6000um
paint via3
box 22.2000um -77.0000um 22.6000um -76.6000um
paint via3
box -4.2000um -32.2000um -3.8000um -31.8000um
paint via3
box 38.2000um -132.2000um 38.6000um -131.8000um
paint via3
box -5.0000um -113.0000um -4.6000um -112.6000um
paint via3
box -24.2000um 2.2000um -23.8000um 2.6000um
paint via3
box -37.0000um -131.5100um -36.6000um -130.5200um
paint metal4
box -37.0000um -131.0300um -36.6000um -130.6300um
paint via3
box -38.6000um -111.5600um -38.2000um -110.8900um
paint metal4
box -38.6000um -111.4500um -38.2000um -111.0500um
paint via3
box -5.0000um -111.5600um -4.6000um -110.8900um
paint metal4
box -5.0000um -111.4500um -4.6000um -111.0500um
paint via3
box -1.8000um -115.8200um -1.4000um -114.8900um
paint metal4
box -1.8000um -115.7100um -1.4000um -115.3100um
paint via3
box 38.2000um -115.8200um 38.6000um -114.8900um
paint metal4
box 38.2000um -115.7100um 38.6000um -115.3100um
paint via3
box 37.4000um -131.5100um 37.8000um -130.5200um
paint metal4
box 37.4000um -131.0300um 37.8000um -130.6300um
paint via3
box 2.2000um -115.8200um 2.6000um -114.8900um
paint metal4
box 2.2000um -115.7100um 2.6000um -115.3100um
paint via3
box 7.8000um -76.3100um 8.2000um -75.4800um
paint metal4
box 7.8000um -75.9900um 8.2000um -75.5900um
paint via3
box 7.8000um -75.5100um 8.2000um -74.6800um
paint metal4
box 7.8000um -75.1900um 8.2000um -74.7900um
paint via3
box 22.2000um -76.3100um 22.6000um -75.4800um
paint metal4
box 22.2000um -75.9900um 22.6000um -75.5900um
paint via3
box 26.2000um -76.3100um 26.6000um -75.4800um
paint metal4
box 26.2000um -75.9900um 26.6000um -75.5900um
paint via3
box 26.2000um -75.5100um 26.6000um -74.6800um
paint metal4
box 26.2000um -75.1900um 26.6000um -74.7900um
paint via3
box -4.2000um -29.9100um -3.8000um -28.9700um
paint metal4
box -4.2000um -29.4800um -3.8000um -29.0800um
paint via3
box -16.2000um -29.9100um -15.8000um -28.9700um
paint metal4
box -16.2000um -29.4800um -15.8000um -29.0800um
paint via3
box -16.2000um -25.1100um -15.8000um -24.4200um
paint metal4
box -16.2000um -24.9300um -15.8000um -24.5300um
paint via3
box -4.2000um -25.1100um -3.8000um -24.4200um
paint metal4
box -4.2000um -24.9300um -3.8000um -24.5300um
paint via3
box -24.2000um -6.7100um -23.8000um -5.9900um
paint metal4
box -24.2000um -6.5000um -23.8000um -6.1000um
paint via3
box -24.2000um -28.4400um -23.8000um -27.6900um
paint metal4
box -24.2000um -28.3300um -23.8000um -27.9300um
paint via3
box -37.0500um -131.0800um -36.5500um -130.5800um
paint locali
box -36.9700um -131.0000um -36.6300um -130.6600um
paint mcon
box -36.9700um -131.0000um -36.6300um -130.6600um
paint m2c
box -37.0000um -131.0300um -36.6000um -130.6300um
paint m3c
box -37.0500um -131.0800um -36.5500um -130.5800um
paint metal3
box 37.3500um -131.0800um 37.8500um -130.5800um
paint locali
box 37.4300um -131.0000um 37.7700um -130.6600um
paint mcon
box 37.4300um -131.0000um 37.7700um -130.6600um
paint m2c
box 37.4000um -131.0300um 37.8000um -130.6300um
paint m3c
box 37.3500um -131.0800um 37.8500um -130.5800um
paint metal3
box 7.7500um -76.0400um 8.2500um -75.5400um
paint locali
box 7.8300um -75.9600um 8.1700um -75.6200um
paint mcon
box 7.8300um -75.9600um 8.1700um -75.6200um
paint m2c
box 7.8000um -75.9900um 8.2000um -75.5900um
paint m3c
box 7.7500um -76.0400um 8.2500um -75.5400um
paint metal3
box 22.1500um -76.0400um 22.6500um -75.5400um
paint locali
box 22.2300um -75.9600um 22.5700um -75.6200um
paint mcon
box 22.2300um -75.9600um 22.5700um -75.6200um
paint m2c
box 22.2000um -75.9900um 22.6000um -75.5900um
paint m3c
box 22.1500um -76.0400um 22.6500um -75.5400um
paint metal3
box 26.1500um -76.0400um 26.6500um -75.5400um
paint locali
box 26.2300um -75.9600um 26.5700um -75.6200um
paint mcon
box 26.2300um -75.9600um 26.5700um -75.6200um
paint m2c
box 26.2000um -75.9900um 26.6000um -75.5900um
paint m3c
box 26.1500um -76.0400um 26.6500um -75.5400um
paint metal3
box -4.2500um -29.5300um -3.7500um -29.0300um
paint locali
box -4.1700um -29.4500um -3.8300um -29.1100um
paint mcon
box -4.1700um -29.4500um -3.8300um -29.1100um
paint m2c
box -4.2000um -29.4800um -3.8000um -29.0800um
paint m3c
box -4.2500um -29.5300um -3.7500um -29.0300um
paint metal3
box -16.2500um -29.5300um -15.7500um -29.0300um
paint locali
box -16.1700um -29.4500um -15.8300um -29.1100um
paint mcon
box -16.1700um -29.4500um -15.8300um -29.1100um
paint m2c
box -16.2000um -29.4800um -15.8000um -29.0800um
paint m3c
box -16.2500um -29.5300um -15.7500um -29.0300um
paint metal3
box -24.2500um -6.5500um -23.7500um -6.0500um
paint locali
box -24.1700um -6.4700um -23.8300um -6.1300um
paint mcon
box -24.1700um -6.4700um -23.8300um -6.1300um
paint m2c
box -24.2000um -6.5000um -23.8000um -6.1000um
paint m3c
box -24.2500um -6.5500um -23.7500um -6.0500um
paint metal3
box -36.8500um -131.2500um -36.7500um -131.1500um
label VDD c metal4
box -41.0000um -133.8000um -27.0000um -133.4000um
paint metal3
box -20.2000um -132.2000um -15.8000um -131.8000um
paint metal3
box -42.6000um -107.4000um -40.6000um -107.0000um
paint metal3
box -0.2000um -88.2000um 1.8000um -87.8000um
paint metal3
box -42.6000um -87.4000um -39.8000um -87.0000um
paint metal3
box 1.4000um -83.4000um 5.0000um -83.0000um
paint metal3
box -43.4000um -81.0000um -41.4000um -80.6000um
paint metal3
box -43.4000um -59.4000um -41.4000um -59.0000um
paint metal3
box -18.6000um -41.0000um -17.4000um -40.6000um
paint metal3
box -17.8000um -37.0000um -13.4000um -36.6000um
paint metal3
box -43.4000um -30.6000um -40.6000um -30.2000um
paint metal3
box -43.4000um -81.0000um -43.0000um -30.2000um
paint metal4
box -42.6000um -107.4000um -42.2000um -87.0000um
paint metal4
box -41.8000um -82.6000um -41.4000um -80.6000um
paint metal4
box -41.8000um -59.4000um -41.4000um -57.4000um
paint metal4
box -41.0000um -133.8000um -40.6000um -105.4000um
paint metal4
box -41.0000um -47.4000um -40.6000um -43.8000um
paint metal4
box -41.0000um -31.4000um -40.6000um -30.2000um
paint metal4
box -40.2000um -89.0000um -39.8000um -82.2000um
paint metal4
box -38.6000um -61.8000um -38.2000um -57.4000um
paint metal4
box -29.0000um -162.6000um -28.6000um -156.6000um
paint metal4
box -27.4000um -137.0000um -27.0000um -133.4000um
paint metal4
box -23.4000um -85.8000um -23.0000um -83.0000um
paint metal4
box -21.8000um -157.0000um -21.4000um -136.6000um
paint metal4
box -20.2000um -137.0000um -19.8000um -131.8000um
paint metal4
box -18.6000um -41.0000um -18.2000um -31.8000um
paint metal4
box -17.8000um -47.4000um -17.4000um -36.6000um
paint metal4
box -16.2000um -162.6000um -15.8000um -158.2000um
paint metal4
box -16.2000um -134.6000um -15.8000um -131.8000um
paint metal4
box -13.8000um -38.6000um -13.4000um -36.6000um
paint metal4
box -0.2000um -88.2000um 0.2000um -82.2000um
paint metal4
box 1.4000um -88.2000um 1.8000um -83.0000um
paint metal4
box 4.6000um -83.4000um 5.0000um -81.4000um
paint metal4
box 36.6000um -211.4000um 37.0000um -162.2000um
paint metal4
box 1.4000um -83.4000um 1.8000um -83.0000um
paint via3
box -27.4000um -133.8000um -27.0000um -133.4000um
paint via3
box -16.2000um -132.2000um -15.8000um -131.8000um
paint via3
box 1.4000um -88.2000um 1.8000um -87.8000um
paint via3
box -43.4000um -30.6000um -43.0000um -30.2000um
paint via3
box -18.6000um -41.0000um -18.2000um -40.6000um
paint via3
box -41.0000um -30.6000um -40.6000um -30.2000um
paint via3
box -42.6000um -107.4000um -42.2000um -107.0000um
paint via3
box -13.8000um -37.0000um -13.4000um -36.6000um
paint via3
box -0.2000um -88.2000um 0.2000um -87.8000um
paint via3
box -17.8000um -37.0000um -17.4000um -36.6000um
paint via3
box 4.6000um -83.4000um 5.0000um -83.0000um
paint via3
box -43.4000um -81.0000um -43.0000um -80.6000um
paint via3
box -17.8000um -41.0000um -17.4000um -40.6000um
paint via3
box -41.8000um -81.0000um -41.4000um -80.6000um
paint via3
box -41.8000um -59.4000um -41.4000um -59.0000um
paint via3
box -41.0000um -107.4000um -40.6000um -107.0000um
paint via3
box -42.6000um -87.4000um -42.2000um -87.0000um
paint via3
box -43.4000um -59.4000um -43.0000um -59.0000um
paint via3
box -41.0000um -133.8000um -40.6000um -133.4000um
paint via3
box -40.2000um -87.4000um -39.8000um -87.0000um
paint via3
box -20.2000um -132.2000um -19.8000um -131.8000um
paint via3
box 36.6000um -211.5100um 37.0000um -210.7300um
paint metal4
box 36.6000um -211.2400um 37.0000um -210.8400um
paint via3
box 36.6000um -163.0300um 37.0000um -162.0900um
paint metal4
box 36.6000um -162.9200um 37.0000um -162.5200um
paint via3
box -16.2000um -163.0300um -15.8000um -162.0900um
paint metal4
box -16.2000um -162.9200um -15.8000um -162.5200um
paint via3
box -16.2000um -159.1100um -15.8000um -158.0900um
paint metal4
box -16.2000um -159.0000um -15.8000um -158.6000um
paint via3
box -29.0000um -163.0300um -28.6000um -162.0900um
paint metal4
box -29.0000um -162.9200um -28.6000um -162.5200um
paint via3
box -29.0000um -157.2100um -28.6000um -156.4900um
paint metal4
box -29.0000um -157.1000um -28.6000um -156.7000um
paint via3
box -21.8000um -157.2100um -21.4000um -156.4900um
paint metal4
box -21.8000um -157.1000um -21.4000um -156.7000um
paint via3
box -21.8000um -137.1100um -21.4000um -136.3800um
paint metal4
box -21.8000um -136.8900um -21.4000um -136.4900um
paint via3
box -20.2000um -137.1100um -19.8000um -136.3800um
paint metal4
box -20.2000um -136.8900um -19.8000um -136.4900um
paint via3
box -16.2000um -134.7100um -15.8000um -133.9300um
paint metal4
box -16.2000um -134.4400um -15.8000um -134.0400um
paint via3
box -27.4000um -137.1100um -27.0000um -136.3800um
paint metal4
box -27.4000um -136.8900um -27.0000um -136.4900um
paint via3
box -41.0000um -106.0500um -40.6000um -105.2900um
paint metal4
box -41.0000um -105.9400um -40.6000um -105.5400um
paint via3
box -40.2000um -89.1100um -39.8000um -88.3700um
paint metal4
box -40.2000um -88.8800um -39.8000um -88.4800um
paint via3
box -40.2000um -83.9000um -39.8000um -82.8900um
paint metal4
box -40.2000um -83.7900um -39.8000um -83.3900um
paint via3
box -40.2000um -83.1000um -39.8000um -82.0900um
paint metal4
box -40.2000um -82.9900um -39.8000um -82.5900um
paint via3
box -23.4000um -83.9000um -23.0000um -82.8900um
paint metal4
box -23.4000um -83.7900um -23.0000um -83.3900um
paint via3
box -23.4000um -85.9200um -23.0000um -85.2900um
paint metal4
box -23.4000um -85.8100um -23.0000um -85.4100um
paint via3
box -0.2000um -83.1000um 0.2000um -82.0900um
paint metal4
box -0.2000um -82.9900um 0.2000um -82.5900um
paint via3
box 4.6000um -82.7100um 5.0000um -82.0300um
paint metal4
box 4.6000um -82.5400um 5.0000um -82.1400um
paint via3
box 4.6000um -81.9100um 5.0000um -81.2300um
paint metal4
box 4.6000um -81.7400um 5.0000um -81.3400um
paint via3
box -41.8000um -83.1000um -41.4000um -82.0900um
paint metal4
box -41.8000um -82.9900um -41.4000um -82.5900um
paint via3
box -41.8000um -57.9100um -41.4000um -57.1800um
paint metal4
box -41.8000um -57.6900um -41.4000um -57.2900um
paint via3
box -38.6000um -57.9100um -38.2000um -57.1800um
paint metal4
box -38.6000um -57.6900um -38.2000um -57.2900um
paint via3
box -38.6000um -61.1100um -38.2000um -60.3500um
paint metal4
box -38.6000um -60.8600um -38.2000um -60.4600um
paint via3
box -38.6000um -61.9100um -38.2000um -61.1500um
paint metal4
box -38.6000um -61.6600um -38.2000um -61.2600um
paint via3
box -41.0000um -31.8500um -40.6000um -30.8900um
paint metal4
box -41.0000um -31.7400um -40.6000um -31.3400um
paint via3
box -18.6000um -32.3100um -18.2000um -31.2300um
paint metal4
box -18.6000um -31.7400um -18.2000um -31.3400um
paint via3
box -17.8000um -47.5100um -17.4000um -46.5400um
paint metal4
box -17.8000um -47.0500um -17.4000um -46.6500um
paint via3
box -41.0000um -47.5100um -40.6000um -46.5400um
paint metal4
box -41.0000um -47.0500um -40.6000um -46.6500um
paint via3
box -41.0000um -44.3100um -40.6000um -43.3700um
paint metal4
box -41.0000um -43.8800um -40.6000um -43.4800um
paint via3
box -13.8000um -39.0200um -13.4000um -38.0900um
paint metal4
box -13.8000um -38.9100um -13.4000um -38.5100um
paint via3
box 36.5500um -211.2900um 37.0500um -210.7900um
paint locali
box 36.6300um -211.2100um 36.9700um -210.8700um
paint mcon
box 36.6300um -211.2100um 36.9700um -210.8700um
paint m2c
box 36.6000um -211.2400um 37.0000um -210.8400um
paint m3c
box 36.5500um -211.2900um 37.0500um -210.7900um
paint metal3
box -16.2500um -159.0500um -15.7500um -158.5500um
paint locali
box -16.1700um -158.9700um -15.8300um -158.6300um
paint mcon
box -16.1700um -158.9700um -15.8300um -158.6300um
paint m2c
box -16.2000um -159.0000um -15.8000um -158.6000um
paint m3c
box -16.2500um -159.0500um -15.7500um -158.5500um
paint metal3
box -21.8500um -136.9400um -21.3500um -136.4400um
paint locali
box -21.7700um -136.8600um -21.4300um -136.5200um
paint mcon
box -21.7700um -136.8600um -21.4300um -136.5200um
paint m2c
box -21.8000um -136.8900um -21.4000um -136.4900um
paint m3c
box -21.8500um -136.9400um -21.3500um -136.4400um
paint metal3
box -20.2500um -136.9400um -19.7500um -136.4400um
paint locali
box -20.1700um -136.8600um -19.8300um -136.5200um
paint mcon
box -20.1700um -136.8600um -19.8300um -136.5200um
paint m2c
box -20.2000um -136.8900um -19.8000um -136.4900um
paint m3c
box -20.2500um -136.9400um -19.7500um -136.4400um
paint metal3
box -27.4500um -136.9400um -26.9500um -136.4400um
paint locali
box -27.3700um -136.8600um -27.0300um -136.5200um
paint mcon
box -27.3700um -136.8600um -27.0300um -136.5200um
paint m2c
box -27.4000um -136.8900um -27.0000um -136.4900um
paint m3c
box -27.4500um -136.9400um -26.9500um -136.4400um
paint metal3
box -41.0500um -105.9900um -40.5500um -105.4900um
paint locali
box -40.9700um -105.9100um -40.6300um -105.5700um
paint mcon
box -40.9700um -105.9100um -40.6300um -105.5700um
paint m2c
box -41.0000um -105.9400um -40.6000um -105.5400um
paint m3c
box -41.0500um -105.9900um -40.5500um -105.4900um
paint metal3
box -40.2500um -83.8400um -39.7500um -83.3400um
paint locali
box -40.1700um -83.7600um -39.8300um -83.4200um
paint mcon
box -40.1700um -83.7600um -39.8300um -83.4200um
paint m2c
box -40.2000um -83.7900um -39.8000um -83.3900um
paint m3c
box -40.2500um -83.8400um -39.7500um -83.3400um
paint metal3
box -23.4500um -83.8400um -22.9500um -83.3400um
paint locali
box -23.3700um -83.7600um -23.0300um -83.4200um
paint mcon
box -23.3700um -83.7600um -23.0300um -83.4200um
paint m2c
box -23.4000um -83.7900um -23.0000um -83.3900um
paint m3c
box -23.4500um -83.8400um -22.9500um -83.3400um
paint metal3
box -23.4500um -85.8600um -22.9500um -85.3600um
paint locali
box -23.3700um -85.7800um -23.0300um -85.4400um
paint mcon
box -23.3700um -85.7800um -23.0300um -85.4400um
paint m2c
box -23.4000um -85.8100um -23.0000um -85.4100um
paint m3c
box -23.4500um -85.8600um -22.9500um -85.3600um
paint metal3
box 4.5500um -82.5900um 5.0500um -82.0900um
paint locali
box 4.6300um -82.5100um 4.9700um -82.1700um
paint mcon
box 4.6300um -82.5100um 4.9700um -82.1700um
paint m2c
box 4.6000um -82.5400um 5.0000um -82.1400um
paint m3c
box 4.5500um -82.5900um 5.0500um -82.0900um
paint metal3
box -38.6500um -60.9100um -38.1500um -60.4100um
paint locali
box -38.5700um -60.8300um -38.2300um -60.4900um
paint mcon
box -38.5700um -60.8300um -38.2300um -60.4900um
paint m2c
box -38.6000um -60.8600um -38.2000um -60.4600um
paint m3c
box -38.6500um -60.9100um -38.1500um -60.4100um
paint metal3
box -41.0500um -31.7900um -40.5500um -31.2900um
paint locali
box -40.9700um -31.7100um -40.6300um -31.3700um
paint mcon
box -40.9700um -31.7100um -40.6300um -31.3700um
paint m2c
box -41.0000um -31.7400um -40.6000um -31.3400um
paint m3c
box -41.0500um -31.7900um -40.5500um -31.2900um
paint metal3
box -18.6500um -31.7900um -18.1500um -31.2900um
paint locali
box -18.5700um -31.7100um -18.2300um -31.3700um
paint mcon
box -18.5700um -31.7100um -18.2300um -31.3700um
paint m2c
box -18.6000um -31.7400um -18.2000um -31.3400um
paint m3c
box -18.6500um -31.7900um -18.1500um -31.2900um
paint metal3
box -17.8500um -47.1000um -17.3500um -46.6000um
paint locali
box -17.7700um -47.0200um -17.4300um -46.6800um
paint mcon
box -17.7700um -47.0200um -17.4300um -46.6800um
paint m2c
box -17.8000um -47.0500um -17.4000um -46.6500um
paint m3c
box -17.8500um -47.1000um -17.3500um -46.6000um
paint metal3
box -41.0500um -47.1000um -40.5500um -46.6000um
paint locali
box -40.9700um -47.0200um -40.6300um -46.6800um
paint mcon
box -40.9700um -47.0200um -40.6300um -46.6800um
paint m2c
box -41.0000um -47.0500um -40.6000um -46.6500um
paint m3c
box -41.0500um -47.1000um -40.5500um -46.6000um
paint metal3
box -13.8500um -38.9600um -13.3500um -38.4600um
paint locali
box -13.7700um -38.8800um -13.4300um -38.5400um
paint mcon
box -13.7700um -38.8800um -13.4300um -38.5400um
paint m2c
box -13.8000um -38.9100um -13.4000um -38.5100um
paint m3c
box -13.8500um -38.9600um -13.3500um -38.4600um
paint metal3
box 36.7500um -211.2500um 36.8500um -211.1500um
label VSS c metal4
box 37.4000um -133.0000um 39.4000um -132.6000um
paint metal3
box 11.8000um -105.8000um 12.2000um -94.2000um
paint metal4
box 37.4000um -161.8000um 37.8000um -132.6000um
paint metal4
box 39.0000um -133.0000um 39.4000um -106.2000um
paint metal4
box 39.0000um -133.0000um 39.4000um -132.6000um
paint via3
box 37.4000um -133.0000um 37.8000um -132.6000um
paint via3
box 37.4000um -161.9100um 37.8000um -160.9100um
paint metal4
box 37.4000um -161.4200um 37.8000um -161.0200um
paint via3
box 39.0000um -106.7100um 39.4000um -105.4400um
paint metal4
box 39.0000um -105.9500um 39.4000um -105.5500um
paint via3
box 11.8000um -106.0600um 12.2000um -105.2900um
paint metal4
box 11.8000um -105.9500um 12.2000um -105.5500um
paint via3
box 11.8000um -94.7100um 12.2000um -93.7400um
paint metal4
box 11.8000um -94.2500um 12.2000um -93.8500um
paint via3
box 37.5500um -161.6500um 37.6500um -161.5500um
label cmc c metal4
box -28.2500um -158.6500um -27.7500um -158.1500um
paint metal4
box -28.2000um -158.7100um -27.8000um -158.0900um
paint metal4
box -28.2000um -158.6000um -27.8000um -158.2000um
paint via3
box -28.0500um -158.4500um -27.9500um -158.3500um
label in c metal4
box -27.4500um -157.8500um -26.9500um -157.3500um
paint metal4
box -27.4000um -157.9600um -27.0000um -157.2900um
paint metal4
box -27.4000um -157.8500um -27.0000um -157.4500um
paint via3
box -27.2500um -157.6500um -27.1500um -157.5500um
label ip c metal4
tech revert
save iadc_ota_v2_routed
gds write iadc_ota_v2_routed
quit -noprompt
