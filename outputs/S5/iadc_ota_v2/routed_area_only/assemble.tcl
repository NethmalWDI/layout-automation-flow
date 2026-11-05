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
load iadc_ota_v2_routed -silent
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
box -9.8000um -23.4000um -9.4000um -9.4000um
paint metal4
box -9.8000um -23.5100um -9.4000um -22.7600um
paint metal4
box -9.8000um -23.2700um -9.4000um -22.8700um
paint via3
box -9.8000um -9.9100um -9.4000um -9.1500um
paint metal4
box -9.8000um -9.6600um -9.4000um -9.2600um
paint via3
box 5.4000um -41.0000um 5.8000um -7.8000um
paint metal4
box 5.4000um -41.4100um 5.8000um -40.4900um
paint metal4
box 5.4000um -41.3000um 5.8000um -40.9000um
paint via3
box 5.4000um -8.3100um 5.8000um -7.6500um
paint metal4
box 5.4000um -8.1600um 5.8000um -7.7600um
paint via3
box 6.2000um -42.6000um 6.6000um -8.6000um
paint metal4
box 6.2000um -42.9100um 6.6000um -42.0900um
paint metal4
box 6.2000um -42.8000um 6.6000um -42.4000um
paint via3
box 6.2000um -9.1100um 6.6000um -8.4000um
paint metal4
box 6.2000um -8.9100um 6.6000um -8.5100um
paint via3
box -40.2000um -56.2000um -37.4000um -55.8000um
paint metal3
box -13.0000um -17.0000um 10.6000um -16.6000um
paint metal3
box -40.2000um -10.6000um -33.4000um -10.2000um
paint metal3
box -40.2000um -56.2000um -39.8000um -10.2000um
paint metal4
box -37.8000um -73.8000um -37.4000um -55.8000um
paint metal4
box -33.8000um -13.0000um -33.4000um -10.2000um
paint metal4
box -13.0000um -17.0000um -12.6000um -12.6000um
paint metal4
box 10.2000um -20.2000um 10.6000um -16.6000um
paint metal4
box -13.0000um -17.0000um -12.6000um -16.6000um
paint via3
box -33.8000um -10.6000um -33.4000um -10.2000um
paint via3
box -40.2000um -56.2000um -39.8000um -55.8000um
paint via3
box -40.2000um -10.6000um -39.8000um -10.2000um
paint via3
box 10.2000um -17.0000um 10.6000um -16.6000um
paint via3
box -37.8000um -56.2000um -37.4000um -55.8000um
paint via3
box -37.8000um -74.0800um -37.4000um -73.2900um
paint metal4
box -37.8000um -73.9700um -37.4000um -73.5700um
paint via3
box -33.8000um -13.1100um -33.4000um -12.1500um
paint metal4
box -33.8000um -12.6600um -33.4000um -12.2600um
paint via3
box -13.0000um -13.1100um -12.6000um -12.1500um
paint metal4
box -13.0000um -12.6600um -12.6000um -12.2600um
paint via3
box 10.2000um -20.3100um 10.6000um -19.6500um
paint metal4
box 10.2000um -20.1600um 10.6000um -19.7600um
paint via3
box -33.8000um -56.2000um -19.0000um -55.8000um
paint metal3
box -19.4000um -45.0000um -15.0000um -44.6000um
paint metal3
box -15.4000um -17.8000um 9.0000um -17.4000um
paint metal3
box 8.6000um -16.2000um 11.4000um -15.8000um
paint metal3
box -33.8000um -75.4000um -33.4000um -55.8000um
paint metal4
box -19.4000um -56.2000um -19.0000um -44.6000um
paint metal4
box -15.4000um -45.0000um -15.0000um -13.4000um
paint metal4
box 8.6000um -17.8000um 9.0000um -15.8000um
paint metal4
box 11.0000um -18.6000um 11.4000um -15.8000um
paint metal4
box 8.6000um -17.8000um 9.0000um -17.4000um
paint via3
box 8.6000um -16.2000um 9.0000um -15.8000um
paint via3
box -15.4000um -17.8000um -15.0000um -17.4000um
paint via3
box -33.8000um -56.2000um -33.4000um -55.8000um
paint via3
box -15.4000um -45.0000um -15.0000um -44.6000um
paint via3
box -19.4000um -56.2000um -19.0000um -55.8000um
paint via3
box 11.0000um -16.2000um 11.4000um -15.8000um
paint via3
box -19.4000um -45.0000um -19.0000um -44.6000um
paint via3
box -33.8000um -75.5800um -33.4000um -74.8900um
paint metal4
box -33.8000um -75.4700um -33.4000um -75.0700um
paint via3
box -15.4000um -13.9100um -15.0000um -12.9000um
paint metal4
box -15.4000um -13.4100um -15.0000um -13.0100um
paint via3
box 11.0000um -18.7700um 11.4000um -18.0900um
paint metal4
box 11.0000um -18.6600um 11.4000um -18.2600um
paint via3
box 31.8000um -56.2000um 35.4000um -55.8000um
paint metal3
box -13.8000um -45.8000um 1.8000um -45.4000um
paint metal3
box -13.8000um -45.8000um -13.4000um -13.4000um
paint metal4
box 1.4000um -46.6000um 1.8000um -45.4000um
paint metal4
box 31.8000um -56.2000um 32.2000um -47.0000um
paint metal4
box 35.0000um -92.2000um 35.4000um -55.8000um
paint metal4
box -13.8000um -45.8000um -13.4000um -45.4000um
paint via3
box 1.4000um -45.8000um 1.8000um -45.4000um
paint via3
box 31.8000um -56.2000um 32.2000um -55.8000um
paint via3
box 35.0000um -56.2000um 35.4000um -55.8000um
paint via3
box 35.0000um -92.3400um 35.4000um -91.6900um
paint metal4
box 35.0000um -92.2300um 35.4000um -91.8300um
paint via3
box 31.8000um -47.5100um 32.2000um -46.6400um
paint metal4
box 31.8000um -47.1500um 32.2000um -46.7500um
paint via3
box 1.4000um -47.2600um 1.8000um -46.0900um
paint metal4
box 1.4000um -47.1500um 1.8000um -46.7500um
paint via3
box -13.8000um -14.2700um -13.4000um -13.2900um
paint metal4
box -13.8000um -14.1600um -13.4000um -13.7600um
paint via3
box 35.1500um -92.0500um 35.2500um -91.9500um
label on c metal4
box -10.6000um -96.2000um -7.0000um -95.8000um
paint metal3
box -17.8000um -69.8000um -10.2000um -69.4000um
paint metal3
box -14.6000um -25.0000um -11.0000um -24.6000um
paint metal3
box -17.8000um -69.8000um -17.4000um -55.0000um
paint metal4
box -14.6000um -25.0000um -14.2000um -15.0000um
paint metal4
box -11.4000um -55.4000um -11.0000um -24.6000um
paint metal4
box -10.6000um -96.2000um -10.2000um -69.4000um
paint metal4
box -7.4000um -96.2000um -7.0000um -91.0000um
paint metal4
box -17.8000um -69.8000um -17.4000um -69.4000um
paint via3
box -10.6000um -69.8000um -10.2000um -69.4000um
paint via3
box -11.4000um -25.0000um -11.0000um -24.6000um
paint via3
box -14.6000um -25.0000um -14.2000um -24.6000um
paint via3
box -7.4000um -96.2000um -7.0000um -95.8000um
paint via3
box -10.6000um -96.2000um -10.2000um -95.8000um
paint via3
box -7.4000um -91.5900um -7.0000um -90.8900um
paint metal4
box -7.4000um -91.4800um -7.0000um -91.0800um
paint via3
box -17.8000um -55.5100um -17.4000um -54.8400um
paint metal4
box -17.8000um -55.3500um -17.4000um -54.9500um
paint via3
box -11.4000um -55.5100um -11.0000um -54.8400um
paint metal4
box -11.4000um -55.3500um -11.0000um -54.9500um
paint via3
box -14.6000um -15.7700um -14.2000um -14.8900um
paint metal4
box -14.6000um -15.6600um -14.2000um -15.2600um
paint via3
box -7.2500um -91.2500um -7.1500um -91.1500um
label op c metal4
box 37.4000um -112.2000um 39.4000um -111.8000um
paint metal3
box 37.4000um -99.4000um 39.4000um -99.0000um
paint metal3
box 37.4000um -168.2000um 37.8000um -111.8000um
paint metal4
box 37.4000um -99.4000um 37.8000um -94.2000um
paint metal4
box 39.0000um -112.2000um 39.4000um -99.0000um
paint metal4
box 39.0000um -99.4000um 39.4000um -99.0000um
paint via3
box 39.0000um -112.2000um 39.4000um -111.8000um
paint via3
box 37.4000um -99.4000um 37.8000um -99.0000um
paint via3
box 37.4000um -112.2000um 37.8000um -111.8000um
paint via3
box 37.4000um -168.3100um 37.8000um -167.4300um
paint metal4
box 37.4000um -167.9400um 37.8000um -167.5400um
paint via3
box 37.4000um -94.7100um 37.8000um -93.9700um
paint metal4
box 37.4000um -94.4800um 37.8000um -94.0800um
paint via3
box 36.6000um -115.4000um 40.2000um -115.0000um
paint metal3
box 36.6000um -100.2000um 40.2000um -99.8000um
paint metal3
box 36.6000um -169.8000um 37.0000um -115.0000um
paint metal4
box 36.6000um -100.2000um 37.0000um -93.4000um
paint metal4
box 39.8000um -115.4000um 40.2000um -99.8000um
paint metal4
box 36.6000um -115.4000um 37.0000um -115.0000um
paint via3
box 39.8000um -100.2000um 40.2000um -99.8000um
paint via3
box 36.6000um -100.2000um 37.0000um -99.8000um
paint via3
box 39.8000um -115.4000um 40.2000um -115.0000um
paint via3
box 36.6000um -169.9100um 37.0000um -168.9300um
paint metal4
box 36.6000um -169.4400um 37.0000um -169.0400um
paint via3
box 36.6000um -93.9100um 37.0000um -93.2200um
paint metal4
box 36.6000um -93.7300um 37.0000um -93.3300um
paint via3
box 35.8000um -116.2000um 41.0000um -115.8000um
paint metal3
box -17.0000um -70.6000um -15.0000um -70.2000um
paint metal3
box 31.8000um -65.8000um 41.0000um -65.4000um
paint metal3
box -20.2000um -57.0000um -16.6000um -56.6000um
paint metal3
box -34.6000um -45.0000um -33.4000um -44.6000um
paint metal3
box -34.6000um 0.6000um -17.4000um 1.0000um
paint metal3
box -34.6000um -45.0000um -34.2000um 1.0000um
paint metal4
box -33.8000um -45.0000um -33.4000um -43.8000um
paint metal4
box -20.2000um -57.0000um -19.8000um -43.8000um
paint metal4
box -17.8000um -1.0000um -17.4000um 1.0000um
paint metal4
box -17.0000um -70.6000um -16.6000um -56.6000um
paint metal4
box -15.4000um -70.6000um -15.0000um -67.0000um
paint metal4
box 31.8000um -67.4000um 32.2000um -65.4000um
paint metal4
box 35.8000um -116.2000um 36.2000um -114.2000um
paint metal4
box 40.6000um -116.2000um 41.0000um -65.4000um
paint metal4
box 35.8000um -116.2000um 36.2000um -115.8000um
paint via3
box 40.6000um -116.2000um 41.0000um -115.8000um
paint via3
box -33.8000um -45.0000um -33.4000um -44.6000um
paint via3
box -17.0000um -70.6000um -16.6000um -70.2000um
paint via3
box -15.4000um -70.6000um -15.0000um -70.2000um
paint via3
box -17.8000um 0.6000um -17.4000um 1.0000um
paint via3
box 40.6000um -65.8000um 41.0000um -65.4000um
paint via3
box -34.6000um -45.0000um -34.2000um -44.6000um
paint via3
box -34.6000um 0.6000um -34.2000um 1.0000um
paint via3
box -17.0000um -57.0000um -16.6000um -56.6000um
paint via3
box -20.2000um -57.0000um -19.8000um -56.6000um
paint via3
box 31.8000um -65.8000um 32.2000um -65.4000um
paint via3
box 35.8000um -114.7100um 36.2000um -113.7200um
paint metal4
box 35.8000um -114.2300um 36.2000um -113.8300um
paint via3
box 31.8000um -67.6600um 32.2000um -66.8900um
paint metal4
box 31.8000um -67.5500um 32.2000um -67.1500um
paint via3
box -15.4000um -67.6600um -15.0000um -66.8900um
paint metal4
box -15.4000um -67.5500um -15.0000um -67.1500um
paint via3
box -20.2000um -44.3100um -19.8000um -43.4400um
paint metal4
box -20.2000um -43.9500um -19.8000um -43.5500um
paint via3
box -33.8000um -44.3100um -33.4000um -43.4400um
paint metal4
box -33.8000um -43.9500um -33.4000um -43.5500um
paint via3
box -17.8000um -1.1100um -17.4000um -0.3900um
paint metal4
box -17.8000um -0.9000um -17.4000um -0.5000um
paint via3
box -39.4000um -105.0000um -38.2000um -104.6000um
paint metal3
box -39.4000um -61.8000um -31.8000um -61.4000um
paint metal3
box -18.6000um -56.2000um -10.2000um -55.8000um
paint metal3
box -39.4000um -105.0000um -39.0000um -61.4000um
paint metal4
box -38.6000um -105.8000um -38.2000um -104.6000um
paint metal4
box -32.2000um -62.6000um -31.8000um -61.4000um
paint metal4
box -18.6000um -62.6000um -18.2000um -55.8000um
paint metal4
box -10.6000um -56.2000um -10.2000um -6.2000um
paint metal4
box -10.6000um -56.2000um -10.2000um -55.8000um
paint via3
box -39.4000um -61.8000um -39.0000um -61.4000um
paint via3
box -38.6000um -105.0000um -38.2000um -104.6000um
paint via3
box -18.6000um -56.2000um -18.2000um -55.8000um
paint via3
box -32.2000um -61.8000um -31.8000um -61.4000um
paint via3
box -39.4000um -105.0000um -39.0000um -104.6000um
paint via3
box -38.6000um -105.9100um -38.2000um -105.2300um
paint metal4
box -38.6000um -105.7400um -38.2000um -105.3400um
paint via3
box -32.2000um -62.7400um -31.8000um -62.0900um
paint metal4
box -32.2000um -62.6300um -31.8000um -62.2300um
paint via3
box -18.6000um -62.7400um -18.2000um -62.0900um
paint metal4
box -18.6000um -62.6300um -18.2000um -62.2300um
paint via3
box -10.6000um -6.7700um -10.2000um -6.0900um
paint metal4
box -10.6000um -6.6600um -10.2000um -6.2600um
paint via3
box 38.2000um -113.0000um 41.8000um -112.6000um
paint metal3
box -5.8000um -105.0000um 41.8000um -104.6000um
paint metal3
box -9.8000um -97.0000um -5.4000um -96.6000um
paint metal3
box 37.4000um -72.2000um 41.8000um -71.8000um
paint metal3
box -18.6000um -71.4000um -9.4000um -71.0000um
paint metal3
box -18.6000um -71.4000um -18.2000um -66.2000um
paint metal4
box -9.8000um -97.0000um -9.4000um -71.0000um
paint metal4
box -5.8000um -105.0000um -5.4000um -96.6000um
paint metal4
box 37.4000um -72.2000um 37.8000um -69.4000um
paint metal4
box 38.2000um -113.0000um 38.6000um -109.4000um
paint metal4
box 41.4000um -113.0000um 41.8000um -71.8000um
paint metal4
box 37.4000um -72.2000um 37.8000um -71.8000um
paint via3
box -5.8000um -97.0000um -5.4000um -96.6000um
paint via3
box 41.4000um -105.0000um 41.8000um -104.6000um
paint via3
box 41.4000um -72.2000um 41.8000um -71.8000um
paint via3
box -5.8000um -105.0000um -5.4000um -104.6000um
paint via3
box -18.6000um -71.4000um -18.2000um -71.0000um
paint via3
box -9.8000um -71.4000um -9.4000um -71.0000um
paint via3
box 41.4000um -113.0000um 41.8000um -112.6000um
paint via3
box -9.8000um -97.0000um -9.4000um -96.6000um
paint via3
box 38.2000um -113.0000um 38.6000um -112.6000um
paint via3
box 38.2000um -110.0200um 38.6000um -109.2900um
paint metal4
box 38.2000um -109.9100um 38.6000um -109.5100um
paint via3
box 37.4000um -70.0800um 37.8000um -69.2900um
paint metal4
box 37.4000um -69.9700um 37.8000um -69.5700um
paint via3
box -5.8000um -103.8300um -5.4000um -102.8900um
paint metal4
box -5.8000um -103.7200um -5.4000um -103.3200um
paint via3
box -18.6000um -66.9100um -18.2000um -66.0900um
paint metal4
box -18.6000um -66.8000um -18.2000um -66.4000um
paint via3
box -40.2000um -112.2000um -37.4000um -111.8000um
paint metal3
box -40.2000um -97.0000um -37.4000um -96.6000um
paint metal3
box -26.6000um -74.6000um -25.4000um -74.2000um
paint metal3
box -40.2000um -112.2000um -39.8000um -96.6000um
paint metal4
box -37.8000um -121.0000um -37.4000um -111.8000um
paint metal4
box -37.8000um -99.4000um -37.4000um -96.6000um
paint metal4
box -26.6000um -99.4000um -26.2000um -67.0000um
paint metal4
box -25.8000um -76.2000um -25.4000um -74.2000um
paint metal4
box -40.2000um -112.2000um -39.8000um -111.8000um
paint via3
box -37.8000um -97.0000um -37.4000um -96.6000um
paint via3
box -25.8000um -74.6000um -25.4000um -74.2000um
paint via3
box -37.8000um -112.2000um -37.4000um -111.8000um
paint via3
box -26.6000um -74.6000um -26.2000um -74.2000um
paint via3
box -40.2000um -97.0000um -39.8000um -96.6000um
paint via3
box -37.8000um -121.2800um -37.4000um -120.4900um
paint metal4
box -37.8000um -121.1700um -37.4000um -120.7700um
paint via3
box -37.8000um -99.6600um -37.4000um -98.8900um
paint metal4
box -37.8000um -99.5500um -37.4000um -99.1500um
paint via3
box -26.6000um -99.6600um -26.2000um -98.8900um
paint metal4
box -26.6000um -99.5500um -26.2000um -99.1500um
paint via3
box -25.8000um -76.3100um -25.4000um -75.4600um
paint metal4
box -25.8000um -75.9700um -25.4000um -75.5700um
paint via3
box -26.6000um -67.6600um -26.2000um -66.8900um
paint metal4
box -26.6000um -67.5500um -26.2000um -67.1500um
paint via3
box -37.6500um -120.8500um -37.5500um -120.7500um
label bias_a c metal4
box 7.8000um -45.8000um 10.6000um -45.4000um
paint metal3
box -9.0000um -21.8000um -8.6000um -4.6000um
paint metal4
box 7.8000um -45.8000um 8.2000um -21.4000um
paint metal4
box 10.2000um -58.6000um 10.6000um -43.8000um
paint metal4
box 10.2000um -45.8000um 10.6000um -45.4000um
paint via3
box 7.8000um -45.8000um 8.2000um -45.4000um
paint via3
box 10.2000um -58.7100um 10.6000um -57.9500um
paint metal4
box 10.2000um -58.4600um 10.6000um -58.0600um
paint via3
box 10.2000um -44.3100um 10.6000um -43.4400um
paint metal4
box 10.2000um -43.9500um 10.6000um -43.5500um
paint via3
box 7.8000um -21.9100um 8.2000um -21.2600um
paint metal4
box 7.8000um -21.7700um 8.2000um -21.3700um
paint via3
box -9.0000um -21.9100um -8.6000um -21.2600um
paint metal4
box -9.0000um -21.7700um -8.6000um -21.3700um
paint via3
box -9.0000um -5.2700um -8.6000um -4.4900um
paint metal4
box -9.0000um -5.1600um -8.6000um -4.7600um
paint via3
box 9.4000um -57.0000um 36.2000um -56.6000um
paint metal3
box 9.4000um -57.0000um 9.8000um -7.0000um
paint metal4
box 35.8000um -97.8000um 36.2000um -56.6000um
paint metal4
box 9.4000um -57.0000um 9.8000um -56.6000um
paint via3
box 35.8000um -57.0000um 36.2000um -56.6000um
paint via3
box 35.8000um -98.1600um 36.2000um -97.2900um
paint metal4
box 35.8000um -98.0500um 36.2000um -97.6500um
paint via3
box 9.4000um -7.5200um 9.8000um -6.8900um
paint metal4
box 9.4000um -7.4100um 9.8000um -7.0100um
paint via3
box 35.9500um -97.6500um 36.0500um -97.5500um
label cm c metal4
box -25.8000um -98.6000um -25.4000um -93.4000um
paint metal4
box -25.8000um -98.9100um -25.4000um -98.0900um
paint metal4
box -25.8000um -98.8000um -25.4000um -98.4000um
paint via3
box -25.8000um -93.9100um -25.4000um -93.2200um
paint metal4
box -25.8000um -93.7300um -25.4000um -93.3300um
paint via3
box -35.4500um -118.6500um -34.9500um -118.1500um
paint metal4
box -35.4000um -118.7100um -35.0000um -117.8900um
paint metal4
box -35.4000um -118.4000um -35.0000um -118.0000um
paint via3
box -35.2500um -118.4500um -35.1500um -118.3500um
label IBIAS c metal4
box -41.0000um -171.4000um -37.4000um -171.0000um
paint metal3
box -41.0000um -72.2000um -36.6000um -71.8000um
paint metal3
box -41.0000um -171.4000um -40.6000um -71.8000um
paint metal4
box -37.8000um -171.4000um -37.4000um -167.0000um
paint metal4
box -37.0000um -74.6000um -36.6000um -71.8000um
paint metal4
box -41.0000um -171.4000um -40.6000um -171.0000um
paint via3
box -37.0000um -72.2000um -36.6000um -71.8000um
paint via3
box -37.8000um -171.4000um -37.4000um -171.0000um
paint via3
box -41.0000um -72.2000um -40.6000um -71.8000um
paint via3
box -37.8000um -167.5100um -37.4000um -166.6800um
paint metal4
box -37.8000um -167.1900um -37.4000um -166.7900um
paint via3
box -37.0000um -74.8300um -36.6000um -74.0900um
paint metal4
box -37.0000um -74.7200um -36.6000um -74.3200um
paint via3
box -33.0000um -14.6000um -32.6000um -11.8000um
paint metal4
box -29.0000um -12.2000um -28.6000um -9.4000um
paint metal4
box -17.8000um -10.6000um -17.4000um -5.4000um
paint metal4
box -15.4000um -11.4000um -15.0000um -10.2000um
paint metal4
box -8.2000um -22.6000um -7.8000um -10.2000um
paint metal4
box 7.0000um -44.2000um 7.4000um -22.2000um
paint metal4
box 11.8000um -19.4000um 12.2000um -10.2000um
paint metal4
box 22.2000um -17.8000um 22.6000um -9.4000um
paint metal4
box 7.0000um -44.4600um 7.4000um -43.6900um
paint metal4
box 7.0000um -44.3500um 7.4000um -43.9500um
paint via3
box 7.0000um -22.7100um 7.4000um -22.0100um
paint metal4
box 7.0000um -22.5200um 7.4000um -22.1200um
paint via3
box -8.2000um -22.7100um -7.8000um -22.0100um
paint metal4
box -8.2000um -22.5200um -7.8000um -22.1200um
paint via3
box -8.2000um -10.7100um -7.8000um -9.9500um
paint metal4
box -8.2000um -10.4600um -7.8000um -10.0600um
paint via3
box -15.4000um -10.7100um -15.0000um -9.9500um
paint metal4
box -15.4000um -10.4600um -15.0000um -10.0600um
paint via3
box -15.4000um -11.9700um -15.0000um -10.8900um
paint metal4
box -15.4000um -11.8600um -15.0000um -11.4600um
paint via3
box -29.0000um -12.3100um -28.6000um -11.3500um
paint metal4
box -29.0000um -11.8600um -28.6000um -11.4600um
paint via3
box -29.0000um -10.7100um -28.6000um -9.9500um
paint metal4
box -29.0000um -10.4600um -28.6000um -10.0600um
paint via3
box -29.0000um -9.9100um -28.6000um -9.1500um
paint metal4
box -29.0000um -9.6600um -28.6000um -9.2600um
paint via3
box -33.0000um -12.3100um -32.6000um -11.3500um
paint metal4
box -33.0000um -11.8600um -32.6000um -11.4600um
paint via3
box -33.0000um -15.0200um -32.6000um -14.0900um
paint metal4
box -33.0000um -14.9100um -32.6000um -14.5100um
paint via3
box -17.8000um -10.7100um -17.4000um -9.9500um
paint metal4
box -17.8000um -10.4600um -17.4000um -10.0600um
paint via3
box -17.8000um -6.0200um -17.4000um -5.2900um
paint metal4
box -17.8000um -5.9100um -17.4000um -5.5100um
paint via3
box 11.8000um -10.7100um 12.2000um -9.9500um
paint metal4
box 11.8000um -10.4600um 12.2000um -10.0600um
paint via3
box 11.8000um -17.9700um 12.2000um -17.2900um
paint metal4
box 11.8000um -17.8600um 12.2000um -17.4600um
paint via3
box 11.8000um -19.5200um 12.2000um -18.8900um
paint metal4
box 11.8000um -19.4100um 12.2000um -19.0100um
paint via3
box 22.2000um -17.9700um 22.6000um -17.2900um
paint metal4
box 22.2000um -17.8600um 22.6000um -17.4600um
paint via3
box 22.2000um -10.7100um 22.6000um -9.9500um
paint metal4
box 22.2000um -10.4600um 22.6000um -10.0600um
paint via3
box 22.2000um -9.9100um 22.6000um -9.1500um
paint metal4
box 22.2000um -9.6600um 22.6000um -9.2600um
paint via3
box 6.9500um -44.4000um 7.4500um -43.9000um
paint locali
box 7.0300um -44.3200um 7.3700um -43.9800um
paint mcon
box 7.0300um -44.3200um 7.3700um -43.9800um
paint m2c
box 7.0000um -44.3500um 7.4000um -43.9500um
paint m3c
box 6.9500um -44.4000um 7.4500um -43.9000um
paint metal3
box -8.2500um -10.5100um -7.7500um -10.0100um
paint locali
box -8.1700um -10.4300um -7.8300um -10.0900um
paint mcon
box -8.1700um -10.4300um -7.8300um -10.0900um
paint m2c
box -8.2000um -10.4600um -7.8000um -10.0600um
paint m3c
box -8.2500um -10.5100um -7.7500um -10.0100um
paint metal3
box -15.4500um -10.5100um -14.9500um -10.0100um
paint locali
box -15.3700um -10.4300um -15.0300um -10.0900um
paint mcon
box -15.3700um -10.4300um -15.0300um -10.0900um
paint m2c
box -15.4000um -10.4600um -15.0000um -10.0600um
paint m3c
box -15.4500um -10.5100um -14.9500um -10.0100um
paint metal3
box -15.4500um -11.9100um -14.9500um -11.4100um
paint locali
box -15.3700um -11.8300um -15.0300um -11.4900um
paint mcon
box -15.3700um -11.8300um -15.0300um -11.4900um
paint m2c
box -15.4000um -11.8600um -15.0000um -11.4600um
paint m3c
box -15.4500um -11.9100um -14.9500um -11.4100um
paint metal3
box -29.0500um -11.9100um -28.5500um -11.4100um
paint locali
box -28.9700um -11.8300um -28.6300um -11.4900um
paint mcon
box -28.9700um -11.8300um -28.6300um -11.4900um
paint m2c
box -29.0000um -11.8600um -28.6000um -11.4600um
paint m3c
box -29.0500um -11.9100um -28.5500um -11.4100um
paint metal3
box -29.0500um -10.5100um -28.5500um -10.0100um
paint locali
box -28.9700um -10.4300um -28.6300um -10.0900um
paint mcon
box -28.9700um -10.4300um -28.6300um -10.0900um
paint m2c
box -29.0000um -10.4600um -28.6000um -10.0600um
paint m3c
box -29.0500um -10.5100um -28.5500um -10.0100um
paint metal3
box -33.0500um -11.9100um -32.5500um -11.4100um
paint locali
box -32.9700um -11.8300um -32.6300um -11.4900um
paint mcon
box -32.9700um -11.8300um -32.6300um -11.4900um
paint m2c
box -33.0000um -11.8600um -32.6000um -11.4600um
paint m3c
box -33.0500um -11.9100um -32.5500um -11.4100um
paint metal3
box -17.8500um -10.5100um -17.3500um -10.0100um
paint locali
box -17.7700um -10.4300um -17.4300um -10.0900um
paint mcon
box -17.7700um -10.4300um -17.4300um -10.0900um
paint m2c
box -17.8000um -10.4600um -17.4000um -10.0600um
paint m3c
box -17.8500um -10.5100um -17.3500um -10.0100um
paint metal3
box 11.7500um -10.5100um 12.2500um -10.0100um
paint locali
box 11.8300um -10.4300um 12.1700um -10.0900um
paint mcon
box 11.8300um -10.4300um 12.1700um -10.0900um
paint m2c
box 11.8000um -10.4600um 12.2000um -10.0600um
paint m3c
box 11.7500um -10.5100um 12.2500um -10.0100um
paint metal3
box 11.7500um -17.9100um 12.2500um -17.4100um
paint locali
box 11.8300um -17.8300um 12.1700um -17.4900um
paint mcon
box 11.8300um -17.8300um 12.1700um -17.4900um
paint m2c
box 11.8000um -17.8600um 12.2000um -17.4600um
paint m3c
box 11.7500um -17.9100um 12.2500um -17.4100um
paint metal3
box 22.1500um -17.9100um 22.6500um -17.4100um
paint locali
box 22.2300um -17.8300um 22.5700um -17.4900um
paint mcon
box 22.2300um -17.8300um 22.5700um -17.4900um
paint m2c
box 22.2000um -17.8600um 22.6000um -17.4600um
paint m3c
box 22.1500um -17.9100um 22.6500um -17.4100um
paint metal3
box 22.1500um -10.5100um 22.6500um -10.0100um
paint locali
box 22.2300um -10.4300um 22.5700um -10.0900um
paint mcon
box 22.2300um -10.4300um 22.5700um -10.0900um
paint m2c
box 22.2000um -10.4600um 22.6000um -10.0600um
paint m3c
box 22.1500um -10.5100um 22.6500um -10.0100um
paint metal3
box 7.1500um -44.0500um 7.2500um -43.9500um
label VDD c metal4
box -19.4000um -177.0000um -18.2000um -176.6000um
paint metal3
box -41.8000um -113.0000um -36.6000um -112.6000um
paint metal3
box -41.8000um -96.2000um -37.4000um -95.8000um
paint metal3
box -19.4000um -72.2000um -14.2000um -71.8000um
paint metal3
box -41.8000um -113.0000um -41.4000um -95.8000um
paint metal4
box -37.8000um -96.2000um -37.4000um -93.4000um
paint metal4
box -37.0000um -121.8000um -36.6000um -110.2000um
paint metal4
box -37.0000um -97.8000um -36.6000um -93.4000um
paint metal4
box -35.4000um -112.2000um -35.0000um -110.2000um
paint metal4
box -32.2000um -73.0000um -31.8000um -67.8000um
paint metal4
box -31.4000um -93.0000um -31.0000um -72.6000um
paint metal4
box -25.0000um -97.8000um -24.6000um -94.2000um
paint metal4
box -19.4000um -177.0000um -19.0000um -170.2000um
paint metal4
box -19.4000um -72.2000um -19.0000um -67.8000um
paint metal4
box -18.6000um -177.0000um -18.2000um -175.0000um
paint metal4
box -18.6000um -172.2000um -18.2000um -170.2000um
paint metal4
box -14.6000um -72.2000um -14.2000um -67.8000um
paint metal4
box -6.6000um -97.8000um -6.2000um -92.6000um
paint metal4
box -3.4000um -97.0000um -3.0000um -95.0000um
paint metal4
box 35.0000um -170.6000um 35.4000um -121.4000um
paint metal4
box 35.7500um -112.2500um 36.2500um -111.7500um
paint metal4
box -41.8000um -113.0000um -41.4000um -112.6000um
paint via3
box -37.0000um -113.0000um -36.6000um -112.6000um
paint via3
box -14.6000um -72.2000um -14.2000um -71.8000um
paint via3
box -18.6000um -177.0000um -18.2000um -176.6000um
paint via3
box -19.4000um -72.2000um -19.0000um -71.8000um
paint via3
box -37.8000um -96.2000um -37.4000um -95.8000um
paint via3
box -41.8000um -96.2000um -41.4000um -95.8000um
paint via3
box -19.4000um -177.0000um -19.0000um -176.6000um
paint via3
box -18.6000um -175.8600um -18.2000um -174.8900um
paint metal4
box -18.6000um -175.7500um -18.2000um -175.3500um
paint via3
box -19.4000um -170.7100um -19.0000um -169.7300um
paint metal4
box -19.4000um -170.2400um -19.0000um -169.8400um
paint via3
box -18.6000um -170.7100um -18.2000um -169.7300um
paint metal4
box -18.6000um -170.2400um -18.2000um -169.8400um
paint via3
box -18.6000um -172.3100um -18.2000um -171.3500um
paint metal4
box -18.6000um -171.8600um -18.2000um -171.4600um
paint via3
box 35.0000um -170.7100um 35.4000um -169.7300um
paint metal4
box 35.0000um -170.2400um 35.4000um -169.8400um
paint via3
box 35.0000um -122.0300um 35.4000um -121.2900um
paint metal4
box 35.0000um -121.9200um 35.4000um -121.5200um
paint via3
box -37.0000um -122.0300um -36.6000um -121.2900um
paint metal4
box -37.0000um -121.9200um -36.6000um -121.5200um
paint via3
box -37.0000um -110.8200um -36.6000um -110.0900um
paint metal4
box -37.0000um -110.7100um -36.6000um -110.3100um
paint via3
box -35.4000um -110.8200um -35.0000um -110.0900um
paint metal4
box -35.4000um -110.7100um -35.0000um -110.3100um
paint via3
box -35.4000um -112.3100um -35.0000um -111.4200um
paint metal4
box -35.4000um -111.9300um -35.0000um -111.5300um
paint via3
box 35.8000um -112.3100um 36.2000um -111.4200um
paint metal4
box 35.8000um -111.9300um 36.2000um -111.5300um
paint via3
box 35.8000um -112.8400um 36.2000um -111.6900um
paint metal4
box 35.8000um -112.7300um 36.2000um -112.3300um
paint via3
box -37.8000um -93.9100um -37.4000um -92.8700um
paint metal4
box -37.8000um -93.3800um -37.4000um -92.9800um
paint via3
box -37.0000um -93.9100um -36.6000um -92.8700um
paint metal4
box -37.0000um -93.3800um -36.6000um -92.9800um
paint via3
box -37.0000um -98.1100um -36.6000um -97.2900um
paint metal4
box -37.0000um -98.0000um -36.6000um -97.6000um
paint via3
box -25.0000um -98.1100um -24.6000um -97.2900um
paint metal4
box -25.0000um -98.0000um -24.6000um -97.6000um
paint via3
box -25.0000um -95.5100um -24.6000um -94.7700um
paint metal4
box -25.0000um -95.2800um -24.6000um -94.8800um
paint via3
box -25.0000um -94.7100um -24.6000um -93.9700um
paint metal4
box -25.0000um -94.4800um -24.6000um -94.0800um
paint via3
box -6.6000um -98.1100um -6.2000um -97.2900um
paint metal4
box -6.6000um -98.0000um -6.2000um -97.6000um
paint via3
box -6.6000um -95.5100um -6.2000um -94.7700um
paint metal4
box -6.6000um -95.2800um -6.2000um -94.8800um
paint via3
box -3.4000um -95.5100um -3.0000um -94.7700um
paint metal4
box -3.4000um -95.2800um -3.0000um -94.8800um
paint via3
box -3.4000um -96.6100um -3.0000um -95.6900um
paint metal4
box -3.4000um -96.5000um -3.0000um -96.1000um
paint via3
box -3.4000um -97.4100um -3.0000um -96.4900um
paint metal4
box -3.4000um -97.3000um -3.0000um -96.9000um
paint via3
box -6.6000um -93.1100um -6.2000um -92.4700um
paint metal4
box -6.6000um -92.9800um -6.2000um -92.5800um
paint via3
box -31.4000um -93.4900um -31.0000um -92.4900um
paint metal4
box -31.4000um -93.3800um -31.0000um -92.9800um
paint via3
box -31.4000um -73.2800um -31.0000um -72.4900um
paint metal4
box -31.4000um -73.1700um -31.0000um -72.7700um
paint via3
box -32.2000um -73.2800um -31.8000um -72.4900um
paint metal4
box -32.2000um -73.1700um -31.8000um -72.7700um
paint via3
box -32.2000um -68.4600um -31.8000um -67.6900um
paint metal4
box -32.2000um -68.3500um -31.8000um -67.9500um
paint via3
box -19.4000um -68.4600um -19.0000um -67.6900um
paint metal4
box -19.4000um -68.3500um -19.0000um -67.9500um
paint via3
box -14.6000um -68.4600um -14.2000um -67.6900um
paint metal4
box -14.6000um -68.3500um -14.2000um -67.9500um
paint via3
box -18.6500um -175.8000um -18.1500um -175.3000um
paint locali
box -18.5700um -175.7200um -18.2300um -175.3800um
paint mcon
box -18.5700um -175.7200um -18.2300um -175.3800um
paint m2c
box -18.6000um -175.7500um -18.2000um -175.3500um
paint m3c
box -18.6500um -175.8000um -18.1500um -175.3000um
paint metal3
box -19.4500um -170.2900um -18.9500um -169.7900um
paint locali
box -19.3700um -170.2100um -19.0300um -169.8700um
paint mcon
box -19.3700um -170.2100um -19.0300um -169.8700um
paint m2c
box -19.4000um -170.2400um -19.0000um -169.8400um
paint m3c
box -19.4500um -170.2900um -18.9500um -169.7900um
paint metal3
box -18.6500um -170.2900um -18.1500um -169.7900um
paint locali
box -18.5700um -170.2100um -18.2300um -169.8700um
paint mcon
box -18.5700um -170.2100um -18.2300um -169.8700um
paint m2c
box -18.6000um -170.2400um -18.2000um -169.8400um
paint m3c
box -18.6500um -170.2900um -18.1500um -169.7900um
paint metal3
box 34.9500um -170.2900um 35.4500um -169.7900um
paint locali
box 35.0300um -170.2100um 35.3700um -169.8700um
paint mcon
box 35.0300um -170.2100um 35.3700um -169.8700um
paint m2c
box 35.0000um -170.2400um 35.4000um -169.8400um
paint m3c
box 34.9500um -170.2900um 35.4500um -169.7900um
paint metal3
box -37.0500um -110.7600um -36.5500um -110.2600um
paint locali
box -36.9700um -110.6800um -36.6300um -110.3400um
paint mcon
box -36.9700um -110.6800um -36.6300um -110.3400um
paint m2c
box -37.0000um -110.7100um -36.6000um -110.3100um
paint m3c
box -37.0500um -110.7600um -36.5500um -110.2600um
paint metal3
box -35.4500um -110.7600um -34.9500um -110.2600um
paint locali
box -35.3700um -110.6800um -35.0300um -110.3400um
paint mcon
box -35.3700um -110.6800um -35.0300um -110.3400um
paint m2c
box -35.4000um -110.7100um -35.0000um -110.3100um
paint m3c
box -35.4500um -110.7600um -34.9500um -110.2600um
paint metal3
box -35.4500um -111.9800um -34.9500um -111.4800um
paint locali
box -35.3700um -111.9000um -35.0300um -111.5600um
paint mcon
box -35.3700um -111.9000um -35.0300um -111.5600um
paint m2c
box -35.4000um -111.9300um -35.0000um -111.5300um
paint m3c
box -35.4500um -111.9800um -34.9500um -111.4800um
paint metal3
box 35.7500um -111.9800um 36.2500um -111.4800um
paint locali
box 35.8300um -111.9000um 36.1700um -111.5600um
paint mcon
box 35.8300um -111.9000um 36.1700um -111.5600um
paint m2c
box 35.8000um -111.9300um 36.2000um -111.5300um
paint m3c
box 35.7500um -111.9800um 36.2500um -111.4800um
paint metal3
box -37.0500um -98.0500um -36.5500um -97.5500um
paint locali
box -36.9700um -97.9700um -36.6300um -97.6300um
paint mcon
box -36.9700um -97.9700um -36.6300um -97.6300um
paint m2c
box -37.0000um -98.0000um -36.6000um -97.6000um
paint m3c
box -37.0500um -98.0500um -36.5500um -97.5500um
paint metal3
box -25.0500um -98.0500um -24.5500um -97.5500um
paint locali
box -24.9700um -97.9700um -24.6300um -97.6300um
paint mcon
box -24.9700um -97.9700um -24.6300um -97.6300um
paint m2c
box -25.0000um -98.0000um -24.6000um -97.6000um
paint m3c
box -25.0500um -98.0500um -24.5500um -97.5500um
paint metal3
box -25.0500um -95.3300um -24.5500um -94.8300um
paint locali
box -24.9700um -95.2500um -24.6300um -94.9100um
paint mcon
box -24.9700um -95.2500um -24.6300um -94.9100um
paint m2c
box -25.0000um -95.2800um -24.6000um -94.8800um
paint m3c
box -25.0500um -95.3300um -24.5500um -94.8300um
paint metal3
box -6.6500um -98.0500um -6.1500um -97.5500um
paint locali
box -6.5700um -97.9700um -6.2300um -97.6300um
paint mcon
box -6.5700um -97.9700um -6.2300um -97.6300um
paint m2c
box -6.6000um -98.0000um -6.2000um -97.6000um
paint m3c
box -6.6500um -98.0500um -6.1500um -97.5500um
paint metal3
box -6.6500um -95.3300um -6.1500um -94.8300um
paint locali
box -6.5700um -95.2500um -6.2300um -94.9100um
paint mcon
box -6.5700um -95.2500um -6.2300um -94.9100um
paint m2c
box -6.6000um -95.2800um -6.2000um -94.8800um
paint m3c
box -6.6500um -95.3300um -6.1500um -94.8300um
paint metal3
box -3.4500um -95.3300um -2.9500um -94.8300um
paint locali
box -3.3700um -95.2500um -3.0300um -94.9100um
paint mcon
box -3.3700um -95.2500um -3.0300um -94.9100um
paint m2c
box -3.4000um -95.2800um -3.0000um -94.8800um
paint m3c
box -3.4500um -95.3300um -2.9500um -94.8300um
paint metal3
box -3.4500um -96.5500um -2.9500um -96.0500um
paint locali
box -3.3700um -96.4700um -3.0300um -96.1300um
paint mcon
box -3.3700um -96.4700um -3.0300um -96.1300um
paint m2c
box -3.4000um -96.5000um -3.0000um -96.1000um
paint m3c
box -3.4500um -96.5500um -2.9500um -96.0500um
paint metal3
box -31.4500um -73.2200um -30.9500um -72.7200um
paint locali
box -31.3700um -73.1400um -31.0300um -72.8000um
paint mcon
box -31.3700um -73.1400um -31.0300um -72.8000um
paint m2c
box -31.4000um -73.1700um -31.0000um -72.7700um
paint m3c
box -31.4500um -73.2200um -30.9500um -72.7200um
paint metal3
box -32.2500um -73.2200um -31.7500um -72.7200um
paint locali
box -32.1700um -73.1400um -31.8300um -72.8000um
paint mcon
box -32.1700um -73.1400um -31.8300um -72.8000um
paint m2c
box -32.2000um -73.1700um -31.8000um -72.7700um
paint m3c
box -32.2500um -73.2200um -31.7500um -72.7200um
paint metal3
box -32.2500um -68.4000um -31.7500um -67.9000um
paint locali
box -32.1700um -68.3200um -31.8300um -67.9800um
paint mcon
box -32.1700um -68.3200um -31.8300um -67.9800um
paint m2c
box -32.2000um -68.3500um -31.8000um -67.9500um
paint m3c
box -32.2500um -68.4000um -31.7500um -67.9000um
paint metal3
box -19.4500um -68.4000um -18.9500um -67.9000um
paint locali
box -19.3700um -68.3200um -19.0300um -67.9800um
paint mcon
box -19.3700um -68.3200um -19.0300um -67.9800um
paint m2c
box -19.4000um -68.3500um -19.0000um -67.9500um
paint m3c
box -19.4500um -68.4000um -18.9500um -67.9000um
paint metal3
box -14.6500um -68.4000um -14.1500um -67.9000um
paint locali
box -14.5700um -68.3200um -14.2300um -67.9800um
paint mcon
box -14.5700um -68.3200um -14.2300um -67.9800um
paint m2c
box -14.6000um -68.3500um -14.2000um -67.9500um
paint m3c
box -14.6500um -68.4000um -14.1500um -67.9000um
paint metal3
box -18.4500um -175.2500um -18.3500um -175.1500um
label VSS c metal4
box 35.8000um -119.4000um 42.6000um -119.0000um
paint metal3
box -9.0000um -56.2000um 1.8000um -55.8000um
paint metal3
box 38.2000um -56.2000um 42.6000um -55.8000um
paint metal3
box -9.0000um -56.2000um -8.6000um -47.0000um
paint metal4
box 1.4000um -56.2000um 1.8000um -55.0000um
paint metal4
box 35.8000um -120.2000um 36.2000um -119.0000um
paint metal4
box 38.2000um -56.2000um 38.6000um -55.0000um
paint metal4
box 42.2000um -119.4000um 42.6000um -55.8000um
paint metal4
box 42.2000um -56.2000um 42.6000um -55.8000um
paint via3
box -9.0000um -56.2000um -8.6000um -55.8000um
paint via3
box 1.4000um -56.2000um 1.8000um -55.8000um
paint via3
box 42.2000um -119.4000um 42.6000um -119.0000um
paint via3
box 35.8000um -119.4000um 36.2000um -119.0000um
paint via3
box 38.2000um -56.2000um 38.6000um -55.8000um
paint via3
box 35.8000um -120.5300um 36.2000um -119.6900um
paint metal4
box 35.8000um -120.4200um 36.2000um -120.0200um
paint via3
box 38.2000um -55.5100um 38.6000um -54.8400um
paint metal4
box 38.2000um -55.3500um 38.6000um -54.9500um
paint via3
box 1.4000um -55.5100um 1.8000um -54.8400um
paint metal4
box 1.4000um -55.3500um 1.8000um -54.9500um
paint via3
box -9.0000um -47.5100um -8.6000um -46.6400um
paint metal4
box -9.0000um -47.1500um -8.6000um -46.7500um
paint via3
box 35.9500um -120.0500um 36.0500um -119.9500um
label cmc c metal4
box -36.2500um -94.6500um -35.7500um -94.1500um
paint metal4
box -36.2000um -94.9900um -35.8000um -94.0900um
paint metal4
box -36.2000um -94.8800um -35.8000um -94.4800um
paint via3
box -36.0500um -94.4500um -35.9500um -94.3500um
label in c metal4
box -35.4500um -93.8500um -34.9500um -93.3500um
paint metal4
box -35.4000um -94.2400um -35.0000um -93.2900um
paint metal4
box -35.4000um -94.1300um -35.0000um -93.7300um
paint via3
box -35.2500um -93.6500um -35.1500um -93.5500um
label ip c metal4
tech revert
save iadc_ota_v2_routed
gds write iadc_ota_v2_routed
quit -noprompt
