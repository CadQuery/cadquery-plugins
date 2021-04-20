# cq_cache

This plugin provides a decorator function that allows you to add a file based cache to your functions to allow you to speed up the execution of your computationally heavy cadquery functions.

## Installation

To install this plugin, the following line should be used.

```
pip install -e "git+https://github.com/CadQuery/cadquery-plugins.git#egg=cq_cache&subdirectory=plugins/cq_cache"
```
You can also clone the repository of the plugin and run in the repository the following command :
```
python setup.py install
```

## Dependencies

This plugin has no dependencies other than the cadquery library.

## Usage

To use this plugin after it has been installed, just import it and use the decorator on your functions

```python
# decorate your functions that build computationally heavy shapes
from cq_cache import cq_cache, clear_cq_cache

@cq_cache(cache_size=1)
def make_cube(a,b,c):
    cube = cq.Workplane().box(a,b,c)
    return cube

for i in range(200):
    make_cube(1,1,1+i)

clear_cq_cache()
# >>> Cache cleared for 1.036 MB
```

## Speed gain example 
```python
import cadquery as cq 
import time, functools
from cq_cache import cq_cache
from itertools import cycle

@cq_cache()
def lofting(nb_sec):
    wires = []
    radius = cycle([2,5,8,6,10])
    for i in range(nb_sec):  
        if i%2==0:
            Y = 1
        else:
            Y = 0     
        wires.append(cq.Wire.makeCircle(next(radius),cq.Vector(0,0,5*i),cq.Vector(0,Y,1)))
    loft = cq.Solid.makeLoft(wires)
    return loft

lofting(500)

# First script run :
# >>> 4500 ms
# Second script run :
# >>> 20 ms
```

## Limitations

Cache results are stored under a unique value generated from the function name and arguments. Arguments are compared using `repr(arg)`, so if your argument has a string representation involving the address (like `<class MyClass at 0x7fa34d805940>`) then caching will ineffective. In particular, using a CadQuery Workplane as an argument will raise a TypeError (a Workplane as a return type from your decorated function is fine).
