#Punto de entrada de la aplicación.
"""
Módulo: main.py
Propósito: Punto de entrada de la aplicación GUI y orquestador del ciclo de vida.
"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Asegura que la raíz del proyecto esté en sys.path sin importar desde dónde se ejecute
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.registry import discover_modules


class FeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Feather Arch")
        self.geometry("480x420")
        self.minsize(360, 300)

        # Configuración estética nativa ligera
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Contenedor de pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Cargar plugins y vincular cierre seguro
        self.modules = discover_modules()
        self._build_interface()
        self.protocol("WM_DELETE_WINDOW", self._on_app_close)

    def _build_interface(self):
        """Monta una pestaña por cada módulo detectado o muestra un aviso si no hay ninguno."""
        if not self.modules:
            empty_frame = ttk.Frame(self.notebook)
            self.notebook.add(empty_frame, text="Inicio")
            lbl = ttk.Label(
                empty_frame,
                text="No hay módulos en 'src/modules/'.\nAñade uno implementando BaseModule.",
                justify="center",
            )
            lbl.pack(expand=True)
            return

        for module in self.modules:
            tab_frame = ttk.Frame(self.notebook)
            tab_title = f"{module.icon} {module.module_name}".strip()
            self.notebook.add(tab_frame, text=tab_title)

            # Cada módulo construye su propia vista dentro de su pestaña
            module.build_view(tab_frame)

    def _on_app_close(self):
        """Notifica a todos los módulos antes de destruir la ventana."""
        for module in self.modules:
            try:
                module.on_close()
            except Exception as err:
                print(f"[Error] Fallo al cerrar {module.module_name}: {err}")
        self.destroy()


if __name__ == "__main__":
    app = FeatherApp()
    app.mainloop()
