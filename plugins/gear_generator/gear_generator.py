import cadquery as cq
from math import pi, cos, sin, tan, sqrt, degrees, radians, atan2, atan, acos
from helpers import involute, test_bevel_parameters
from cutter_objects import make_bevel_tooth_gap_wire, make_rack_tooth_gap, make_crown_gear_tooth_gap
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections



def make_bevel_gear(self, m, z, b, delta, alpha = 20, clearance = None):
    """
    Creates a bevel gear

    Parameters
    ----------
    m : float
        Crown gear modulus
    z : int
        Number of teeth       
    b : float
        Tooth width
    delta : float
        Cone angle in degrees
    alpha : float
        Pressure angle in degrees, industry standard is 20°
    clearance : float
        Spacing after teeth root to add some material below the teeth
        Below a (half) bevel gear sketch to understand what is the clearance
              ____
             /   / } addendum
        ____/___/  } dedendum
        _______/   } clearance (the length of the tilted bar)                

    Returns
    -------
    cq.Workplane
        Returns the bevel gear solid in a cq.Workplane using eachpoint method
    """

    # PARAMETERS
    delta = radians(delta) # cone angle
    phi = pi/2 - delta # complementary cone angle
    r = m*z/2 # pitch radius
    r_inner = r-b*sin(delta) #pitch radius inner radius
    r_equiv_outer = r/sin(phi) #pitch radius of the associated virtual spur gear
    r_base_equiv = r_equiv_outer*cos(radians(alpha)) #base radius of the associated virtual spur gear
    r_f_equiv = (r - 1.25*m*cos(delta))/sin(phi) #root radius of the associated virtual spur gear
    r_a_equiv = (r + m*cos(delta))/sin(phi) #top radius of the associated virtual spur gear
    h_f = 1.25*m # dedendum
    h_a = m # addendum
    # Z positions of outer and inner pitch radius and top of complementary cone
    Z_P = -r/tan(delta) 
    Z_P_inner = - r_inner/tan(delta)
    Z_W =  (Z_P - r/tan(phi))*1.0000001 # This allow for the tooth gap wire to be slightly shifted otherwise leads to failing cut operation
    if clearance is None:
        clearance = 0.2*r
    # Test if input parameters make a valid gear
    
    test_bevel_parameters(m, z, b, r_inner, delta, alpha, phi, clearance, r_f_equiv, r_base_equiv) 

    #Definition of bevel half cross section points
    A = (r + h_a*cos(delta), 0, Z_P + h_a*sin(delta))
    B = (r - h_f*cos(delta), 0, Z_P - h_f*sin(delta))
    C = (r - clearance*cos(delta), 0, Z_P - clearance*sin(delta))
    D = (0, 0, C[2])
    H = (r_inner + h_a*cos(delta), 0, Z_P_inner + h_a*sin(delta))
    G = (r_inner - h_f*cos(delta), 0, Z_P_inner - h_f*sin(delta))
    F = (r_inner - clearance*cos(delta), 0, Z_P_inner - clearance*sin(delta))
    E = (0, 0, F[2])

    #Creation of the half cross section
    edges = []
    edges.append(cq.Edge.makeLine(cq.Vector(A), cq.Vector (B)))
    edges.append(cq.Edge.makeLine(cq.Vector(B), cq.Vector (C)))
    edges.append(cq.Edge.makeLine(cq.Vector(C), cq.Vector (D)))
    edges.append(cq.Edge.makeLine(cq.Vector(D), cq.Vector (E)))
    edges.append(cq.Edge.makeLine(cq.Vector(E), cq.Vector (F)))
    edges.append(cq.Edge.makeLine(cq.Vector(F), cq.Vector (G)))
    edges.append(cq.Edge.makeLine(cq.Vector(G), cq.Vector (H)))
    edges.append(cq.Edge.makeLine(cq.Vector(H), cq.Vector (A)))
    cross_sec = cq.Wire.assembleEdges(edges)
    #Making base solid
    base = cq.Solid.revolve(cross_sec,[],360, cq.Vector(0,0,0), cq.Vector(0,0,1))  

    tooth_gap = make_bevel_tooth_gap_wire(Z_W, m, phi, r_a_equiv, r_f_equiv, r_base_equiv)

    builder = BRepOffsetAPI_ThruSections(True,False) #Builder to create loft to vertex
    builder.AddWire(tooth_gap.wrapped)
    builder.AddVertex(cq.Vertex.makeVertex(0,0,0).wrapped)
    cutter = cq.Workplane(obj=cq.Shape.cast(builder.Shape())) #cutter solid
    #Make a compound of cutters
    cutters = []
    for i in range(z):
        angle = 360/z*i
        cutters.append(cutter.rotate((0,0,0),(0,0,1),angle).val())
    final_cutter =  cq.Compound.makeCompound(cutters)
    gear = base.cut(final_cutter)
    return self.eachpoint(lambda loc: gear.located(loc), True)

