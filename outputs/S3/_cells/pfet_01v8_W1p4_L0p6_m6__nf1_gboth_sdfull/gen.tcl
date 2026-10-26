drc off
snap internal
cellname delete pfet_01v8_W1p4_L0p6_m6__nf1_gboth_sdfull
load pfet_01v8_W1p4_L0p6_m6__nf1_gboth_sdfull -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 pfet_01v8_W1p4_L0p6_m6__nf1_gboth_sdfull_pc w 1.4 l 0.6 nf 1 m 1 topc 1 botc 1 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 0
select top cell
expand
save pfet_01v8_W1p4_L0p6_m6__nf1_gboth_sdfull
gds write pfet_01v8_W1p4_L0p6_m6__nf1_gboth_sdfull
quit -noprompt
