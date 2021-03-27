import cadquery as cq
import gear_generator


def test_make_bevel_gear():
    """
    Tests if the bevel gear has been created successfully 
    by checking it's resulting volume
    """
    m = 1.5
    z = 16
    b = 6
    delta = 40
    alpha = 20
    clearance = 6
    gear = cq.Workplane().make_bevel_gear(m, z, b, delta, alpha = alpha, clearance = clearance)


def test_make_bevel_gear_system():
    """
    Tests if the bevel gear has been created successfully 
    by checking it's resulting volume
    """
    gear = cq.Workplane().make_bevel_gear_system(m, z1, z2, b, alpha=alpha, clearance = clearance, compound = False)

def test_make_gear():
    """
    Tests if the bevel gear has been created successfully 
    by checking it's resulting volume
    """
    gear = cq.Workplane().make_gear(m, z, b, alpha=alpha, helix_angle = helix_angle, raw = False)

def test_make_crown_gear():
    """
    Tests if the bevel gear has been created successfully 
    by checking it's resulting volume
    """
    gear = cq.Workplane().make_crown_gear(m, z, b, alpha = alpha, clearance = clearance)

def test_make_rack_gear():
    """
    Tests if the bevel gear has been created successfully 
    by checking it's resulting volume
    """
    gear = cq.Workplane().make_rack_gear(m, b, length, clearance, alpha = alpha, helix_angle = helix_angle)

# test_make_bevel_gear_system()
test_make_bevel_gear()
# test_make_gear()
# test_make_crown_gear()
# test_make_rack_gear()