def make_bevel_gear_system(m, z1, z2, b, alpha=20, clearance = None, compound = False):
    """
    Creates a bevel gear system made of two bevel gears

    Parameters
    ----------
    m : float
        Bevel gears modulus (to be able to mesh they need the same modulus)
    z1 : int
        Number of teeth of the first bevel gear     
    z2 : int
        Number of teeth of the second bevel gear          
    b : float
        Tooth width
    delta : float
        Cone angle in degrees
    alpha : float
        Pressure angle in degrees, industry standard is 20°
    clearance : float
        Spacing after teeth root to add some material below the teeth
        Below a (half) bevel gear sketch to understand what is the clearance
              ____
             /   / } addendum
        ____/___/  } dedendum
        _______/   } clearance (the length of the tilted bar)                

    Returns
    -------
    tuple 
        Returns a 2-tuple with the two gear solid in a cq.Workplane
    """
    delta_1 = degrees(atan2(z2,z1))
    delta_2 = degrees(atan2(z1,z2))
    gear1 = cq.Workplane("XY").make_bevel_gear(m, z, b, delta_1, alpha = alpha, clearance = clearance)                                
    gear2 = cq.Workplane("YZ").make_bevel_gear(m, z, b, delta_2, alpha = alpha, clearance = clearance)
    if compound:
        return cq.Compound.makeCompound([gear1.val(), gear2.val()])
    else:
        return gear1, gear2

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
        Pressure angle in degrees, industry standard is 20°
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
    inv = lambda a: tan(a) - a
    
    # angles of interest
    alpha_inv = inv(alpha)
    alpha_tip = acos(r_base/r_a)
    alpha_tip_inv = inv(alpha_tip)
    
    a = 90/z+degrees(alpha_inv)
    a2 = 90/z++degrees(alpha_inv)-degrees(alpha_tip_inv)
    a3 = 360/z-a
    
    # construct all the profiles
    right = (
        cq.Workplane()
        .transformed(rotate=(0,0,a))
        .parametricCurve(involute(r_base,-1), start=r_base, stop = r_a, makeWire=False, N=8)
        .val()
    )
    
    left = (
        cq.Workplane()
        .transformed(rotate=(0,0,-a))
        .parametricCurve(involute(r_base), start=r_base, stop = r_a, makeWire=False, N=8)
        .val()
    )

    top = cq.Edge.makeCircle(r_a,angle1=-a2, angle2=a2)
    bottom = cq.Edge.makeCircle(r_f, angle1=-a3, angle2=-a)
    
    side = cq.Edge.makeLine( cq.Vector(r_f,0), cq.Vector(r_base,0))
    side1 = side.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -a)
    side2 = side.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -a3)
    
    # single tooth profile
    profile = cq.Wire.assembleEdges([left,top,right,side1,bottom,side2])
    if not raw:
        profile = profile.fillet2D(0.25*m, profile.Vertices()[-3:-1])

    # complete gear
    gear = (
        cq.Workplane()
        .polarArray(0,0,360,z)
        .each(lambda loc: profile.located(loc))
        .consolidateWires()
    )

    return self.eachpoint(lambda loc: gear.located(loc), True)

def make_crown_gear(self, m, z, b, alpha = 20, clearance = None):
    """
    Create a crown gear (which is the same as a rack gear made circular, also called face gear)

    Parameters
    ----------
    m : float
        Crown gear modulus
    z : int
        Number of teeth       
    b : float
        Tooth width
    alpha : float
        Pressure angle in degrees, industry standard is 20°
    clearance : float
        The height of the cylinder under the teeth
        If None, clearance is equal to 1.7*m

    Returns
    -------
    cq.Workplane
        Returns the crown gear solid in a cq.Workplane using eachpoint method
    """
    r = m*z/2
    if clearance is None:
        clearance = 1.7*m
    base =  cq.Workplane("XY").tag("base").circle(r).extrude(-2.25*m-clearance)

    teeths = cq.Workplane("XY").polarArray(0,0,360,z)._make_crown_gear_tooth_gap(m, r, alpha)
    teeths = cq.Compound.makeCompound(teeths.vals())
    gear = base.cut(teeths)
    gear = gear.cut(cq.Workplane("XY", origin=(0,0,-2.25*m)).circle(r-b).extrude(2.25*m))

    return self.eachpoint(lambda loc: gear.located(loc), True)

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

# Adds the functions to cq.Workplane class

cq.Workplane.make_gear = make_gear  
cq.Workplane.make_bevel_gear = make_bevel_gear  
cq.Workplane.make_bevel_gear_system = make_bevel_gear_system  
cq.Workplane.make_rack_gear = make_rack_gear  
cq.Workplane.make_crown_gear = make_crown_gear  