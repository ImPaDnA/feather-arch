"""
Módulo: registry.py
Propósito: Escanear e instanciar dinámicamente los submódulos que implementan BaseModule.
"""

import importlib
import inspect
import pkgutil
from typing import List

from src.core.base_module import BaseModule
import src.modules as modules_pkg


def discover_modules() -> List[BaseModule]:
    """
    Inspecciona el paquete 'src.modules', localiza todas las clases que 
    implementan BaseModule (sin ser abstractas) y devuelve sus instancias.
    """
    loaded_instances: List[BaseModule] = []

    # Itera sobre todos los archivos .py presentes en la carpeta src/modules/
    package_path = modules_pkg.__path__
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        full_module_name = f"src.modules.{module_name}"
        
        try:
            imported_module = importlib.import_module(full_module_name)
        except Exception as err:
            print(f"[Error] No se pudo importar '{full_module_name}': {err}")
            continue

        # Busca clases dentro del archivo importado
        for _, obj in inspect.getmembers(imported_module, inspect.isclass):
            is_valid_plugin = (
                issubclass(obj, BaseModule)
                and obj is not BaseModule
                and not inspect.isabstract(obj)
            )
            
            if is_valid_plugin:
                try:
                    instance = obj()
                    loaded_instances.append(instance)
                    print(f"[Registry] Módulo cargado: {instance.module_name}")
                except Exception as err:
                    print(f"[Error] Fallo al instanciar '{obj.__name__}': {err}")

    return loaded_instances
