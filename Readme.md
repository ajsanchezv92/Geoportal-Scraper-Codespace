# Geoportal Scraper - GitHub Codespace

Scraper optimizado para ejecutar en GitHub Codespace.

## Características para Codespace

- ✅ Ejecución continua aunque cierres el navegador
- ✅ Guardado automático cada 100 URLs
- ✅ Recuperación desde el punto de interrupción
- ✅ Monitoreo web en puerto 5000
- ✅ Manejo correcto de señales de cierre

## Uso en Codespace

1. **Al abrir el Codespace** se iniciará automáticamente
2. **Ver el progreso**: Abre la pestaña "Ports" y preview en puerto 5000
3. **Si se detiene**: Solo ejecuta `python main.py` de nuevo

## URLs a scrapear

- **10,000,000** URLs numéricas (0-9999999)
- **190,000** URLs con prefijos (19 prefijos × 10000 cada uno)
- **Total**: 10,190,000 URLs

## Estructura de archivos

- `main.py` - Script principal con Flask integrado
- `start.sh` - Script de inicio para Codespace
- `app.py` - Servidor de monitoreo
- `data/` - Progreso y resultados

## Monitoreo

Abre la URL del puerto 5000 en tu Codespace para ver:
- Progreso en tiempo real
- URLs válidas encontradas
- Tiempo estimado restante
- Velocidad de scraping
