#!/bin/bash

echo "🔄 ACTUALIZANDO REPOSITORIO GITHUB..."
echo "=========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Verificar si estamos en un repo git
if [ ! -d ".git" ]; then
    error "No es un repositorio Git. Inicializando..."
    git init
    info "Por favor configura el remote manualmente:"
    info "git remote add origin https://github.com/USUARIO/REPOSITORIO.git"
    exit 1
fi

# Verificar conexión con remote
info "Verificando conexión con GitHub..."
git remote -v

# Obtener información del repositorio
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "No configurado")
info "Repositorio: $REPO_URL"

# Mostrar estado actual
info "Estado actual de los archivos:"
git status --short

# Mostrar cambios pendientes
CHANGES=$(git status --porcelain | wc -l)
if [ "$CHANGES" -eq 0 ]; then
    warning "No hay cambios para subir"
    exit 0
fi

info "Archivos modificados/creados: $CHANGES"

# Agregar todos los cambios
info "Agregando archivos..."
git add .

# Hacer commit
COMMIT_MSG="update: $(date '+%Y-%m-%d %H:%M:%S') - Geoportal scraper progress"
info "Haciendo commit: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Subir a GitHub
info "Subiendo cambios a GitHub..."
if git push origin main; then
    success "✅ Cambios subidos correctamente a GitHub"
    info "📊 Resumen:"
    git log --oneline -3
    echo ""
    info "🌐 Puedes ver los cambios en:"
    echo "   https://github.com/$(echo $REPO_URL | cut -d'/' -f4-5 | sed 's/.git$//')"
else
    error "Error al subir cambios"
    info "Intentando con force..."
    if git push --force-with-lease origin main; then
        success "Cambios forzados correctamente"
    else
        error "Error grave. Revisa la configuración."
        info "Comandos manuales:"
        echo "  git pull origin main"
        echo "  git push origin main"
    fi
fi

echo ""
info "📁 Archivos importantes subidos:"
find . -name "*.py" -o -name "*.json" -o -name "*.html" -o -name "*.md" -o -name "*.sh" | head -10
echo ""

success "🎉 Actualización completada!"
