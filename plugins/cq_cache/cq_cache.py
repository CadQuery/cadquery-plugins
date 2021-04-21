import cadquery as cq
import cadquery
from cadquery import exporters, importers
from functools import wraps
import tempfile
import os
import inspect
import base64
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape
from itertools import chain
import hashlib


TEMPDIR_PATH = tempfile.gettempdir()
CACHE_DIR_NAME = "cadquery_geom_cache"
CACHE_DIR_PATH = os.path.join(TEMPDIR_PATH, CACHE_DIR_NAME)
CQ_TYPES = [
    cq.Shape,
    cq.Solid,
    cq.Shell,
    cq.Compound,
    cq.Face,
    cq.Wire,
    cq.Edge,
    cq.Vertex,
    TopoDS_Shape,
    cq.Workplane,
]

if CACHE_DIR_NAME not in os.listdir(TEMPDIR_PATH):
    os.mkdir(CACHE_DIR_PATH)


def importBrep(file_path):
    """
    Import a boundary representation model
    Returns a TopoDS_Shape object
    """
    builder = BRep_Builder()
    shape = TopoDS_Shape()
    return_code = BRepTools.Read_s(shape, file_path, builder)
    if return_code is False:
        raise ValueError("Import failed, check file name")
    return shape


def get_cache_dir_size(cache_dir_path):
    """
    Returns size of the specified directory in bytes
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(cache_dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def delete_oldest_file(cache_dir_path):
    """
    When the cache directory size exceed the limit, this function is called
    deleting the oldest file of the cache
    """
    cwd = os.getcwd()
    os.chdir(cache_dir_path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    oldest = files[0]
    os.remove(os.path.join(cache_dir_path, oldest))
    os.chdir(cwd)


def build_file_name(fct, *args, **kwargs):
    """
    Returns a file name given the specified function and args.
    If the function and the args are the same this function returns the same filename
    """
    if cq.Workplane in (type(x) for x in chain(args, kwargs.values())):
        raise TypeError(
            "Can not cache a function that accepts Workplane objects as argument"
        )

    # hash all relevant variables
    hasher = hashlib.md5()
    for val in [fct.__name__, repr(args), repr(kwargs)]:
        hasher.update(bytes(val, "utf-8"))
    # encode the hash as a filesystem safe string
    filename = base64.urlsafe_b64encode(hasher.digest()).decode("utf-8")
    # strip the padding
    return filename.rstrip("=")


def clear_cq_cache():
    """
    Removes all the files from the cq cache
    """
    cache_size = get_cache_dir_size(CACHE_DIR_PATH)
    for cache_file in os.listdir(CACHE_DIR_PATH):
        os.remove(os.path.join(CACHE_DIR_PATH, cache_file))
    print(f"Cache cleared for {round(cache_size*1e-6,3)} MB ")


def using_same_function(fct, file_name):
    """
    Checks if this exact function call has been cached.
    Take care of the eventuality where the user cache a function but
    modify the body of the function afterwards.
    It assure that if the function has been modify, the cache won't load a wrong cached file
    """
    with open(file_name, "r") as f:
        cached_function = "".join(f.readlines()[:-1])

    caching_function = inspect.getsource(fct)
    if cached_function == caching_function:
        return True
    else:
        return False


def return_right_wrapper(source, target_file):
    """
    Cast the TopoDS_Shape object loaded by importBrep as the right type that the original function is returning
    """

    with open(target_file, "r") as tf:
        stored = tf.readlines()[-1]

    target = next(x for x in CQ_TYPES if x.__name__ == stored)

    if target == cq.Workplane:
        shape = cq.Shape(source)
        shape = cq.Workplane(obj=shape)
    else:
        shape = target(source)

    return shape


def cq_cache(cache_size=500):
    """
    cache_size : Maximum cache memory in MB

    This function save the model created by the cached function as a BREP file and
    loads it if the cached function is called several time with the same arguments.

    Note that it is primarly made for caching function with simple types as argument.
    Objects passed as an argument with a __repr__ function that returns the same value
    for different object will fail without raising an error. If the __repr__ function
    returns different values for equivalent objects (which is the default behaviour of
    user defined classes) then the caching will be ineffective.
    """

    def _cq_cache(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            file_name = build_file_name(function, *args, **kwargs)
            file_path = os.path.join(CACHE_DIR_PATH, file_name)

            if file_name in os.listdir(CACHE_DIR_PATH) and using_same_function(
                function, file_path
            ):  # check that a change in function passed doesn't load up an old BREP file.
                shape = importBrep(
                    os.path.join(CACHE_DIR_PATH, file_name + ".brep")
                )  # If implemented in cadquery, could switch to the cadquery version of importBrep
                return return_right_wrapper(shape, file_path)

            else:
                shape = function(*args, **kwargs)
                shape_type = type(shape)
                if shape_type not in CQ_TYPES:
                    raise TypeError(f"cq_cache cannot wrap {shape_type} objects")
                try:
                    shape_export = (
                        shape.val()
                    )  # if shape is a workplane retrive only the shape object
                except AttributeError:
                    shape_export = shape

                shape_export.exportBrep(
                    os.path.join(CACHE_DIR_PATH, file_name) + ".brep"
                )

                with open(os.path.join(CACHE_DIR_PATH, file_name), "w") as fun_file:
                    fun_file.write(inspect.getsource(function))
                    fun_file.write(shape_type.__name__)

                cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)
                while (cache_dir_size * 1e-6) > cache_size:
                    delete_oldest_file(CACHE_DIR_PATH)
                    cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)

                return shape

        return wrapper

    return _cq_cache
