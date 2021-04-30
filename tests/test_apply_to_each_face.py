import sys

from typing import List

import cadquery as cq
from plugins.apply_to_each_face import (
    apply_to_each_face,
    XAxisInPlane,
    WORLD_AXIS_PLANES_XY_ZX_YZ,
    XAxisClosestTo,
    WORLD_AXIS_UNIT_VECTORS_YXZ,
)


TOLERANCE = 0.0001


def test_x_axis_in_plane_45pyramid_sides():
    rotated_pyramid = (
        cq.Workplane("XY")
        .rect(5, 5)
        .extrude(2, taper=45)
        .rotateAboutCenter((0, 0, 1), 45)
    )

    workplane_selector = XAxisInPlane(WORLD_AXIS_PLANES_XY_ZX_YZ)

    faces = rotated_pyramid.faces("not |Z").vals()

    face_normals = [x.normalAt() for x in faces]

    workplanes = [workplane_selector(x) for x in faces]

    x_axis_vectors = [w.plane.xDir for w in workplanes]

    world_z_vector = cq.Vector(0, 0, 1)

    z_projections = [x.dot(world_z_vector) for x in x_axis_vectors]

    assert all(
        [abs(x) < TOLERANCE for x in z_projections]
    ), f"Non-zero x axis unit vector Z world projection: {z_projections}"

    face_normal_projections = [x.dot(n) for (x, n) in zip(x_axis_vectors, face_normals)]

    assert all(
        [abs(x) < TOLERANCE for x in face_normal_projections]
    ), f"Non-zero x axis unit vector face normal projection: {face_normal_projections}"


def _argmin(lst: List[float]) -> int:
    """
    returns index of min element.
    Don't want to bring in numpy dependency for that
    """
    min_val = sys.float_info.max
    min_idx = -1
    for i, x in enumerate(lst):
        if x < min_val:
            min_idx = i
            min_val = x
    return min_idx


def test_x_axis_closest_to_45pyramid_sides():
    rotated_pyramid = (
        cq.Workplane("XY")
        .rect(5, 5)
        .extrude(2, taper=45)
        .rotateAboutCenter((0, 0, 1), 45)
    )

    workplane_selector = XAxisClosestTo(WORLD_AXIS_UNIT_VECTORS_YXZ)

    faces = rotated_pyramid.faces("not |Z").vals()

    face_normals = [x.normalAt() for x in faces]

    workplanes = [workplane_selector(x) for x in faces]

    x_axis_vectors = [w.plane.xDir for w in workplanes]

    face_normal_projections = [x.dot(n) for (x, n) in zip(x_axis_vectors, face_normals)]

    assert all(
        [abs(x) < TOLERANCE for x in face_normal_projections]
    ), f"Non-zero x axis unit vector face normal projection: {face_normal_projections}"

    world_y = cq.Vector(0, 1, 0)

    true_x_axis_vectors = [
        (world_y - z.multiply(world_y.dot(z))).normalized() for z in face_normals
    ]

    true_x_diff = [
        x.sub(true_x) for x, true_x in zip(x_axis_vectors, true_x_axis_vectors)
    ]

    assert all([x.Length < TOLERANCE for x in true_x_diff]), (
        "Wrong world vector chosen as X axis candidate. "
        + f"True x ax differences: {true_x_diff}"
    )


def test_two_disconnected_cubes_x_axis_in_plane():
    result = (
        cq.Workplane("XY")
        .box(10, 10, 10, centered=(True, True, True))
        .union(
            cq.Workplane("XY").move(15, 0).box(10, 10, 10, centered=(True, True, True))
        )
        .faces()
        .applyToEachFace(
            XAxisInPlane(WORLD_AXIS_PLANES_XY_ZX_YZ),
            lambda wp, face: wp.circle(4).extrude(1),
        )
    )

    # Each cylinder has 3 faces
    # 1 cylinder is created for each face of two cubes
    # each cube has 6 faces
    assert len(result.faces().vals()) == 3 * 6 * 2, "Wrong number of faces"


def test_two_disconnected_cubes_x_axis_closest_to():
    result = (
        cq.Workplane("XY")
        .box(10, 10, 10, centered=(True, True, True))
        .union(
            cq.Workplane("XY").move(15, 0).box(10, 10, 10, centered=(True, True, True))
        )
        .faces()
        .applyToEachFace(
            XAxisClosestTo(WORLD_AXIS_UNIT_VECTORS_YXZ),
            lambda wp, face: wp.circle(4).extrude(1),
        )
    )

    # Each cylinder has 3 faces
    # 1 cylinder is created for each face of two cubes
    # each cube has 6 faces
    assert len(result.faces().vals()) == 3 * 6 * 2, "Wrong number of faces"
