from cadquery import *
from .sample_plugin import make_cubes

# Link the plugin in
Workplane.make_cubes = make_cubes
