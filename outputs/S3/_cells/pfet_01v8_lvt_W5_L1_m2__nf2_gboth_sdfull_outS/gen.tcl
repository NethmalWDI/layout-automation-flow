drc off
snap internal
cellname delete pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS
load pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS_pc w 2.5 l 1.0 nf 2 m 1 topc 1 botc 1 diffcov 100 viasrc 100 viadrn 100 guard 1 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS
gds write pfet_01v8_lvt_W5_L1_m2__nf2_gboth_sdfull_outS
quit -noprompt
