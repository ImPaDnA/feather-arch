#El primer Código: El contrato/interfaz.
"""
Módulo: base_module.py
Propósito: Definir la interfaz abstracta que todo plugin/herramienta debe implementar.
Patrón: Inversión de Dependencias (Dependency Inversion Principle).
"""

from abc import ABC, abstracmethod
import tkinter as tk
from tkinter import ttk

class BaseModule(ABC):
  """
  Clase base abstracta.
  El núcleo de feather-arch no conoce los detalles internos de cada módulo;
  solo interactúa con ellos a través de los métodos definidos en este contrato.
  """

  @property
  @abstractmethod
  def module_name(self) -> str:
    """
    Identificador visible del módulo.
    Se utilizará como título de la prestaña em la interfaz gráfica.
    """
    pass

  @property
  def icon(self) -> str:
    """
    Carácter o simbolo ligero opcional para representar la pestaña.
    Al no ser abstracto, tiene un valor predeterminado si no se sobreescribe.
    """
    return "\u2638"

  @abstractmethod
  def build_view(self, parent: ttk.Frame) -> None:
    """
    Construye y posiciona los componentes visuales (widgets) del módulo.

    Parámetros:
      parent: Contenedor (ttk.Frame) donde el módulo debe dibujar su UI.
      El módulo no debe invocar métodos de la ventana principal
      para preservar el desacoplamiento.
    """
    pass

  def on_close(self) -> None:
    """
    Método gancho (hook) opcional para liberar recursos, detener hilos
    o guardar estado antes de que la aplicación se cierre.
    """
    pass
