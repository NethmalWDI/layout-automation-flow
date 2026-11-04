# KLayout batch render at a fixed scale, for side-by-side comparisons in a report (plan v4 Phase 8 report):
#   klayout -zz -rd gds=<in.gds> -rd png=<out.png> -rd w=<um> -rd h=<um> [-rd ppu=<px per um>] [-rd outline=<W>x<H>]
#           [-rd cell=<name>] -r scripts/report_layout_png.py
# Every picture rendered with the same w, h and ppu has the same scale. `outline` draws a W x H um box (the hard
# outline) centred on the layout. `cell` also prints the bounding box of every instance of that cell (to measure a
# block inside a larger layout, e.g. the op-amp inside a Tiny Tapeout tile). Prints one JSON line.
import json
import os
import pya

gds = gds  # noqa: F821  (injected by -rd)
png = png  # noqa: F821
w = float(globals().get("w") or 260)
h = float(globals().get("h") or 240)
ppu = float(globals().get("ppu") or 4)
lyp = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), "sky130A/libs.tech/klayout/tech/sky130A.lyp")
view = pya.LayoutView()
view.set_config("background-color", "#ffffff")
view.set_config("grid-visible", "false")
view.load_layout(gds, True)
if os.path.exists(lyp):
    view.load_layer_props(lyp)
view.max_hier()
ly = view.cellview(0).layout()
top = ly.top_cell()
bb = top.dbbox()
cx, cy = bb.center().x, bb.center().y
out = {"top": top.name, "bbox_um": [round(bb.left, 3), round(bb.bottom, 3), round(bb.right, 3), round(bb.top, 3)],
       "w_um": round(bb.width(), 3), "h_um": round(bb.height(), 3), "png": png, "scale_px_per_um": ppu}
ol = globals().get("outline")
if ol:
    ow, oh = (float(x) for x in ol.lower().split("x"))
    a = pya.Annotation()
    a.p1, a.p2 = pya.DPoint(cx - ow / 2, cy - oh / 2), pya.DPoint(cx + ow / 2, cy + oh / 2)
    a.outline = pya.Annotation.OutlineBox
    a.style = pya.Annotation.StyleLine                   # a plain box, no ruler ticks
    a.fmt, a.fmt_x, a.fmt_y = "", "", ""
    view.insert_annotation(a)
    out["outline_um"] = [ow, oh]
names = [x for x in (globals().get("cell") or "").split(",") if x]   # one cell name or several, comma-separated
if names:
    found = {n: [] for n in names}
    it = top.begin_instances_rec()
    while not it.at_end():
        if it.inst_cell().name in found:
            # the instance's box in the top cell: the cell's own box, through the instance and its parents
            b = it.inst_cell().dbbox().transformed(it.dtrans() * it.inst_dtrans())
            found[it.inst_cell().name].append([round(b.left, 3), round(b.bottom, 3), round(b.right, 3), round(b.top, 3)])
        it.next()
    out["cells"] = found
view.zoom_box(pya.DBox(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
view.save_image(png, int(w * ppu), int(h * ppu))
print("REPORT_PNG " + json.dumps(out))
