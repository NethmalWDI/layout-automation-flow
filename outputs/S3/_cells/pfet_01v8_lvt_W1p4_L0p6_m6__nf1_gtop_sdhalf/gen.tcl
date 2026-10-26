drc off
snap internal
cellname delete pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf
load pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf_pc w 1.4 l 0.6 nf 1 m 1 topc 1 botc 0 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 0
select top cell
expand
save pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf
gds write pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf
quit -noprompt
