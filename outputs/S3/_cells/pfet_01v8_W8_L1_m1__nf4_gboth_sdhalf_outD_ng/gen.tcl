drc off
snap internal
cellname delete pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
load pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng_pc w 2.0 l 1.0 nf 4 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 0 conn_gates 1
select top cell
expand
save pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
gds write pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outD_ng
quit -noprompt
