drc off
snap internal
cellname delete nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdfull_outS_ng
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdfull_outS_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdfull_outS_ng_pc w 16.5325 l 2.03 nf 4 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 0 conn_gates 1
select top cell
expand
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdfull_outS_ng
quit -noprompt
