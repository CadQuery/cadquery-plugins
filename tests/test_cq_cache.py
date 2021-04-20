import cadquery as cq
import cadquery
from plugins.cq_cache.cq_cache import cq_cache, clear_cq_cache, get_cache_dir_size
import tempfile
import os
import pytest

TEMPDIR_PATH = tempfile.gettempdir()
CACHE_DIR_NAME = "cadquery_geom_cache"
CACHE_DIR_PATH = os.path.join(TEMPDIR_PATH, CACHE_DIR_NAME)
CACHE_SIZE = 0.1
for f in os.listdir(CACHE_DIR_PATH):
    os.remove(os.path.join(CACHE_DIR_PATH, f))


@cq_cache(CACHE_SIZE)
def cube(a, b, c):
    cube = cq.Workplane().box(a, b, c)
    return cube.val()


def test_get_cache_dir_size():
    with open(os.path.join(CACHE_DIR_PATH, "fill.txt"), "w") as f:
        f.write("test")
    assert get_cache_dir_size(CACHE_DIR_PATH) == 4


def test_clear_cache():
    with open(os.path.join(CACHE_DIR_PATH, "fill.txt"), "w") as f:
        f.write("test")
    assert len(os.listdir(CACHE_DIR_PATH)) == 1
    clear_cq_cache()
    assert len(os.listdir(CACHE_DIR_PATH)) == 0


def test_cache_file_creation():
    clear_cq_cache()
    cube1 = cube(1, 1, 1)
    cube2 = cube(1, 1, 1)
    files = os.listdir(CACHE_DIR_PATH)
    assert len(files) == 2
    assert "Fv2MB2hDeoH6xwu4aBh5wA.brep" in files
    assert "Fv2MB2hDeoH6xwu4aBh5wA" in files


def test_cache_unique():
    clear_cq_cache()
    for _ in range(2):
        cube1 = cube(1, 1, 1)
        cube2 = cube(2, 2, 2)
    assert cube1.BoundingBox().zlen == pytest.approx(1)
    assert cube2.BoundingBox().zlen == pytest.approx(2)


def test_not_exceeding_size():
    clear_cq_cache()
    for i in range(20):
        cube(1, 1, 1 + i)
    assert get_cache_dir_size(CACHE_DIR_PATH) < CACHE_SIZE * 1e6


def test_cache_type_return():
    cube1 = cube(1, 1, 1)  # at first call get the type directly from function call
    # at second call the decorator retrives the right type with some logic that may fail
    cube2 = cube(1, 1, 1)
    assert isinstance(cube1, cadquery.occ_impl.shapes.Solid)
    assert isinstance(cube2, cadquery.occ_impl.shapes.Solid)


def test_cache_type_return_with_modified_function():
    @cq_cache(CACHE_SIZE)
    def cube(a, b, c):
        cube = cq.Workplane().box(a, b, c)
        return cube

    cube1 = cube(1, 1, 1)  # at first call get the type directly from function call
    # at second call the decorator retrives the right type with some logic that may fail
    cube2 = cube(1, 1, 1)
    assert isinstance(cube1, cq.Workplane)
    assert isinstance(cube2, cq.Workplane)

    @cq_cache(CACHE_SIZE)
    def cube(a, b, c):
        cube = cq.Workplane().box(a, b, c).val()
        return cube

    cube3 = cube(1, 1, 1)
    cube4 = cube(1, 1, 1)
    assert isinstance(cube3, cq.Solid)
    assert isinstance(cube4, cq.Solid)


def test_workplane_typeerror():
    @cq_cache(CACHE_SIZE)
    def wp(a, kwarg=None):
        return a

    with pytest.raises(TypeError):
        wp(cq.Workplane())

    with pytest.raises(TypeError):
        wp(1, kwarg=cq.Workplane())
