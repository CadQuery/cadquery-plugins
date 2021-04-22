import cadquery as cq
from math import pi, cos, sin, tan, sqrt, degrees, radians, atan2, atan, acos, asin
from .helpers import involute, spherical_involute, rotate_vector_2D

class BaseGear:
    """Base gear class
    This class stores attributes that are shared by any types of gear
    Other gear classes inherit from this class

    Attributes :
        m : gear modulus
        b : gear tooth facewidth
        z : gear number of teeth
        p : gear pitch 
        r_p : gear pitch radius
        alpha : gear pressure angle (radians)
        helix_angle : helix angle for helical bevel gear (radians)

    """

    def __init__(self, m: float, z: int, b: float, alpha: float, helix_angle: float):
        """
        Initialize a gear object with it's parameters

        Args:
            m : gear modulus
            b : gear tooth facewidth
            z : gear number of teeth
            alpha : gear pressure angle (degrees)
            helix_angle : helix angle for helical bevel gear (degrees)
        """    
        self.m = m 
        self.b = b 
        self.z = z 
        self.p = pi*self.m        
        self.r_p = m * z / 2
        self.alpha = radians(alpha)
        self.helix_angle = radians(helix_angle)


class BevelGear(BaseGear):
    """Inherits BaseGear class

    This class compute and store all the relevant parameters used to create a bevel gear.
    The build() method create and returns a cadquery Worplane object with the bevel gear.

    Attributes:
        clearance : Extra distance at the base of the gear cone to strengthened the gear 
        helix_angle : helix angle for helical bevel gear (radians)
        right_handed : Direction of the gear helix for helical gears
        N : Number of sections used to generate helical gear teeth. Higher `N` number gives better teeth surface but increase rendering time
        delta_p : pitch cone angle (radians) 
        R : radius of the inscribed sphere at pitch circle radius
        R_min : radius of the inscribed sphere at the end of gear teeth
        delta_b : base cone angle (radians)
        theta_a : pitch circle radius to tooth tip radius
        theta_f : pitch circle radius to tooth root radius
        r_a : tooth tip circle radius
        r_f : tooth root circle radius
        theta_p : angle of rotation of the involute curve to have tooth tickness = p at pitch circle
    """
    __doc__ = BaseGear.__doc__ + __doc__

    def __init__(self, m: float, z: int , b: int, delta_p: float, R: float, clearance: float = None, alpha: float = 15, helix_angle: float = 0, right_handed: bool = True, N: int = 4):
        
        """
        Args:
            m : gear modulus
            z : gear number of teeth 
            b : gear tooth facewidth
            delta_p : pitch cone angle (degrees)
            R : radius of the inscribed sphere at pitch circle radius
            clearance : extra distance at the base of the gear cone to strengthened the gear 
            alpha : pressure angle (degrees)
            helix_angle : helix angle for helical bevel gear (degrees) 
            right_handed : direction of the helix for helical bevel gear            
            N : number of tooth sections to interpolate when creating a spiral bevel gear

        """
        if clearance is None:
            self.clearance = m*z/10
        else :
            self.clearance = clearance
        super().__init__(m, z, b, alpha, helix_angle)
        self.right_handed = right_handed
        self.N = N
        self.delta_p = radians(delta_p) #pitch cone angle
        self.R = R
        self.R_min = R - b
        self.delta_b = asin(sin(self.delta_p)*cos(self.alpha))
        self.r_b = R * sin(self.delta_b)
        self.theta_a = atan2(m, R)
        self.theta_f = atan2(1.25*m, R)
        self.delta_a = self.delta_p + self.theta_a
        self.delta_f = self.delta_p - self.theta_f
        self.r_a = R*sin(self.delta_a)
        self.r_f = R*sin(self.delta_f)
        self.theta_p = self.p/(R*sin(self.delta_p))/4 #angle of rotation of the involute curve to have tooth tickness = p at pitch circle

    def make_tooth_profile(self, radius):
        """
        This method creates the tooth profile wire that lie on a sphere of radius `radius`
        """
        right_involute = cq.Workplane().parametricCurve(lambda delta : spherical_involute(delta, self.delta_b, radius), start = self.delta_b, stop = self.delta_a).rotate((0,0,0),(0,0,1),-degrees(self.theta_p))
        left_involute = right_involute.mirror("ZX") 
        right_top_pt = right_involute.val().endPoint()
        left_top_pt = left_involute.val().endPoint()
        right_bot_pt = right_involute.val().startPoint()
        left_bot_pt = left_involute.val().startPoint()
        end_point = right_top_pt-left_top_pt

        if right_top_pt.y > 0:
            raise ValueError("Inputed parameters leads to undefined tooth geometry.\nThis is due to either : too high gear ratio (z1/z2), too high pressure angle (alpha) or too big tooth face width (b).\
                \nIn general higher gear ratio needs lower pressure angle to obtain to good tooth geometry.")
        top_arc = cq.Workplane("XY", origin=left_top_pt.toTuple()).radiusArc(end_point.toTuple(), self.r_a)
        pos = (0,0,radius*cos(self.delta_f))

        if self.r_b <= self.r_f: #if undercut
            bot_arc = cq.Edge.makeCircle(self.r_f, pos, (0,0,1), angle1 = -self.theta_p, angle2 = self.theta_p)
            tooth_profile = cq.Wire.assembleEdges([right_involute.val(), top_arc.val(), left_involute.val(), bot_arc])
        else: 
            bot_arc = cq.Edge.makeCircle(tan(self.delta_f)*(radius*cos(self.delta_f)), pos, (0,0,1), angle1=-degrees(self.theta_p), angle2=degrees(self.theta_p))
            left_bot_arc_pt = bot_arc.endPoint()
            right_bot_arc_pt = bot_arc.startPoint()
            left_bot_line = cq.Edge.makeLine(left_bot_arc_pt,left_bot_pt)
            right_bot_line = cq.Edge.makeLine(right_bot_arc_pt,right_bot_pt)           

            tooth_profile = cq.Wire.assembleEdges([right_involute.val(), top_arc.val(), left_involute.val(), left_bot_line, bot_arc, right_bot_line])

        return tooth_profile

    def make_tooth(self):
        """
        This function creates the tooth solid from lofting tooth section wires.
        If the gear is standard, loft from wire at R radius to wire at R_min radius.
        If the gear is helical, creates intermediary tooth profiles rotated along the cone height. Finally loft by all the tooth sections.
        """ 
        N = self.N
        R_sphere = cq.Solid.makeSphere(self.R,angleDegrees1=-90, angleDegrees2=90).rotate((0,0,0),(0,0,1),90)
        Rmin_sphere = cq.Solid.makeSphere(self.R_min,angleDegrees1=-90, angleDegrees2=90).rotate((0,0,0),(0,0,1),90)
        outer = self.make_tooth_profile(self.R*1.2)
        inner = self.make_tooth_profile(self.R_min*0.8)
        splitter = cq.Solid.makeLoft([outer,inner])

        closing_face1 = R_sphere.Faces()[0].split(splitter).Faces()[1] # cuts a sphere to retrieve the surface enclosed by tooth profile wire
        closing_face2 = Rmin_sphere.Faces()[0].split(splitter).Faces()[1] # cuts a sphere to retrieve the surface enclosed by tooth profile wire
        
        sections = []
        dr = (self.b)/N
        dangle =  degrees(self.b * tan(self.helix_angle) / self.r_p) / N

        if self.helix_angle == 0:                             
            tooth = cq.Solid.makeLoft([closing_face1.Wires()[0], closing_face2.Wires()[0]])
        else :
            if self.right_handed:
                rot_dir = -1
            else:
                rot_dir = 1
            for i in range(N+1):
                sections.append(self.make_tooth_profile(self.R-dr*i).rotate((0,0,0),(0,0,1),rot_dir*dangle*i))                  
            sides = cq.Solid.makeLoft(sections)

            closing_face2 = Rmin_sphere.Faces()[0].split(sides).Faces()[1] # cuts a sphere to retrieve the surface enclosed by tooth profile wire
            sections[0] = closing_face1.Wires()[0]# remove the first and last section since we will loft from the closing face wires
            sections[-1] = closing_face2.Wires()[0]


            sides = cq.Solid.makeLoft(sections)  # There is a bug here, the solid isnt valid for unknown reasons.
            shell = cq.Shell.makeShell([closing_face1, sides, closing_face2]) # But the workaround is to build a shell from the faces that are valid
            tooth = cq.Solid.makeSolid(shell)
 
        return tooth

    def build(self):
        """
        Creates the cadquery objects and returns them as a cq.Workplane

        Returns:
            gear -> cq.Workplane : The gear shape in a cq.Workplane
        """
        tooths = []
        tooth = self.make_tooth()

        for i in range(1,self.z+1):
            angle = i*360/self.z
            tooths.append(tooth.rotate(cq.Vector(0,0,0),cq.Vector(0,0,1),angle))

        comp = cq.Compound.makeCompound(tooths)


        self.gear = (cq.Workplane("ZX",obj=comp).moveTo(self.R_min*cos(self.delta_f),0)
                .vLineTo(self.R_min*sin(self.delta_f))
                .lineTo(self.R*cos(self.delta_f),self.R*sin(self.delta_f))
                .line(self.clearance*sin(self.delta_p), -self.clearance*cos(self.delta_p))
                .vLineTo(0)
                .close()
                .revolve(axisStart=(0,0,0), axisEnd=(1,0,0))
                )   
        return self.gear 
        
