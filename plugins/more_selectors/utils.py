def make_cylinder(plane, height, radius):
    cyl = cq.Workplane(plane).circle(radius).extrude(height)
    try:
        show_object(cyl, options={"alpha":0.7, "color": (64, 164, 223)})
    except NameError:
        pass