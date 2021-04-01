import cadquery as cq
from .plugins.cq_cache.cq_cache import cq_cache, clear_cq_cache
import os 

@cq_cache(1)
def cube(a,b,c):
    cube = cq.Workplane().box(a,b,c)
    return cube.val()

# def test_clear_cache():

def test_cache_file_creation():
    cube1 = cube(1,1,1)
    cube2 = cube(1,1,1)

def test_cache():
    cube1 = cube(1,1,1)
    cube2 = cube(1,1,1)
    print(type(cube1))
    # assert type(cube1) == type(cube2) == cq

