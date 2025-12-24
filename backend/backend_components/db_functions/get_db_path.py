"""
ES: Este script define una función para obtener la ruta de la base de datos local.\n
EN: This script defines a function to get the local database's path.
"""


import os, platform
from pathlib import Path


def get_db_path():
    """
    ES: Obtiene la ruta de la base de datos local.\n
    EN: Gets the local database's path.
    
    Returns:
        Path: Absolute path to the .db file
    """
    
    # obteniendo el sistema operativo
    # getting the operative system
    system = platform.system()
    
    # Windows
    if system == "Windows":
        base_dir = Path(os.getenv("APPDATA", Path.home()))
    
    # Mac 
    elif system == "Darwin":  # macOS
        base_dir = Path.home() / "Library" / "Application Support"
    
    # Linux
    else:
        xdg_home = os.getenv("XDG_DATA_HOME")
        base_dir = Path(xdg_home) if xdg_home else Path.home() / ".local/share"
    
    # creando un nuevo directorio para la base de datos dentro del previo si no se ha creado todavía
    # creating a new directory for the database inside the previous one if it has not been created yet
    db_dir = base_dir / "epsilon_ome_trainer"
    db_dir.mkdir(parents = True, exist_ok=True)
    
    return db_dir / "epsilon_data.db"