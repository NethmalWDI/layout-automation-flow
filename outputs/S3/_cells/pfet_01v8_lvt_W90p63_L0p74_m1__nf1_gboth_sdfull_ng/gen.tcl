drc off
snap internal
cellname delete pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
load pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng_pc w 90.63 l 0.74 nf 1 m 1 topc 1 botc 1 diffcov 100 viasrc 100 viadrn 100 guard 0 conn_gates 0
select top cell
expand
save pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf1_gboth_sdfull_ng
quit -noprompt
