drc off
snap internal
cellname delete pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outD
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outD -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outD_pc w 7.105 l 0.89 nf 2 m 1 topc 1 botc 0 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outD
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gtop_sdhalf_outD
quit -noprompt
