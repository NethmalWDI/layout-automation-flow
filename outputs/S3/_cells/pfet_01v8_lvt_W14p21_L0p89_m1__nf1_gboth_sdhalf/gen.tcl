drc off
snap internal
cellname delete pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdhalf
load pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdhalf -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdhalf_pc w 14.21 l 0.89 nf 1 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 0
select top cell
expand
save pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdhalf
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdhalf
quit -noprompt
