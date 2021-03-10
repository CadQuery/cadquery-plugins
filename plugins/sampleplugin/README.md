# Sample Plugin

Provide a short description of your plugin here.

## Installation

It is possible to install individual plugins from this repository, as long as the plugin has a valid setup.py. If you copied the `sample_plugin` directory, it has a starter setup.py in it.

Installation will take this form:

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=[your_plugin_name]&subdirectory=[your_plugin_subdirectory]"
```

For example, to install this sample plugin, the following line could be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=sampleplugin&subdirectory=plugins/sampleplugin"
```

## Considerations

Are there any other dependencies that need to be installed for your plugin to work?

Is there anything else that is different about your plugin that the user needs to know?

## Usage

Place descriptions and examples of how to use your plugin here.
