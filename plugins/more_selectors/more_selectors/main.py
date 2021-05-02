import cadquery as cq
from math import sqrt
from . import utils


class InfiniteCylinderSelector(cq.Selector):
    """
    Selects any shape present in the defined infinite cylinder 
    based on the shape center of mass point.   

    """

    def __init__(self, origin, along_axis, radius, debug=False):
        self.outer_radius = radius
        self.axis = self.get_axis(along_axis)
        xdir = self.get_ortho_vector(self.axis)
        self.base = cq.Plane(cq.Vector(origin), xdir, self.axis.toTuple())
        if debug:
            utils.make_debug_cylinder(self.base, self.outer_radius)

    def get_axis(self, axis_value):
        named_vectors = {
            "X": cq.Vector(1, 0, 0),
            "-X": cq.Vector(-1, 0, 0),
            "Y": cq.Vector(0, 1, 0),
            "-Y": cq.Vector(0, -1, 0),
            "Z": cq.Vector(0, 0, 1),
            "-Z": cq.Vector(0, 0, -1),
        }
        if isinstance(axis_value, str):
            try:
                return named_vectors[axis_value]
            except KeyError:
                raise ValueError(
                    "Supported names are {}".format(list(named_vectors.keys()))
                )
        else:
            if cq.Vector(axis_value).Length != 0:
                return cq.Vector(axis_value)
            else:
                raise ValueError("Axis of the cylinder must be non null")

    def get_ortho_vector(self, vector):
        # returns a vector orthogonal to the provided vector
        if 0 not in vector.toTuple():
            return (1, 1, (-vector.x - vector.y) / vector.z)
        else:
            if vector.x != 0:
                return ((-vector.y - vector.z) / vector.x, 1, 1)
            elif vector.y != 0:
                return (1, (-vector.x - vector.z) / vector.y, 1)
            else:
                return (1, 1, (-vector.x - vector.y) / vector.z)

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x ** 2 + projected_p.y ** 2)

            if p_radius < self.outer_radius:
                result.append(o)

        return result


class InfHollowCylinderSelector(InfiniteCylinderSelector):
    """
    Selects any shape present in the defined infinite hollow  
    cylinder based on the shape center of mass point.   
    """

    def __init__(self, origin, along_axis, outer_radius, inner_radius, debug=False):
        if outer_radius < inner_radius:
            raise ValueError("outer_radius must be greater than inner_radius")
        super().__init__(origin, along_axis, outer_radius, debug=False)
        self.inner_radius = inner_radius
        if debug:
            utils.make_debug_cylinder(
                self.base, self.outer_radius, inner_radius=self.inner_radius
            )

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x ** 2 + projected_p.y ** 2)

            if p_radius < self.outer_radius and p_radius > self.inner_radius:
                result.append(o)
        return result


class CylinderSelector(InfiniteCylinderSelector):
    """
    Selects any shape present in the defined cylinder 
    based on the shape center of mass point.   
    """

    def __init__(self, origin, along_axis, height, radius, debug=False):
        super().__init__(origin, along_axis, radius)
        self.height = height
        if debug:
            utils.make_debug_cylinder(self.base, radius, height=height)

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x ** 2 + projected_p.y ** 2)

            if p_radius < self.outer_radius and (
                projected_p.z < self.height and projected_p.z > 0
            ):
                result.append(o)
        return result


class HollowCylinderSelector(InfHollowCylinderSelector):
    """
    Selects any shape present in the defined hollow cylinder 
    based on the shape center of mass point.   
    """

    def __init__(
        self, origin, along_axis, height, outer_radius, inner_radius, debug=False
    ):
        super().__init__(origin, along_axis, outer_radius, inner_radius)
        self.height = height
        if debug:
            utils.make_debug_cylinder(
                self.base, outer_radius, inner_radius=inner_radius, height=height
            )

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x ** 2 + projected_p.y ** 2)

            if (p_radius < self.outer_radius and p_radius > self.inner_radius) and (
                projected_p.z < self.height and projected_p.z > 0
            ):
                result.append(o)
        return result


class SphereSelector(cq.Selector):
    """
    Selects any shape present in the defined sphere
    based on the shape center of mass point.   
    """

    def __init__(self, origin, radius, debug=False):
        self.origin = cq.Vector(origin)
        self.outer_radius = radius
        if debug:
            utils.make_debug_sphere(origin, radius)

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = p - self.origin
            p_radius = sqrt(
                projected_p.x ** 2 + projected_p.y ** 2 + projected_p.z ** 2
            )

            if p_radius < self.outer_radius:
                result.append(o)
        return result


class HollowSphereSelector(SphereSelector):
    """
    Selects any shape present in the defined hollow sphere
    based on the shape center of mass point.   
    """

    def __init__(self, origin, outer_radius, inner_radius, debug=False):
        if outer_radius < inner_radius:
            raise ValueError("outer_radius must be greater than inner_radius")
        super().__init__(origin, outer_radius)
        self.inner_radius = inner_radius
        if debug:
            utils.make_debug_sphere(origin, outer_radius, inner_radius=inner_radius)

    def filter(self, objectList):
        result = []
        for o in objectList:
            p = o.Center()
            projected_p = p - self.origin
            p_radius = sqrt(
                projected_p.x ** 2 + projected_p.y ** 2 + projected_p.z ** 2
            )

            if p_radius < self.outer_radius and p_radius > self.inner_radius:
                result.append(o)
        return result
