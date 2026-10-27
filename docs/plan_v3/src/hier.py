# Hierarchy pictures for the Plan v3 review pack. Data: circuits/<d>/upstream/hierarchy.json and primitives.json
# (primitives are PREDICTED rule-based recognition, except LOADBench's own recognition). Roles and flags: reviewer's reading.
import sys, html
INK="#1f2937"; QUIET="#64748b"; EDGE="#94a3b8"; FILL="#f8fafc"
FLAG={"error":("#b91c1c","#fee2e2"),"check":("#b45309","#fef3c7"),"info":("#1d4ed8","#dbeafe")}
def esc(s): return html.escape(s)
def draw(title, subtitle, design, blocks, outpath):
    # blocks: list of (block_name, block_desc, [ (prim_id, kind, devices, role, flag, flagtext) ])
    out=[]; RH=30; y=96
    X0, W0 = 24, 190; X1, W1 = 250, 250; X2, W2 = 540, 1180
    def t(x,y,s,size=14,col=INK,anchor="start",weight="normal"):
        out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')
    t(24,34,title,20,INK,"start","bold"); t(24,58,subtitle,14,QUIET)
    t(X0,84,"design",12,QUIET); t(X1,84,"block (schematic hierarchy)",12,QUIET); t(X2,84,"primitives: recognised structure · devices · role (reviewer's reading)",12,QUIET)
    block_y=[]
    for bname,bdesc,prims in blocks:
        h=max(len(prims),3)*RH+12
        by=y
        out.append(f'<rect x="{X1}" y="{by}" width="{W1}" height="{h-8}" rx="8" fill="{FILL}" stroke="{EDGE}"/>')
        t(X1+12,by+24,bname,15,INK,"start","bold")
        for i,line in enumerate(bdesc): t(X1+12,by+44+i*17,line,12.5,QUIET)
        for j,(pid,kind,dev,role,flag,ftext) in enumerate(prims):
            ry=by+j*RH
            col,bg=FLAG.get(flag,(EDGE,"white"))
            out.append(f'<rect x="{X2}" y="{ry+2}" width="{W2}" height="{RH-6}" rx="6" fill="{bg if flag else "white"}" stroke="{col if flag else EDGE}"/>')
            t(X2+10,ry+19,pid,12.5,QUIET); t(X2+120,ry+19,kind,13,INK,"start","bold")
            t(X2+420,ry+19,dev,13,INK); t(X2+730,ry+19,role,12.5,QUIET)
            if flag: t(X2+W2-10,ry+19,ftext,12,col,"end","bold")
            out.append(f'<path d="M{X1+W1} {by+20} C{X1+W1+20} {by+20} {X2-20} {ry+RH/2-1} {X2} {ry+RH/2-1}" fill="none" stroke="{EDGE}"/>')
        block_y.append(by+20)
        y+=h+8
    # design box
    dy=96; dh=y-96-8
    out.append(f'<rect x="{X0}" y="{dy}" width="{W0}" height="{dh}" rx="8" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    for i,line in enumerate(design): t(X0+12,dy+26+i*18,line,14 if i==0 else 12.5,INK if i==0 else QUIET,"start","bold" if i==0 else "normal")
    for by in block_y:
        out.append(f'<path d="M{X0+W0} {dy+20} C{X0+W0+18} {dy+20} {X1-18} {by} {X1} {by}" fill="none" stroke="{EDGE}"/>')
    # legend
    ly=y+10
    for k,(name,txt) in enumerate([("error","recognition error"),("check","check: operating point or grouping"),("info","information")]):
        col,bg=FLAG[name]; x=24+k*300
        out.append(f'<rect x="{x}" y="{ly}" width="18" height="14" rx="3" fill="{bg}" stroke="{col}"/>'); t(x+26,ly+12,txt,12.5,QUIET)
    H=ly+40
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1744 {H}" width="1744" height="{H}" font-family="DejaVu Sans, Arial, sans-serif"><rect width="1744" height="{H}" fill="white"/>'+"".join(out)+'</svg>'
    open(outpath,"w").write(svg)

d=sys.argv[1]; o=sys.argv[2]
if d=="loadbench":
    draw("LOADBench two-stage Miller: hierarchy as the flow reads it",
         "Source: LOADBench struct_recognition.xml (real, converted). 8 transistors; Cc and Ibias are ideal elements with no layout device.",
         ["loadbench_miller","diff-in, single-out","op-amp, 8 MOS"],
         [("top (one level)",["LOADBench partition:","5 structures"],[
            ("X2","pmos-differential-pair","P7, P6","input pair","",""),
            ("X3","nmos-current-mirror-load","N1, N4","first-stage load; mirror node","check","mirror pole ≈ 33 MHz"),
            ("X4","pmos-current-mirror","P2 → P8","tail current source","",""),
            ("X5","pmos-current-mirror","P2 → P5","second-stage current source","info","P2 shared with X4"),
            ("X1","common-source-stage","P5, N3","second stage","info","nf = 1, W up to 887 µm"),
            ("—","ideal elements","Cc, Ibias","compensation, bias","info","no layout device"),
         ])], o)
elif d=="iadc":
    draw("iadc folded-cascode OTA: hierarchy as the flow reads it",
         "Source: upstream netlist hierarchy (real); primitives by rule-based recognition (PREDICTED). 85 devices, 38 of them dummies.",
         ["iadc_ota","diff-in, diff-out","folded cascode","83 MOS, 2 MIM"],
         [("x2 · core",["folded_cascode_3_core","28 devices"],[
            ("X39","nmos-differential-pair","M1, M2","input pair, L 0.2 µm lvt","",""),
            ("X54","pmos-matched-current-source-pair","M11, M12","fold current sources","check","in triode at our bias"),
            ("X56","pmos-matched-cascode-pair","M1A, M8","PMOS cascodes (fold → out)","",""),
            ("X42","nmos-matched-cascode-pair","M3A, M7","NMOS cascodes","",""),
            ("X41","nmos-matched-current-source-pair","M3, M4","NMOS current sources","",""),
            ("X64, X65","nmos-single × 2","M5, M6","tail: fixed half, CMFB half","info","one tail, split in two"),
            ("X23–X38","nmos/pmos-dummy × 16","M23 … M83","dummies (shorted, or off to a rail)","info","S1 tags shorted ones as diodes"),
          ]),
          ("x1 · bias",["folded_cascode_3_bias","52 devices"],[
            ("X40","nmos-current-mirror","M7 → M6","i_bias input mirror","",""),
            ("X57–X63","diodes and singles","M1–M5, M31, M32","bias_a … bias_d generation","",""),
            ("X53, X55","pmos source + cascode pairs","M21, M25 · M22, M26","PMOS bias legs","check","M21, M25 in triode"),
            ("X43–X52","nmos-matched-cascode-pair × 10","M33 … M79 (gate cm)","5 stacks × 4 series units","error","composite device, not pairs"),
            ("X4–X22","nmos/pmos-dummy × 19","M8 … M60","dummies","",""),
          ]),
          ("top",["CMFB capacitors,","top-level dummies"],[
            ("X66, X67","capacitor × 2","C3, C4","op→cmc, on→cmc (CMFB, kept)","info","load the outputs in DM"),
            ("X1–X3","dummy × 3","M43, M45, M9","dummies","",""),
          ])], o)
elif d=="ttsky":
    draw("TTSKY25a fully differential op-amp: hierarchy as the flow reads it",
         "Source: xschem hierarchy (real); primitives by rule-based recognition (PREDICTED). 54 MOS, 2 MIM, 40 poly resistors, external Rgm.",
         ["ttsky25a_fd","diff-in, diff-out","two-stage, 2 CMFB","Opamp_with_bias"],
         [("x1 · Diff_opamp",["folded-cascode stage 1","+ its CMFB, 27 devices"],[
            ("X1","nmos-differential-pair","M5, M6","input pair, L 4 µm","",""),
            ("X20","pmos-matched-current-source-pair","M13, M14","fold sources (gate = CMFB1)","",""),
            ("X19","pmos-matched-cascode-pair","M11, M12","PMOS cascodes, L 5 µm","check","sets the fold pole"),
            ("X13","nmos-matched-cascode-pair","M19, M4","tail cascode + output cascode","error","should be (M4, M8)"),
            ("X14","nmos-matched-cascode-pair","M3, M8","tail cascode + output cascode","error","should be (M19, M3)"),
            ("X6","nmos-current-mirror","M46 → M1, M2, M7, M9, M22, M15","net4 sinks, three roles","info","tail · outputs · CMFB tails"),
            ("X2, X3","nmos-differential-pair × 2","M18, M16 · M10, M17","CMFB1 sense pairs, L 20 µm","check","load Vop1, Vom1"),
            ("X11","pmos-current-mirror-load","M20, M21","CMFB1 load","",""),
            ("X7, X25, X26","mirror and diodes","M23, M24, M25, M47","cascode bias (x1_Vbias, net5)","",""),
          ]),
          ("x2 · Common_source_stage",["stage 2 + resistive","CMFB, 12 devices"],[
            ("X27, X28","pmos-single × 2","M9, M4","second-stage input devices","error","missing matched pair"),
            ("X15","nmos-matched-current-source-pair","M2, M1","second-stage loads (CMFB2)","",""),
            ("X4","pmos-differential-pair","M7, M8","CMFB2 amplifier","",""),
            ("X9, X12, X8","mirrors","M5, M6 · M12, M3 · M10, M11","CMFB2 load, tail, bias","",""),
          ]),
          ("x2/x1, x2/x2 · res_pack",["CM sense resistors"],[
            ("X31, X32","resistor-string × 2","20 × poly 40/0.5 µm each","Vop/Vom → Vcm, ≈ 87 kΩ","info","long parallel strings"),
          ]),
          ("top",["bias and Miller caps","18 elements"],[
            ("X16, X10, X5","beta multiplier","M32, M34 · M39, M38 · M33, M37, M41","PBias / NBias core","",""),
            ("X21–X24","diodes and singles","M35, M36, M40, M42","core + start-up","",""),
            ("X17, X18","pmos pairs","M43, M44 · M45, M54","bias legs → net4 … net7","",""),
            ("X29, X30","capacitor × 2","C1, C2 (MIM 5 × 10×10 µm)","Miller caps","",""),
            ("X33","resistor","Rgm_ext 12 kΩ","off-chip bias resistor","info","outside the layout"),
          ])], o)
