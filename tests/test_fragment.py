import cadquery as cq
import plugins.fragment.fragment as fragment

def test_fragment_volume():

    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate = plate.fragment(plate2)

    assert (abs(plate.vals()[0].Solids()[1].Volume()) - 125.0) < 1e-6
