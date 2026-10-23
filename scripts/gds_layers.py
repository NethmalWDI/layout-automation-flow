# klayout -zz -rd gds=<file> -r scripts/gds_layers.py : list layers, shape and text counts, sample texts
import pya
ly = pya.Layout(); ly.read(gds)  # noqa: F821
top = ly.top_cell()
for li in ly.layer_indexes():
    info = ly.get_info(li)
    n_poly = n_txt = 0; texts = []
    it = top.begin_shapes_rec(li)
    while not it.at_end():
        sh = it.shape()
        if sh.is_text():
            n_txt += 1
            if len(texts) < 6: texts.append(sh.text_string)
        else:
            n_poly += 1
        it.next()
    print(f"{info.layer}/{info.datatype}\tshapes={n_poly}\ttexts={n_txt}\t{texts}")
