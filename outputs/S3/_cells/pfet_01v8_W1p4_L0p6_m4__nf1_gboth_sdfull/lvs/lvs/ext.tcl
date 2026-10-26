gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull.gds
load pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gboth_sdfull/lvs/lvs/extracted.spice
quit -noprompt
