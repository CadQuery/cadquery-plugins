import cadquery as cq 
from cadquery import exporters, importers
from functools import wraps
import tempfile
import os

TEMPDIR_PATH = tempfile.gettempdir()
CACHE_DIR_NAME = "cadquery_geom_cache"
CACHE_DIR_PATH = os.path.join(TEMPDIR_PATH,CACHE_DIR_NAME)

if CACHE_DIR_NAME not in os.listdir(TEMPDIR_PATH):
    os.mkdir(CACHE_DIR_PATH)


def get_cache_dir_size(cache_dir_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(cache_dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def delete_oldest_file(cache_dir_path):
    cwd = os.getcwd()
    os.chdir(cache_dir_path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    oldest = files[0]
    os.remove(os.path.join(cache_dir_path,oldest))
    os.chdir(cwd)


def build_file_name(fct, *args, **kwargs):
    SPACER = "_"
    file_name = fct.__name__
    for arg in args:
        file_name += SPACER + str(arg)
    for kwarg_value in kwargs.values():
        file_name += SPACER + str(kwarg_value)

    return file_name + ".step"

def cq_cache(cache_size = 100):
    """
    Maximum cache memory in MB
    """
    def _cq_cache(function):     

        @wraps(function) 
        def wrapper(*args, **kwargs):
            file_name = build_file_name(function, *args, **kwargs)

            if file_name in os.listdir(CACHE_DIR_PATH):
                return importers.importStep(os.path.join(CACHE_DIR_PATH,file_name))
            else:
                shape = function(*args, **kwargs)
                exporters.export(shape, os.path.join(CACHE_DIR_PATH,file_name))
                
                cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)
                while (cache_dir_size/1024**2) > cache_size:
                    delete_oldest_file(CACHE_DIR_PATH)
                    cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)

                return shape

        return wrapper
 
    return _cq_cache



def clear_cq_cache():
    cache_size = get_cache_dir_size(CACHE_DIR_PATH)
    for cache_file in os.listdir(CACHE_DIR_PATH):
        os.remove(os.path.join(CACHE_DIR_PATH, cache_file))
    print(f"Cache cleared for {round(cache_size*1e-6,3)} MB ")

