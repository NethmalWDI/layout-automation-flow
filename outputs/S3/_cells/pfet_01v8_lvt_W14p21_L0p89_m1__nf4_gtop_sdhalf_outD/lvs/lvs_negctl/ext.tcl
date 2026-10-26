gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdhalf_outD/lvs/lvs_negctl/extracted.spice
quit -noprompt
