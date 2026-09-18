import tkinter as tk
from tkinter import ttk
from src.core.base_module import BaseModule


class SystemPulse(BaseModule):
    @property
    def module_name(self) -> str:
        return "Pulso"

    @property
    def icon(self) -> str:
        return "⚡"

    def build_view(self, parent: ttk.Frame) -> None:
        lbl = ttk.Label(
            parent,
            text="Módulo detectado y montado dinámicamente.",
            font=("sans-serif", 10, "italic"),
        )
        lbl.pack(expand=True)
