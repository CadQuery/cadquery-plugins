from typing import Callable, List, TypeVar, Union, Literal

import cadquery as cq


def applyToEachFace(
    wp: cq.Workplane,
    f_workplane_selector: Callable[[cq.Face], cq.Workplane],
    f_draw: Callable[[cq.Workplane, cq.Face], cq.Workplane],
    combine: Union[bool, Literal["cut", "a", "s"]] = True,
    clean: bool = True,
) -> cq.Workplane:
    """
    Basically equivalent to `Workplane.each(..)` but
    applicable only to faces and with tasks of face coordinate
    system selection and actually drawing in this coordinate
    system separated.

    :param wp: Workplane with some faces selected
    :param f_workplane_selector: callback that accepts
        a face and returns a Workplane (a coordinate system to
        that is passed to `f_draw`). See `XAxisInPlane`
        and `XAxisClosestTo`
    :param f_draw: a callback that accepts a workplane and
        a face and draws something in that workplane
    :param combine: True or "a" to combine the resulting solid 
        with parent solids if found, "cut" or "s" to remove 
        the resulting solid from the parent solids if found. 
        False to keep the resulting solid separated from 
        the parent solids.
    :param boolean clean: call :py:meth:`clean` afterwards to
        have a clean shape
    """

    def each_callback(face):
        wp_face = f_workplane_selector(face)

        return f_draw(wp_face, face).vals()[0]

    return wp.each(each_callback, combine=combine, clean=clean)


v_x_unit = cq.Vector(1, 0, 0)
v_y_unit = cq.Vector(0, 1, 0)
v_z_unit = cq.Vector(0, 0, 1)

# ---- VECTORS ----

WORLD_AXIS_UNIT_VECTORS_XYZ = [v_x_unit, v_y_unit, v_z_unit]

WORLD_AXIS_UNIT_VECTORS_XZY = [v_x_unit, v_z_unit, v_y_unit]

WORLD_AXIS_UNIT_VECTORS_YXZ = [v_y_unit, v_x_unit, v_z_unit]

WORLD_AXIS_UNIT_VECTORS_YZX = [v_y_unit, v_z_unit, v_x_unit]

WORLD_AXIS_UNIT_VECTORS_ZXY = [v_z_unit, v_x_unit, v_y_unit]

WORLD_AXIS_UNIT_VECTORS_ZYX = [v_z_unit, v_y_unit, v_x_unit]

# ---- PLANES ----

WORLD_XY_NORMAL = v_z_unit
WORLD_ZX_NORMAL = v_y_unit
WORLD_YZ_NORMAL = v_x_unit

WORLD_AXIS_PLANES_XY_ZX_YZ = [WORLD_XY_NORMAL, WORLD_ZX_NORMAL, WORLD_YZ_NORMAL]

WORLD_AXIS_PLANES_XY_YZ_ZX = [WORLD_XY_NORMAL, WORLD_YZ_NORMAL, WORLD_ZX_NORMAL]

WORLD_AXIS_PLANES_YZ_XY_ZX = [WORLD_YZ_NORMAL, WORLD_XY_NORMAL, WORLD_ZX_NORMAL]

WORLD_AXIS_PLANES_YZ_ZX_XY = [WORLD_YZ_NORMAL, WORLD_ZX_NORMAL, WORLD_XY_NORMAL]

WORLD_AXIS_PLANES_ZX_XY_YZ = [WORLD_ZX_NORMAL, WORLD_XY_NORMAL, WORLD_YZ_NORMAL]

WORLD_AXIS_PLANES_ZX_YZ_XY = [WORLD_ZX_NORMAL, WORLD_YZ_NORMAL, WORLD_XY_NORMAL]


def _create_workplane(
    v_center: cq.Vector, v_xaxis: cq.Vector, v_zaxis: cq.Vector
) -> cq.Workplane:
    return cq.Workplane(cq.Plane(v_center, v_xaxis, v_zaxis), origin=v_center)


