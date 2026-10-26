gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W5_L20_m2__nf2_gtop_sdhalf_outD/lvs/lvs_negctl/extracted.spice
quit -noprompt
