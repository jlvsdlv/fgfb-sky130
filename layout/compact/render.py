import klayout.lay as lay, klayout.db as db
for gds,box,out,px in [("fgfb_c.gds",db.DBox(-9,-8.7,13.3,6.1),"compact.png",(1500,1000)),
                       ("../layout/fgfb_cell.gds",db.DBox(-15.5,-5.5,22.7,24.5),"orig.png",(1500,1180))]:
    lv=lay.LayoutView(); lv.load_layout(gds,0)
    lv.load_layer_props("/home/claude/pdk/sky130A/libs.tech/klayout/tech/sky130A.lyp")
    lv.max_hier(); lv.set_config("background-color","#ffffff"); lv.set_config("grid-visible","false"); lv.set_config("text-visible","false")
    lv.zoom_box(box); lv.save_image_with_options(out,px[0],px[1],0,0,0,db.DBox(),False)
