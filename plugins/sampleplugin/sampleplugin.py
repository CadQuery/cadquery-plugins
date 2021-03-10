import cadquery as cq

def make_cubes(self, length):
    # self refers to the Workplane object

    # create the solid
    s = cq.Solid.makeBox(length, length, length, cq.Vector(0, 0, 0))

    # use CQ utility method to iterate over the stack and position the cubes
    return self.eachpoint(lambda loc: s.located(loc), True)
