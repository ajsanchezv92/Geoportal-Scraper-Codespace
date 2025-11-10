import os

# Configuración del scraper
BASE_URL = "https://geoportal.minetur.gob.es/VCTEL/detalleEstacion.do?emplazamiento="

# Todos los códigos a scrapear (mezcla de numéricos y prefijos)
ALL_CODES = []

# Agregar códigos numéricos (0-9999999)
ALL_CODES.extend([str(i) for i in range(0, 10000000)])

# Agregar códigos con prefijos
PREFIXES = [
    'ANDR', 'ARAR', 'ASTR', 'BALR', 'CANR', 'CATR', 'CEUR', 'CLMR', 
    'CTBR', 'CYLR', 'EXTR', 'GARR', 'MADR', 'MELL', 'MURR', 'NAVR', 
    'PVAR', 'RIOR', 'VALR'
]

for prefix in PREFIXES:
    ALL_CODES.extend([f"{prefix}{i:04d}" for i in range(0, 10000)])

TOTAL_URLS = len(ALL_CODES)

# Configuración de workers
MAX_WORKERS = 8
REQUEST_DELAY = 0.3  # Reducido ligeramente para Codespace
TIMEOUT = 15
BATCH_SIZE = 500  # Procesar en lotes más pequeños

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
AUTO_SAVE_INTERVAL = 100  # Guardar cada 100 URLs procesadas
