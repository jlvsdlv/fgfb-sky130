import klayout.lay as lay, klayout.db as db
lv = lay.LayoutView()
lv.load_layout("fgfb_cell.gds", 0)
lv.load_layer_props("/home/claude/pdk/sky130A/libs.tech/klayout/tech/sky130A.lyp")
lv.max_hier()
lv.set_config("background-color", "#ffffff"); lv.set_config("grid-visible", "false")
lv.set_config("text-visible", "false")
lv.zoom_box(db.DBox(-15.5, -5.5, 22.7, 24.5))
lv.save_image_with_options("layout_paper.png", 2400, 1885, 0, 0, 0, db.DBox(), False)
