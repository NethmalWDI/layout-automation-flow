gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf.gds
load pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdhalf/lvs/lvs/extracted.spice
quit -noprompt
