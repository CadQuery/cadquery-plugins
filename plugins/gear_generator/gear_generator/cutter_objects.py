"""
This module stores functions that are used by the make_XXX_gear functions but are not intended to be used by the final user
"""

import cadquery as cq
from math import *
from .helpers import *

def make_rack_tooth_gap(self, m, b, alpha = 20, helix_angle = None):
    """
    Creates a solid which represents the gap between the teeth of the rack gear

    Parameters
    ----------
    m : float
        Crown gear modulus    
    b : float
        Tooth width
    alpha : float
        Pressure angle in degrees, industry standard is 20°
    helix_angle : float
        Helix angle in degrees to create a helical rack gear

    Returns
    -------
    cq.Workplane
        Returns the tooth gap solid in a cq.Workplane using eachpoint method
    """
    p = pi*m
    alpha = radians(alpha)
    
    A = (-2.25*m*sin(alpha)-(p/2 - 2*m*sin(alpha)),0)
    B = (-(p/2 - 2*m*sin(alpha)), -2.25*m*cos(alpha))
    C = (B[0] + (p/2 - 2*m*sin(alpha)), -2.25*m*cos(alpha))
    D = (C[0] + 2.25*m*sin(alpha), 0)
    tooth_wire = (cq.Workplane("XY").polyline([A,B,C,D])).close()
    if helix_angle is None:
        tooth = tooth_wire.extrude(b)
    else:
        helix_angle = radians(helix_angle)
        tooth = tooth_wire.center(tan(helix_angle)*b, 0).workplane(offset=b).polyline([A,B,C,D]).close().loft()
    return self.eachpoint(lambda loc: tooth.val().located(loc), True)

def make_bevel_tooth_gap_wire(self, Z_W, m, phi, r_a, r_f, r_base):
    """
    Creates the bevel tooth gap wire that will be lofted to a vertex to make the cutter object

    Parameters
    ----------
    Z_W : float
        Z position of the top of the complementary cone in the coord system which as it's origin at the bevel gear cone top point
    m : float
        Bevel gear modulus  
    phi : float
        Complementary cone angle in radians
    r_a : float
        Associated virtual spur gear top radius
    r_f : float
        Associated virtual spur gear root radius
    r_base : float
        Associated virtual spur gear base radius 

    Returns
    -------
    cq.Workplane
        Returns a wire in a cq.Workplane that defines the tooth gap cross section at the bevel outer radius
    """
    STOP = 2*sqrt((r_a/r_base)**2 - 1) # 2* To be sure to have extra working room
    #right side
    right = (cq.Workplane("XY", origin=(0,0,Z_W)).transformed(rotate=(-pi*m,-90+degrees(phi),0))
            .tag("baseplane")
            .parametricCurve(involute(r_base), N=8, stop=STOP, makeWire=False))           
    bot_right = right.moveTo(r_f,0).hLine(r_base-r_f)
    #left side           
    left = (cq.Workplane("XY", origin=(0,0,Z_W)).transformed(rotate=(pi*m,-90+degrees(phi),0))
            .moveTo(r_f,0)
            .hLine(r_base-r_f)
            .parametricCurve(involute(r_base, sign=-1), N=8, stop=STOP, makeWire=False))             
    bot_left = left.moveTo(r_f,0).hLine(r_base-r_f)
    #Getting points to close the wire
    pt_top_right = right.vertices(">X").val()
    pt_bot_right = bot_right.vertices("<X").val()
    pt_top_left = left.vertices(">X").val()
    pt_bot_left = bot_left.vertices("<X").val()
    pt_bot_mid = cq.Workplane("XY", origin=(0,0,Z_W)).transformed(rotate=(0,-90+degrees(phi),0)).pushPoints([(r_f,0)]).val()
    #TODO : make top an arc instead of a straight line
    top = cq.Edge.makeLine(cq.Vector(pt_top_right.toTuple()), cq.Vector(pt_top_left.toTuple()))
    bot = cq.Edge.makeThreePointArc(cq.Vector(pt_bot_left.toTuple()),
                                    cq.Vector(pt_bot_mid.toTuple()),
                                    cq.Vector(pt_bot_right.toTuple()))
    wire = cq.Wire.assembleEdges([bot_right.val(), right.val(), top, left.val(), bot_left.val(), bot])
    return self.eachpoint(lambda loc: wire.located(loc), True)

def make_crown_gear_tooth_gap(self, m, r, alpha = 20):
    """
    Create a solid which represents the gap between the teeth of the crown gear

    Parameters
    ----------
    m : float
        Crown gear modulus
    r : float
        Crown gear outer radius
    alpha : float
        Pressure angle in degrees, industry standard is 20°

    Returns
    -------
    cq.Workplane
        Returns the tooth gap solid in a cq.Workplane using eachpoint method
    """

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

cq.Workplane.make_rack_tooth_gap = make_rack_tooth_gap
cq.Workplane.make_crown_gear_tooth_gap = make_crown_gear_tooth_gap
cq.Workplane.make_bevel_tooth_gap_wire = make_bevel_tooth_gap_wire