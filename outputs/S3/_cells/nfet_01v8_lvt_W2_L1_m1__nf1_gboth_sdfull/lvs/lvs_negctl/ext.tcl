gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull/lvs/lvs_negctl/extracted.spice
quit -noprompt
