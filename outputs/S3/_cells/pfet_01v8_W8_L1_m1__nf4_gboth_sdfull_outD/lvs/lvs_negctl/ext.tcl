gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD.gds
load pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf4_gboth_sdfull_outD/lvs/lvs_negctl/extracted.spice
quit -noprompt
