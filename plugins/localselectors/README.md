# Sample Plugin

This plugin modifies `Workplane` selectors so that they can be used to specify axes in the local coordinate plane.
This is done by using the lowercase letters `x`, `y`, and `z` instead of the uppercase ones.

## Installation

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=localselectors&subdirectory=plugins/localselectors"
```


## Dependencies

This plugin has no dependencies other than the cadquery library. To install CadQuery, follow the [instructions in its readme](https://github.com/CadQuery/cadquery#getting-started).
It uses a lot of internal structures, so it may break more easily on later versions of CadQuery than other plugins.
It was tested on CadQuery 2.5, feel free to post an issue in my [fork](https://github.com/cactorium/cadquery-plugins) if you run into any issues

## Usage

To use this plugin after it has been installed, import it to automatically patch its function(s) into the `cadquery.Workplane` class. Any function that uses string selectors should now work with these new selectors after import, but be sure to import `cadquery` first.

```python
import cadquery as cq
import localselectors # Adds local selectors to cadquery.Workplane

result = (cq.Workplane().rect(50, 50)
                        .extrude(50))

new_workplane = (result.faces(">x") # this should be the same as '>X' because we're starting off in the default coordinate system
                        .workplane())
result2 = (new_workplane.rect(30, 30)
           .extrude(30))

new_workplane = (result2
            .faces(">z")
            .workplane()) # this should be the face sticking away from the first cube
```
