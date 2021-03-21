import cadquery as cq
from math import pi, cos, sin, tan, sqrt, degrees, radians, atan2, atan, acos
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections


def involute(r, sign = 1):
    def curve(t):
        x = r*(cos(t) + t*sin(t))
        y = r*(sin(t) - t*cos(t))
        return x,sign*y
    return curve

def make_bevel_tooth_gap_wire(Z_W, m, phi, r_a, r_f, r_base):
    """
    Make the tooth gap wire that will be used to cut the base shape
    """
    STOP = 2*sqrt((r_a/r_base)**2 - 1) # 2* To be sure to have extra working room
    #right side
    right = (cq.Workplane("XY", origin=(0,0,Z_W)).transformed(rotate=(-pi*m/2,-90+degrees(phi),0))
            .tag("baseplane")
            .parametricCurve(involute(r_base), N=8, stop=STOP, makeWire=False))           
    bot_right = right.moveTo(r_f,0).hLine(r_base-r_f)
    #left side           
    left = (cq.Workplane("XY", origin=(0,0,Z_W)).transformed(rotate=(pi*m/2,-90+degrees(phi),0))
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
    top = cq.Edge.makeLine(cq.Vector(pt_top_right.toTuple()), cq.Vector(pt_top_left.toTuple()))
    bot = cq.Edge.makeThreePointArc(cq.Vector(pt_bot_left.toTuple()),
                                    cq.Vector(pt_bot_mid.toTuple()),
                                    cq.Vector(pt_bot_right.toTuple()))
    wire = cq.Wire.assembleEdges([bot_right.val(), right.val(), top, left.val(), bot_left.val(), bot])
    return wire


def _make_bevel_gear(self, m, z, b, delta, alpha, clearance):
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
    Z_W =  (Z_P - r/tan(phi))*1.0000001 # This allow for the tooth gap wire to be shifted otherwise leads to failing cut operation

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

m = 0.75
z = 16
alpha = 20
delta = 40
b = 4 # L/4 <= b <= L/3
clearance = 4

cq.Workplane.make_bevel_gear=_make_bevel_gear
test= cq.Workplane("ZY").polarArray(30, 0, 360, 10).make_bevel_gear(m, z, b, delta, alpha, clearance)

show_object(test)

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


# show_object(
#     cq.Workplane(obj=involute_gear(1, 20)).toPending().twistExtrude(30, 45)
# )