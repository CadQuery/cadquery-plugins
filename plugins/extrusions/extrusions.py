import cadquery as cq
from cadquery.occ_impl import importers
from cadquery.occ_impl.geom import Vector, Location
from cadquery.occ_impl.shapes import Face, sortWiresByBuildOrder
import ezdxf
import importlib.resources
from typing import TypeVar, Union, Tuple

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
        res = importers._dxf_convert(layer, tol) if name.lower() not in exclude_lwr else None
        if res:
            wire_sets = sortWiresByBuildOrder(res)
            for wire_set in wire_sets:
                faces.append(Face.makeFromWires(wire_set[0], wire_set[1:]))
    return faces


def _extrusion(
    size: Tuple[float, float],
    profile,
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]]
):
    ref = importlib.resources.files('plugins.extrusions').joinpath('profiles/').joinpath(profile)
    with ref.open() as fp:
        faces = _importDXFstream(fp)

    PROFILE =  cq.Workplane("XY").newObject(faces).wires()

    if isinstance(centered, bool):
        centered = (centered, centered, centered)

    offset = Vector()
    if not centered[0]:
        offset += Vector(size[0] / 2, 0, 0)
    if not centered[1]:
        offset += Vector(0, size[1] / 2, 0)
    if centered[2]:
        offset += Vector(0, 0, -len / 2)

    e = PROFILE.toPending()._extrude(len).move(Location(offset))
    return cq.Workplane("XY").newObject([e])


def e2020(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([20, 20], 'e2020.dxf', len, centered)

def e2040(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([40, 20], 'e2040.dxf', len, centered)

def e2080(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([80, 20], 'e2080.dxf', len, centered)

def e4040(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([40, 40], 'e4040.dxf', len, centered)

def v2020(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([20, 20], 'v2020.dxf', len, centered)

def v2040(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([40, 20], 'v2040.dxf', len, centered)

def v4040(
    len: float,
    centered: Union[bool, Tuple[bool, bool, bool]] = True
):
    return _extrusion([40, 40], 'v4040.dxf', len, centered)
