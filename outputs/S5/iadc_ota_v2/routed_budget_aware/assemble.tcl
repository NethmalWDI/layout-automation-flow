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
load iadc_ota_v2_routed -silent
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
box -34.6000um -25.0000um -29.4000um -24.6000um
paint metal3
box -34.6000um -25.0000um -34.2000um -22.2000um
paint metal4
box -29.8000um -25.0000um -29.4000um -22.2000um
paint metal4
box -34.6000um -25.0000um -34.2000um -24.6000um
paint via3
box -29.8000um -25.0000um -29.4000um -24.6000um
paint via3
box -34.6000um -22.7900um -34.2000um -22.0900um
paint metal4
box -34.6000um -22.6800um -34.2000um -22.2800um
paint via3
box -29.8000um -22.7900um -29.4000um -22.0900um
paint metal4
box -29.8000um -22.6800um -29.4000um -22.2800um
paint via3
box -35.4000um -25.8000um -28.6000um -25.4000um
paint metal3
box -35.4000um -25.8000um -35.0000um -19.8000um
paint metal4
box -29.0000um -25.8000um -28.6000um -20.6000um
paint metal4
box -29.0000um -25.8000um -28.6000um -25.4000um
paint via3
box -35.4000um -25.8000um -35.0000um -25.4000um
paint via3
box -29.0000um -21.2900um -28.6000um -20.4900um
paint metal4
box -29.0000um -21.1800um -28.6000um -20.7800um
paint via3
box -35.4000um -20.5400um -35.0000um -19.6900um
paint metal4
box -35.4000um -20.4300um -35.0000um -20.0300um
paint via3
box -36.2000um -26.6000um -27.8000um -26.2000um
paint metal3
box -36.2000um -26.6000um -35.8000um -21.4000um
paint metal4
box -28.2000um -26.6000um -27.8000um -21.4000um
paint metal4
box -36.2000um -26.6000um -35.8000um -26.2000um
paint via3
box -28.2000um -26.6000um -27.8000um -26.2000um
paint via3
box -36.2000um -22.0400um -35.8000um -21.2900um
paint metal4
box -36.2000um -21.9300um -35.8000um -21.5300um
paint via3
box -28.2000um -22.0400um -27.8000um -21.2900um
paint metal4
box -28.2000um -21.9300um -27.8000um -21.5300um
paint via3
box 16.6000um -96.2000um 17.0000um -89.4000um
paint metal4
box 24.6000um -96.2000um 25.0000um -91.0000um
paint metal4
box 24.6000um -96.6600um 25.0000um -95.6900um
paint metal4
box 24.6000um -96.5500um 25.0000um -96.1500um
paint via3
box 24.6000um -91.5100um 25.0000um -90.6300um
paint metal4
box 24.6000um -91.1400um 25.0000um -90.7400um
paint via3
box 16.6000um -96.6600um 17.0000um -95.6900um
paint metal4
box 16.6000um -96.5500um 17.0000um -96.1500um
paint via3
box 16.6000um -89.9100um 17.0000um -89.1300um
paint metal4
box 16.6000um -89.6400um 17.0000um -89.2400um
paint via3
box 17.4000um -97.0000um 17.8000um -91.0000um
paint metal4
box 25.4000um -97.0000um 25.8000um -90.2000um
paint metal4
box 17.4000um -97.4100um 17.8000um -96.4900um
paint metal4
box 17.4000um -97.3000um 17.8000um -96.9000um
paint via3
box 17.4000um -91.5100um 17.8000um -90.6300um
paint metal4
box 17.4000um -91.1400um 17.8000um -90.7400um
paint via3
box 25.4000um -97.4100um 25.8000um -96.4900um
paint metal4
box 25.4000um -97.3000um 25.8000um -96.9000um
paint via3
box 25.4000um -90.7100um 25.8000um -89.8800um
paint metal4
box 25.4000um -90.3900um 25.8000um -89.9900um
paint via3
box 34.2000um -112.2000um 34.6000um -89.4000um
paint metal4
box 61.4000um -89.8000um 61.8000um -57.4000um
paint metal4
box 34.2000um -112.3100um 34.6000um -111.5300um
paint metal4
box 34.2000um -112.0400um 34.6000um -111.6400um
paint via3
box 34.2000um -89.9100um 34.6000um -89.1300um
paint metal4
box 34.2000um -89.6400um 34.6000um -89.2400um
paint via3
box 61.4000um -89.9100um 61.8000um -89.1300um
paint metal4
box 61.4000um -89.6400um 61.8000um -89.2400um
paint via3
box 61.4000um -57.9700um 61.8000um -57.2900um
paint metal4
box 61.4000um -57.8600um 61.8000um -57.4600um
paint via3
box 34.3500um -112.0500um 34.4500um -111.9500um
label on c metal4
box 35.0000um -113.0000um 35.4000um -87.8000um
paint metal4
box 62.2000um -88.2000um 62.6000um -44.6000um
paint metal4
box 35.0000um -113.1100um 35.4000um -112.2800um
paint metal4
box 35.0000um -112.7900um 35.4000um -112.3900um
paint via3
box 35.0000um -88.3100um 35.4000um -87.6300um
paint metal4
box 35.0000um -88.1400um 35.4000um -87.7400um
paint via3
box 62.2000um -88.3100um 62.6000um -87.6300um
paint metal4
box 62.2000um -88.1400um 62.6000um -87.7400um
paint via3
box 62.2000um -45.4700um 62.6000um -44.4900um
paint metal4
box 62.2000um -45.3600um 62.6000um -44.9600um
paint via3
box 35.1500um -112.8500um 35.2500um -112.7500um
label op c metal4
box 11.0000um -105.0000um 15.4000um -104.6000um
paint metal3
box 11.0000um -108.2000um 11.4000um -104.6000um
paint metal4
box 15.0000um -110.6000um 15.4000um -104.6000um
paint metal4
box 15.0000um -105.0000um 15.4000um -104.6000um
paint via3
box 11.0000um -105.0000um 11.4000um -104.6000um
paint via3
box 15.0000um -110.7100um 15.4000um -110.0300um
paint metal4
box 15.0000um -110.5400um 15.4000um -110.1400um
paint via3
box 11.0000um -108.4000um 11.4000um -107.6900um
paint metal4
box 11.0000um -108.2900um 11.4000um -107.8900um
paint via3
box 10.2000um -104.2000um 16.2000um -103.8000um
paint metal3
box 10.2000um -106.6000um 10.6000um -103.8000um
paint metal4
box 15.8000um -111.4000um 16.2000um -103.8000um
paint metal4
box 15.8000um -104.2000um 16.2000um -103.8000um
paint via3
box 10.2000um -104.2000um 10.6000um -103.8000um
paint via3
box 15.8000um -111.5100um 16.2000um -110.7800um
paint metal4
box 15.8000um -111.2900um 16.2000um -110.8900um
paint via3
box 10.2000um -106.9000um 10.6000um -106.0900um
paint metal4
box 10.2000um -106.7900um 10.6000um -106.3900um
paint via3
box -38.6000um -48.2000um 26.6000um -47.8000um
paint metal3
box -30.6000um -13.0000um -29.4000um -12.6000um
paint metal3
box -38.6000um -48.2000um -38.2000um -27.0000um
paint metal4
box -30.6000um -28.2000um -30.2000um -12.6000um
paint metal4
box -29.8000um -13.8000um -29.4000um -12.6000um
paint metal4
box -9.8000um -48.2000um -9.4000um -27.8000um
paint metal4
box 26.2000um -76.2000um 26.6000um -47.8000um
paint metal4
box -9.8000um -48.2000um -9.4000um -47.8000um
paint via3
box -38.6000um -48.2000um -38.2000um -47.8000um
paint via3
box 26.2000um -48.2000um 26.6000um -47.8000um
paint via3
box -29.8000um -13.0000um -29.4000um -12.6000um
paint via3
box -30.6000um -13.0000um -30.2000um -12.6000um
paint via3
box 26.2000um -76.3100um 26.6000um -75.3600um
paint metal4
box 26.2000um -75.8700um 26.6000um -75.4700um
paint via3
box -9.8000um -28.3100um -9.4000um -27.6000um
paint metal4
box -9.8000um -28.1100um -9.4000um -27.7100um
paint via3
box -30.6000um -28.3100um -30.2000um -27.6000um
paint metal4
box -30.6000um -28.1100um -30.2000um -27.7100um
paint via3
box -29.8000um -14.0300um -29.4000um -13.2900um
paint metal4
box -29.8000um -13.9200um -29.4000um -13.5200um
paint via3
box -38.6000um -27.5100um -38.2000um -26.8300um
paint metal4
box -38.6000um -27.3400um -38.2000um -26.9400um
paint via3
box 6.2000um -49.0000um 11.4000um -48.6000um
paint metal3
box -9.0000um -51.4000um -8.6000um -19.0000um
paint metal4
box 6.2000um -51.4000um 6.6000um -48.6000um
paint metal4
box 11.0000um -49.8000um 11.4000um -48.6000um
paint metal4
box 11.0000um -49.0000um 11.4000um -48.6000um
paint via3
box 6.2000um -49.0000um 6.6000um -48.6000um
paint via3
box 6.2000um -51.9000um 6.6000um -50.8900um
paint metal4
box 6.2000um -51.7900um 6.6000um -51.3900um
paint via3
box 11.0000um -50.0000um 11.4000um -49.2900um
paint metal4
box 11.0000um -49.8900um 11.4000um -49.4900um
paint via3
box -9.0000um -51.9000um -8.6000um -50.8900um
paint metal4
box -9.0000um -51.7900um -8.6000um -51.3900um
paint via3
box -9.0000um -19.7900um -8.6000um -18.8900um
paint metal4
box -9.0000um -19.6800um -8.6000um -19.2800um
paint via3
box 23.0000um -93.0000um 36.2000um -92.6000um
paint metal3
box 23.0000um -57.0000um 27.4000um -56.6000um
paint metal3
box -5.0000um -51.4000um -4.6000um -46.2000um
paint metal4
box 11.8000um -50.6000um 12.2000um -46.2000um
paint metal4
box 23.0000um -93.0000um 23.4000um -56.6000um
paint metal4
box 27.0000um -57.0000um 27.4000um -46.2000um
paint metal4
box 35.8000um -156.2000um 36.2000um -92.6000um
paint metal4
box 23.0000um -57.0000um 23.4000um -56.6000um
paint via3
box 35.8000um -93.0000um 36.2000um -92.6000um
paint via3
box 23.0000um -93.0000um 23.4000um -92.6000um
paint via3
box 27.0000um -57.0000um 27.4000um -56.6000um
paint via3
box 35.8000um -156.3100um 36.2000um -155.3000um
paint metal4
box 35.8000um -155.8100um 36.2000um -155.4100um
paint via3
box 27.0000um -46.7100um 27.4000um -45.7600um
paint metal4
box 27.0000um -46.2700um 27.4000um -45.8700um
paint via3
box 11.8000um -46.7100um 12.2000um -45.7600um
paint metal4
box 11.8000um -46.2700um 12.2000um -45.8700um
paint via3
box 11.8000um -50.7500um 12.2000um -50.0900um
paint metal4
box 11.8000um -50.6400um 12.2000um -50.2400um
paint via3
box -5.0000um -46.7100um -4.6000um -45.7600um
paint metal4
box -5.0000um -46.2700um -4.6000um -45.8700um
paint via3
box -5.0000um -51.5100um -4.6000um -50.5300um
paint metal4
box -5.0000um -51.0400um -4.6000um -50.6400um
paint via3
box 9.4000um -93.0000um 22.6000um -92.6000um
paint metal3
box 7.0000um -59.4000um 7.4000um -45.4000um
paint metal4
box 9.4000um -156.2000um 9.8000um -92.6000um
paint metal4
box 11.0000um -59.4000um 11.4000um -54.2000um
paint metal4
box 22.2000um -93.0000um 22.6000um -59.0000um
paint metal4
box 22.2000um -93.0000um 22.6000um -92.6000um
paint via3
box 9.4000um -93.0000um 9.8000um -92.6000um
paint via3
box 9.4000um -156.3100um 9.8000um -155.3000um
paint metal4
box 9.4000um -155.8100um 9.8000um -155.4100um
paint via3
box 22.2000um -59.6900um 22.6000um -58.8900um
paint metal4
box 22.2000um -59.5800um 22.6000um -59.1800um
paint via3
box 11.0000um -59.6900um 11.4000um -58.8900um
paint metal4
box 11.0000um -59.5800um 11.4000um -59.1800um
paint via3
box 11.0000um -54.9200um 11.4000um -54.0900um
paint metal4
box 11.0000um -54.8100um 11.4000um -54.4100um
paint via3
box 7.0000um -59.6900um 7.4000um -58.8900um
paint metal4
box 7.0000um -59.5800um 7.4000um -59.1800um
paint via3
box 7.0000um -45.9100um 7.4000um -45.0100um
paint metal4
box 7.0000um -45.5200um 7.4000um -45.1200um
paint via3
box 9.5500um -156.0500um 9.6500um -155.9500um
label bias_a c metal4
box 19.8000um -67.4000um 28.2000um -67.0000um
paint metal3
box 7.0000um -25.0000um 28.2000um -24.6000um
paint metal3
box -34.6000um -3.4000um 8.2000um -3.0000um
paint metal3
box -53.0000um 0.6000um -51.0000um 1.0000um
paint metal3
box -53.0000um -28.2000um -52.6000um 1.0000um
paint metal4
box -51.4000um -1.0000um -51.0000um 1.0000um
paint metal4
box -34.6000um -3.4000um -34.2000um -0.6000um
paint metal4
box 7.0000um -25.0000um 7.4000um -18.2000um
paint metal4
box 7.8000um -25.0000um 8.2000um -3.0000um
paint metal4
box 19.8000um -70.6000um 20.2000um -67.0000um
paint metal4
box 27.8000um -67.4000um 28.2000um -24.6000um
paint metal4
box 7.8000um -3.4000um 8.2000um -3.0000um
paint via3
box -53.0000um 0.6000um -52.6000um 1.0000um
paint via3
box 7.0000um -25.0000um 7.4000um -24.6000um
paint via3
box 27.8000um -25.0000um 28.2000um -24.6000um
paint via3
box 7.8000um -25.0000um 8.2000um -24.6000um
paint via3
box -51.4000um 0.6000um -51.0000um 1.0000um
paint via3
box 27.8000um -67.4000um 28.2000um -67.0000um
paint via3
box -34.6000um -3.4000um -34.2000um -3.0000um
paint via3
box 19.8000um -67.4000um 20.2000um -67.0000um
paint via3
box 19.8000um -70.9700um 20.2000um -70.0900um
paint metal4
box 19.8000um -70.8600um 20.2000um -70.4600um
paint via3
box 7.0000um -18.7100um 7.4000um -17.6700um
paint metal4
box 7.0000um -18.1800um 7.4000um -17.7800um
paint via3
box -34.6000um -1.1100um -34.2000um -0.3900um
paint metal4
box -34.6000um -0.9000um -34.2000um -0.5000um
paint via3
box -51.4000um -1.1100um -51.0000um -0.3900um
paint metal4
box -51.4000um -0.9000um -51.0000um -0.5000um
paint via3
box -53.0000um -28.3100um -52.6000um -27.5800um
paint metal4
box -53.0000um -28.0900um -52.6000um -27.6900um
paint via3
box -26.6000um -56.2000um 8.2000um -55.8000um
paint metal3
box -5.8000um -47.4000um 8.2000um -47.0000um
paint metal3
box -26.6000um -58.6000um -26.2000um -55.8000um
paint metal4
box -5.8000um -47.4000um -5.4000um -19.8000um
paint metal4
box 7.8000um -56.2000um 8.2000um -47.0000um
paint metal4
box -5.8000um -47.4000um -5.4000um -47.0000um
paint via3
box 7.8000um -47.4000um 8.2000um -47.0000um
paint via3
box -26.6000um -56.2000um -26.2000um -55.8000um
paint via3
box 7.8000um -56.2000um 8.2000um -55.8000um
paint via3
box -26.6000um -58.9400um -26.2000um -58.0900um
paint metal4
box -26.6000um -58.8300um -26.2000um -58.4300um
paint via3
box -5.8000um -20.5400um -5.4000um -19.6900um
paint metal4
box -5.8000um -20.4300um -5.4000um -20.0300um
paint via3
box -26.4500um -58.4500um -26.3500um -58.3500um
label cm c metal4
box 21.4000um -57.8000um 29.0000um -57.4000um
paint metal3
box 27.0000um -39.4000um 29.0000um -39.0000um
paint metal3
box 21.4000um -61.0000um 21.8000um -57.4000um
paint metal4
box 27.0000um -41.0000um 27.4000um -39.0000um
paint metal4
box 28.6000um -57.8000um 29.0000um -39.0000um
paint metal4
box 28.6000um -57.8000um 29.0000um -57.4000um
paint via3
box 21.4000um -57.8000um 21.8000um -57.4000um
paint via3
box 27.0000um -39.4000um 27.4000um -39.0000um
paint via3
box 28.6000um -39.4000um 29.0000um -39.0000um
paint via3
box 21.4000um -61.1900um 21.8000um -60.4900um
paint metal4
box 21.4000um -61.0800um 21.8000um -60.6800um
paint via3
box 27.0000um -41.4600um 27.4000um -40.4900um
paint metal4
box 27.0000um -41.3500um 27.4000um -40.9500um
paint via3
box -33.8500um -27.4500um -33.3500um -26.9500um
paint metal4
box -33.8000um -27.5100um -33.4000um -26.8500um
paint metal4
box -33.8000um -27.3600um -33.4000um -26.9600um
paint via3
box -33.6500um -27.2500um -33.5500um -27.1500um
label IBIAS c metal4
box 8.6000um -93.8000um 18.6000um -93.4000um
paint metal3
box 8.6000um -109.0000um 9.0000um -93.4000um
paint metal4
box 18.2000um -95.4000um 18.6000um -93.4000um
paint metal4
box 18.2000um -93.8000um 18.6000um -93.4000um
paint via3
box 8.6000um -93.8000um 9.0000um -93.4000um
paint via3
box 8.6000um -109.1500um 9.0000um -108.4900um
paint metal4
box 8.6000um -109.0400um 9.0000um -108.6400um
paint via3
box 18.2000um -95.9100um 18.6000um -94.8900um
paint metal4
box 18.2000um -95.8000um 18.6000um -95.4000um
paint via3
box 19.8000um -93.8000um 26.6000um -93.4000um
paint metal3
box 19.8000um -73.8000um 25.0000um -73.4000um
paint metal3
box 6.2000um -34.6000um 36.2000um -34.2000um
paint metal3
box 50.2000um -34.6000um 55.4000um -34.2000um
paint metal3
box 6.2000um -25.8000um 9.0000um -25.4000um
paint metal3
box -34.6000um -12.2000um 9.0000um -11.8000um
paint metal3
box -51.4000um -23.4000um -51.0000um -20.6000um
paint metal4
box -34.6000um -20.2000um -34.2000um -11.8000um
paint metal4
box -27.4000um -23.4000um -27.0000um -18.2000um
paint metal4
box 6.2000um -34.6000um 6.6000um -23.0000um
paint metal4
box 8.6000um -25.8000um 9.0000um -11.8000um
paint metal4
box 19.8000um -93.8000um 20.2000um -91.8000um
paint metal4
box 19.8000um -73.8000um 20.2000um -72.6000um
paint metal4
box 24.6000um -76.2000um 25.0000um -73.4000um
paint metal4
box 26.2000um -93.8000um 26.6000um -91.8000um
paint metal4
box 31.8000um -76.2000um 32.2000um -34.2000um
paint metal4
box 35.8000um -34.6000um 36.2000um -32.6000um
paint metal4
box 50.2000um -34.6000um 50.6000um -33.4000um
paint metal4
box 55.0000um -34.6000um 55.4000um -32.6000um
paint metal4
box 63.0000um -92.2000um 63.4000um -76.6000um
paint metal4
box 55.0000um -34.6000um 55.4000um -34.2000um
paint via3
box 31.8000um -34.6000um 32.2000um -34.2000um
paint via3
box 8.6000um -12.2000um 9.0000um -11.8000um
paint via3
box 26.2000um -93.8000um 26.6000um -93.4000um
paint via3
box 6.2000um -34.6000um 6.6000um -34.2000um
paint via3
box 6.2000um -25.8000um 6.6000um -25.4000um
paint via3
box 19.8000um -93.8000um 20.2000um -93.4000um
paint via3
box 8.6000um -25.8000um 9.0000um -25.4000um
paint via3
box 35.8000um -34.6000um 36.2000um -34.2000um
paint via3
box 19.8000um -73.8000um 20.2000um -73.4000um
paint via3
box 24.6000um -73.8000um 25.0000um -73.4000um
paint via3
box -34.6000um -12.2000um -34.2000um -11.8000um
paint via3
box 50.2000um -34.6000um 50.6000um -34.2000um
paint via3
box 19.8000um -92.3100um 20.2000um -91.4300um
paint metal4
box 19.8000um -91.9400um 20.2000um -91.5400um
paint via3
box 26.2000um -92.3100um 26.6000um -91.4300um
paint metal4
box 26.2000um -91.9400um 26.6000um -91.5400um
paint via3
box 63.0000um -92.3100um 63.4000um -91.4300um
paint metal4
box 63.0000um -91.9400um 63.4000um -91.5400um
paint via3
box 63.0000um -77.1100um 63.4000um -76.1100um
paint metal4
box 63.0000um -76.6200um 63.4000um -76.2200um
paint via3
box 24.6000um -76.7300um 25.0000um -75.6900um
paint metal4
box 24.6000um -76.6200um 25.0000um -76.2200um
paint via3
box 19.8000um -73.1100um 20.2000um -71.8500um
paint metal4
box 19.8000um -72.3600um 20.2000um -71.9600um
paint via3
box 31.8000um -76.7300um 32.2000um -75.6900um
paint metal4
box 31.8000um -76.6200um 32.2000um -76.2200um
paint via3
box 35.8000um -33.9100um 36.2000um -33.1900um
paint metal4
box 35.8000um -33.7000um 36.2000um -33.3000um
paint via3
box 35.8000um -33.1100um 36.2000um -32.3900um
paint metal4
box 35.8000um -32.9000um 36.2000um -32.5000um
paint via3
box 50.2000um -33.9100um 50.6000um -33.1900um
paint metal4
box 50.2000um -33.7000um 50.6000um -33.3000um
paint via3
box 55.0000um -33.9100um 55.4000um -33.1900um
paint metal4
box 55.0000um -33.7000um 55.4000um -33.3000um
paint via3
box 55.0000um -33.1100um 55.4000um -32.3900um
paint metal4
box 55.0000um -32.9000um 55.4000um -32.5000um
paint via3
box 6.2000um -23.5900um 6.6000um -22.8900um
paint metal4
box 6.2000um -23.4800um 6.6000um -23.0800um
paint via3
box -27.4000um -23.5900um -27.0000um -22.8900um
paint metal4
box -27.4000um -23.4800um -27.0000um -23.0800um
paint via3
box -27.4000um -19.0400um -27.0000um -18.0900um
paint metal4
box -27.4000um -18.9300um -27.0000um -18.5300um
paint via3
box -34.6000um -21.2900um -34.2000um -19.6900um
paint metal4
box -34.6000um -21.1800um -34.2000um -20.7800um
paint via3
box -51.4000um -21.2900um -51.0000um -20.4900um
paint metal4
box -51.4000um -21.1800um -51.0000um -20.7800um
paint via3
box -51.4000um -23.5900um -51.0000um -22.8900um
paint metal4
box -51.4000um -23.4800um -51.0000um -23.0800um
paint via3
box 19.7500um -91.9900um 20.2500um -91.4900um
paint locali
box 19.8300um -91.9100um 20.1700um -91.5700um
paint mcon
box 19.8300um -91.9100um 20.1700um -91.5700um
paint m2c
box 19.8000um -91.9400um 20.2000um -91.5400um
paint m3c
box 19.7500um -91.9900um 20.2500um -91.4900um
paint metal3
box 26.1500um -91.9900um 26.6500um -91.4900um
paint locali
box 26.2300um -91.9100um 26.5700um -91.5700um
paint mcon
box 26.2300um -91.9100um 26.5700um -91.5700um
paint m2c
box 26.2000um -91.9400um 26.6000um -91.5400um
paint m3c
box 26.1500um -91.9900um 26.6500um -91.4900um
paint metal3
box 62.9500um -91.9900um 63.4500um -91.4900um
paint locali
box 63.0300um -91.9100um 63.3700um -91.5700um
paint mcon
box 63.0300um -91.9100um 63.3700um -91.5700um
paint m2c
box 63.0000um -91.9400um 63.4000um -91.5400um
paint m3c
box 62.9500um -91.9900um 63.4500um -91.4900um
paint metal3
box 35.7500um -33.7500um 36.2500um -33.2500um
paint locali
box 35.8300um -33.6700um 36.1700um -33.3300um
paint mcon
box 35.8300um -33.6700um 36.1700um -33.3300um
paint m2c
box 35.8000um -33.7000um 36.2000um -33.3000um
paint m3c
box 35.7500um -33.7500um 36.2500um -33.2500um
paint metal3
box 50.1500um -33.7500um 50.6500um -33.2500um
paint locali
box 50.2300um -33.6700um 50.5700um -33.3300um
paint mcon
box 50.2300um -33.6700um 50.5700um -33.3300um
paint m2c
box 50.2000um -33.7000um 50.6000um -33.3000um
paint m3c
box 50.1500um -33.7500um 50.6500um -33.2500um
paint metal3
box 54.9500um -33.7500um 55.4500um -33.2500um
paint locali
box 55.0300um -33.6700um 55.3700um -33.3300um
paint mcon
box 55.0300um -33.6700um 55.3700um -33.3300um
paint m2c
box 55.0000um -33.7000um 55.4000um -33.3000um
paint m3c
box 54.9500um -33.7500um 55.4500um -33.2500um
paint metal3
box 6.1500um -23.5300um 6.6500um -23.0300um
paint locali
box 6.2300um -23.4500um 6.5700um -23.1100um
paint mcon
box 6.2300um -23.4500um 6.5700um -23.1100um
paint m2c
box 6.2000um -23.4800um 6.6000um -23.0800um
paint m3c
box 6.1500um -23.5300um 6.6500um -23.0300um
paint metal3
box -27.4500um -23.5300um -26.9500um -23.0300um
paint locali
box -27.3700um -23.4500um -27.0300um -23.1100um
paint mcon
box -27.3700um -23.4500um -27.0300um -23.1100um
paint m2c
box -27.4000um -23.4800um -27.0000um -23.0800um
paint m3c
box -27.4500um -23.5300um -26.9500um -23.0300um
paint metal3
box -51.4500um -23.5300um -50.9500um -23.0300um
paint locali
box -51.3700um -23.4500um -51.0300um -23.1100um
paint mcon
box -51.3700um -23.4500um -51.0300um -23.1100um
paint m2c
box -51.4000um -23.4800um -51.0000um -23.0800um
paint m3c
box -51.4500um -23.5300um -50.9500um -23.0300um
paint metal3
box 19.9500um -92.0500um 20.0500um -91.9500um
label VDD c metal4
box 12.6000um -105.8000um 17.0000um -105.4000um
paint metal3
box 7.8000um -103.4000um 13.0000um -103.0000um
paint metal3
box 33.4000um -93.8000um 37.0000um -93.4000um
paint metal3
box -26.6000um -67.4000um -21.4000um -67.0000um
paint metal3
box -71.4000um -62.6000um -67.0000um -62.2000um
paint metal3
box -22.6000um -58.6000um -21.4000um -58.2000um
paint metal3
box -71.4000um -49.0000um -69.4000um -48.6000um
paint metal3
box 31.0000um -41.8000um 33.8000um -41.4000um
paint metal3
box -6.6000um -39.4000um -4.6000um -39.0000um
paint metal3
box 26.2000um -38.6000um 31.4000um -38.2000um
paint metal3
box -63.4000um -25.0000um -61.4000um -24.6000um
paint metal3
box -71.4000um -62.6000um -71.0000um -48.6000um
paint metal4
box -69.8000um -50.6000um -69.4000um -48.6000um
paint metal4
box -67.4000um -65.8000um -67.0000um -62.2000um
paint metal4
box -64.2000um -107.4000um -63.8000um -105.4000um
paint metal4
box -63.4000um -50.6000um -63.0000um -24.6000um
paint metal4
box -61.8000um -26.6000um -61.4000um -24.6000um
paint metal4
box -33.8000um -50.6000um -33.4000um -45.4000um
paint metal4
box -26.6000um -67.4000um -26.2000um -65.4000um
paint metal4
box -22.6000um -67.4000um -22.2000um -58.2000um
paint metal4
box -21.8000um -67.4000um -21.4000um -65.4000um
paint metal4
box -21.8000um -60.2000um -21.4000um -58.2000um
paint metal4
box -6.6000um -50.6000um -6.2000um -39.0000um
paint metal4
box -5.0000um -40.2000um -4.6000um -39.0000um
paint metal4
box 7.8000um -105.8000um 8.2000um -103.0000um
paint metal4
box 11.8000um -60.2000um 12.2000um -55.0000um
paint metal4
box 12.6000um -105.8000um 13.0000um -103.0000um
paint metal4
box 16.6000um -109.8000um 17.0000um -105.4000um
paint metal4
box 19.0000um -94.6000um 19.4000um -65.4000um
paint metal4
box 26.2000um -40.2000um 26.6000um -38.2000um
paint metal4
box 31.0000um -41.8000um 31.4000um -38.2000um
paint metal4
box 33.4000um -94.6000um 33.8000um -93.4000um
paint metal4
box 33.4000um -41.8000um 33.8000um -39.8000um
paint metal4
box 36.6000um -155.4000um 37.0000um -93.4000um
paint metal4
box -5.0000um -39.4000um -4.6000um -39.0000um
paint via3
box -69.8000um -49.0000um -69.4000um -48.6000um
paint via3
box 31.0000um -41.8000um 31.4000um -41.4000um
paint via3
box 7.8000um -103.4000um 8.2000um -103.0000um
paint via3
box 26.2000um -38.6000um 26.6000um -38.2000um
paint via3
box -61.8000um -25.0000um -61.4000um -24.6000um
paint via3
box 12.6000um -103.4000um 13.0000um -103.0000um
paint via3
box 33.4000um -93.8000um 33.8000um -93.4000um
paint via3
box -71.4000um -49.0000um -71.0000um -48.6000um
paint via3
box -22.6000um -58.6000um -22.2000um -58.2000um
paint via3
box -63.4000um -25.0000um -63.0000um -24.6000um
paint via3
box 31.0000um -38.6000um 31.4000um -38.2000um
paint via3
box 33.4000um -41.8000um 33.8000um -41.4000um
paint via3
box -22.6000um -67.4000um -22.2000um -67.0000um
paint via3
box -6.6000um -39.4000um -6.2000um -39.0000um
paint via3
box -26.6000um -67.4000um -26.2000um -67.0000um
paint via3
box -21.8000um -58.6000um -21.4000um -58.2000um
paint via3
box 16.6000um -105.8000um 17.0000um -105.4000um
paint via3
box -67.4000um -62.6000um -67.0000um -62.2000um
paint via3
box 36.6000um -93.8000um 37.0000um -93.4000um
paint via3
box -21.8000um -67.4000um -21.4000um -67.0000um
paint via3
box 12.6000um -105.8000um 13.0000um -105.4000um
paint via3
box -71.4000um -62.6000um -71.0000um -62.2000um
paint via3
box 36.6000um -155.5100um 37.0000um -154.5500um
paint metal4
box 36.6000um -155.0600um 37.0000um -154.6600um
paint via3
box 36.6000um -109.9100um 37.0000um -109.2300um
paint metal4
box 36.6000um -109.7400um 37.0000um -109.3400um
paint via3
box 33.4000um -95.1100um 33.8000um -94.0900um
paint metal4
box 33.4000um -95.0000um 33.8000um -94.6000um
paint via3
box 16.6000um -109.9100um 17.0000um -109.2300um
paint metal4
box 16.6000um -109.7400um 17.0000um -109.3400um
paint via3
box 7.8000um -106.1000um 8.2000um -105.2900um
paint metal4
box 7.8000um -105.9900um 8.2000um -105.5900um
paint via3
box -64.2000um -106.1000um -63.8000um -105.2900um
paint metal4
box -64.2000um -105.9900um -63.8000um -105.5900um
paint via3
box -64.2000um -107.6500um -63.8000um -106.8900um
paint metal4
box -64.2000um -107.5400um -63.8000um -107.1400um
paint via3
box 19.0000um -95.1100um 19.4000um -94.0900um
paint metal4
box 19.0000um -95.0000um 19.4000um -94.6000um
paint via3
box 19.0000um -66.1600um 19.4000um -65.2900um
paint metal4
box 19.0000um -66.0500um 19.4000um -65.6500um
paint via3
box -21.8000um -66.1600um -21.4000um -65.2900um
paint metal4
box -21.8000um -66.0500um -21.4000um -65.6500um
paint via3
box -26.6000um -66.1600um -26.2000um -65.2900um
paint metal4
box -26.6000um -66.0500um -26.2000um -65.6500um
paint via3
box -67.4000um -66.1600um -67.0000um -65.2900um
paint metal4
box -67.4000um -66.0500um -67.0000um -65.6500um
paint via3
box -67.4000um -65.3600um -67.0000um -64.4900um
paint metal4
box -67.4000um -65.2500um -67.0000um -64.8500um
paint via3
box -21.8000um -60.4400um -21.4000um -59.6900um
paint metal4
box -21.8000um -60.3300um -21.4000um -59.9300um
paint via3
box 11.8000um -60.4400um 12.2000um -59.6900um
paint metal4
box 11.8000um -60.3300um 12.2000um -59.9300um
paint via3
box 11.8000um -55.7200um 12.2000um -54.8900um
paint metal4
box 11.8000um -55.6100um 12.2000um -55.2100um
paint via3
box -69.8000um -50.7100um -69.4000um -49.7300um
paint metal4
box -69.8000um -50.2400um -69.4000um -49.8400um
paint via3
box -33.8000um -50.7100um -33.4000um -49.7300um
paint metal4
box -33.8000um -50.2400um -33.4000um -49.8400um
paint via3
box -33.8000um -46.7800um -33.4000um -46.0900um
paint metal4
box -33.8000um -46.6700um -33.4000um -46.2700um
paint via3
box -33.8000um -45.9800um -33.4000um -45.2900um
paint metal4
box -33.8000um -45.8700um -33.4000um -45.4700um
paint via3
box -6.6000um -50.7100um -6.2000um -49.7300um
paint metal4
box -6.6000um -50.2400um -6.2000um -49.8400um
paint via3
box -5.0000um -40.6600um -4.6000um -39.6900um
paint metal4
box -5.0000um -40.5500um -4.6000um -40.1500um
paint via3
box 26.2000um -40.6600um 26.6000um -39.6900um
paint metal4
box 26.2000um -40.5500um 26.6000um -40.1500um
paint via3
box 33.4000um -41.1600um 33.8000um -40.4900um
paint metal4
box 33.4000um -41.0500um 33.8000um -40.6500um
paint via3
box 33.4000um -40.3600um 33.8000um -39.6900um
paint metal4
box 33.4000um -40.2500um 33.8000um -39.8500um
paint via3
box -63.4000um -50.7100um -63.0000um -49.7300um
paint metal4
box -63.4000um -50.2400um -63.0000um -49.8400um
paint via3
box -61.8000um -26.7100um -61.4000um -26.0300um
paint metal4
box -61.8000um -26.5400um -61.4000um -26.1400um
paint via3
box 36.5500um -109.7900um 37.0500um -109.2900um
paint locali
box 36.6300um -109.7100um 36.9700um -109.3700um
paint mcon
box 36.6300um -109.7100um 36.9700um -109.3700um
paint m2c
box 36.6000um -109.7400um 37.0000um -109.3400um
paint m3c
box 36.5500um -109.7900um 37.0500um -109.2900um
paint metal3
box 33.3500um -95.0500um 33.8500um -94.5500um
paint locali
box 33.4300um -94.9700um 33.7700um -94.6300um
paint mcon
box 33.4300um -94.9700um 33.7700um -94.6300um
paint m2c
box 33.4000um -95.0000um 33.8000um -94.6000um
paint m3c
box 33.3500um -95.0500um 33.8500um -94.5500um
paint metal3
box 16.5500um -109.7900um 17.0500um -109.2900um
paint locali
box 16.6300um -109.7100um 16.9700um -109.3700um
paint mcon
box 16.6300um -109.7100um 16.9700um -109.3700um
paint m2c
box 16.6000um -109.7400um 17.0000um -109.3400um
paint m3c
box 16.5500um -109.7900um 17.0500um -109.2900um
paint metal3
box 7.7500um -106.0400um 8.2500um -105.5400um
paint locali
box 7.8300um -105.9600um 8.1700um -105.6200um
paint mcon
box 7.8300um -105.9600um 8.1700um -105.6200um
paint m2c
box 7.8000um -105.9900um 8.2000um -105.5900um
paint m3c
box 7.7500um -106.0400um 8.2500um -105.5400um
paint metal3
box -64.2500um -106.0400um -63.7500um -105.5400um
paint locali
box -64.1700um -105.9600um -63.8300um -105.6200um
paint mcon
box -64.1700um -105.9600um -63.8300um -105.6200um
paint m2c
box -64.2000um -105.9900um -63.8000um -105.5900um
paint m3c
box -64.2500um -106.0400um -63.7500um -105.5400um
paint metal3
box 18.9500um -95.0500um 19.4500um -94.5500um
paint locali
box 19.0300um -94.9700um 19.3700um -94.6300um
paint mcon
box 19.0300um -94.9700um 19.3700um -94.6300um
paint m2c
box 19.0000um -95.0000um 19.4000um -94.6000um
paint m3c
box 18.9500um -95.0500um 19.4500um -94.5500um
paint metal3
box 18.9500um -66.1000um 19.4500um -65.6000um
paint locali
box 19.0300um -66.0200um 19.3700um -65.6800um
paint mcon
box 19.0300um -66.0200um 19.3700um -65.6800um
paint m2c
box 19.0000um -66.0500um 19.4000um -65.6500um
paint m3c
box 18.9500um -66.1000um 19.4500um -65.6000um
paint metal3
box -21.8500um -66.1000um -21.3500um -65.6000um
paint locali
box -21.7700um -66.0200um -21.4300um -65.6800um
paint mcon
box -21.7700um -66.0200um -21.4300um -65.6800um
paint m2c
box -21.8000um -66.0500um -21.4000um -65.6500um
paint m3c
box -21.8500um -66.1000um -21.3500um -65.6000um
paint metal3
box -26.6500um -66.1000um -26.1500um -65.6000um
paint locali
box -26.5700um -66.0200um -26.2300um -65.6800um
paint mcon
box -26.5700um -66.0200um -26.2300um -65.6800um
paint m2c
box -26.6000um -66.0500um -26.2000um -65.6500um
paint m3c
box -26.6500um -66.1000um -26.1500um -65.6000um
paint metal3
box -67.4500um -66.1000um -66.9500um -65.6000um
paint locali
box -67.3700um -66.0200um -67.0300um -65.6800um
paint mcon
box -67.3700um -66.0200um -67.0300um -65.6800um
paint m2c
box -67.4000um -66.0500um -67.0000um -65.6500um
paint m3c
box -67.4500um -66.1000um -66.9500um -65.6000um
paint metal3
box 11.7500um -55.6600um 12.2500um -55.1600um
paint locali
box 11.8300um -55.5800um 12.1700um -55.2400um
paint mcon
box 11.8300um -55.5800um 12.1700um -55.2400um
paint m2c
box 11.8000um -55.6100um 12.2000um -55.2100um
paint m3c
box 11.7500um -55.6600um 12.2500um -55.1600um
paint metal3
box -69.8500um -50.2900um -69.3500um -49.7900um
paint locali
box -69.7700um -50.2100um -69.4300um -49.8700um
paint mcon
box -69.7700um -50.2100um -69.4300um -49.8700um
paint m2c
box -69.8000um -50.2400um -69.4000um -49.8400um
paint m3c
box -69.8500um -50.2900um -69.3500um -49.7900um
paint metal3
box -33.8500um -50.2900um -33.3500um -49.7900um
paint locali
box -33.7700um -50.2100um -33.4300um -49.8700um
paint mcon
box -33.7700um -50.2100um -33.4300um -49.8700um
paint m2c
box -33.8000um -50.2400um -33.4000um -49.8400um
paint m3c
box -33.8500um -50.2900um -33.3500um -49.7900um
paint metal3
box -33.8500um -46.7200um -33.3500um -46.2200um
paint locali
box -33.7700um -46.6400um -33.4300um -46.3000um
paint mcon
box -33.7700um -46.6400um -33.4300um -46.3000um
paint m2c
box -33.8000um -46.6700um -33.4000um -46.2700um
paint m3c
box -33.8500um -46.7200um -33.3500um -46.2200um
paint metal3
box -6.6500um -50.2900um -6.1500um -49.7900um
paint locali
box -6.5700um -50.2100um -6.2300um -49.8700um
paint mcon
box -6.5700um -50.2100um -6.2300um -49.8700um
paint m2c
box -6.6000um -50.2400um -6.2000um -49.8400um
paint m3c
box -6.6500um -50.2900um -6.1500um -49.7900um
paint metal3
box -5.0500um -40.6000um -4.5500um -40.1000um
paint locali
box -4.9700um -40.5200um -4.6300um -40.1800um
paint mcon
box -4.9700um -40.5200um -4.6300um -40.1800um
paint m2c
box -5.0000um -40.5500um -4.6000um -40.1500um
paint m3c
box -5.0500um -40.6000um -4.5500um -40.1000um
paint metal3
box 26.1500um -40.6000um 26.6500um -40.1000um
paint locali
box 26.2300um -40.5200um 26.5700um -40.1800um
paint mcon
box 26.2300um -40.5200um 26.5700um -40.1800um
paint m2c
box 26.2000um -40.5500um 26.6000um -40.1500um
paint m3c
box 26.1500um -40.6000um 26.6500um -40.1000um
paint metal3
box 33.3500um -41.1000um 33.8500um -40.6000um
paint locali
box 33.4300um -41.0200um 33.7700um -40.6800um
paint mcon
box 33.4300um -41.0200um 33.7700um -40.6800um
paint m2c
box 33.4000um -41.0500um 33.8000um -40.6500um
paint m3c
box 33.3500um -41.1000um 33.8500um -40.6000um
paint metal3
box -63.4500um -50.2900um -62.9500um -49.7900um
paint locali
box -63.3700um -50.2100um -63.0300um -49.8700um
paint mcon
box -63.3700um -50.2100um -63.0300um -49.8700um
paint m2c
box -63.4000um -50.2400um -63.0000um -49.8400um
paint m3c
box -63.4500um -50.2900um -62.9500um -49.7900um
paint metal3
box -61.8500um -26.5900um -61.3500um -26.0900um
paint locali
box -61.7700um -26.5100um -61.4300um -26.1700um
paint mcon
box -61.7700um -26.5100um -61.4300um -26.1700um
paint m2c
box -61.8000um -26.5400um -61.4000um -26.1400um
paint m3c
box -61.8500um -26.5900um -61.3500um -26.0900um
paint metal3
box 36.7500um -155.2500um 36.8500um -155.1500um
label VSS c metal4
box 11.0000um -157.0000um 64.2000um -156.6000um
paint metal3
box 11.0000um -157.0000um 11.4000um -155.0000um
paint metal4
box 40.6000um -65.8000um 41.0000um -53.4000um
paint metal4
box 63.8000um -157.0000um 64.2000um -66.2000um
paint metal4
box 11.0000um -157.0000um 11.4000um -156.6000um
paint via3
box 63.8000um -157.0000um 64.2000um -156.6000um
paint via3
box 11.0000um -155.5100um 11.4000um -154.5500um
paint metal4
box 11.0000um -155.0600um 11.4000um -154.6600um
paint via3
box 63.8000um -66.7100um 64.2000um -65.5500um
paint metal4
box 63.8000um -66.0600um 64.2000um -65.6600um
paint via3
box 40.6000um -66.1700um 41.0000um -65.2900um
paint metal4
box 40.6000um -66.0600um 41.0000um -65.6600um
paint via3
box 40.6000um -53.9100um 41.0000um -53.0500um
paint metal4
box 40.6000um -53.5600um 41.0000um -53.1600um
paint via3
box 11.1500um -155.2500um 11.2500um -155.1500um
label cmc c metal4
box 16.5500um -102.6500um 17.0500um -102.1500um
paint metal4
box 16.6000um -102.8800um 17.0000um -102.0900um
paint metal4
box 16.6000um -102.7700um 17.0000um -102.3700um
paint via3
box 16.7500um -102.4500um 16.8500um -102.3500um
label in c metal4
box 17.3500um -101.8500um 17.8500um -101.3500um
paint metal4
box 17.4000um -102.1300um 17.8000um -101.2900um
paint metal4
box 17.4000um -102.0200um 17.8000um -101.6200um
paint via3
box 17.5500um -101.6500um 17.6500um -101.5500um
label ip c metal4
tech revert
save iadc_ota_v2_routed
gds write iadc_ota_v2_routed
quit -noprompt
