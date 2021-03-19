import cadquery as cq
from math import sqrt
# from utils import make_cylinder

def show(obj, name= None):
    try:
        show_object(obj, name)
    except:
        pass
def deb(obj, name=None):
    try:
        debug(obj, name)
    except:
        pass

def make_cylinder(plane, radius, height = None):
    infinite = False
    if height is None:
        infinite = True
        height = 10000

    cyl = cq.Workplane(plane).circle(radius).extrude(height,both = infinite)
    try:
        show_object(cyl, name = "selected cylinder", options={"alpha":0.7, "color": (64, 164, 223)})
    except NameError:
        pass


class InfiniteCylinderSelector(cq.Selector):
    """
    Selects any shape present in the defined infinite cylinder 
    based on the shape center of mass point.   

    """
    def __init__(self, origin, along_axis, radius, debug=False):

        self.r = radius
        self.axis = self.get_axis(along_axis)
        xdir = self.get_ortho_vector(self.axis)
        self.base = cq.Plane(cq.Vector(origin), xdir, self.axis.toTuple())
        if debug:
            make_cylinder(self.base, radius)

    def get_axis(self, axis_value):
        named_vectors = {
            "X" : cq.Vector(1,0,0),
            "-X" : cq.Vector(-1,0,0),
            "Y" : cq.Vector(0,1,0),
            "-Y" : cq.Vector(0,-1,0),
            "Z" : cq.Vector(0,0,1),
            "-Z" : cq.Vector(0,0,-1)
        }
        if isinstance(axis_value, str):
            try:
                return named_vectors[axis_value]
            except KeyError:
                raise ValueError("Supported names are {}".format(list(named_vectors.keys())))    
        else:
            if cq.Vector(axis_value).Length != 0:
                return cq.Vector(axis_value)
            else:
                raise ValueError("Axis of the cylinder must be non null")

    def get_ortho_vector(self, vector):
        #returns a vector orthogonal to the provided vector
        if 0 not in vector.toTuple():
            return (1,1, (-vector.x - vector.y)/vector.z)    
        else:
            if vector.x != 0:
                return ((-vector.y - vector.z)/vector.x, 1, 1)
            elif vector.y != 0:
                return (1, (-vector.x - vector.z)/vector.y,1)
            else:
                return (1,1, (-vector.x - vector.y)/vector.z)

    def filter(self, objectList):
        result =[]
        for o in objectList:            
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x**2 + projected_p.y**2)

            if p_radius < self.r:   
                result.append(o)
                    

        return result

class CylinderSelector(InfiniteCylinderSelector):
    """
    Selects any shape present in the defined cylinder.   

    """
    def __init__(self, origin, along_axis, height, radius, debug=False):
        super().__init__(origin,along_axis, radius)
        self.height = height
        if debug:
            make_cylinder(self.base, radius, height)

    def filter(self, objectList):
        result =[]
        for o in objectList:            
            p = o.Center()
            projected_p = self.base.toLocalCoords(p)
            p_radius = sqrt(projected_p.x**2 + projected_p.y**2)

            if p_radius < self.r and (projected_p.z < self.height and projected_p.z > 0):   
                result.append(o)                   

        return result

# cyl = make_cylinder(cq.Plane((0,10,0), (1,0,0), (0,1,1)), 5, 4)
select = cq.Workplane().box(10,10,10).edges(CylinderSelector((3,3,2),(0,0,1), 6, 6, debug=True))
select = cq.Workplane().box(10,10,10).edges(InfiniteCylinderSelector((3,3,2), "X", 6, debug=True))
# deb(cq.Workplane().box(10,10,10))
show(select, name = "selec")


