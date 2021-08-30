from typing import TypeVar, Union, Tuple
#import importlib.resources
import pkg_resources
import cadquery as cq
from cadquery.occ_impl import importers
from cadquery.occ_impl.geom import Vector, Location

T = TypeVar("T", bound="Workplane")


def _extrusion(
    size: Tuple[float, float],
    profile,
    length: float,
    centered: Union[bool, Tuple[bool, bool, bool]],
):
    """
    Return an extrusion with the specified profile and length

    :param size: size of the extrusion, used for centering
    :param profile: filename of the extrusion's profile
    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    #file = (
    #    importlib.resources.files("plugins.extrusions")
    #    .joinpath("profiles/")
    #    .joinpath(profile)
    #)
    file = pkg_resources.resource_filename(__name__, "profiles/" + profile)
    profile = importers.importDXF(file).wires()

    if isinstance(centered, bool):
        centered = (centered, centered, centered)

    offset = Vector(
        0 if centered[0] else size[0] / 2,
        0 if centered[1] else size[0] / 2,
        -length / 2 if centered[2] else 0,
    )

    extrusion = profile.toPending()._extrude(length).move(Location(offset))
    return cq.Workplane("XY").newObject([extrusion])


def e2020(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 2020 extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([20, 20], "e2020.dxf", length, centered)


def e2040(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 2040 extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([40, 20], "e2040.dxf", length, centered)


def e2080(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 2080 extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([80, 20], "e2080.dxf", length, centered)


def e4040(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 4040 extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([40, 40], "e4040.dxf", length, centered)


def v2020(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 2020 v-slot extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([20, 20], "v2020.dxf", length, centered)


def v2040(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 2040 v-slot extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([40, 20], "v2040.dxf", length, centered)


def v4040(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = True):
    """
    Return a 4040 v-slot extrusion with the specified length

    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """
    return _extrusion([40, 40], "v4040.dxf", length, centered)
