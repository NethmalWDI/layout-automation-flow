drc off
snap internal
cellname delete pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS_ng
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS_ng_pc w 9.325 l 0.74 nf 4 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 0 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gboth_sdhalf_outS_ng
quit -noprompt
