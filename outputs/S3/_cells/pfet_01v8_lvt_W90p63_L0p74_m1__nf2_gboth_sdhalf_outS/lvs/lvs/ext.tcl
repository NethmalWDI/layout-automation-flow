gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gboth_sdhalf_outS/lvs/lvs/extracted.spice
quit -noprompt
