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

def test_bevel_parameters(m, z, b, r_inner, delta, alpha, phi, clearance, r_f_equiv, r_b_equiv):
    """
    Test the provided parameters to see if they lead to a valid bevel gear

    Giving the way bevel gears are made in this plugin, there is parameters combinaison that leads
    to an unvalid bevel gear geometry.
    
    This function aims to provide more informations to the user by raising more understandables errors 
    that the ones OCP raises.

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
