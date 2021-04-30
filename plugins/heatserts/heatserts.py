import cadquery as cq
from collections import namedtuple
from typing import Tuple, Optional, Union
from numbers import Real

dims = namedtuple("dims", ["diam", "depth", "bolt_diam"])

heatsert_dims = {
    "M6": dims(diam=8, depth=12.7, bolt_diam=6),
    "M5": dims(diam=6.4, depth=9.5, bolt_diam=5),
    "M4": dims(diam=5.6, depth=8.1, bolt_diam=4),
    "M3": dims(diam=4.0, depth=5.8, bolt_diam=3),
}


def heatsert(
    self,
    size: str = "M6",
    bolt_clear: float = 0,
    chamfer: Optional[Union[float, Tuple[float, float]]] = None,
    clean: bool = True,
):
    """
    Creates a hole for a heatsert at each point on the stack.

    :param size: What size heatsert the hole is intended for
    :param bolt_clear: Allow clearance for this length of fastener below the surface
    :param chamfer: If a tuple of two floats, the first value is the setback on the face of your
      part (added to the diameter) and the second is the depth of the chamfer. If one value then
      it is both the setback and the depth (ie. a 45 degree chamfer).
    :param clean: Passed through to Workplane.cutEach
    """
    diam, depth, bolt_diam = heatsert_dims[size]

    if isinstance(chamfer, Real):
        chamfer_vals = (chamfer, chamfer)
    else:
        chamfer_vals = chamfer

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

        if chamfer:
            cone_face_radius = diam / 2 + chamfer_vals[0]
            cone = cq.Solid.makeCone(
                cone_face_radius, diam / 2, chamfer_vals[1], pnt, boreDir
            )
            hole = hole.fuse(cone)

        return hole.move(loc)

    return self.cutEach(_one_heatsert, True, clean)


# Patch the function into the Workplane class
cq.Workplane.heatsert = heatsert
