import cadquery as cq
import plugins.fragment.fragment as fragment


def test_fragment_volume():
    """
    Tests if fragment with default arguments and a Workplane as first argument value produces correct number of fragments of expected volumes
    """
    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate = plate.fragment(plate2)

    assert (abs(plate.vals()[0].Solids()[0].Volume()) - 7875.0) < 1e-6
    assert (abs(plate.vals()[0].Solids()[1].Volume()) - 125.0) < 1e-6
    assert (abs(plate.vals()[0].Solids()[2].Volume()) - 875.0) < 1e-6


def test_fragment_glue():
    """
    Tests if 'glue=True' argument of fragment() works as expected
    """
    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate_glue = plate.fragment(plate2, glue=True)

    assert len(plate_glue.vals()[0].Solids()) == 2


def test_fragment_tol():
    """
    Tests if tol argument of fragment() works as expected
    """
    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate_tol = plate.fragment(plate2, tol=1e-6)

    assert len(plate_tol.vals()[0].Solids()) == 3


def test_fragment_solid():
    """
    Tests if fragment method works with Solid passed as first argument value
    """
    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate_solid = plate.fragment(plate2.val())

    assert len(plate_solid.vals()[0].Solids()) == 3


def test_fragment_compound():
    """
    Tests if fragment method works with Compound passed as first argument value
    """
    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate3 = cq.Workplane("XY").box(2, 2, 2).add(plate2)
    vals = [o.vals()[0] for o in plate3.all()]
    plate3 = cq.Compound.makeCompound(vals)
    plate_compound = plate.fragment(plate3)

    assert len(plate_compound.vals()[0].Solids()) == 4
