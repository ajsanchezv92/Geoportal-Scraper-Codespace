#!/bin/bash

echo "=========================================="
echo "  Geoportal Scraper - GitHub Codespace"
echo "=========================================="
echo ""

# Crear directorios necesarios
mkdir -p data templates

echo "📁 Directorios creados/verificados"
echo "🔧 Instalando dependencias..."

# Instalar dependencias si es necesario
if [ ! -f "installed.flag" ]; then
    pip install -r requirements.txt
    touch installed.flag
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "🚀 Iniciando aplicación..."
echo "📊 Dashboard disponible en: https://${CODESPACE_NAME}-5000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo "📝 Logs detallados en: data/debug.log"
echo "⏹️  Para detener: Ctrl+C"
echo ""

# Ejecutar la aplicación
python main.py
