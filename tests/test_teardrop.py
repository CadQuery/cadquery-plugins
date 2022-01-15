import pytest
import cadquery as cq
from plugins.teardrop import teardrop


@pytest.fixture
def box():
    return cq.Workplane().box(8, 20, 20)


def test_teardrop_makes_a_hole(box):
    box_with_hole = box.faces(">X").workplane().teardrop(4).cutThruAll()
    assert box.faces().size() < box_with_hole.faces().size()


def test_teardrop_rotation():
    rad = 4
    r = cq.Workplane("XZ").teardrop(rad, 90,).extrude(5)
    assert r.size() == 1

    # expect vertex of shape pointing in -X
    x1 = r.vertices("<X").val().Center().x
    assert x1 == pytest.approx(-5.65685, rel=1e-3)

    r = cq.Workplane("XZ").teardrop(rad, -90,).extrude(5)
    x2 = r.vertices(">X").val().Center().x
    assert abs(x1 + x2) < 0.001


def test_teardrop_clip():
    r = cq.Workplane("XZ").teardrop(4, 0, 4.1).extrude(5)
    assert r.vertices(">Z").val().Center().z == pytest.approx(4.1, rel=1e-3)


@pytest.mark.parametrize(
    "rad, clipval, reason", [(4, 4 * 2, "less"), (4, -4, "greater")]
)
def test_teardrop_clip_value_illegal(box, rad, clipval, reason):
    with pytest.raises(ValueError, match=fr".* argument must be {reason} than .*"):
        box_with_hole = (
            box.faces(">X").workplane().teardrop(rad, 0, clipval).cutThruAll()
        )
