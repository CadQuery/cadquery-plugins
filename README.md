# cadquery-plugins

cadquery-plugins is a collection of community contributed plugins that extend the functionality of CadQuery. A description of each of the included plugins can be found in the [Plugins](plugins.md) documentation. This documentation only includes plugins that have been accepted into this repository by the core CadQuery development team. Installation of third-party plugins from other sources is also possible, but extra care must be taken to ensure that the plugins are safe to use. A list of third-party plugins that meet a minimum criteria of quality are included in the [Third-Party Plugins](third_party.md) documentation.

## Installing Plugins

Each plugin should have installation instructions in its readme, but in general it should be possible to install each of the plugins in this repository using the following form.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=[the plugin name]&subdirectory=plugins/[the plugin name]"
```

## Using Plugins

Plugins need to have their `register` function called after they are imported, which makes the plugin's function(s) available. Using the included `sampleplugin` as an example, the following code gives the general method, assuming that the plugin has been installed using pip.

```python
import cadquery as cq
from sampleplugin import sampleplugin

# Adds the make_cubes function to cadquery.Workplane
sampleplugin.register()

result = (cq.Workplane().rect(50, 50, forConstruction=True)
                        .vertices()
                        .make_cubes(10))
```

## Contributing

You will need to set up an Anaconda environment to build and test your plugins before submitting them. If you need full instructions on installing CadQuery with Anaconda, please see the [CadQuery readme](https://github.com/CadQuery/cadquery#getting-started). Otherwise, run the following in a fresh Anaconda environment:

```
conda install -c conda-forge -c cadquery cadquery=master pytest
```

There is a sample plugin directory called `sampleplugin` that you can copy and rename. Be sure that you are chosing a unique name that is not already part of the Workplane class. Plugins using monkey patching, and if your plugin causes a naming conflict your plugin contribution will not be accepted.

Once you have renamed the `sampleplugin` directory, you can then add your plugin code to that directory. In general, these are the steps for adding your plugin to this plugins repository.

* Fork this repository
* Clone your fork locally
* Make a copy of the `sampleplugin` directory
* Rename `sampleplugin` to the name of your plugin
* Rename `sampleplugin.py` to an appropriate name
* Replace the contents of `sampleplugin.py` with your code, making sure that the `register` function is at the bottom of the file and pathes the appropriate functions into the Workplane class
* Add a test file for your plugin to the `tests` directory, using `tests/test_sampleplugin.py` as a template
* Run `pytest` and ensure that your plugin passes
* Replace the content of the sections in the sample plugin's README.md with your plugin's information
* Alter the variables at the top of setup.py with your plugin's information
    * You can test pip installation locally with `pip install /path/to/your/plugin/directory` and then by trying to import the plugin module in a Python REPL
* Submit a PR when your plugin is ready

## Considerations

* Plugins which create objects should allow for the fact that they may be required to place an object at each of multiple locations. This is why the sample plugin uses `eachpoint`.
