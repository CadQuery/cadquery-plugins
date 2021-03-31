import pytest
import math
import cadquery as cq
import plugins.heatserts.heatserts as heatsert_module


@pytest.fixture
def box():
    return cq.Workplane().box(20, 20, 20)


def test_heatsert_makes_a_hole(box):

    box_with_hole = box.faces(">Z").workplane().heatsert("M6")
    assert box.faces().size() < box_with_hole.faces().size()


def test_heatsert_basic_dims(box):

    box_volume = box.val().Volume()

    for size in ["M6", "M5", "M4", "M3"]:
        dims = heatsert_module.heatsert_dims[size]
        box_with_hole = box.faces(">X").workplane().heatsert(size)
        volume_cut_out = box_volume - box_with_hole.val().Volume()
        heatsert_volume = math.pi * (dims.diam / 2) ** 2 * dims.depth
        assert volume_cut_out > heatsert_volume - 0.1


def test_heatsert_bolt_clear(box):

    size = "M3"
    _, depth, bolt_diam = heatsert_module.heatsert_dims[size]
    bolt_clear = 15

    short_hole = box.faces(">Y").workplane().heatsert(size)
    long_hole = box.faces(">Y").workplane().heatsert(size, bolt_clear=bolt_clear)

    extra_hole_volume = math.pi * (bolt_diam * 1.2 / 2) ** 2 * (bolt_clear - depth)
    assert (
        short_hole.val().Volume() - long_hole.val().Volume() > extra_hole_volume - 0.1
    )


def test_heatsert_pattern():

    plate_w_heatserts = (
        cq.Workplane()
        .box(100, 100, 10)
        .faces(">Z")
        .wires()
        .toPending()
        .offset2D(-5, forConstruction=True)
        .vertices()
        .heatsert("M4")
    )

    # should be able to select 4 circles on the top face
    selected = plate_w_heatserts.faces(">Z").edges("%CIRCLE")
    assert selected.size() == 4
