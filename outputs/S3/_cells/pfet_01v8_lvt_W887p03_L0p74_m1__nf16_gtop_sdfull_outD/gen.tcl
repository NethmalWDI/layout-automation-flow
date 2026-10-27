drc off
snap internal
cellname delete pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD_pc w 55.4394 l 0.74 nf 16 m 1 topc 1 botc 0 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdfull_outD
quit -noprompt
