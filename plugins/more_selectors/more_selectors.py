import cadquery as cq

import numpy as np

def recover_homogenous_affine_transformation(p, p_prime):
    '''
    Find the unique homogeneous affine transformation that
    maps a set of 3 points to another set of 3 points in 3D
    space:

        p_prime == np.dot(p, R) + t

    where `R` is an unknown rotation matrix, `t` is an unknown
    translation vector, and `p` and `p_prime` are the original
    and transformed set of points stored as row vectors:

        p       = np.array((p1,       p2,       p3))
        p_prime = np.array((p1_prime, p2_prime, p3_prime))

    The result of this function is an augmented 4-by-4
    matrix `A` that represents this affine transformation:

        np.column_stack((p_prime, (1, 1, 1))) == \
            np.dot(np.column_stack((p, (1, 1, 1))), A)

    Source: https://math.stackexchange.com/a/222170 (robjohn)
    '''

    # construct intermediate matrix
    Q       = p[1:]       - p[0]
    Q_prime = p_prime[1:] - p_prime[0]

    # calculate rotation matrix
    R = np.dot(np.linalg.inv(np.row_stack((Q, np.cross(*Q)))),
               np.row_stack((Q_prime, np.cross(*Q_prime))))

    # calculate translation vector
    t = p_prime[0] - np.dot(p[0], R)

    # calculate affine transformation matrix
    matrix = np.column_stack((np.row_stack((R, t)),
                            (0, 0, 0, 1)))
    return matrix


class CylinderSelector(cq.Selector):
    """
    Selects any shape present in the infinite hollow cylinder.   
    """
    def __init__(self, outer_radius, along_axis, start = None, height = None, inner_radius = None):
        if (start is None and height is not None) or (start is not None and height is None):
            raise ValueError("If defining a non infinite CylinderSelector start and height must be defined.")
        self.r1 = inner_radius
        self.r2 = outer_radius
        self.axis = self.get_axis(along_axis)


        self.start = start


        self.end = start + self.axis.normalized().multiply(height)

        self.base = self.get_base(self.axis)
        self.M = self.get_transform_matrix(self.base)
        print(self.M)

        if start is None:
            self.infite = True
        else:
            self.infite = False

    def get_axis(self, axis_value):
        if axis_value == "X":
            axis = cq.Vector(1,0,0)
        elif axis_value == "Y":
            axis = cq.Vector(0,1,0)
        elif axis_value == "Z":
            axis = cq.Vector(0,0,1)
        else:
            axis = axis_value
        return axis

    def get_base(self, v):
        if v.x != 0:
            u = cq.Vector(-v.z, 0, v.x)
        else:
            u = cq.Vector(-v.z, 0, v.x)
        w = u.cross(v)
        return np.array(u.toTuple()), np.array(v.toTuple()), np.array(w.toTuple())
    
    def get_transform_matrix(self, target_base):
        source_base = np.array((1,0,0)), np.array((0,1,0)), np.array((0,0,1))    
        np_matrix = recover_homogenous_affine_transformation(source_base, target_base)
        # print(np_matrix.T.tolist())
        test = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        # print(isinstance(test, list))
        # return cq.Matrix(np_matrix.T.tolist())
        return cq.Matrix(test)

    def filter(self, objectList):
        result =[]
        for o in objectList:
            if self.infite:
                pass
            else:                
                p = o.Center()
                p_prime = p.transform(self.M)


            p_radius = sqrt(p_prime.X**2 + p_prime.y**2)

            if self.r1 is None:
                if p_radius < self.r2 :   
                    result.append(o)    
            else:
                if p_radius> self.r1 and p_radius < self.r2 :   
                    result.append(o)

        return result



box = cq.Workplane().box(10,10,10).edges(CylinderSelector(5,"Z",cq.Vector(0,0,0), height= 10))
