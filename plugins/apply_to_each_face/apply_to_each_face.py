import cadquery as cq

def apply_to_each_face(wp, f_workplane_selector, f_draw):
    def each_callback(face):
        wp_face = f_workplane_selector(face)
        
        return f_draw(wp_face, face).vals()[0]
    
    return wp.each(each_callback)


v_x_unit = cq.Vector(1,0,0)
v_y_unit = cq.Vector(0,1,0)
v_z_unit = cq.Vector(0,0,1)

# ---- VECTORS ----

WORLD_AXIS_UNIT_VECTORS_XYZ = \
    [v_x_unit, 
     v_y_unit, 
     v_z_unit]
    
WORLD_AXIS_UNIT_VECTORS_XZY = \
    [v_x_unit, 
     v_z_unit, 
     v_y_unit]
    
WORLD_AXIS_UNIT_VECTORS_YXZ = \
    [v_y_unit, 
     v_x_unit, 
     v_z_unit]
    
WORLD_AXIS_UNIT_VECTORS_YZX = \
    [v_y_unit, 
     v_z_unit, 
     v_x_unit]
    
WORLD_AXIS_UNIT_VECTORS_ZXY = \
    [v_z_unit, 
     v_x_unit, 
     v_y_unit]
    
WORLD_AXIS_UNIT_VECTORS_ZYX = \
    [v_z_unit, 
     v_y_unit, 
     v_x_unit]

# ---- PLANES ----

WORLD_XY_NORMAL = v_z_unit   
WORLD_ZX_NORMAL = v_y_unit   
WORLD_YZ_NORMAL = v_x_unit  

WORLD_AXIS_PLANES_XY_ZX_YZ = \
    [WORLD_XY_NORMAL,
     WORLD_ZX_NORMAL,
     WORLD_YZ_NORMAL]

WORLD_AXIS_PLANES_XY_YZ_ZX = \
    [WORLD_XY_NORMAL,
     WORLD_YZ_NORMAL,
     WORLD_ZX_NORMAL]

WORLD_AXIS_PLANES_YZ_XY_ZX = \
    [WORLD_YZ_NORMAL,
     WORLD_XY_NORMAL,
     WORLD_ZX_NORMAL]

WORLD_AXIS_PLANES_YZ_ZX_XY = \
    [WORLD_YZ_NORMAL,
     WORLD_ZX_NORMAL,
     WORLD_XY_NORMAL]

WORLD_AXIS_PLANES_ZX_XY_YZ = \
    [WORLD_ZX_NORMAL,
     WORLD_XY_NORMAL,
     WORLD_YZ_NORMAL]

WORLD_AXIS_PLANES_ZX_YZ_XY = \
    [WORLD_ZX_NORMAL,
     WORLD_YZ_NORMAL,
     WORLD_XY_NORMAL]        

def _create_workplane(v_center, v_xaxis, v_zaxis):
    return cq.Workplane(
            cq.Plane(
                v_center,
                v_xaxis,
                v_zaxis),
            origin=v_center)

class XAxisInPlane:
  def __init__(self, plane_normals, tolerance=1e-3):      
    self.__plane_normals = [x.normalized() for x in plane_normals]
    self.__tolerance = tolerance
    
  def __call__(self, face):
    v_zaxis = face.normalAt()

    selected_plane_normal = None
    for plane_normal in self.__plane_normals:   
      plane_normal_projection = plane_normal.dot(v_zaxis)
      if (1-abs(plane_normal_projection)) > self.__tolerance:
        selected_plane_normal = plane_normal
        break
    if selected_plane_normal is None:
      raise ValueError(
          "All plane normals are too close to face normal %s" % v_zaxis)
    v_xaxis = selected_plane_normal.cross(v_zaxis)

    return _create_workplane(
                face.Center(),
                v_xaxis,
                v_zaxis)

class XAxisClosestTo:
  def __init__(self, 
      candidate_vectors,
      tolerance = 1e-3):

      self.__tolerance = tolerance
      self.__weighted_candidate_vectors = \
          [(i, x.normalized()) \
           for i, x in enumerate(candidate_vectors)]
  
  def __get_best_candidate(
          self, 
          objectlist, 
          key_selector, 
          cluster_sort_key):
    # idea borrowed from
    # https://github.com/CadQuery/cadquery/blob/a71a93ea274089ddbd48dbbd84d84710fc82a432/cadquery/selectors.py#L343
    key_and_obj = []
    for obj in objectlist:
        key_and_obj.append((key_selector(obj), obj))
    key_and_obj.sort(key=lambda x: x[0])

    first_cluster = []
    start = key_and_obj[0][0]
    for key, obj in key_and_obj:
        if abs(key - start) <= self.__tolerance:
            first_cluster.append(obj)
        else:
            break
    first_cluster.sort(key=cluster_sort_key)
    
    return first_cluster[0]
    
  def __call__(self, face):
    v_zaxis = face.normalAt()
    
    best_xax_candidate = \
      self.__get_best_candidate(
          self.__weighted_candidate_vectors,
          lambda x: abs(x[1].dot(v_zaxis)),
          lambda x: x[0])[1]
    
    v_xaxis = (best_xax_candidate \
            - v_zaxis.multiply(best_xax_candidate.dot(v_zaxis)))\
           .normalized()

    return _create_workplane(
                face.Center(),
                v_xaxis,
                v_zaxis)


cq.Workplane.apply_to_each_face = apply_to_each_face
