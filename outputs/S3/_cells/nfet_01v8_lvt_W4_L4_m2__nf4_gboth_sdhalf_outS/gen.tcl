drc off
snap internal
cellname delete nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdhalf_outS
load nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdhalf_outS -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdhalf_outS_pc w 1.0 l 4.0 nf 4 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdhalf_outS
quit -noprompt
