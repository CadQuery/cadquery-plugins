# FreeCAD Importer Plugin

This plugin allows users to import FreeCAD models into CadQuery, and will apply parameters to the model if they are provided and the model is a parametric one (contains a FreeCAD spreadsheet document). At this time this plugin does not handle FreeCAD assemblies.

## Installation

Something like an Anaconda environment with FreeCAD installed as a conda package may be required on some Linux distros like Ubuntu because of the requirement to use the FreeCAD Snap to get the latest version of FreeCAD. The Snap does not seem to allow FreeCAD to be imported properly in Python. If you do use Anaconda, name the environment `freecad` to help this plugin find it. See the [documentation here](https://cadquery.readthedocs.io/en/latest/installation.html#install-the-conda-package-manager) for instructions on how to set up Anaconda without messing up your local Python installation. A example conda installation to get this plugin working is shown below.
```bash
mamba create -n freecad python=3.10
mamba install -c cadquery cadquery=master
mamba install freecad:freecad
```

Assuming that you have pip and git installed, the following line can be used to install this plugin.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=freecad_import&subdirectory=plugins/freecad_import"
```

## Dependencies

FreeCAD must be installed and importable via Python in order for this plugin to work. CadQuery is also required. To install CadQuery, follow the [instructions here](https://cadquery.readthedocs.io/en/latest/installation.html), or use the conda instructions above.

## Usage

To use this plugin after it has been installed, import it to automatically patch its functions into the `cadquery.importers` package.

Here is an example of importing a parametric FreeCAD part.

```python
import cadquery as cq
# The below adds the plugin's functions to cadquery.importers
from freecad_importer import import_freecad_part

# Imports a FreeCAD part while altering its parameters.
# The parameter must exist for the part or an errorr will be thrown.
result = import_freecad_part(
        "path_to_freecad_part_file.FCStd", parameters={"mount_dia": {"value": 4.8, "units": "mm"}}
    )
```

Here is an example of retrieving the parameters from a parametric FreeCAD part.

```python
import cadquery as cq
# The below adds the plugin's functions to cadquery.importers
from freecad_importer import get_freecad_part_parameters

# Get the parameters from the objectr
params = get_freecad_part_parameters(
    "path_to_freecad_part_file.FCStd", name_column_letter="A", value_column_letter="B"
)
```

The tests associated with this plugin have additional code that also might be useful to review as examples.
