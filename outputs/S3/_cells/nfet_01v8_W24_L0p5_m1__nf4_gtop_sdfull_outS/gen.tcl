drc off
snap internal
cellname delete nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outS
load nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outS -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outS_pc w 6.0 l 0.5 nf 4 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 1
select top cell
expand
save nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outS
gds write nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outS
quit -noprompt
