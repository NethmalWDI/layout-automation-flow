gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf.gds
load nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/lvs/lvs -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf/lvs/lvs/extracted.spice
quit -noprompt
