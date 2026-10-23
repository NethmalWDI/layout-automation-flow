# KLayout batch render: klayout -zz -rd gds=<in.gds> -rd png=<out.png> [-rd lyp=<file>] -r scripts/gds_to_png.py
import os
import pya

gds = gds  # noqa: F821  (injected by -rd)
png = png  # noqa: F821
lyp = globals().get("lyp") or os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"),
                                           "sky130A/libs.tech/klayout/tech/sky130A.lyp")
view = pya.LayoutView()
view.set_config("background-color", "#ffffff")
view.set_config("grid-visible", "false")
view.load_layout(gds, True)
if os.path.exists(lyp):
    view.load_layer_props(lyp)
view.max_hier()
view.zoom_fit()
view.save_image(png, 1600, 1200)
ly = view.cellview(0).layout()
top = ly.top_cell()
bb = top.dbbox()
print(f"top={top.name} bbox_um=({bb.left:.3f},{bb.bottom:.3f})-({bb.right:.3f},{bb.top:.3f}) "
      f"W={bb.width():.3f} H={bb.height():.3f} area_um2={bb.width()*bb.height():.2f} png={png}")
