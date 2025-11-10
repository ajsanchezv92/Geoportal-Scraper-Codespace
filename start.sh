#!/bin/bash

echo "Iniciando Geoportal Scraper en GitHub Codespace..."

# Crear directorios necesarios
mkdir -p data templates

# Instalar dependencias si es necesario
if [ ! -f "installed.flag" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
    touch installed.flag
fi

# Ejecutar la aplicación
echo "Iniciando servidor Flask y scraper..."
python main.py
