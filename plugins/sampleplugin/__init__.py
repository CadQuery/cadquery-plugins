import cadquery as cq
from .sampleplugin import make_cubes

# Link the plugin in
cq.Workplane.make_cubes = make_cubes
