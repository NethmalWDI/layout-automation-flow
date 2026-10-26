drc off
snap internal
cellname delete nfet_01v8_lvt_W0p6_L5_m2__nf1_gtop_sdfull
load nfet_01v8_lvt_W0p6_L5_m2__nf1_gtop_sdfull -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt nfet_01v8_lvt_W0p6_L5_m2__nf1_gtop_sdfull_pc w 0.6 l 5.0 nf 1 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 0
select top cell
expand
save nfet_01v8_lvt_W0p6_L5_m2__nf1_gtop_sdfull
gds write nfet_01v8_lvt_W0p6_L5_m2__nf1_gtop_sdfull
quit -noprompt
