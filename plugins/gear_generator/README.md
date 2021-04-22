# Gear generator

This plugin provide classes to create various gears. 
As for now you can create these gears (all the gears are involutes):
* Spur gear

<img src="images/straight_gear.PNG" width="600"/>

* Helical gear

<img src="images/helical_gear.PNG" width="600"/>

* Bevel gear (straight and helical)

<img src="images/bevel_gear.PNG" width="600"/>

* Bevel gear system (straight and helical)

<img src="images/bevel_gear_system.PNG" width="600"/>


## Installation

To install this plugin, the following line should be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=gear_generator&subdirectory=plugins/gear_generator"
```


## Dependencies

This plugin has no dependencies other than the cadquery library.

## Usage

To use this plugin after it has been installed, import it and create Gear objects
```python
import cadquery as cq
import gear_generator

module = 2
nb_teeth = 12
width = 8
gear = Gear(module, nb_teeth, width).build() #Instantiate a gear object and call it's build method to get the gear in a cq.Workplane
```
<img src="images/readme_example.PNG" width="300"/>

Below is the list of implemented gear classes :
```python
Gear(args)
BevelGear(args)
BevelGearSystem(args)

#You can get info about the parameters by running 
help(BevelGear)
>>> _make_gear(m, z, b, alpha=20, helix_angle=None, raw=False) method of cadquery.cq.Workplane instance
>>>     Creates a spur or helical involute gear
>>> 
>>>     Parameters
>>>     ----------
>>>     m : float
>>>         Spur gear modulus
>>>     z : int
>>>         Number of teeth
>>>     b : float
>>>         Tooth width
>>>     alpha : float
>>>         Pressure angle in degrees, industry standard is 20\ufffd
>>>     helix_angle : float
>>>         Helix angle of the helical gear in degrees
>>>         If None creates a spur gear, if specified create a helical gear
```
