drc off
snap internal
cellname delete nfet_01v8_W24_L0p5_m1__nf1_gboth_sdhalf
load nfet_01v8_W24_L0p5_m1__nf1_gboth_sdhalf -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 nfet_01v8_W24_L0p5_m1__nf1_gboth_sdhalf_pc w 24.0 l 0.5 nf 1 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 0
select top cell
expand
save nfet_01v8_W24_L0p5_m1__nf1_gboth_sdhalf
gds write nfet_01v8_W24_L0p5_m1__nf1_gboth_sdhalf
quit -noprompt
