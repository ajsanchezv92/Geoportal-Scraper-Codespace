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
echo "📝 CAPTURA DE TERMINAL ACTIVADA - Todo se guarda en data/terminal_capture.log"
echo "📊 Para ver logs: python view_logs.py"
echo "📊 Para ver errores: python view_logs.py errors"
echo "📈 Para ver estadísticas: python view_logs.py stats"
echo "⏹️  Para detener: Ctrl+C"
echo ""

# Ejecutar la aplicación
python main.py
