gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng/lvs/lvs -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gboth_sdfull_outS_ng/lvs/lvs/extracted.spice
quit -noprompt
