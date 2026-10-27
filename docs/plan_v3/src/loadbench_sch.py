# Draws the LOADBench two-stage Miller op-amp (row 546) as an SVG, from circuits/loadbench_miller/source/loadbench_miller.spice.
import sys
INK="#1f2937"; WIRE="#334155"; QUIET="#64748b"; BLUE="#1d4ed8"; ORANGE="#c2410c"; RED="#b91c1c"
out=[]
def w(*pts, col=WIRE, sw=2, dash=None):
    d="M"+" L".join(f"{x},{y}" for x,y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def dot(x,y,col=WIRE,r=4): out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
def t(x,y,s,size=14,col=INK,anchor="start",weight="normal"):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')
def mos(cx,cy,kind,gate="L",name="",size=""):
    # channel and gate plate
    g=-1 if gate=="L" else 1
    w((cx,cy-18),(cx,cy+18),sw=3,col=INK)
    w((cx+g*9,cy-18),(cx+g*9,cy+18),sw=2,col=INK)
    lead_end=cx+g*40
    if kind=="p":
        out.append(f'<circle cx="{cx+g*14}" cy="{cy}" r="5" fill="white" stroke="{INK}" stroke-width="2"/>')
        w((cx+g*19,cy),(lead_end,cy),col=INK)
    else:
        w((cx+g*9,cy),(lead_end,cy),col=INK)
    # top and bottom leads
    w((cx,cy-18),(cx,cy-40),col=INK); w((cx,cy+18),(cx,cy+40),col=INK)
    # source arrow: nmos source at bottom (arrow out), pmos source at top (arrow in)
    if kind=="n":
        out.append(f'<path d="M{cx-6},{cy+26} L{cx},{cy+34} L{cx+6},{cy+26}" fill="none" stroke="{INK}" stroke-width="2"/>')
    else:
        out.append(f'<path d="M{cx-6},{cy-28} L{cx},{cy-20} L{cx+6},{cy-28}" fill="none" stroke="{INK}" stroke-width="2"/>')
    tx=cx-g*14; anc="start" if gate=="L" else "end"
    t(tx,cy-4,name,15,INK,anc,"bold"); t(tx,cy+14,size,13,QUIET,anc)
    return lead_end
VDD=50; VSS=600
# rails
w((60,VDD),(1060,VDD),sw=2.5); t(60,VDD-12,"sourcePmos (VDD 1.8 V)",14,QUIET)
w((60,VSS),(1060,VSS),sw=2.5); t(60,VSS+22,"sourceNmos (VSS)",14,QUIET)
# P2 diode + Ibias
g=mos(150,110,"p","L","P2","37.3 / 0.74")
w((150,70),(150,VDD)); w((g,110),(g,170),(150,170)); w((150,130),(150,170)); dot(150,170)
t(160,190,"ibias",14,INK)
w((150,170),(150,330)); out.append(f'<circle cx="150" cy="360" r="22" fill="white" stroke="{INK}" stroke-width="2"/>')
w((150,348),(150,372),col=INK); out.append(f'<path d="M144,364 L150,372 L156,364" fill="none" stroke="{INK}" stroke-width="2"/>')
w((150,382),(150,VSS)); t(122,356,"Ibias",15,INK,"end","bold"); t(122,374,"10 µA ideal",13,QUIET,"end")
# P8 tail
g=mos(380,110,"p","L","P8","90.6 / 0.74")
w((380,70),(380,VDD)); t(g-4,106,"ibias",13,QUIET,"end")
w((380,150),(380,200)); w((270,200),(500,200)); dot(380,200)
t(510,190,"tail (FirstStageYsourceTransconductance)",13,QUIET)
# P7 / P6
g7=mos(270,262,"p","L","P7","14.2 / 0.89"); w((270,222),(270,200)); t(g7-4,266,"in1",15,INK,"end")
g6=mos(500,262,"p","R","P6","14.2 / 0.89"); w((500,222),(500,200)); t(g6+6,266,"in2",15,INK,"start","bold")
# mirror node and outFirstStage
w((270,302),(270,402)); w((500,302),(500,402))
# N1 diode / N4
mos(270,440,"n","R","",""); t(284,470,"N1",15,INK,"start","bold"); t(284,488,"66.1 / 2.03",13,QUIET); mos(500,440,"n","L","N4","66.1 / 2.03")
w((310,440),(460,440)); w((310,440),(310,370),(270,370)); dot(270,370); dot(310,440)
w((270,480),(270,VSS)); w((500,480),(500,VSS))
dot(270,340,ORANGE,6); t(282,330,"FirstStageYout1",14,ORANGE,"start","bold"); t(282,350,"mirror node, 1.14 pF,",13,ORANGE); t(282,366,"pole ≈ 33 MHz",13,ORANGE)
# outFirstStage to N3 and Cc
w((500,340),(700,340)); dot(500,340,BLUE,6); dot(700,340)
t(596,330,"outFirstStage",14,BLUE,"start","bold"); t(512,362,"dominant pole 0.52 MHz,",13,BLUE); t(512,378,"high impedance",13,BLUE)
w((700,340),(700,500),(820,500))
# Cc
w((700,340),(700,340)); w((700,340),(772,340)); w((772,322),(772,358),col=INK,sw=3); w((786,322),(786,358),col=INK,sw=3); w((786,340),(860,340))
t(779,378,"Cc 0.5 pF (ideal)",13,INK,"middle","bold")
# P5 / N3 second stage
g=mos(860,110,"p","L","P5","887 / 0.74"); w((860,70),(860,VDD)); t(g-4,106,"ibias",13,QUIET,"end")
w((860,150),(860,462)); dot(860,340,INK,5)
mos(860,500,"n","L","N3","484 / 0.24"); w((860,540),(860,VSS))
# out and CL
w((860,340),(1010,340)); t(1018,345,"out",15,INK,"start","bold")
w((1010,340),(1010,452)); w((992,452),(1028,452),col=INK,sw=3); w((992,466),(1028,466),col=INK,sw=3); w((1010,466),(1010,VSS))
t(1036,456,"CL 1 pF",13,QUIET); t(1036,472,"(testbench)",13,QUIET)
# critical couplings markers
def badge(x,y,n):
    out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{RED}"/>'); t(x,y+5,str(n),13,"white","middle","bold")
w((588,262),(588,340),col=RED,sw=2,dash="6 5"); badge(588,296,1)
w((262,345),(230,345),(230,560),(970,560),(970,348),col=RED,sw=2,dash="6 5"); badge(600,560,2)
w((724,334),(724,290),(840,290),(840,334),col=RED,sw=2,dash="6 5"); badge(782,290,3)
# legend
t(60,670,"Most critical parasitics (S1, nominal): capacitance that alone uses the whole margin",14,INK,"start","bold")
badge(72,696,1); t(92,701,"in2 ↔ outFirstStage: 59 fF uses the 5.3° PM margin (input coupling into the high-impedance node)",13,INK)
badge(72,722,2); t(92,727,"FirstStageYout1 ↔ out: 77 fF uses the PM margin",13,INK)
badge(72,748,3); t(92,753,"out ↔ outFirstStage, in parallel with Cc: 83 fF uses the 2.3 MHz GBW margin",13,INK)
t(60,782,"For comparison, a capacitance to ground needs 613 fF or more on any node. Sizes are W / L in µm, nf = 1, from LOADBench row 546.",13,QUIET)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1130 800" width="1130" height="800" font-family="DejaVu Sans, Arial, sans-serif"><rect width="1130" height="800" fill="white"/>'+"".join(out)+'</svg>'
open(sys.argv[1],"w").write(svg)
