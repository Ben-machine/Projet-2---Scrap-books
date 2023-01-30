import os
from datetime import datetime
import config
from functools import wraps

def get_data_folder():
    """Retourne le chemin vers le sous-dossier horodaté où stocker les données 
        après l'avoir créé."""
    time_code = datetime.now().strftime("%y%m%d%H%M%S")
    dir_path = f"{config.DIR_DATA}/{time_code}"
    os.makedirs(dir_path)
    return dir_path

def time_exec(func):
    """Decorateur affichant le temps d'execution du script."""
    @wraps(func)
    def time_exec_wrapper(*args, **kwargs):
        debut = datetime.now()
        result = func(*args, **kwargs)
        fin = datetime.now()
        print(f"Execution en {fin - debut}")
        return result     
    return time_exec_wrapper