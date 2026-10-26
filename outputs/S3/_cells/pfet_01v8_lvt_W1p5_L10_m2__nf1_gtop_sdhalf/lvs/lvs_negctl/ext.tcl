gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf.gds
load pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf/lvs/lvs_negctl/extracted.spice
quit -noprompt
