drc off
snap internal
cellname delete pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdfull
load pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdfull -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdfull_pc w 14.21 l 0.89 nf 1 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 0
select top cell
expand
save pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdfull
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdfull
quit -noprompt
