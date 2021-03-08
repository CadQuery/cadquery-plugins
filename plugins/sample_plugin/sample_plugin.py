from cadquery import *

def make_cubes(self, length):
    # self refers to the CQ or Workplane object

    # create the solid
    s = Solid.makeBox(length, length, length, Vector(0, 0, 0))

    # use CQ utility method to iterate over the stack an position the cubes
    return self.eachpoint(lambda loc: s.located(loc), True)