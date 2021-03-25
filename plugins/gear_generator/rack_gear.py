import cadquery as cq
from math import *

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

def make_rack_gear(self, m, b, length, clearance, alpha = 20, helix_angle = None):
    """
    Creates a rack gear 

    Parameters
    ----------
    m : float
        Crown gear modulus     
    b : float
        Tooth width / rack gear width
    length : float
        Length of the rack gear
    alpha : float
        Pressure angle in degrees, industry standard is 20°
    helix_angle : float
        Helix angle in degrees to create a helical rack gear

    Returns
    -------
    cq.Workplane
        Returns the rack gear solid in a cq.Workplane using eachpoint method
    """
    p = pi*m 
    z = int(length // p)+1
    height = 2.25*m*cos(alpha) + clearance
    points = [(p*i,0) for i in range(z)] + [(-p*i,0) for i in range(z)]
    teeths = cq.Workplane("XY").pushPoints(points).make_rack_tooth_gap(m, b, alpha, helix_angle)
    base = cq.Workplane("ZY").rect(b, -height, centered=False).extrude(-length)
    gear = base.cut(teeths)
    return self.eachpoint(lambda loc: gear.located(loc), True)



cq.Workplane.make_rack_tooth_gap = make_rack_tooth_gap
cq.Workplane.make_rack_gear = make_rack_gear





test = make_rack_gear(1, 20, 60, 5, helix_angle=30)

show_object(test)