class BevelGearSystem():
    """Inherits BaseGear class
    This class compute the right parameters for the creation of a system of 2 bevels gears positioned in a way they can mesh.

    Attributes:
        m : gears modulus (gears can mesh only if they have the same modulus)
        b : gears tooth facewidth
        z1 : pinion number of teeth
        z2 : gear number of teeth 
        delta_p1 : pinion pitch cone angle (radians)
        delta_p2 : gear pitch cone angle (radians)
        clearance1 : extra distance at the base of the pinion cone to strengthened the pinion 
        clearance2 : extra distance at the base of the gear cone to strengthened the gear 
        helix_angle : helix angle of the pinion and gear teeth (radians)
        alpha : pressure angle of the pinion and gear (radians)
        R : radius of the inscribed sphere at pitch circle radius
        N : number of tooth sections to interpolate when creating a spiral bevel gear system
    """
    __doc__ = BaseGear.__doc__ + __doc__

    def __init__(self, m: float, z1: int, z2: int, b: float, clearance1: float = None, clearance2: float = None, helix_angle: float = 0, alpha: float = 15, N: int = 4):
        """
        Args:
            m : gears modulus (gears can mesh only if they have the same modulus)
            z1 : pinion number of teeth
            z2 : gear number of teeth (note that if z1 > z2, the value will be swap to be sure that the pinion is always the gear with the smallest number of teeth)
            b : gears tooth facewidth
            clearance1 : extra distance at the base of the pinion cone to strengthened the pinion 
            clearance2 : extra distance at the base of the gear cone to strengthened the gear 
            alpha : pressure angle (degrees)
            helix_angle : helix angle of the pinion and gear teeth (degrees)
            alpha : pressure angle of the pinion and gear (degrees)        
            N : number of tooth sections to interpolate when creating a spiral bevel gear system

        """
        if z1>z2:
            z1,z2 = z2,z1
        if clearance1 == None:
            self.clearance1 = m*z1/20
        else:
            self.clearance1 = clearance1
        if clearance2 == None:
            self.clearance2 = m*z2/20
        else:
            self.clearance2 = clearance2
        self.m = m 
        self.b = b
        self.z1 = z1 
        self.z2 = z2
        self.delta_p1 = degrees(atan2(z1, z2)) #pitch cone angle
        self.delta_p2 = degrees(atan2(z2, z1)) #pitch cone angle
        self.R = (m*z2/2)/sin(radians(self.delta_p2))
        self.helix_angle = helix_angle
        self.alpha = alpha
        self.N = N 

    def build(self):
        """
        Creates the cadquery objects and returns them as a cq.Workplane

        Returns:
            pinion, gear -> tuple(cq.Workplane, cq.Workplane) : The pinion and gear bevel gears of the system positionned correctly in space
        """
        self.pinion = BevelGear(self.m, self.z1, self.b, self.delta_p1, self.R, self.clearance1, helix_angle=self.helix_angle, right_handed=False, alpha=self.alpha, N=self.N)
        self.gear = BevelGear(self.m, self.z2, self.b, self.delta_p2, self.R, self.clearance2, helix_angle=self.helix_angle, alpha=self.alpha, N=self.N)

        if self.gear.z % 2 == 0:
            return self.pinion.build(), self.gear.build().rotate((0,0,0),(0,1,0), 90).rotate((0,0,0),(1,0,0), (360/self.gear.z)/2)
        else:
            return self.pinion.build(), self.gear.build().rotate((0,0,0),(0,1,0),90)

