import cadquery as cq 
from functools import wraps
import tempfile
import os

TEMPDIR_PATH = tempfile.gettempdir()
CACHE_DIR_NAME = "cadquery_geom_cache"
CACHE_DIR_PATH = os.path.join(TEMPDIR_PATH,CACHE_DIR_NAME)

if CACHE_DIR_NAME not in os.listdir(TEMPDIR_PATH):
    os.mkdir(CACHE_DIR_NAME)
 

def un_decorateur_passant_un_argument(fonction_a_decorer):
 
    def un_wrapper_acceptant_des_arguments(arg1, arg2):
        print("J'ai des arguments regarde :", arg1, arg2)
        fonction_a_decorer(arg1, arg2)
 
    return un_wrapper_acceptant_des_arguments

def cq_cache(memory = 100):
 
    def _cq_cache(cq_function):        
        @wraps(cq_function) 

        def wrapper(*args, **kwargs):
            if existe_deja:
                return function_qui_charge_le_fichier
            else:
                return cq_function(*args, **kwargs)
 
        print("En tant que décorateur, je retourne le wrapper")
 
        return wrapper
 
    print("En tant que créateur de décorateur, je retourne un décorateur")
    return mon_decorateur