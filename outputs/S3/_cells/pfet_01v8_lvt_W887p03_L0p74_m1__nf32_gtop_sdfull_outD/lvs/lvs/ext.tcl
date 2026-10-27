gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf32_gtop_sdfull_outD/lvs/lvs/extracted.spice
quit -noprompt
