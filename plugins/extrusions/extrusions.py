"""
Plugin for standard and v-slot aluminium extrusions in a variety of sizes.

Extrusion profiles are derived from Matronics ApS datasheets, eg
http://www.matronics.eu/Data/Longship/Files/Products/vslot-2020_1.DXF

All used datasheets include in their description the text "Can be used for CAD programs"
"""

from typing import Callable, TypeVar, Union, Tuple

# import importlib.resources
import pkg_resources
import cadquery as cq
from cadquery.occ_impl import importers

T = TypeVar("T", bound="Workplane")


def _extrusion(
    size: Tuple[float, float],
    profile_filename: str,
    extrusion_name: str,
) -> Callable:
    """
    Return a function that will in turn generate an extrusion.
    :param size: size of the extrusion, used for centering
    :param profile_filename: filename of the extrusion's profile
    :param extrusion_name: a string that will be inserted into a docstring template and assigned
        to __doc__ on the returned function
    """
    # importlib.resources is favored over pkg_resources, but not yet available in cadquery,
    # see https://setuptools.readthedocs.io/en/latest/pkg_resources.html
    # When importlib. resources is available, following code should be used instead of pkg_resources
    # file = (
    #    importlib.resources.files("plugins.extrusions")
    #    .joinpath("profiles/")
    #    .joinpath(profile_filename)
    # )
    file = pkg_resources.resource_filename(__name__, "profiles/" + profile_filename)
    profile = importers.importDXF(file).wires()
    docstring = f"""
    Return a {extrusion_name} extrusion with the specified length
    :param length: length of the extrusion
    :type length: float > 0
    :param centered: If True, the extrusion will be centered around the reference point.
        If False, the corner of the extrusion will be on the reference point and it will
        extend in the positive x, y and z directions. Can also use a 3-tuple to
        specify centering along each axis.
    """

    def rv(length: float, centered: Union[bool, Tuple[bool, bool, bool]] = False) -> T:
        if isinstance(centered, bool):
            centered = (centered, centered, centered)
        offset = cq.Vector(
            0 if centered[0] else size[0] / 2,
            0 if centered[1] else size[0] / 2,
            -length / 2 if centered[2] else 0,
        )
        extrusion = profile.toPending()._extrude(length).move(cq.Location(offset))
        return cq.Workplane("XY").newObject([extrusion])

    rv.__doc__ = docstring
    return rv


e2020 = _extrusion([20, 20], "e2020.dxf", "2020")
e2040 = _extrusion([40, 20], "e2040.dxf", "2040")
e2080 = _extrusion([80, 20], "e2080.dxf", "2080")
e4040 = _extrusion([40, 40], "e4040.dxf", "4040")
v2020 = _extrusion([20, 20], "v2020.dxf", "2020 v-slot")
v2040 = _extrusion([40, 20], "v2040.dxf", "2040 v-slot")
v4040 = _extrusion([40, 40], "v4040.dxf", "4040 v-slot")
