import cadquery as cq
from collections import namedtuple

dims = namedtuple("dims", ["diam", "depth", "bolt_diam"])

heatsert_dims = {
    "M6": dims(diam=8, depth=12.7, bolt_diam=6),
    "M5": dims(diam=6.4, depth=9.5, bolt_diam=5),
    "M4": dims(diam=5.6, depth=8.1, bolt_diam=4),
    "M3": dims(diam=4.0, depth=5.8, bolt_diam=3),
}


def heatsert(self, size: str = "M6", bolt_clear: float = 0, clean: bool = True):
    """
    Creates a hole for a heatsert at each point on the stack.

    :param size: what size heatsert the hole is intended for
    :param bolt_clear: allow clearance for this length of fastener below the surface
    :param clean: passed through to Workplane.cutEach
    """
    diam, depth, bolt_diam = heatsert_dims[size]

    def _one_heatsert(loc):
        pnt = cq.Vector(0, 0, 0)
        boreDir = cq.Vector(0, 0, -1)
        hole = cq.Solid.makeCylinder(diam / 2.0, depth, pnt, boreDir)
        if bolt_clear:
            extra_hole_diam = bolt_diam * 1.2
            extra_hole = cq.Solid.makeCylinder(
                extra_hole_diam / 2.0, bolt_clear, pnt, boreDir
            )
            hole = hole.fuse(extra_hole)
        return hole.move(loc)

    return self.cutEach(_one_heatsert, True, clean)


# Patch the function into the Workplane class
cq.Workplane.heatsert = heatsert
