"""
Módulo: system_pulse.py
Propósito: Monitor de CPU y RAM de ultra bajo consumo leyendo directamente del kernel de Linux (/proc).
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple

from src.core.base_module import BaseModule


class SystemPulse(BaseModule):
    def __init__(self):
        self._is_running = False
        self._after_id: Optional[str] = None
        
        # Histórico de tiempos de CPU para calcular el diferencial entre muestras
        self._prev_idle: int = 0
        self._prev_total: int = 0

        # Referencias a widgets de la UI
        self._parent: Optional[ttk.Frame] = None
        self._cpu_bar: Optional[ttk.Progressbar] = None
        self._cpu_label: Optional[ttk.Label] = None
        self._ram_bar: Optional[ttk.Progressbar] = None
        self._ram_label: Optional[ttk.Label] = None

    @property
    def module_name(self) -> str:
        return "Pulso"

    @property
    def icon(self) -> str:
        return "⚡"

    # =========================================================================
    # LÓGICA DE SISTEMA (Lectura pura de /proc)
    # =========================================================================

    def _read_cpu_times(self) -> Tuple[int, int]:
        """
        Lee /proc/stat. La primera línea contiene los tiempos globales de CPU en 'jiffies':
        cpu  user nice system idle iowait irq softirq steal guest guest_nice
        """
        stat_path = Path("/proc/stat")
        if not stat_path.exists():
            return 0, 0

        try:
            with open(stat_path, "r", encoding="utf-8") as f:
                first_line = f.readline()

            parts = first_line.split()[1:]  # Ignora la palabra 'cpu'
            values = [int(p) for p in parts]
            
            idle_time = values[3] + values[4]  # idle + iowait
            total_time = sum(values)
            return idle_time, total_time
        except (ValueError, IndexError, IOError):
            return 0, 0

    def _get_cpu_percentage(self) -> float:
        """Calcula el uso de CPU comparando el diferencial de tiempo con la muestra previa."""
        idle, total = self._read_cpu_times()

        delta_idle = idle - self._prev_idle
        delta_total = total - self._prev_total

        self._prev_idle = idle
        self._prev_total = total

        if delta_total <= 0:
            return 0.0

        usage = (1.0 - (delta_idle / delta_total)) * 100.0
        return max(0.0, min(100.0, usage))

    def _get_ram_info(self) -> Tuple[float, float, float]:
        """
        Lee /proc/meminfo y extrae Total y Disponible.
        Retorna: (usado_gb, total_gb, porcentaje_uso)
        """
        meminfo_path = Path("/proc/meminfo")
        if not meminfo_path.exists():
            return 0.0, 0.0, 0.0

        mem_total_kb = 0
        mem_avail_kb = 0

        try:
            with open(meminfo_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        mem_total_kb = int(line.split()[1])
                    elif line.startswith("MemAvailable:"):
                        mem_avail_kb = int(line.split()[1])

            if mem_total_kb == 0:
                return 0.0, 0.0, 0.0

            used_kb = mem_total_kb - mem_avail_kb
            usage_pct = (used_kb / mem_total_kb) * 100.0

            used_gb = used_kb / (1024 * 1024)
            total_gb = mem_total_kb / (1024 * 1024)

            return used_gb, total_gb, usage_pct
        except (ValueError, IndexError, IOError):
            return 0.0, 0.0, 0.0

    # =========================================================================
    # CONSTRUCCIÓN DE INTERFAZ Y CICLO DE VIDA
    # =========================================================================

    def build_view(self, parent: ttk.Frame) -> None:
        self._parent = parent
        self._is_running = True

        # Inicializa la primera lectura de CPU como referencia base
        self._prev_idle, self._prev_total = self._read_cpu_times()

        # Contenedor con espaciado
        container = ttk.Frame(parent, padding=15)
        container.pack(fill="both", expand=True)

        # Sección: CPU
        cpu_header = ttk.Label(container, text="Procesador (CPU)", font=("sans-serif", 10, "bold"))
        cpu_header.pack(anchor="w", pady=(0, 2))

        self._cpu_label = ttk.Label(container, text="Midiendo...", font=("monospace", 9))
        self._cpu_label.pack(anchor="w", pady=(0, 4))

        self._cpu_bar = ttk.Progressbar(container, orient="horizontal", mode="determinate", maximum=100)
        self._cpu_bar.pack(fill="x", pady=(0, 15))

        # Sección: Memoria RAM
        ram_header = ttk.Label(container, text="Memoria RAM", font=("sans-serif", 10, "bold"))
        ram_header.pack(anchor="w", pady=(0, 2))

        self._ram_label = ttk.Label(container, text="Midiendo...", font=("monospace", 9))
        self._ram_label.pack(anchor="w", pady=(0, 4))

        self._ram_bar = ttk.Progressbar(container, orient="horizontal", mode="determinate", maximum=100)
        self._ram_bar.pack(fill="x", pady=(0, 10))

        # Iniciar ciclo de actualización periódica (cada 1.5 segundos)
        self._update_loop()

    def _update_loop(self) -> None:
        """Actualiza las barras y etiquetas, reprogramándose con widget.after."""
        if not self._is_running or not self._parent:
            return

        # 1. Actualizar CPU
        cpu_pct = self._get_cpu_percentage()
        if self._cpu_bar and self._cpu_label:
            self._cpu_bar["value"] = cpu_pct
            self._cpu_label.config(text=f"Uso actual: {cpu_pct:.1f}%")

        # 2. Actualizar RAM
        used_gb, total_gb, ram_pct = self._get_ram_info()
        if self._ram_bar and self._ram_label:
            self._ram_bar["value"] = ram_pct
            self._ram_label.config(
                text=f"Uso actual: {used_gb:.2f} GB / {total_gb:.2f} GB ({ram_pct:.1f}%)"
            )

        # Reprogramar ejecución sin bloquear el hilo gráfico de Tkinter
        self._after_id = self._parent.after(1500, self._update_loop)

    def on_close(self) -> None:
        """Detiene el timer de refresco para evitar fugas de memoria o errores al salir."""
        self._is_running = False
        if self._parent and self._after_id:
            self._parent.after_cancel(self._after_id)
