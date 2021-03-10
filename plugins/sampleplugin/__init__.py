import cadquery as cq
from .sample_plugin import make_cubes

# Link the plugin in
cq.Workplane.make_cubes = make_cubes
