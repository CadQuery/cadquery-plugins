import cadquery as cq

def make_cubes(self, length):
    """
    Sample function that will be monkey patched into cadquery.Workplane.
    self refers to the Workplane object, as this function will be part of
    that class once it has been monkey patched in.
    Note the use of eachpoint so that this plugin will work with multiple 
    points on the stack simultaneously, like other cadquery objects (rect,
    box, sphere, etc).
    """

    # Create the box solid
    s = cq.Solid.makeBox(length, length, length, cq.Vector(0, 0, 0))

    # Use CQ eachpoint utility method to iterate over the stack and position the cubes
    return self.eachpoint(lambda loc: s.located(loc), True)


def register():
    """
    Makes plugin functions available in the cadquery.Workplane class.
    Needs to be called before this plugin's functions can be used.
    """

    cq.Workplane.make_cubes = make_cubes
