# Extrusions

Aluminium extrusions in a variety of sizes in both standard and v-slot profiles.
Currently e2020, e2040, e2080, and e4040 standard profiles
and v2020, v2040, and v4040 v-slot profiles are available.

## Installation

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=extrusions&subdirectory=plugins/extrusions"
```
You can also clone the repository of the plugin and run in the repository the following command:
```
python setup.py install
```

## Dependencies

This plugin has no dependencies other than the cadquery library.

## Usage

To use this plugin after it has been installed, just import it and use the extrusion functions.

```python
import cadquery as cq
import extrusions

extrusion = extrusions.e2020(100)
```
