import cadquery as cq
from math import *





def make_crown_gear_tooth_gap(self, m, r, b, alpha = 20):

    alpha = radians(alpha)
    pitch = pi*m
    P = (pitch/4 , 0)
    A = (r, P[0] + m*sin(alpha),  m*cos(alpha))
    B = (r, P[0] - 1.25*m*sin(alpha),  -1.25*m*cos(alpha))
    C = (r, -P[0] + 1.25*m*sin(alpha),  -1.25*m*cos(alpha))
    D = (r, -P[0] - m*sin(alpha),  m*cos(alpha))

    edge = cq.Workplane("XZ", origin=(0,0,-1.25*m*cos(alpha))).line(0,2.25*m*cos(alpha))
    U = edge.val().endPoint()
    V = edge.val().startPoint()
    profile = cq.Workplane("XY").polyline([A,B,C,D,A]).wire()
    faces_to_shell = [cq.Face.makeFromWires(profile.val())]
    shell_wires = []
    #top_face
    shell_wires.append(
        cq.Wire.assembleEdges([
            cq.Edge.makeLine(cq.Vector(A),
                            cq.Vector(D)),
            cq.Edge.makeLine(cq.Vector(D),
                            cq.Vector(U)),
            cq.Edge.makeLine(cq.Vector(U),
                            cq.Vector(A)),                                                 
        ]))
    shell_wires.append(
        cq.Wire.assembleEdges([
            cq.Edge.makeLine(cq.Vector(A),
                            cq.Vector(U)),
            cq.Edge.makeLine(cq.Vector(U),
                            cq.Vector(V)),
            cq.Edge.makeLine(cq.Vector(V),
                            cq.Vector(B)),                                                 
            cq.Edge.makeLine(cq.Vector(B),
                            cq.Vector(A)),                                                 
        ]))
    shell_wires.append(
        cq.Wire.assembleEdges([
            cq.Edge.makeLine(cq.Vector(B),
                            cq.Vector(V)),
            cq.Edge.makeLine(cq.Vector(V),
                            cq.Vector(C)),
            cq.Edge.makeLine(cq.Vector(C),
                            cq.Vector(B)),                                                 
        ]))
    shell_wires.append(
        cq.Wire.assembleEdges([
            cq.Edge.makeLine(cq.Vector(C),
                            cq.Vector(V)),
            cq.Edge.makeLine(cq.Vector(V),
                            cq.Vector(U)),
            cq.Edge.makeLine(cq.Vector(U),
                            cq.Vector(D)),                                                 
            cq.Edge.makeLine(cq.Vector(D),
                            cq.Vector(C)),                                                 
        ]))

    U = edge.val().endPoint()
    V = edge.val().startPoint()

    for wire in shell_wires:
        faces_to_shell.append(cq.Workplane("XY").interpPlate(cq.Workplane("XY", obj=wire)).val())
    shell = cq.Shell.makeShell(faces_to_shell)
    tooth = cq.Solid.makeSolid(shell)
    tooth = tooth.translate(cq.Vector(0,0,-m*cos(alpha)))

    return self.eachpoint(lambda loc: tooth.located(loc), True)


def make_crown_gear(self, m, z, b, alpha = 20, clearance = None):
    r = m*z/2
    if clearance is None:
        clearance = 1.7*m
    base =  cq.Workplane("XY").tag("base").circle(r).extrude(-2.25*m-clearance)

    teeths = cq.Workplane("XY").polarArray(0,0,360,z)._make_crown_gear_tooth_gap(m, r, b, alpha)
    teeths = cq.Compound.makeCompound(teeths.vals())
    gear = base.cut(teeths)
    gear = gear.cut(cq.Workplane("XY", origin=(0,0,-2.25*m)).circle(r-b).extrude(2.25*m))

    return gear


 
cq.Workplane._make_crown_gear_tooth_gap = make_crown_gear_tooth_gap
cq.Workplane.make_crown_gear = make_crown_gear

tooth = cq.Workplane("XY").make_crown_gear(3,20,20)

show_object(tooth)















# base = cq.Workplane("YZ").transformed(offset=(0,0,r_p)).rect(10,10)
# base = cq.Workplane("YZ").transformed(offset=(0,0,r_p)).moveTo(-2,0).line(4,0).line(4,10).line(-12,0).close()

# show_object(edge)

# show_object(base.extrude(-20, taper=3))

"""
# show_object(MakeWeirdPrism(wire,edge))
v_edge = cq.Workplane("YZ").vLine(10).wire()
o_edge = cq.Workplane("YZ", origin=(10,0,0)).transformed(rotate=(0,0,30)).vLine(10).wire()
# wire = cq.Workplane("XY").rect(5,5).workplane(offset=10).transformed(rotate=(0,0,45)).rect(5,5).wire()
edge_wire = cq.Workplane("XY").polyline(
    [(-7.0, -7.0), (7.0, -7.0), (7.0, 7.0), (-7.0, 7.0)])

edge_wire = edge_wire.add(
    cq.Workplane("YZ")
    .workplane()
    .transformed(offset=cq.Vector(0, 0, -7), rotate=cq.Vector(45, 0, 0))
    .spline([(-7.0, 0.0), (3, -3), (7.0, 0.0)])
)
wire = cq.Workplane("YZ").interpPlate(edge_wire)

show_object(wire)"""