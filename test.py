import cadquery as cq
import lib
from plugins.extrusions import extrusions
from cadquery.occ_impl.geom import Vector, Location

#def extrusionOZ(len):
#    EXTRUSION_2020_PROFILE = cq.importers.importDXF("lib/dxf/serie-20-2020_1.dxf").wires()
#    return EXTRUSION_2020_PROFILE.toPending().extrude(len)


cube = (cq.Workplane("YZ")
          .box(20, 10, 10)
          .edges("|Z")
          .fillet(0.125)
          #.rotateZ(45)
          )

eZ = extrusions.e2020(50, centered=not True)
#eOZ = (
#    cq.Assembly()
#    .add(extrusion.e2020(5, centered=True))
#    .add(cube)
#)

#log(cube.plane.zDir)
#log(eZ.plane.zDir)
show_object(cube)
show_object(eZ)
#show_object(eOZ, name='eOZ')
#eOZ.save('eOZ.step')
#print(eOZ)
