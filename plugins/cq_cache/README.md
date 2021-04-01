# cq_cache

This plugin provide a decorator function that allow you to add a file based cache to your functions to allow you to speed up the execution of your computational heavy cadquery functions.

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
#decorate your functions that build computational heavy shapes
from cq_cache import cq_cache, clear_cq_cache

@cq_cache(cache_size=1)
def make_cube(a,b,c):
    cube = cq.Workplane().box(a,b,c)
    return cube

for i in range(200):
    make_cube(1,1,1+i)

clear_cq_cache()
#>>> Cache cleared for 1.036 MB
```
