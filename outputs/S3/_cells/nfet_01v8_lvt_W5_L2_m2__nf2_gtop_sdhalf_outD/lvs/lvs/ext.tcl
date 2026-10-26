gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD/lvs/lvs -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outD/lvs/lvs/extracted.spice
quit -noprompt
