drc off
snap internal
cellname delete XDiodeTransistorNmos1
load XDiodeTransistorNmos1 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt XDiodeTransistorNmos1_pc w 66.13 l 2.03 nf 1 m 1
select top cell
expand
save XDiodeTransistorNmos1
gds write XDiodeTransistorNmos1
cellname delete XDiodeTransistorPmos2
load XDiodeTransistorPmos2 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt XDiodeTransistorPmos2_pc w 37.3 l 0.74 nf 1 m 1
select top cell
expand
save XDiodeTransistorPmos2
gds write XDiodeTransistorPmos2
cellname delete XNormalTransistorNmos3
load XNormalTransistorNmos3 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt XNormalTransistorNmos3_pc w 484.2 l 0.24 nf 1 m 1
select top cell
expand
save XNormalTransistorNmos3
gds write XNormalTransistorNmos3
cellname delete XNormalTransistorNmos4
load XNormalTransistorNmos4 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8_lvt XNormalTransistorNmos4_pc w 66.13 l 2.03 nf 1 m 1
select top cell
expand
save XNormalTransistorNmos4
gds write XNormalTransistorNmos4
cellname delete XNormalTransistorPmos5
load XNormalTransistorPmos5 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt XNormalTransistorPmos5_pc w 887.03 l 0.74 nf 1 m 1
select top cell
expand
save XNormalTransistorPmos5
gds write XNormalTransistorPmos5
cellname delete XNormalTransistorPmos6
load XNormalTransistorPmos6 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt XNormalTransistorPmos6_pc w 14.21 l 0.89 nf 1 m 1
select top cell
expand
save XNormalTransistorPmos6
gds write XNormalTransistorPmos6
cellname delete XNormalTransistorPmos7
load XNormalTransistorPmos7 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt XNormalTransistorPmos7_pc w 14.21 l 0.89 nf 1 m 1
select top cell
expand
save XNormalTransistorPmos7
gds write XNormalTransistorPmos7
cellname delete XNormalTransistorPmos8
load XNormalTransistorPmos8 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt XNormalTransistorPmos8_pc w 90.63 l 0.74 nf 1 m 1
select top cell
expand
save XNormalTransistorPmos8
gds write XNormalTransistorPmos8
cellname delete Capacitor2
load Capacitor2 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__cap_mim_m3_1 Capacitor2_pc w 15.66 l 15.66 nx 1 ny 1
select top cell
expand
save Capacitor2
gds write Capacitor2
quit -noprompt
