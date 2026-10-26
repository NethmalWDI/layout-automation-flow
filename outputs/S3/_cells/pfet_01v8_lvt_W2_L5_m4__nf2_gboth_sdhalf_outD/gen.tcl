drc off
snap internal
cellname delete pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdhalf_outD
load pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdhalf_outD -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdhalf_outD_pc w 1.0 l 5.0 nf 2 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdhalf_outD
quit -noprompt
