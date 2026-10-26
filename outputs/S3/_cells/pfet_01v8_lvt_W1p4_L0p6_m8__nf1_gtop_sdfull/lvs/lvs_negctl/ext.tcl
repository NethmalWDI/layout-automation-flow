gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull/lvs/lvs_negctl/extracted.spice
quit -noprompt
