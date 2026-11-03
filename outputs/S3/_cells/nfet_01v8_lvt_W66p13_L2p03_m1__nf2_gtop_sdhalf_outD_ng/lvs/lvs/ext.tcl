gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng/lvs/lvs -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outD_ng/lvs/lvs/extracted.spice
quit -noprompt