class XAxisInPlane:
    """
    Selects face center of origin at face center 
    (`Face.Center()`) and face normal at face 
    center as Z axis.

    Selects X axis as intersection of face plane and one of
    user provided planes (specified by their unit normal vectors).

    The first one of the list that is not too close to
    being parallel to face plane is chosen.

    User-provided plane normals do not
    have to be linearly independent but their span
    (linear hull) should be all 3D vector space
    for XAxisInPlane to work on arbitrary faces.
    In some cases this requirement can be relaxed.
    """

    def __init__(self, plane_normals: List[cq.Vector], tolerance: float = 1e-3):
        self.__plane_normals = [x.normalized() for x in plane_normals]
        self.__tolerance = tolerance

    def __call__(self, face: cq.Face) -> cq.Workplane:
        v_zaxis = face.normalAt()

        selected_plane_normal = None
        for plane_normal in self.__plane_normals:
            plane_normal_projection = plane_normal.dot(v_zaxis)
            if (1 - abs(plane_normal_projection)) > self.__tolerance:
                selected_plane_normal = plane_normal
                break
        if selected_plane_normal is None:
            raise ValueError(
                "All plane normals are too close to face normal %s" % v_zaxis
            )

        v_xaxis = selected_plane_normal.cross(v_zaxis)

        return _create_workplane(face.Center(), v_xaxis, v_zaxis)


T = TypeVar("T")


class XAxisClosestTo:
    """
    Selects face center of origin at face center 
    (`Face.Center()`) and face normal at face 
    center as Z axis.

    Selects one of provided vectors with the smallest
    projection on face normal and choses normalized
    projection of that vector onto face plane as X axis.

    If two or more vectors have the same and smallest
    projection on face normal the one that comes first
    in provided list is chosen.

    User-provided vectors do not
    have to be linearly independent but their span
    (linear hull) should be all 3D vector space
    for XAxisInPlane to work on arbitrary faces.
    In some cases this requirement can be relaxed.
    """

    def __init__(self, candidate_vectors: List[cq.Vector], tolerance: float = 1e-3):

        self.__tolerance = tolerance
        self.__weighted_candidate_vectors = [
            (i, x.normalized()) for i, x in enumerate(candidate_vectors)
        ]

    def __get_best_candidate(
        self,
        objectlist: List[T],
        key_selector: Callable[[T], float],
        cluster_sort_key: Callable[[T], float],
    ):
        # idea borrowed from
        # https://github.com/CadQuery/cadquery/blob/a71a93ea274089ddbd48dbbd84d84710fc82a432/cadquery/selectors.py#L343
        key_and_obj = []
        for obj in objectlist:
            key_and_obj.append((key_selector(obj), obj))
        key_and_obj.sort(key=lambda x: x[0])

        first_cluster = []
        start = key_and_obj[0][0]
        for key, obj in key_and_obj:
            if abs(key - start) <= self.__tolerance:
                first_cluster.append(obj)
            else:
                break
        first_cluster.sort(key=cluster_sort_key)

        return first_cluster[0]

    def __call__(self, face: cq.Face) -> cq.Workplane:
        v_zaxis = face.normalAt()

        # Choosing user-specified vector with minimum
        # face normal projection. If multiple vectors
        # have the same projection, the one that
        # comes first in the list is chosen
        best_xax_candidate = self.__get_best_candidate(
            self.__weighted_candidate_vectors,
            lambda x: abs(x[1].dot(v_zaxis)),
            lambda x: x[0],
        )[1]

        # projecting onto face plane and normalizing
        v_xaxis = (
            best_xax_candidate - v_zaxis.multiply(best_xax_candidate.dot(v_zaxis))
        ).normalized()

        return _create_workplane(face.Center(), v_xaxis, v_zaxis)


cq.Workplane.applyToEachFace = applyToEachFace
