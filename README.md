# feather-arch

Arquitectura de escritorio modular y ultraligera para herramientas de productividad personal. Diseñada para operar con consumo mínimo de recursos de CPU y RAM, permitiendo desacoplamiento estricto y extensibilidad mediante contratos base.

## Principios Técnicos
* **Cero sobrecarga:** Sin navegadores integrados ni entornos de ejecución pesados. Interfaz nativa `tkinter/ttk`.
* **Arquitectura de Plugins:** La aplicación base desconoce las herramientas internas; cada vista implementa `BaseModule`.
* **Diseño asistido por IA:** Las especificaciones y contratos arquitectónicos dictan las reglas del código autogenerado.

## Requisitos de Entorno
* Python 3.10+
* Soporte nativo de Tkinter (`sudo apt install python3-tk`)

## Puesta en marcha
```bash
./run.sh
