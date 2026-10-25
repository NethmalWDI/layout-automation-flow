drc off
snap internal
cellname delete nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
load nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS_pc w 3.0 l 0.5 nf 8 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
gds write nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outS
quit -noprompt
