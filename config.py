import os

# Configuración del scraper
BASE_URL = "https://geoportal.minetur.gob.es/VCTEL/detalleEstacion.do?emplazamiento="

# Generar todos los códigos a scrapear
ALL_CODES = []

# Agregar códigos numéricos (0-9999999)
print("Generando códigos numéricos...")
ALL_CODES.extend([str(i) for i in range(0, 10000000)])

# Agregar códigos con prefijos - LISTA COMPLETA ACTUALIZADA
PREFIXES = [
    'ANDR', 'ARAR', 'ASTR', 'BALR', 'CANR', 'CATR', 'CEUR', 'CLMR', 
    'CTBR', 'CYLR', 'EXTR', 'GARR', 'MADR', 'MELL', 'MURR', 'NAVR', 
    'PVAR', 'RIOR', 'VALR'
]

# LISTA COMPLETA DE TODOS LOS PREFIJOS EXISTENTES SEGÚN TU SOLICITACIÓN:
PREFIXES_COMPLETE = [
    'ANDR',  # Andalucía
    'ARAR',  # Aragón
    'ASTR',  # Asturias
    'BALR',  # Baleares
    'CANR',  # Canarias
    'CATR',  # Cataluña
    'CEUR',  # Ceuta
    'CLMR',  # Castilla-La Mancha
    'CTBR',  # Cantabria
    'CYLR',  # Castilla y León
    'EXTR',  # Extremadura
    'GARR',  # Galicia
    'MADR',  # Madrid
    'MELL',  # Melilla
    'MURR',  # Murcia
    'NAVR',  # Navarra
    'PVAR',  # País Vasco
    'RIOR',  # La Rioja
    'VALR'   # Valencia
]

print("Generando códigos con prefijos...")
for prefix in PREFIXES_COMPLETE:
    ALL_CODES.extend([f"{prefix}{i:04d}" for i in range(0, 10000)])

TOTAL_URLS = len(ALL_CODES)
print(f"Total URLs a scrapear: {TOTAL_URLS:,}")

# Configuración de workers
MAX_WORKERS = 8
REQUEST_DELAY = 0.3
TIMEOUT = 15
BATCH_SIZE = 500

# Archivos de guardado
VALID_URLS_FILE = "data/valid_urls.json"
PROGRESS_FILE = "data/progress_state.json"
LOG_FILE = "data/scraped_urls.log"

# Palabras clave para validar contenido válido
KEYWORDS = [
    "ESTACIONES DE TELEFONÍA MÓVIL",
    "LOCALIZACIÓN",
    "CARACTERISTICAS TÉCNICAS",
    "Operador",
    "Banda Asignada",
    "NIVELES MEDIDOS"
]

# Configuración para Codespace
CODESPACE_PORT = 5000
AUTO_SAVE_INTERVAL = 100
