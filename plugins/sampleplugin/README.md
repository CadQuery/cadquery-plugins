# Sample Plugin

[Provide a short description of your plugin here.]

This sample plugin gives an example of how to build a plugin that is installable from this repository. Once installed, it should be possible to import the plugin, making its `make_cubes` function available for use as if it was part of the `cadquery.Workplane` class.

## Installation

[How does a user install your plugin?]

It is possible to install individual plugins from this repository, as long as the plugin has a valid `setup.py`. If you copied the `sampleplugin` directory, it has a starter `setup.py` file in it.

Installation takes form:

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=[your_plugin_name]&subdirectory=[your_plugin_subdirectory]"
```

To install this sample plugin, the following line should be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=sampleplugin&subdirectory=plugins/sampleplugin"
```

## Dependencies

[Are there any other dependencies that need to be installed for your plugin to work?]

[Is there anything else that is different about your plugin that the user needs to know?]

This sample plugin has no dependencies other than the cadquery library. To install CadQuery, follow the [instructions in its readme](https://github.com/CadQuery/cadquery#getting-started).

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
