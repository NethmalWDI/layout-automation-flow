gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS/nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS]]"
flatten nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS_flat
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS/drc/drc_report.txt w]
puts $f "top nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS (flattened) gds /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS/nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outS.gds"
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
