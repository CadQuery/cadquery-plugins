import cadquery as cq
from cadquery import *
# import gear_generator

def rotate_vector_2D(vector, angle):
    """
    rotate a cq.Vector by angle in radians
    """
    angle = radians(angle)
    x = cos(angle)*vector.x - sin(angle)*vector.y
    y = sin(angle)*vector.x + cos(angle)*vector.y
    return cq.Vector((x,y))

m = 1
z = 20
b = 4
clearance = 4
length = 30
delta = 40

# r = cq.Workplane("XY").make_gear(m,z,b)
# r = cq.Workplane("XY").make_rack_gear(m, b, length, clearance, alpha = 20, helix_angle = None)
# r = cq.Workplane("XY").make_crown_gear(m, z, b, alpha = 20, clearance = None)
# r = cq.Workplane("XY").make_bevel_gear(m, z, b, delta, alpha = 20, clearance = None)

from math import *
def involute(r, sign = 1):
    """
    Defines an involute curve to create the flanks of the involute gears

    Parameters
    ----------
    r : float
        Radius of the involute (for a gear it's the pitch radius)
    sign : positive or negative int
        To draw the involute in positive or negative direction      

    Returns
    -------
    function
        Returns a function to be used in cq.Workplane parametricCurve function
    """
    def curve(t):
        x = r*(cos(t) + t*sin(t))
        y = r*(sin(t) - t*cos(t))
        return x,sign*y
    return curve

def make_gear(self, m, z, b, alpha=20, helix_angle = None, raw = False):
    """
    Creates a spur or helical involute gear 

    Parameters
    ----------
    m : float
        Spur gear modulus
    z : int
        Number of teeth    
    b : float
        Tooth width       
    alpha : float
        Pressure angle in degrees, industry standard is 20�
    helix_angle : float
        Helix angle of the helical gear in degrees
        If None creates a spur gear, if specified create a helical gear
    raw : bool
        False : Adds filleting a the root teeth edges            
        True : Left the gear with no filleting          

    Returns
    -------
    cq.Workplane  
        Returns the gear solid in a cq.Workplane using eachpoint method
    """
    
    alpha = radians(alpha)

    # radii
    r_p = m*z/2
    r_a = r_p + m
    r_base = r_p*cos(alpha)
    r_f = r_p - 1.25*m
    p = pi * m 
    inv = lambda a: tan(a) - a
    
    # angles of interest
    alpha_inv = inv(alpha)
    alpha_tip = acos(r_base/r_a)
    alpha_tip_inv = inv(alpha_tip)
    
    a = 90/z+degrees(alpha_inv)
    a2 = 90/z+degrees(alpha_inv)-degrees(alpha_tip_inv)
    STOP = sqrt((r_a/r_base)**2 - 1) 
    # construct all the profiles
    left = (
        cq.Workplane()
        .transformed(rotate=(0,0,a))
        .parametricCurve(involute(r_base,-1), start=0, stop = STOP, makeWire=False, N=8)
        .val()
    )
    
    right = (
        cq.Workplane()
        .transformed(rotate=(0,0,-a))
        .parametricCurve(involute(r_base), start=0, stop = STOP, makeWire=False, N=8)
        .val()
    )

    top = cq.Edge.makeCircle(r_a,angle1=-a2, angle2=a2)

    p0 = left.startPoint()
    p1 = right.startPoint()  
    side0 = cq.Workplane(origin=p0.toTuple()).hLine(r_f-r_base).val()
    side1 = cq.Workplane(origin=p1.toTuple()).hLine(r_f-r_base).val()
    side2 = side0.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -360/z)

    p_bot_left = side1.endPoint()
    p_bot_right = rotate_vector_2D(side0.endPoint(), -360/z)

    bottom = cq.Workplane().moveTo(p_bot_left.x, p_bot_left.y).radiusArc(p_bot_right,r_f).val()

    # single tooth profile
    profile = cq.Wire.assembleEdges([left,top,right,side1,bottom, side2])
    # return profile
    if not raw:
        profile = profile.fillet2D(0.25*m, profile.Vertices()[-3:-1])
    # complete gear
    gear = (
        cq.Workplane()
        .polarArray(0,0,360,z)
        .each(lambda loc: profile.located(loc))
        .consolidateWires()
    )
    if helix_angle is None:
        gear = gear.extrude(b)
    else:
        gear = gear.twistExtrude(b, helix_angle)
    return self.eachpoint(lambda loc: gear.val().located(loc), True)



cq.Workplane.make_gear = make_gear
r = cq.Workplane("XY").make_gear(m,z,2*b, helix_angle = 20)



