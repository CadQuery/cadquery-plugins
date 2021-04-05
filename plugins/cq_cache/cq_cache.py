import cadquery as cq 
from cadquery import exporters, importers
from functools import wraps
import tempfile
import os
import inspect

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

    return file_name

def clear_cq_cache():
    cache_size = get_cache_dir_size(CACHE_DIR_PATH)
    for cache_file in os.listdir(CACHE_DIR_PATH):
        os.remove(os.path.join(CACHE_DIR_PATH, cache_file))
    print(f"Cache cleared for {round(cache_size*1e-6,3)} MB ")

def compare_functions(fct, file_name):
    with open(file_name,"r") as file :
        cached_function = file.read()

    caching_function = inspect.getsource(fct)

    if cached_function == caching_function:
        return True 
    else :
        return False

def cq_cache(cache_size = 500):
    """
    Maximum cache memory in MB
    """
    def _cq_cache(function):     

        @wraps(function) 
        def wrapper(*args, **kwargs):
            file_name = build_file_name(function, *args, **kwargs)

            if file_name+".txt" in os.listdir(CACHE_DIR_PATH):
                if compare_functions(function, file_name + ".txt") is True: #check that a change in function passed doesn't load up an old BREP file.
                    # return importers.importBrep(os.path.join(CACHE_DIR_PATH,file_name)) #Needed to be implemented in CADQUERY
                    return importers.importStep(os.path.join(CACHE_DIR_PATH,file_name+".step")) #Needed to be implemented in CADQUERY
                else: 
                    pass
            else:
                shape = function(*args, **kwargs)
                try :
                    shape = shape.val() # if shape is a workplane retrive only the shape object
                except AttributeError:
                    pass
                # shape.exportBrep(os.path.join(CACHE_DIR_PATH,file_name,".brep"))
                shape.exportStep(os.path.join(CACHE_DIR_PATH,file_name,".step"))
                with open(os.path.join(CACHE_DIR_PATH,file_name, ".txt")) as fun_file:
                    fun_file.write(inspect.getsource(function))
            
                
                cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)
                while (cache_dir_size*1e-6) > cache_size:
                    delete_oldest_file(CACHE_DIR_PATH)
                    cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)

                return shape

        return wrapper
 
    return _cq_cache




