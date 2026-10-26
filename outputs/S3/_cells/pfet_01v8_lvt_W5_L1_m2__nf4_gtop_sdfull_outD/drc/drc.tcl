gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD/pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD]]"
flatten pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD_flat
load pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD/drc/drc_report.txt w]
puts $f "top pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD (flattened) gds /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD/pfet_01v8_lvt_W5_L1_m2__nf4_gtop_sdfull_outD.gds"
puts $f "DRC_TOTAL $n"
foreach {why boxes} [drc listall why] { puts $f "[llength $boxes]\t$why" }
close $f
# negative control: a 0.05 um wide met1 sliver must be flagged
box 0um 0um 0.05um 1um
paint metal1
drc check
drc catchup
puts "NEG_CONTROL_TOTAL [drc list count total]"
quit -noprompt
