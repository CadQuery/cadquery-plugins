# FreeCAD Importer Plugin

This plugin allows users to import FreeCAD models into CadQuery, and will apply parameters to the model if they are provided and the model is a parametric one. At this time this plugin does not handle FreeCAD assemblies.

Something like an Anaconda environment with FreeCAD installed as a conda package may be required on some Linux distros like Ubuntu because of the requirement to use the FreeCAD Snap. The Snap does not seem to allow FreeCAD to be imported properly in Python. If you do use Anaconda, name the environment `freecad` to help this plugin find it.

## Installation

Installation takes form:

Assuming that you have pip and git installed, the following line can be used to install this plugin.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=freecad_importer&subdirectory=plugins/freecad_importer"
```

## Dependencies

FreeCAD must be installed and importable via Python in order for this plugin to work. CadQuery is also required. To install CadQuery, follow the [instructions here](https://cadquery.readthedocs.io/en/latest/installation.html).

## Usage

[Place descriptions and examples of how to use your plugin here.]

To use this plugin after it has been installed, import it to automatically patch its function(s) into the `cadquery.Workplane` class. The `make_cubes` function should be available after import, but be sure to import `cadquery` first.

```python
import cadquery as cq
import sampleplugin # Adds the make_cubes function to cadquery.Workplane

result = (cq.Workplane().rect(50, 50, forConstruction=True)
                        .vertices()
                        .make_cubes(10))
```
