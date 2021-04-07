import pytest
import math
import importlib
import itertools
import cadquery as cq
import plugins.heatserts.heatserts as heatsert_module
import numbers


@pytest.fixture
def box():
    return cq.Workplane().box(20, 20, 20)


possible_chamfer_vals = [0.1, 0.5, 2]


@pytest.mark.parametrize("size", heatsert_module.heatsert_dims.keys())
class TestSizes:
    def test_heatsert_makes_a_hole(self, box, size):

        box_with_hole = box.faces(">Z").workplane().heatsert(size)
        assert box.faces().size() < box_with_hole.faces().size()

    def test_heatsert_basic_dims(self, box, size):

        box_volume = box.val().Volume()

        dims = heatsert_module.heatsert_dims[size]
        box_with_hole = box.faces(">X").workplane().heatsert(size)
        volume_cut_out = box_volume - box_with_hole.val().Volume()
        heatsert_volume = math.pi * (dims.diam / 2) ** 2 * dims.depth
        assert volume_cut_out > heatsert_volume - 0.1

    def test_heatsert_bolt_clear(self, box, size):

        _, depth, bolt_diam = heatsert_module.heatsert_dims[size]
        bolt_clear = 15

        short_hole = box.faces(">Y").workplane().heatsert(size)
        long_hole = box.faces(">Y").workplane().heatsert(size, bolt_clear=bolt_clear)

        extra_hole_volume = math.pi * (bolt_diam * 1.2 / 2) ** 2 * (bolt_clear - depth)
        assert (
            short_hole.val().Volume() - long_hole.val().Volume()
            > extra_hole_volume - 0.1
        )

    @pytest.mark.parametrize(
        "chamfer_arg",
        possible_chamfer_vals
        + [el for el in itertools.product(possible_chamfer_vals, repeat=2)],
    )
    def test_heatsert_chamfer(self, box, size, chamfer_arg):

        dims = heatsert_module.heatsert_dims[size]

        face_center = box.faces("<Z").val().Center()
        chamfered = box.faces("<Z").workplane().heatsert(size, chamfer=chamfer_arg)
        circles = chamfered.edges("%CIRCLE").vals()
        radii = [c.radius() for c in circles]

        expected_radii = [dims.diam / 2]

        if isinstance(chamfer_arg, numbers.Real):
            chamfer_vals = (chamfer_arg, chamfer_arg)
        else:
            chamfer_vals = chamfer_arg

        expected_radii.append(dims.diam / 2 + chamfer_vals[0])
        for er in expected_radii:
            assert any([abs(er - actual_radius) < 0.001 for actual_radius in radii])

        main_circles = [c for c in circles if abs(c.radius() - dims.diam / 2) < 0.01]
        main_circles_depth = [(c.Center() - face_center).Length for c in main_circles]
        # one of those main circles should be at the chamfer depth from the face
        assert any(
            [abs(chamfer_vals[1] - depth) < 0.01 for depth in main_circles_depth]
        )


@pytest.mark.parametrize("selector1", ["X", "Y", "Z"])
@pytest.mark.parametrize("selector0", [">", "<"])
def test_heatsert_makes_a_hole_with_direction(box, selector0, selector1):

    box_with_hole = box.faces(selector0 + selector1).workplane().heatsert("M5")
    assert box.faces().size() < box_with_hole.faces().size()


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


def test_heatsert_add_size(box):

    heatsert_module.heatsert_dims["M8"] = heatsert_module.dims(
        diam=10, depth=15, bolt_diam=8
    )
    TestSizes.test_heatsert_makes_a_hole(None, box, "M8")
    TestSizes.test_heatsert_basic_dims(None, box, "M8")
    TestSizes.test_heatsert_bolt_clear(None, box, "M8")

    # clean up
    importlib.reload(heatsert_module)
