# cadquery-plugins

A collection of community contributed plugins that extend the functionality of CadQuery.

## Contributing

You will need to set up an Anaconda environment to build and test your plugins against before submitting them. If you need full instructions on installing CadQuery with Anaconda, please see the [CadQuery readme](https://github.com/CadQuery/cadquery#getting-started). Otherwise, run the following in a fresh Anaconda environment:

```
conda install -c conda-forge -c cadquery cadquery=master pytest
```

There is a sample plugin directory called `sample_plugin` that you need to copy and rename. You can then add your plugin code to that sample project. In general, these are the steps for adding your plugin to this plugins repository.

* Fork this repository
* Clone your fork locally
* Make a copy of the `sample_plugin` directory
* Rename `sample_plugin` to the name of your plugin
* Add your plugin code to the directory
* Update `__init__.py` to import your function and link it in to the CadQuery `Workplane` class
* Add a test file for your plugin to the `tests` directory, using `tests/test_sample_plugin` as a template
* Run pytest
* Fill out the sections in the README.md template with your plugin's information
* Submit a PR when your plugin is ready

## Considerations

* Plugins which create objects should allow for the fact that they may be required to place an object at each of multiple locations. This is why the sample plugin uses `eachpoint`.
