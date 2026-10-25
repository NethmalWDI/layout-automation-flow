drc off
snap internal
load w_locali_single_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.17um
paint locali
label A c locali
port makeall
save w_locali_single_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_single_50.spice
load w_locali_pair_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.17um
paint locali
label A c locali
box 0um 0.34um 50um 0.51um
paint locali
label B c locali
port makeall
save w_locali_pair_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_pair_50.spice
load w_locali_plane_50 -silent
box 0 0 0 0
box -2um -2um 52um 2.17um
paint poly
label P c poly
box 0um 0um 50um 0.17um
paint locali
label A c locali
port makeall
save w_locali_plane_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_plane_50.spice
load w_locali_single_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.17um
paint locali
label A c locali
port makeall
save w_locali_single_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_single_100.spice
load w_locali_pair_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.17um
paint locali
label A c locali
box 0um 0.34um 100um 0.51um
paint locali
label B c locali
port makeall
save w_locali_pair_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_pair_100.spice
load w_locali_plane_100 -silent
box 0 0 0 0
box -2um -2um 102um 2.17um
paint poly
label P c poly
box 0um 0um 100um 0.17um
paint locali
label A c locali
port makeall
save w_locali_plane_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_locali_plane_100.spice
load w_metal1_single_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.14um
paint metal1
label A c metal1
port makeall
save w_metal1_single_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_single_50.spice
load w_metal1_pair_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.14um
paint metal1
label A c metal1
box 0um 0.28um 50um 0.42000000000000004um
paint metal1
label B c metal1
port makeall
save w_metal1_pair_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_pair_50.spice
load w_metal1_plane_50 -silent
box 0 0 0 0
box -2um -2um 52um 2.14um
paint locali
label P c locali
box 0um 0um 50um 0.14um
paint metal1
label A c metal1
port makeall
save w_metal1_plane_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_plane_50.spice
load w_metal1_single_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.14um
paint metal1
label A c metal1
port makeall
save w_metal1_single_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_single_100.spice
load w_metal1_pair_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.14um
paint metal1
label A c metal1
box 0um 0.28um 100um 0.42000000000000004um
paint metal1
label B c metal1
port makeall
save w_metal1_pair_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_pair_100.spice
load w_metal1_plane_100 -silent
box 0 0 0 0
box -2um -2um 102um 2.14um
paint locali
label P c locali
box 0um 0um 100um 0.14um
paint metal1
label A c metal1
port makeall
save w_metal1_plane_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal1_plane_100.spice
load w_metal2_single_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.14um
paint metal2
label A c metal2
port makeall
save w_metal2_single_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_single_50.spice
load w_metal2_pair_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.14um
paint metal2
label A c metal2
box 0um 0.28um 50um 0.42000000000000004um
paint metal2
label B c metal2
port makeall
save w_metal2_pair_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_pair_50.spice
load w_metal2_plane_50 -silent
box 0 0 0 0
box -2um -2um 52um 2.14um
paint metal1
label P c metal1
box 0um 0um 50um 0.14um
paint metal2
label A c metal2
port makeall
save w_metal2_plane_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_plane_50.spice
load w_metal2_single_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.14um
paint metal2
label A c metal2
port makeall
save w_metal2_single_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_single_100.spice
load w_metal2_pair_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.14um
paint metal2
label A c metal2
box 0um 0.28um 100um 0.42000000000000004um
paint metal2
label B c metal2
port makeall
save w_metal2_pair_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_pair_100.spice
load w_metal2_plane_100 -silent
box 0 0 0 0
box -2um -2um 102um 2.14um
paint metal1
label P c metal1
box 0um 0um 100um 0.14um
paint metal2
label A c metal2
port makeall
save w_metal2_plane_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal2_plane_100.spice
load w_metal3_single_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.3um
paint metal3
label A c metal3
port makeall
save w_metal3_single_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_single_50.spice
load w_metal3_pair_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.3um
paint metal3
label A c metal3
box 0um 0.6um 50um 0.8999999999999999um
paint metal3
label B c metal3
port makeall
save w_metal3_pair_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_pair_50.spice
load w_metal3_plane_50 -silent
box 0 0 0 0
box -2um -2um 52um 2.3um
paint metal2
label P c metal2
box 0um 0um 50um 0.3um
paint metal3
label A c metal3
port makeall
save w_metal3_plane_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_plane_50.spice
load w_metal3_single_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.3um
paint metal3
label A c metal3
port makeall
save w_metal3_single_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_single_100.spice
load w_metal3_pair_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.3um
paint metal3
label A c metal3
box 0um 0.6um 100um 0.8999999999999999um
paint metal3
label B c metal3
port makeall
save w_metal3_pair_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_pair_100.spice
load w_metal3_plane_100 -silent
box 0 0 0 0
box -2um -2um 102um 2.3um
paint metal2
label P c metal2
box 0um 0um 100um 0.3um
paint metal3
label A c metal3
port makeall
save w_metal3_plane_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal3_plane_100.spice
load w_metal4_single_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.3um
paint metal4
label A c metal4
port makeall
save w_metal4_single_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_single_50.spice
load w_metal4_pair_50 -silent
box 0 0 0 0
box 0um 0um 50um 0.3um
paint metal4
label A c metal4
box 0um 0.6um 50um 0.8999999999999999um
paint metal4
label B c metal4
port makeall
save w_metal4_pair_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_pair_50.spice
load w_metal4_plane_50 -silent
box 0 0 0 0
box -2um -2um 52um 2.3um
paint metal3
label P c metal3
box 0um 0um 50um 0.3um
paint metal4
label A c metal4
port makeall
save w_metal4_plane_50
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_plane_50.spice
load w_metal4_single_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.3um
paint metal4
label A c metal4
port makeall
save w_metal4_single_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_single_100.spice
load w_metal4_pair_100 -silent
box 0 0 0 0
box 0um 0um 100um 0.3um
paint metal4
label A c metal4
box 0um 0.6um 100um 0.8999999999999999um
paint metal4
label B c metal4
port makeall
save w_metal4_pair_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_pair_100.spice
load w_metal4_plane_100 -silent
box 0 0 0 0
box -2um -2um 102um 2.3um
paint metal3
label P c metal3
box 0um 0um 100um 0.3um
paint metal4
label A c metal4
port makeall
save w_metal4_plane_100
extract all
ext2spice cthresh 0
ext2spice format ngspice
ext2spice -o w_metal4_plane_100.spice
quit -noprompt
