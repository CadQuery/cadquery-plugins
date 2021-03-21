import cadquery as cq
from math import pi, cos, sin, tan, sqrt, degrees, radians, atan2, atan, acos
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections


def involute(r, sign = 1):
    def curve(t):
        x = r*(cos(t) + t*sin(t))
        y = r*(sin(t) - t*cos(t))
        return x,sign*y
    return curve

def test_bevel_parameters(m, z, b, r_inner, delta, alpha, phi, clearance, r_f_equiv, r_b_equiv):
    """
    Handles all wrong sets of parameters with some feedback for the user rather than the usual "BREP API command not done"
    """
    if z % 2 != 0:
        raise ValueError(f"Number of teeths z must be even, try with {z-1} or {z+1}")
    if r_b_equiv < r_f_equiv:
        raise ValueError(f"Base radius < root radius leads to undercut gear. Undercut gears are not supported.\nTry with different values of parameters m, z or alpha")
    h_f = 1.25*m
    r_f_inner = r_inner - h_f*cos(delta)
    clearance_max = r_f_inner / sin(phi)
    if clearance > clearance_max:
        raise ValueError(f"Too much clearance, for this set of parameters clearance must be <= {round(clearance_max,3)}")



def make_bevel_tooth_gap_wire(Z_W, m, phi, r_a, r_f, r_base):
    """
    Make the tooth gap wire that will be used to cut the base shape
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
    return wire


def make_bevel_gear(self, m, z, b, delta, alpha = 20, clearance = None):
    """
    Make a bevel gear based on the specified parameters
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
    Make a system of bevel gear achieving the required gear ratio defined by:
    GR = z1/z2
    """
    delta_1 = degrees(atan2(z2,z1))
    delta_2 = degrees(atan2(z1,z2))
    gear1 = cq.Workplane("XY").make_bevel_gear(m, z, b, delta_1, alpha = alpha, clearance = clearance)                                
    gear2 = cq.Workplane("YZ").make_bevel_gear(m, z, b, delta_2, alpha = alpha, clearance = clearance)
    if compound:
        return cq.Compound.makeCompound([gear1.val(), gear2.val()])
    else:
        return gear1, gear2

def involute_gear(m, z, alpha=20, shift=0, N=8):
    '''
    See https://khkgears.net/new/gear_knowledge/gear_technical_reference/involute_gear_profile.html
    for math
    '''
    
    alpha = radians(alpha)

    # radii
    r_ref = m*z/2
    r_top = r_ref + m*(1+shift)
    r_base = r_ref*cos(alpha)
    r_d = r_ref - 1.25*m
    
    inv = lambda a: tan(a) - a
    
    # angles of interest
    alpha_inv = inv(alpha)
    alpha_tip = acos(r_base/r_top)
    alpha_tip_inv = inv(alpha_tip)
    
    a = 90/z+degrees(alpha_inv)
    a2 = 90/z++degrees(alpha_inv)-degrees(alpha_tip_inv)
    a3 = 360/z-a
    
    # involute curve (radius based parametrization)
    def involute_curve(r_b,sign=1):
        
        def f(r):
            alpha = sign*acos(r_b/r)
            x = r*cos(tan(alpha) - alpha) 
            y = r*sin(tan(alpha) - alpha)
        
            return x,y
        
        return f
    
    # construct all the profiles
    right = (
        cq.Workplane()
        .transformed(rotate=(0,0,a))
        .parametricCurve(involute_curve(r_base,-1), start=r_base, stop = r_top, makeWire=False, N=N)
        .val()
    )
    
    left = (
        cq.Workplane()
        .transformed(rotate=(0,0,-a))
        .parametricCurve(involute_curve(r_base), start=r_base, stop = r_top, makeWire=False, N=N)
        .val()
    )

    top = cq.Edge.makeCircle(r_top,angle1=-a2, angle2=a2)
    bottom = cq.Edge.makeCircle(r_d, angle1=-a3, angle2=-a)
    
    side = cq.Edge.makeLine( cq.Vector(r_d,0), cq.Vector(r_base,0))
    side1 = side.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -a)
    side2 = side.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -a3)
    
    # single tooth profile
    profile = cq.Wire.assembleEdges([left,top,right,side1,bottom,side2])
    profile = profile.chamfer2D(m/4, profile.Vertices()[-3:-1])

    # complete gear
    res = (
        cq.Workplane()
        .polarArray(0,0,360,z)
        .each(lambda loc: profile.located(loc))
        .consolidateWires()
    )

    return res.val()

m = 1
z = 16
alpha = 20
delta = 45
b = 2 # L/4 <= b <= L/3
# clearance = 2*m

cq.Workplane.make_bevel_gear = make_bevel_gear
# cq.Workplane.make_bevel_gear_system = make_bevel_gear_system
test= cq.Workplane("XY").make_bevel_gear(m, z, b, delta, alpha)
# c = cq.Workplane("XY", origin=(0,0,-16.08)).circle(10.2)#.extrude(-20) #10.69

system = make_bevel_gear_system(1,24,14,2, compound=True)
# 
show_object(system)
# show_object(test)
