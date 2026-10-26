gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L10_m2__nf1_gtop_sdfull/lvs/lvs/extracted.spice
quit -noprompt
