gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng.gds
load pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gboth_sdfull_ng/lvs/lvs/extracted.spice
quit -noprompt
