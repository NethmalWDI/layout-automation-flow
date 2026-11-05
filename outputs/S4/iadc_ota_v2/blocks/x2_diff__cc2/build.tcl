drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng.gds
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng/nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng.gds
load x2_diff__cc2 -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 1.080um 0.000um 1.080um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 2.160um 0.000um 2.160um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 3.240um 0.000um 3.240um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 4.320um 0.000um 4.320um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 5.400um 0.000um 5.400um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 6.480um 0.000um 6.480um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 7.560um 0.000um 7.560um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 0.000um 6.970um 0.000um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 1.080um 6.970um 1.080um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 2.160um 6.970um 2.160um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 3.240um 6.970um 3.240um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 4.320um 6.970um 4.320um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 5.400um 6.970um 5.400um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 6.480um 6.970um 6.480um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 7.560um 6.970um 7.560um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 0.335um 1.570um 0.695um 1.930um
paint metal1
box 0.385um 1.590um 0.645um 1.910um
paint m2c
box 0.415um 1.750um 0.615um 2.670um
paint metal2
box 0.315um 2.470um 0.715um 2.870um
paint m3c
box 0.090um 0.180um 0.450um 0.540um
paint metal1
box 0.140um 0.200um 0.400um 0.520um
paint m2c
box 0.170um -0.550um 0.370um 0.360um
paint metal2
box 0.070um -0.750um 0.470um -0.350um
paint m3c
box 0.580um 0.680um 0.940um 1.040um
paint metal1
box 0.630um 0.700um 0.890um 1.020um
paint m2c
box 0.660um -0.550um 0.860um 0.860um
paint metal2
box 0.560um -0.750um 0.960um -0.350um
paint m3c
box 1.415um 1.850um 1.775um 2.210um
paint metal1
box 1.465um 1.870um 1.725um 2.190um
paint m2c
box 1.495um 2.030um 1.695um 3.420um
paint metal2
box 1.395um 3.220um 1.795um 3.620um
paint m3c
box 1.170um 0.460um 1.530um 0.820um
paint metal1
box 1.220um 0.480um 1.480um 0.800um
paint m2c
box 1.250um -0.550um 1.450um 0.640um
paint metal2
box 1.150um -0.750um 1.550um -0.350um
paint m3c
box 1.660um 0.960um 2.020um 1.320um
paint metal1
box 1.710um 0.980um 1.970um 1.300um
paint m2c
box 1.740um -1.300um 1.940um 1.140um
paint metal2
box 1.640um -1.500um 2.040um -1.100um
paint m3c
box 2.495um 1.850um 2.855um 2.210um
paint metal1
box 2.545um 1.870um 2.805um 2.190um
paint m2c
box 2.575um 2.030um 2.775um 4.170um
paint metal2
box 2.475um 3.970um 2.875um 4.370um
paint m3c
box 2.250um 0.460um 2.610um 0.820um
paint metal1
box 2.300um 0.480um 2.560um 0.800um
paint m2c
box 2.330um -2.050um 2.530um 0.640um
paint metal2
box 2.230um -2.250um 2.630um -1.850um
paint m3c
box 2.740um 0.960um 3.100um 1.320um
paint metal1
box 2.790um 0.980um 3.050um 1.300um
paint m2c
box 2.820um -1.300um 3.020um 1.140um
paint metal2
box 2.720um -1.500um 3.120um -1.100um
paint m3c
box 3.575um 1.850um 3.935um 2.210um
paint metal1
box 3.625um 1.870um 3.885um 2.190um
paint m2c
box 3.655um 2.030um 3.855um 3.420um
paint metal2
box 3.555um 3.220um 3.955um 3.620um
paint m3c
box 3.330um 0.460um 3.690um 0.820um
paint metal1
box 3.380um 0.480um 3.640um 0.800um
paint m2c
box 3.410um -0.550um 3.610um 0.640um
paint metal2
box 3.310um -0.750um 3.710um -0.350um
paint m3c
box 3.820um 0.960um 4.180um 1.320um
paint metal1
box 3.870um 0.980um 4.130um 1.300um
paint m2c
box 3.900um -1.300um 4.100um 1.140um
paint metal2
box 3.800um -1.500um 4.200um -1.100um
paint m3c
box 4.655um 1.850um 5.015um 2.210um
paint metal1
box 4.705um 1.870um 4.965um 2.190um
paint m2c
box 4.735um 2.030um 4.935um 4.170um
paint metal2
box 4.635um 3.970um 5.035um 4.370um
paint m3c
box 4.900um 0.460um 5.260um 0.820um
paint metal1
box 4.950um 0.480um 5.210um 0.800um
paint m2c
box 4.980um -2.050um 5.180um 0.640um
paint metal2
box 4.880um -2.250um 5.280um -1.850um
paint m3c
box 4.410um 0.960um 4.770um 1.320um
paint metal1
box 4.460um 0.980um 4.720um 1.300um
paint m2c
box 4.490um -1.300um 4.690um 1.140um
paint metal2
box 4.390um -1.500um 4.790um -1.100um
paint m3c
box 5.735um 1.850um 6.095um 2.210um
paint metal1
box 5.785um 1.870um 6.045um 2.190um
paint m2c
box 5.815um 2.030um 6.015um 3.420um
paint metal2
box 5.715um 3.220um 6.115um 3.620um
paint m3c
box 5.980um 0.460um 6.340um 0.820um
paint metal1
box 6.030um 0.480um 6.290um 0.800um
paint m2c
box 6.060um -0.550um 6.260um 0.640um
paint metal2
box 5.960um -0.750um 6.360um -0.350um
paint m3c
box 5.490um 0.960um 5.850um 1.320um
paint metal1
box 5.540um 0.980um 5.800um 1.300um
paint m2c
box 5.570um -1.300um 5.770um 1.140um
paint metal2
box 5.470um -1.500um 5.870um -1.100um
paint m3c
box 6.815um 1.850um 7.175um 2.210um
paint metal1
box 6.865um 1.870um 7.125um 2.190um
paint m2c
box 6.895um 2.030um 7.095um 4.170um
paint metal2
box 6.795um 3.970um 7.195um 4.370um
paint m3c
box 7.060um 0.460um 7.420um 0.820um
paint metal1
box 7.110um 0.480um 7.370um 0.800um
paint m2c
box 7.140um -2.050um 7.340um 0.640um
paint metal2
box 7.040um -2.250um 7.440um -1.850um
paint m3c
box 6.570um 0.960um 6.930um 1.320um
paint metal1
box 6.620um 0.980um 6.880um 1.300um
paint m2c
box 6.650um -1.300um 6.850um 1.140um
paint metal2
box 6.550um -1.500um 6.950um -1.100um
paint m3c
box 7.895um 1.570um 8.255um 1.930um
paint metal1
box 7.945um 1.590um 8.205um 1.910um
paint m2c
box 7.975um 1.750um 8.175um 2.670um
paint metal2
box 7.875um 2.470um 8.275um 2.870um
paint m3c
box 7.650um 0.180um 8.010um 0.540um
paint metal1
box 7.700um 0.200um 7.960um 0.520um
paint m2c
box 7.730um -0.550um 7.930um 0.360um
paint metal2
box 7.630um -0.750um 8.030um -0.350um
paint m3c
box 8.140um 0.680um 8.500um 1.040um
paint metal1
box 8.190um 0.700um 8.450um 1.020um
paint m2c
box 8.220um -0.550um 8.420um 0.860um
paint metal2
box 8.120um -0.750um 8.520um -0.350um
paint m3c
box 0.335um 8.540um 0.695um 8.900um
paint metal1
box 0.385um 8.560um 0.645um 8.880um
paint m2c
box 0.415um 8.720um 0.615um 9.640um
paint metal2
box 0.315um 9.440um 0.715um 9.840um
paint m3c
box 0.090um 7.150um 0.450um 7.510um
paint metal1
box 0.140um 7.170um 0.400um 7.490um
paint m2c
box 0.170um 6.420um 0.370um 7.330um
paint metal2
box 0.070um 6.220um 0.470um 6.620um
paint m3c
box 0.580um 7.650um 0.940um 8.010um
paint metal1
box 0.630um 7.670um 0.890um 7.990um
paint m2c
box 0.660um 6.420um 0.860um 7.830um
paint metal2
box 0.560um 6.220um 0.960um 6.620um
paint m3c
box 1.415um 8.820um 1.775um 9.180um
paint metal1
box 1.465um 8.840um 1.725um 9.160um
paint m2c
box 1.495um 9.000um 1.695um 10.390um
paint metal2
box 1.395um 10.190um 1.795um 10.590um
paint m3c
box 1.170um 7.430um 1.530um 7.790um
paint metal1
box 1.220um 7.450um 1.480um 7.770um
paint m2c
box 1.250um 6.420um 1.450um 7.610um
paint metal2
box 1.150um 6.220um 1.550um 6.620um
paint m3c
box 1.660um 7.930um 2.020um 8.290um
paint metal1
box 1.710um 7.950um 1.970um 8.270um
paint m2c
box 1.740um 5.670um 1.940um 8.110um
paint metal2
box 1.640um 5.470um 2.040um 5.870um
paint m3c
box 2.495um 8.820um 2.855um 9.180um
paint metal1
box 2.545um 8.840um 2.805um 9.160um
paint m2c
box 2.575um 9.000um 2.775um 11.140um
paint metal2
box 2.475um 10.940um 2.875um 11.340um
paint m3c
box 2.250um 7.430um 2.610um 7.790um
paint metal1
box 2.300um 7.450um 2.560um 7.770um
paint m2c
box 2.330um 4.920um 2.530um 7.610um
paint metal2
box 2.230um 4.720um 2.630um 5.120um
paint m3c
box 2.740um 7.930um 3.100um 8.290um
paint metal1
box 2.790um 7.950um 3.050um 8.270um
paint m2c
box 2.820um 5.670um 3.020um 8.110um
paint metal2
box 2.720um 5.470um 3.120um 5.870um
paint m3c
box 3.575um 8.820um 3.935um 9.180um
paint metal1
box 3.625um 8.840um 3.885um 9.160um
paint m2c
box 3.655um 9.000um 3.855um 10.390um
paint metal2
box 3.555um 10.190um 3.955um 10.590um
paint m3c
box 3.330um 7.430um 3.690um 7.790um
paint metal1
box 3.380um 7.450um 3.640um 7.770um
paint m2c
box 3.410um 6.420um 3.610um 7.610um
paint metal2
box 3.310um 6.220um 3.710um 6.620um
paint m3c
box 3.820um 7.930um 4.180um 8.290um
paint metal1
box 3.870um 7.950um 4.130um 8.270um
paint m2c
box 3.900um 5.670um 4.100um 8.110um
paint metal2
box 3.800um 5.470um 4.200um 5.870um
paint m3c
box 4.655um 8.820um 5.015um 9.180um
paint metal1
box 4.705um 8.840um 4.965um 9.160um
paint m2c
box 4.735um 9.000um 4.935um 11.140um
paint metal2
box 4.635um 10.940um 5.035um 11.340um
paint m3c
box 4.900um 7.430um 5.260um 7.790um
paint metal1
box 4.950um 7.450um 5.210um 7.770um
paint m2c
box 4.980um 4.920um 5.180um 7.610um
paint metal2
box 4.880um 4.720um 5.280um 5.120um
paint m3c
box 4.410um 7.930um 4.770um 8.290um
paint metal1
box 4.460um 7.950um 4.720um 8.270um
paint m2c
box 4.490um 5.670um 4.690um 8.110um
paint metal2
box 4.390um 5.470um 4.790um 5.870um
paint m3c
box 5.735um 8.820um 6.095um 9.180um
paint metal1
box 5.785um 8.840um 6.045um 9.160um
paint m2c
box 5.815um 9.000um 6.015um 10.390um
paint metal2
box 5.715um 10.190um 6.115um 10.590um
paint m3c
box 5.980um 7.430um 6.340um 7.790um
paint metal1
box 6.030um 7.450um 6.290um 7.770um
paint m2c
box 6.060um 6.420um 6.260um 7.610um
paint metal2
box 5.960um 6.220um 6.360um 6.620um
paint m3c
box 5.490um 7.930um 5.850um 8.290um
paint metal1
box 5.540um 7.950um 5.800um 8.270um
paint m2c
box 5.570um 5.670um 5.770um 8.110um
paint metal2
box 5.470um 5.470um 5.870um 5.870um
paint m3c
box 6.815um 8.820um 7.175um 9.180um
paint metal1
box 6.865um 8.840um 7.125um 9.160um
paint m2c
box 6.895um 9.000um 7.095um 11.140um
paint metal2
box 6.795um 10.940um 7.195um 11.340um
paint m3c
box 7.060um 7.430um 7.420um 7.790um
paint metal1
box 7.110um 7.450um 7.370um 7.770um
paint m2c
box 7.140um 4.920um 7.340um 7.610um
paint metal2
box 7.040um 4.720um 7.440um 5.120um
paint m3c
box 6.570um 7.930um 6.930um 8.290um
paint metal1
box 6.620um 7.950um 6.880um 8.270um
paint m2c
box 6.650um 5.670um 6.850um 8.110um
paint metal2
box 6.550um 5.470um 6.950um 5.870um
paint m3c
box 7.895um 8.540um 8.255um 8.900um
paint metal1
box 7.945um 8.560um 8.205um 8.880um
paint m2c
box 7.975um 8.720um 8.175um 9.640um
paint metal2
box 7.875um 9.440um 8.275um 9.840um
paint m3c
box 7.650um 7.150um 8.010um 7.510um
paint metal1
box 7.700um 7.170um 7.960um 7.490um
paint m2c
box 7.730um 6.420um 7.930um 7.330um
paint metal2
box 7.630um 6.220um 8.030um 6.620um
paint m3c
box 8.140um 7.650um 8.500um 8.010um
paint metal1
box 8.190um 7.670um 8.450um 7.990um
paint m2c
box 8.220um 6.420um 8.420um 7.830um
paint metal2
box 8.120um 6.220um 8.520um 6.620um
paint m3c
box 0.270um -0.750um 0.760um -0.350um
paint metal2
box 7.830um -0.750um 8.320um -0.350um
paint metal2
box 0.270um 6.220um 0.760um 6.620um
paint metal2
box 7.830um 6.220um 8.320um 6.620um
paint metal2
box 8.890um -2.050um 9.090um 9.640um
paint metal2
box 8.790um -2.250um 9.190um -1.850um
paint m3c
box 8.790um 6.220um 9.190um 6.620um
paint m3c
box 8.790um 9.440um 9.190um 9.840um
paint m3c
box 9.490um -1.300um 9.690um 5.670um
paint metal2
box 9.390um -1.500um 9.790um -1.100um
paint m3c
box 9.390um 5.470um 9.790um 5.870um
paint m3c
box 10.090um -0.550um 10.290um 4.920um
paint metal2
box 9.990um -0.750um 10.390um -0.350um
paint m3c
box 9.990um 2.470um 10.390um 2.870um
paint m3c
box 9.990um 4.720um 10.390um 5.120um
paint m3c
box 10.690um 3.420um 10.890um 11.140um
paint metal2
box 10.590um 3.220um 10.990um 3.620um
paint m3c
box 10.590um 10.940um 10.990um 11.340um
paint m3c
box 11.290um 4.170um 11.490um 10.390um
paint metal2
box 11.190um 3.970um 11.590um 4.370um
paint m3c
box 11.190um 10.190um 11.590um 10.590um
paint m3c
box -0.400um 9.440um 11.790um 9.840um
paint metal3
box -0.300um 9.590um -0.200um 9.690um
label x2_foldn c metal3
box -0.400um 10.190um 11.790um 10.590um
paint metal3
box -0.300um 10.340um -0.200um 10.440um
label in c metal3
box -0.400um 10.940um 11.790um 11.340um
paint metal3
box -0.300um 11.090um -0.200um 11.190um
label ip c metal3
box -0.400um -0.750um 11.790um -0.350um
paint metal3
box -0.300um -0.600um -0.200um -0.500um
label x2_foldp c metal3
box -0.400um -1.500um 11.790um -1.100um
paint metal3
box -0.300um -1.350um -0.200um -1.250um
label x2_tail c metal3
box -0.400um -2.250um 11.790um -1.850um
paint metal3
box -0.300um -2.100um -0.200um -2.000um
label x2_foldn c metal3
box -0.100um 2.470um 10.490um 2.870um
paint metal3
box -0.100um 3.220um 11.090um 3.620um
paint metal3
box -0.100um 3.970um 11.690um 4.370um
paint metal3
box -0.100um 6.220um 9.290um 6.620um
paint metal3
box -0.100um 5.470um 9.890um 5.870um
paint metal3
box -0.100um 4.720um 10.490um 5.120um
paint metal3
box -0.400um -2.850um 11.790um 11.540um
sky130::guard_ring_draw psc psd
box 5.645um -2.900um 5.745um -2.800um
label VSS_body c locali
tech revert
save x2_diff__cc2
gds write x2_diff__cc2
quit -noprompt
