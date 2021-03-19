# more_selectors

This plugin provide additionals selectors that can be useful in some situations. Since too much Selectors can be overwhelming there are available here rather than directly in cadquery.
If some of these selectors are judged worth to add to cadquery it may happen also.
If you want to add your own selectors to the plugin you can do it by opening a pull request

## Installation

To install this sample plugin, the following line should be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=more_selectors&subdirectory=plugins/more_selectors"
```
You can also clone the repository of the plugin and run in the repository the following command :
```
python setup.py install
```

## Dependencies

This plugin has no dependencies other than the cadquery library.

## Usage

To use this plugin after it has been installed, just import it and use the selectors as regular cadquery selectors

```python
import cadquery as cq
from more_selectors import InfHollowCylinderSelector

# Adds the make_cubes function to cadquery.Workplane
sampleplugin.register()

result = (cq.Workplane().circle(20).circle(10).extrude(30)
                        .edges(
                            InfHollowCylinderSelector((0,0,0), "Z", 25, 12)
                        )
                        .fillet(3)
```
