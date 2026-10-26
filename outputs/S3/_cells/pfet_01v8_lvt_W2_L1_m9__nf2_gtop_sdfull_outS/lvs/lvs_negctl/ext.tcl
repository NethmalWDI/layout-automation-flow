gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS
select top cell
port makeall
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS/lvs/lvs_negctl -o /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L1_m9__nf2_gtop_sdfull_outS/lvs/lvs_negctl/extracted.spice
quit -noprompt
