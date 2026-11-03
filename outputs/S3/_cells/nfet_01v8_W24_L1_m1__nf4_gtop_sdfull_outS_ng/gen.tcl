drc off
snap internal
cellname delete nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
load nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng_pc w 6.0 l 1.0 nf 4 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 0 conn_gates 1
select top cell
expand
save nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
quit -noprompt
