import cadquery as cq


def make_debug_cylinder(plane, outer_radius, inner_radius=None, height=None):
    infinite = False
    if height is None:
        infinite = True
        height = 10000
    if inner_radius is None:
        cyl = cq.Workplane(plane).circle(outer_radius).extrude(height, both=infinite)
    else:
        cyl = (
            cq.Workplane(plane)
            .circle(outer_radius)
            .circle(inner_radius)
            .extrude(height, both=infinite)
        )
    try:
        show_object(
            cyl,
            name="selection cylinder",
            options={"alpha": 0.7, "color": (64, 164, 223)},
        )

    except NameError:
        pass


def make_debug_sphere(origin, outer_radius, inner_radius=None):
    if inner_radius is None:
        sphere = cq.Workplane().transformed(offset=origin).sphere(outer_radius)
    else:
        inner_sphere = cq.Workplane().transformed(offset=origin).sphere(inner_radius)
        sphere = (
            cq.Workplane()
            .transformed(offset=origin)
            .sphere(outer_radius)
            .cut(inner_sphere)
        )
    try:
        show_object(
            sphere,
            name="selection sphere",
            options={"alpha": 0.7, "color": (64, 164, 223)},
        )
    except NameError:
        pass
