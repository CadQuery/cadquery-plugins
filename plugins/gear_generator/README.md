# Gear generator

This plugin provide additionals methods to create various gears. 
As for now you can create these gears (all the gears are involutes):
* Spur gear

<img src="images/straight_gear.PNG" width="600"/>

* Helical gear

<img src="images/helical_gear.PNG" width="600"/>

* Rack gear 

<img src="images/rack_gear_straight.PNG" width="600"/>

* Helical rack gear

<img src="images/rack_gear_helix.PNG" width="600"/>

* Crown (or face) gear

<img src="images/crown_gear.PNG" width="600"/>

* Bevel gear (straight) (experimental)

<img src="images/bevel_gear.PNG" width="600"/>

* Bevel gear (straight) (very experimental)

<img src="images/bevel_gear_system.PNG" width="600"/>


## Installation

To install this plugin, the following line should be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=gear_generator&subdirectory=plugins/gear_generator"
```


## Dependencies

This plugin has no dependencies other than the cadquery library.

## Usage

To use this plugin after it has been installed, just import it and use the make_... methods to create your gears
```python
import cadquery as cq
import gear_generator # automatically links the plugin functions to the cq.Workplane class


module = 2
nb_teeth = 20
width = 5
gear = cq.Workplane("XY").make_gear(module, nb_teeth, width)

```
Currently in cq-editor the automatical linking doesn't work so you should try to link it manually as below : 
```python
import cadquery as cq 
import gear_generator
gear_generator.cutter_objects.register_cutter_objects()
gear_generator.register()
```
