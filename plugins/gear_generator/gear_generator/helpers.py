from math import cos, sin, radians, acos
import cadquery as cq


def involute(r: float, sign: int = 1):
    """
    Defines an involute curve to create the flanks of the involute gears

    Args:
        r : Radius of the involute (for a gear it's the pitch radius)
        sign : 1 or -1 , to draw the involute in positive or negative direction      

    Returns:      
        x,y -> tuple() : 2-tuple of x and y coordinates in space
    """

    def curve(t):
        x = r * (cos(t) + t * sin(t))
        y = r * (sin(t) - t * cos(t))
        return x, sign * y

    return curve


def spherical_involute(delta, delta_b, R):
    """
    Equation of the spherical involute that lies on a sphere

    Args:
        delta : the function variable, goes from the gear root cone angle to the gear tip cone angle
        delta_b : angle of the base cone
        R : radius of the associated sphere

    Returns:      
        x,y,z -> tuple() : 3-tuple of x and y and z coordinates in space  
    """
    theta = acos(cos(delta) / cos(delta_b)) / sin(delta_b)
    x = R * cos(theta * sin(delta_b)) * sin(delta_b) * cos(theta) - R * sin(
        theta * sin(delta_b)
    ) * -sin(theta)
    y = R * cos(theta * sin(delta_b)) * sin(delta_b) * sin(theta) - R * sin(
        theta * sin(delta_b)
    ) * cos(theta)
    z = R * cos(theta * sin(delta_b)) * cos(delta_b)
    return x, y, z


def rotate_vector_2D(vector: cq.Vector, angle: float):
    """
    Rotates a 2D cq.Vector `vector`by an angle of `angle` in degrees
    """
    angle = radians(angle)
    x = cos(angle) * vector.x - sin(angle) * vector.y
    y = sin(angle) * vector.x + cos(angle) * vector.y
    return cq.Vector((x, y))
