drc off
snap internal
cellname delete nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outD
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outD -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outD_pc w 60.525 l 0.24 nf 8 m 1 topc 1 botc 0 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdhalf_outD
quit -noprompt
