import cadquery as cq
import plugins.fragment.fragment as fragment


def test_fragment_volume():

    plate = cq.Workplane("XY").box(20, 20, 20)
    plate2 = cq.Workplane("XY").box(10, 10, 10).translate((10, 10, 10))
    plate = plate.fragment(plate2)
    plate_glue = plate.fragment(plate2, glue=True)
    plate_tol = plate.fragment(plate2, tol=1e-6)
    plate_solid = plate.fragment(plate2.val())

    plate3 = cq.Workplane("XY").box(2, 2, 2).add(plate2)
    vals = [o.vals()[0] for o in plate3.all()] 
    plate3  = cq.Compound.makeCompound(vals)
    plate_compound = plate.fragment(plate3)
    
    assert len(plate_solid.vals()[0].Solids())==3
    assert len(plate_compound.vals()[0].Solids())==4
    assert len(plate_tol.vals()[0].Solids())==3
    assert len(plate_glue.vals()[0].Solids())==3
    assert len(plate.vals()[0].Solids())==3
    assert (abs(plate.vals()[0].Solids()[0].Volume()) - 7875.) < 1e-6
    assert (abs(plate.vals()[0].Solids()[1].Volume()) - 125.) < 1e-6   
    assert (abs(plate.vals()[0].Solids()[2].Volume()) - 875.) < 1e-6
