drc off
snap internal
cellname delete nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
load nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD_pc w 6.0 l 0.5 nf 4 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
gds write nfet_01v8_W24_L0p5_m1__nf4_gboth_sdhalf_outD
quit -noprompt