class Gear(BaseGear):
    """Inherits BaseGear
    """
    __doc__ = BaseGear.__doc__ + __doc__

    def __init__(self, m: float, z: int, b: float, alpha: float = 20, helix_angle: float = 0, raw: bool = False):
        """
        Args:
        m : gear modulus
        b : gear tooth facewidth
        z : gear number of teeth
        alpha : gear pressure angle (degrees)
        helix_angle : helix angle for helical gear (degrees)
        raw : `False` : adds filleting a the root teeth edges; `True` : leaves the gear with no filleting         
        """
        super().__init__(m, z, b, alpha, helix_angle)
        self.raw = raw

        self.r_a = self.r_p + m
        self.r_b = self.r_p*cos(self.alpha)
        self.r_f = self.r_p - 1.25*m
    
    def make_tooth_profile(self):
        """
        Creates a single tooth wire to be rotated to create the full cross section of the gear

        Returns:
            cq.Wire : a wire representing the tooth wire
        """
        inv = lambda a: tan(a) - a    

        # angles of interest
        alpha_inv = inv(self.alpha)
        alpha_tip = acos(self.r_b/self.r_a)
        alpha_tip_inv = inv(alpha_tip)        
        a = 90/self.z + degrees(alpha_inv)
        a2 = 90/self.z + degrees(alpha_inv)-degrees(alpha_tip_inv)
        STOP = sqrt((self.r_a/self.r_b)**2 - 1) 

        # construct all the profiles
        left = (
            cq.Workplane()
            .transformed(rotate=(0,0,a))
            .parametricCurve(involute(self.r_b,-1), start=0, stop = STOP, makeWire=False, N=8)
            .val()
        )
        
        right = (
            cq.Workplane()
            .transformed(rotate=(0,0,-a))
            .parametricCurve(involute(self.r_b), start=0, stop = STOP, makeWire=False, N=8)
            .val()
        )

        top = cq.Edge.makeCircle(self.r_a,angle1=-a2, angle2=a2)

        p0 = left.startPoint()
        p1 = right.startPoint()  
        side0 = cq.Workplane(origin=p0.toTuple()).hLine(self.r_f-self.r_b).val()
        side1 = cq.Workplane(origin=p1.toTuple()).hLine(self.r_f-self.r_b).val()
        side2 = side0.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -360/self.z)

        p_bot_left = side1.endPoint()
        p_bot_right = rotate_vector_2D(side0.endPoint(), -360/self.z)

        bottom = cq.Workplane().moveTo(p_bot_left.x, p_bot_left.y).radiusArc(p_bot_right,self.r_f).val()

        # single tooth profile
        profile = cq.Wire.assembleEdges([left,top,right,side1,bottom, side2])
        # return cross_section
        if not self.raw:
            profile = profile.fillet2D(0.25*self.m, profile.Vertices()[-3:-1])
        return profile

    def build(self) :
        """
        Creates the gear and returns it in a cq.Workplane
        """
        # complete cross section
        gear = (
            cq.Workplane()
            .polarArray(0,0,360,self.z)
            .each(lambda loc: self.make_tooth_profile().located(loc))
            .consolidateWires()
        )
        if self.helix_angle == 0:
            self.gear = gear.extrude(self.b)
        else:
            self.gear = gear.twistExtrude(self.b, self.helix_angle)

        return self.gear
