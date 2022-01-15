import math
from typing import Optional
import cadquery as cq
from cadquery.occ_impl.geom import Vector
from cadquery.occ_impl.shapes import Edge, Wire


def _teardrop(self, radius: float = 1, rotate: float = 0, clip: Optional[float] = None):

    """
    Make a teardrop shape (wire) for each item on the stack.

    The use case is in making teardrop shaped holes for 3D printing with Fused filament fabrication 
    (FFF) to reduce the overhang angle compared to standard holes.  Truncated flat-topped holes can
    be generated where the small horizontal gap is bridged when printing.

    :param radius: radius of circle
    :param rotate: rotation angle in degrees
    :param clip: clipping distance along line from center to vertex to create a truncated teardrop

    """

    overhang_angle = 45
    center = Vector()
    ymax = math.sqrt(2 * radius ** 2)  # y distance circle center to vertex point
    yjoin = radius * math.sin(math.radians(overhang_angle))
    xjoin = radius * math.cos(math.radians(overhang_angle))
    p1 = Vector(center.x - xjoin, center.y + yjoin)  # arc-line intersection point
    p2 = Vector(center.x, center.y - radius)  # arc point
    p3 = Vector(center.x + xjoin, center.y + yjoin)  # arc-line intersection point
    edges = []

    if clip == None:
        # teardrop - three point arc, two lines

        ptop = Vector(center.x, center.y + ymax)  # vertex point

        edges.append(Edge.makeThreePointArc(p1, p2, p3))
        edges.append(Edge.makeLine(p3, ptop))
        edges.append(Edge.makeLine(ptop, p1))

    elif clip >= ymax:
        raise ValueError(
            f"teardrop - value of 'clip' argument must be less than {ymax}"
        )

    elif clip <= -radius:
        raise ValueError(
            f"teardrop - value of 'clip' argument must be greater than {-radius}"
        )

    elif clip > yjoin:
        # teardrop truncated with horizontal line
        # three point arc, two lines at 45 degrees, one horizontal line

        xflat = (clip - yjoin) / math.tan(math.radians(overhang_angle))
        p4 = Vector(p1.x + xflat, center.y + clip)
        p5 = Vector(p3.x - xflat, center.y + clip)

        edges.append(Edge.makeThreePointArc(p1, p2, p3))
        edges.append(Edge.makeLine(p1, p4))
        edges.append(Edge.makeLine(p3, p5))
        edges.append(Edge.makeLine(p4, p5))  # clip

    elif clip <= yjoin:
        # three point arc and horizontal line
        # the 45 degree lines characteristic of the teardrop shape do not exist
        # e.g. clip = 0 results in a half circle

        xflat = math.sqrt(radius ** 2 - clip ** 2)
        p1 = Vector(center.x - xflat, center.y + clip)  # arc endpoint
        p3 = Vector(center.x + xflat, center.y + clip)  # arc endpoint

        edges.append(Edge.makeThreePointArc(p1, p2, p3))
        edges.append(Edge.makeLine(p1, p3))

    w = Wire.assembleEdges(edges).rotate(Vector(0, 0, 0), Vector(0, 0, 1), rotate)

    return self.eachpoint(lambda loc: w.moved(loc), True)


# Patch the function into the Workplane class
cq.Workplane.teardrop = _teardrop
