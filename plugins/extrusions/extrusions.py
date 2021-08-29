from typing import TypeVar, Union, Tuple
import importlib.resources
import cadquery as cq
from cadquery.occ_impl import importers
from cadquery.occ_impl.geom import Vector, Location
from cadquery.occ_impl.shapes import Face, sortWiresByBuildOrder
import ezdxf

T = TypeVar("T", bound="Workplane")


def _importDXFstream(stream, tol=1e-6, exclude=[]):
    """
    Loads a DXF stream

    :param stream: The path and name of the DXF stream to be imported
    :param tol: The tolerance used for merging edges into wires (default: 1e-6)
    :param exclude: a list of layer names not to import (default: [])
    """

    # normalize layer names to conform the DXF spec
    exclude_lwr = [ex.lower() for ex in exclude]

    dxf = ezdxf.read(stream)
    faces = []

    for name, layer in dxf.modelspace().groupby(dxfattrib="layer").items():
        res = (
            importers._dxf_convert(layer, tol)
            if name.lower() not in exclude_lwr
            else None
        )
        if res:
            wire_sets = sortWiresByBuildOrder(res)
            for wire_set in wire_sets:
                faces.append(Face.makeFromWires(wire_set[0], wire_set[1:]))
    return faces


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
    ref = (
        importlib.resources.files("plugins.extrusions")
        .joinpath("profiles/")
        .joinpath(profile)
    )
    with ref.open() as stream:
        faces = _importDXFstream(stream)

    PROFILE = cq.Workplane("XY").newObject(faces).wires()

    if isinstance(centered, bool):
        centered = (centered, centered, centered)

    offset = Vector()
    if not centered[0]:
        offset += Vector(size[0] / 2, 0, 0)
    if not centered[1]:
        offset += Vector(0, size[1] / 2, 0)
    if centered[2]:
        offset += Vector(0, 0, -length / 2)

    extrusion = PROFILE.toPending()._extrude(length).move(Location(offset))
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
