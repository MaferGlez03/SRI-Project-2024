#!/bin/bash

# Navega hasta el directorio donde esta el archivo
cd .\src\

# Ejecutar la aplicación Flask
.\src\python app.py

# Abrir navegador
xdg-open http://127.0.0.1:5000