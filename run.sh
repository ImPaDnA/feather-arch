#!/bin/bash
set -euo pipefail

# Verificación de entorno de ejecución
echo "==> Iniciando feather-arch..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado en este sistema."
    exit 1
fi

# Validar que tkinter esté disponible en el sistema
python3 -c "import tkinter" 2>/dev/null || {
    echo "Advertencia: Tkinter no encontrado. Ejecuta: sudo apt install python3-tk"
    exit 1
}

# Ejecutar el punto de entrada principal
exec python3 src/main.py
