drc off
snap internal
cellname delete pfet_01v8_W8_L1_m1__nf1_gtop_sdhalf_ng
load pfet_01v8_W8_L1_m1__nf1_gtop_sdhalf_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 pfet_01v8_W8_L1_m1__nf1_gtop_sdhalf_ng_pc w 8.0 l 1.0 nf 1 m 1 topc 1 botc 0 diffcov 50 viasrc 50 viadrn 50 guard 0 conn_gates 0
select top cell
expand
save pfet_01v8_W8_L1_m1__nf1_gtop_sdhalf_ng
gds write pfet_01v8_W8_L1_m1__nf1_gtop_sdhalf_ng
quit -noprompt
