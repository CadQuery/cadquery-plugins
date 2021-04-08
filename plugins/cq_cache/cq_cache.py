import cadquery as cq
import cadquery 
from cadquery import exporters, importers
from functools import wraps
import tempfile
import os
import inspect

from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape





TEMPDIR_PATH = tempfile.gettempdir()
CACHE_DIR_NAME = "cadquery_geom_cache"
CACHE_DIR_PATH = os.path.join(TEMPDIR_PATH,CACHE_DIR_NAME)
CQ_TYPES = [cq.Shape, cq.Solid, cq.Shell, cq.Compound, cq.Face, cq.Wire, cq.Edge, cq.Vertex, TopoDS_Shape, cq.Workplane]

if CACHE_DIR_NAME not in os.listdir(TEMPDIR_PATH):
    os.mkdir(CACHE_DIR_PATH)

def importBrep(file_path):
    builder = BRep_Builder()
    shape = TopoDS_Shape()
    return_code = BRepTools.Read_s(shape, file_path, builder)
    if return_code is False:
        raise ValueError("Import failed, check file name")
    return shape


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

def using_same_function(fct, file_name):
    with open(file_name,"r") as f :
        cached_function = "".join(f.readlines()[:-1])

    caching_function = inspect.getsource(fct)
    if cached_function == caching_function:
        return True 
    else :
        return False

def return_right_wrapper(source, target_file):    
    CQ_TYPES_STR = [str(cq_type) for cq_type in CQ_TYPES]

    with open(target_file, "r") as tf:
        target = tf.readlines()[-1]
        target = target.replace("class ","").lstrip("<'").rstrip("'>") #eval cannot evaluate this "<class 'cadquery.cq.Workplane'>"" but this "cadquery.cq.Workplane" is ok
        target = eval(target) #by the checking above forbids malicious excecution
    
    for cq_type in CQ_TYPES:
        if target == cq_type:
            if cq_type == cq.Workplane:
                shape = cq.Shape(source)
                shape = cq.Workplane(obj=shape)
            else:
                shape = cq_type(source)    
            return shape 
        
def cq_cache(cache_size = 500):
    """
    Maximum cache memory in MB
    """
    def _cq_cache(function):     

        @wraps(function) 
        def wrapper(*args, **kwargs):
            file_name = build_file_name(function, *args, **kwargs)
            txt_file_path = os.path.join(CACHE_DIR_PATH, file_name+".txt")

            if file_name+".txt" in os.listdir(CACHE_DIR_PATH) and using_same_function(function, txt_file_path) : #check that a change in function passed doesn't load up an old BREP file.
                shape = importBrep(os.path.join(CACHE_DIR_PATH,file_name+".brep")) #If implemented in cadquery, could switch to the cadquery version of importBrep 
                return return_right_wrapper(shape,txt_file_path)              
     

            else:
                shape = function(*args, **kwargs)
                shape_type = type(shape)
                if shape_type not in CQ_TYPES:
                    raise TypeError(f"cq_cache cannot wrap {shape_type} objects")
                try :
                    shape_export = shape.val() # if shape is a workplane retrive only the shape object
                except AttributeError:
                    shape_export = shape
                    
                shape_export.exportBrep(os.path.join(CACHE_DIR_PATH,file_name)+".brep")

                with open(os.path.join(CACHE_DIR_PATH,file_name)+ ".txt", "w") as fun_file:
                    fun_file.write(inspect.getsource(function))
                    fun_file.write(str(shape_type))
                
                cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)
                while (cache_dir_size*1e-6) > cache_size:
                    delete_oldest_file(CACHE_DIR_PATH)
                    cache_dir_size = get_cache_dir_size(CACHE_DIR_PATH)

                return shape

        return wrapper
 
    return _cq_cache



