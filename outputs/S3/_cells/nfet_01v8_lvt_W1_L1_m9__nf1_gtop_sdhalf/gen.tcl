drc off
snap internal
cellname delete nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
load nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf_pc w 1.0 l 1.0 nf 1 m 1 topc 1 botc 0 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 0
select top cell
expand
save nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
gds write nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
quit -noprompt
