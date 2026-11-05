drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng.gds
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng/nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng.gds
load x2_diff__cc3 -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 1.080um 0.000um 1.080um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 2.160um 0.000um 2.160um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 3.240um 0.000um 3.240um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 4.320um 0.000um 4.320um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 5.400um 0.000um 5.400um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 0.000um 6.970um 0.000um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 1.080um 6.970um 1.080um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 2.160um 6.970um 2.160um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 3.240um 6.970um 3.240um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 4.320um 6.970um 4.320um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 5.400um 6.970um 5.400um 6.970um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 0.000um 14.690um 0.000um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 1.080um 14.690um 1.080um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 2.160um 14.690um 2.160um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng
box 3.240um 14.690um 3.240um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 4.320um 14.690um 4.320um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
box 5.400um 14.690um 5.400um 14.690um
getcell nfet_01v8_lvt_W1p2_L0p2_m6__nf1_gboth_sdfull_ng h
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
box 3.655um 2.030um 3.855um 4.170um
paint metal2
box 3.555um 3.970um 3.955um 4.370um
paint m3c
box 3.820um 0.460um 4.180um 0.820um
paint metal1
box 3.870um 0.480um 4.130um 0.800um
paint m2c
box 3.900um -2.050um 4.100um 0.640um
paint metal2
box 3.800um -2.250um 4.200um -1.850um
paint m3c
box 3.330um 0.960um 3.690um 1.320um
paint metal1
box 3.380um 0.980um 3.640um 1.300um
paint m2c
box 3.410um -1.300um 3.610um 1.140um
paint metal2
box 3.310um -1.500um 3.710um -1.100um
paint m3c
box 4.655um 1.850um 5.015um 2.210um
paint metal1
box 4.705um 1.870um 4.965um 2.190um
paint m2c
box 4.735um 2.030um 4.935um 3.420um
paint metal2
box 4.635um 3.220um 5.035um 3.620um
paint m3c
box 4.900um 0.460um 5.260um 0.820um
paint metal1
box 4.950um 0.480um 5.210um 0.800um
paint m2c
box 4.980um -0.550um 5.180um 0.640um
paint metal2
box 4.880um -0.750um 5.280um -0.350um
paint m3c
box 4.410um 0.960um 4.770um 1.320um
paint metal1
box 4.460um 0.980um 4.720um 1.300um
paint m2c
box 4.490um -1.300um 4.690um 1.140um
paint metal2
box 4.390um -1.500um 4.790um -1.100um
paint m3c
box 5.735um 1.570um 6.095um 1.930um
paint metal1
box 5.785um 1.590um 6.045um 1.910um
paint m2c
box 5.815um 1.750um 6.015um 2.670um
paint metal2
box 5.715um 2.470um 6.115um 2.870um
paint m3c
box 5.490um 0.180um 5.850um 0.540um
paint metal1
box 5.540um 0.200um 5.800um 0.520um
paint m2c
box 5.570um -0.550um 5.770um 0.360um
paint metal2
box 5.470um -0.750um 5.870um -0.350um
paint m3c
box 5.980um 0.680um 6.340um 1.040um
paint metal1
box 6.030um 0.700um 6.290um 1.020um
paint m2c
box 6.060um -0.550um 6.260um 0.860um
paint metal2
box 5.960um -0.750um 6.360um -0.350um
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
box 1.250um 5.670um 1.450um 7.610um
paint metal2
box 1.150um 5.470um 1.550um 5.870um
paint m3c
box 1.660um 7.930um 2.020um 8.290um
paint metal1
box 1.710um 7.950um 1.970um 8.270um
paint m2c
box 1.740um 4.920um 1.940um 8.110um
paint metal2
box 1.640um 4.720um 2.040um 5.120um
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
box 2.330um 6.420um 2.530um 7.610um
paint metal2
box 2.230um 6.220um 2.630um 6.620um
paint m3c
box 2.740um 7.930um 3.100um 8.290um
paint metal1
box 2.790um 7.950um 3.050um 8.270um
paint m2c
box 2.820um 4.920um 3.020um 8.110um
paint metal2
box 2.720um 4.720um 3.120um 5.120um
paint m3c
box 3.575um 8.820um 3.935um 9.180um
paint metal1
box 3.625um 8.840um 3.885um 9.160um
paint m2c
box 3.655um 9.000um 3.855um 11.140um
paint metal2
box 3.555um 10.940um 3.955um 11.340um
paint m3c
box 3.820um 7.430um 4.180um 7.790um
paint metal1
box 3.870um 7.450um 4.130um 7.770um
paint m2c
box 3.900um 6.420um 4.100um 7.610um
paint metal2
box 3.800um 6.220um 4.200um 6.620um
paint m3c
box 3.330um 7.930um 3.690um 8.290um
paint metal1
box 3.380um 7.950um 3.640um 8.270um
paint m2c
box 3.410um 4.920um 3.610um 8.110um
paint metal2
box 3.310um 4.720um 3.710um 5.120um
paint m3c
box 4.655um 8.820um 5.015um 9.180um
paint metal1
box 4.705um 8.840um 4.965um 9.160um
paint m2c
box 4.735um 9.000um 4.935um 10.390um
paint metal2
box 4.635um 10.190um 5.035um 10.590um
paint m3c
box 4.900um 7.430um 5.260um 7.790um
paint metal1
box 4.950um 7.450um 5.210um 7.770um
paint m2c
box 4.980um 5.670um 5.180um 7.610um
paint metal2
box 4.880um 5.470um 5.280um 5.870um
paint m3c
box 4.410um 7.930um 4.770um 8.290um
paint metal1
box 4.460um 7.950um 4.720um 8.270um
paint m2c
box 4.490um 4.920um 4.690um 8.110um
paint metal2
box 4.390um 4.720um 4.790um 5.120um
paint m3c
box 5.735um 8.540um 6.095um 8.900um
paint metal1
box 5.785um 8.560um 6.045um 8.880um
paint m2c
box 5.815um 8.720um 6.015um 9.640um
paint metal2
box 5.715um 9.440um 6.115um 9.840um
paint m3c
box 5.490um 7.150um 5.850um 7.510um
paint metal1
box 5.540um 7.170um 5.800um 7.490um
paint m2c
box 5.570um 6.420um 5.770um 7.330um
paint metal2
box 5.470um 6.220um 5.870um 6.620um
paint m3c
box 5.980um 7.650um 6.340um 8.010um
paint metal1
box 6.030um 7.670um 6.290um 7.990um
paint m2c
box 6.060um 6.420um 6.260um 7.830um
paint metal2
box 5.960um 6.220um 6.360um 6.620um
paint m3c
box 0.335um 16.540um 0.695um 16.900um
paint metal1
box 0.385um 16.560um 0.645um 16.880um
paint m2c
box 0.415um 16.720um 0.615um 17.360um
paint metal2
box 0.315um 17.160um 0.715um 17.560um
paint m3c
box 0.090um 15.150um 0.450um 15.510um
paint metal1
box 0.140um 15.170um 0.400um 15.490um
paint m2c
box 0.170um 14.140um 0.370um 15.330um
paint metal2
box 0.070um 13.940um 0.470um 14.340um
paint m3c
box 0.580um 15.650um 0.940um 16.010um
paint metal1
box 0.630um 15.670um 0.890um 15.990um
paint m2c
box 0.660um 14.140um 0.860um 15.830um
paint metal2
box 0.560um 13.940um 0.960um 14.340um
paint m3c
box 1.415um 16.540um 1.775um 16.900um
paint metal1
box 1.465um 16.560um 1.725um 16.880um
paint m2c
box 1.495um 16.720um 1.695um 18.110um
paint metal2
box 1.395um 17.910um 1.795um 18.310um
paint m3c
box 1.170um 15.150um 1.530um 15.510um
paint metal1
box 1.220um 15.170um 1.480um 15.490um
paint m2c
box 1.250um 13.390um 1.450um 15.330um
paint metal2
box 1.150um 13.190um 1.550um 13.590um
paint m3c
box 1.660um 15.650um 2.020um 16.010um
paint metal1
box 1.710um 15.670um 1.970um 15.990um
paint m2c
box 1.740um 12.640um 1.940um 15.830um
paint metal2
box 1.640um 12.440um 2.040um 12.840um
paint m3c
box 2.495um 16.540um 2.855um 16.900um
paint metal1
box 2.545um 16.560um 2.805um 16.880um
paint m2c
box 2.575um 16.720um 2.775um 18.860um
paint metal2
box 2.475um 18.660um 2.875um 19.060um
paint m3c
box 2.250um 15.150um 2.610um 15.510um
paint metal1
box 2.300um 15.170um 2.560um 15.490um
paint m2c
box 2.330um 11.890um 2.530um 15.330um
paint metal2
box 2.230um 11.690um 2.630um 12.090um
paint m3c
box 2.740um 15.650um 3.100um 16.010um
paint metal1
box 2.790um 15.670um 3.050um 15.990um
paint m2c
box 2.820um 12.640um 3.020um 15.830um
paint metal2
box 2.720um 12.440um 3.120um 12.840um
paint m3c
box 3.575um 16.540um 3.935um 16.900um
paint metal1
box 3.625um 16.560um 3.885um 16.880um
paint m2c
box 3.655um 16.720um 3.855um 18.860um
paint metal2
box 3.555um 18.660um 3.955um 19.060um
paint m3c
box 3.820um 15.150um 4.180um 15.510um
paint metal1
box 3.870um 15.170um 4.130um 15.490um
paint m2c
box 3.900um 11.890um 4.100um 15.330um
paint metal2
box 3.800um 11.690um 4.200um 12.090um
paint m3c
box 3.330um 15.650um 3.690um 16.010um
paint metal1
box 3.380um 15.670um 3.640um 15.990um
paint m2c
box 3.410um 12.640um 3.610um 15.830um
paint metal2
box 3.310um 12.440um 3.710um 12.840um
paint m3c
box 4.655um 16.540um 5.015um 16.900um
paint metal1
box 4.705um 16.560um 4.965um 16.880um
paint m2c
box 4.735um 16.720um 4.935um 18.110um
paint metal2
box 4.635um 17.910um 5.035um 18.310um
paint m3c
box 4.900um 15.150um 5.260um 15.510um
paint metal1
box 4.950um 15.170um 5.210um 15.490um
paint m2c
box 4.980um 13.390um 5.180um 15.330um
paint metal2
box 4.880um 13.190um 5.280um 13.590um
paint m3c
box 4.410um 15.650um 4.770um 16.010um
paint metal1
box 4.460um 15.670um 4.720um 15.990um
paint m2c
box 4.490um 12.640um 4.690um 15.830um
paint metal2
box 4.390um 12.440um 4.790um 12.840um
paint m3c
box 5.735um 16.540um 6.095um 16.900um
paint metal1
box 5.785um 16.560um 6.045um 16.880um
paint m2c
box 5.815um 16.720um 6.015um 17.360um
paint metal2
box 5.715um 17.160um 6.115um 17.560um
paint m3c
box 5.980um 15.150um 6.340um 15.510um
paint metal1
box 6.030um 15.170um 6.290um 15.490um
paint m2c
box 6.060um 14.140um 6.260um 15.330um
paint metal2
box 5.960um 13.940um 6.360um 14.340um
paint m3c
box 5.490um 15.650um 5.850um 16.010um
paint metal1
box 5.540um 15.670um 5.800um 15.990um
paint m2c
box 5.570um 14.140um 5.770um 15.830um
paint metal2
box 5.470um 13.940um 5.870um 14.340um
paint m3c
box 0.270um -0.750um 0.760um -0.350um
paint metal2
box 5.670um -0.750um 6.160um -0.350um
paint metal2
box 0.270um 6.220um 0.760um 6.620um
paint metal2
box 5.670um 6.220um 6.160um 6.620um
paint metal2
box 0.270um 13.940um 0.760um 14.340um
paint metal2
box 5.670um 13.940um 6.160um 14.340um
paint metal2
box 6.730um -2.050um 6.930um 11.890um
paint metal2
box 6.630um -2.250um 7.030um -1.850um
paint m3c
box 6.630um 6.220um 7.030um 6.620um
paint m3c
box 6.630um 9.440um 7.030um 9.840um
paint m3c
box 6.630um 11.690um 7.030um 12.090um
paint m3c
box 7.330um -1.300um 7.530um 12.640um
paint metal2
box 7.230um -1.500um 7.630um -1.100um
paint m3c
box 7.230um 4.720um 7.630um 5.120um
paint m3c
box 7.230um 12.440um 7.630um 12.840um
paint m3c
box 7.930um -0.550um 8.130um 13.390um
paint metal2
box 7.830um -0.750um 8.230um -0.350um
paint m3c
box 7.830um 2.470um 8.230um 2.870um
paint m3c
box 7.830um 5.470um 8.230um 5.870um
paint m3c
box 7.830um 13.190um 8.230um 13.590um
paint m3c
box 8.530um 3.420um 8.730um 18.110um
paint metal2
box 8.430um 3.220um 8.830um 3.620um
paint m3c
box 8.430um 10.190um 8.830um 10.590um
paint m3c
box 8.430um 17.910um 8.830um 18.310um
paint m3c
box 9.130um 4.170um 9.330um 18.860um
paint metal2
box 9.030um 3.970um 9.430um 4.370um
paint m3c
box 9.030um 10.940um 9.430um 11.340um
paint m3c
box 9.030um 18.660um 9.430um 19.060um
paint m3c
box 9.730um 14.140um 9.930um 17.360um
paint metal2
box 9.630um 13.940um 10.030um 14.340um
paint m3c
box 9.630um 17.160um 10.030um 17.560um
paint m3c
box -0.400um 17.160um 10.230um 17.560um
paint metal3
box -0.300um 17.310um -0.200um 17.410um
label VSS c metal3
box -0.400um 17.910um 10.230um 18.310um
paint metal3
box -0.300um 18.060um -0.200um 18.160um
label ip c metal3
box -0.400um 18.660um 10.230um 19.060um
paint metal3
box -0.300um 18.810um -0.200um 18.910um
label in c metal3
box -0.400um -0.750um 10.230um -0.350um
paint metal3
box -0.300um -0.600um -0.200um -0.500um
label x2_foldp c metal3
box -0.400um -1.500um 10.230um -1.100um
paint metal3
box -0.300um -1.350um -0.200um -1.250um
label x2_tail c metal3
box -0.400um -2.250um 10.230um -1.850um
paint metal3
box -0.300um -2.100um -0.200um -2.000um
label x2_foldn c metal3
box -0.100um 2.470um 8.330um 2.870um
paint metal3
box -0.100um 3.220um 8.930um 3.620um
paint metal3
box -0.100um 3.970um 9.530um 4.370um
paint metal3
box -0.100um 6.220um 7.130um 6.620um
paint metal3
box -0.100um 5.470um 8.330um 5.870um
paint metal3
box -0.100um 4.720um 7.730um 5.120um
paint metal3
box -0.100um 9.440um 7.130um 9.840um
paint metal3
box -0.100um 10.190um 8.930um 10.590um
paint metal3
box -0.100um 10.940um 9.530um 11.340um
paint metal3
box -0.100um 13.940um 10.130um 14.340um
paint metal3
box -0.100um 13.190um 8.330um 13.590um
paint metal3
box -0.100um 12.440um 7.730um 12.840um
paint metal3
box -0.100um 11.690um 7.130um 12.090um
paint metal3
box -0.400um -2.850um 10.230um 19.260um
sky130::guard_ring_draw psc psd
box 4.865um -2.900um 4.965um -2.800um
label VSS_body c locali
tech revert
save x2_diff__cc3
gds write x2_diff__cc3
quit -noprompt
