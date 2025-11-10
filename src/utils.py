import json
import logging
import time
import os
import sys
from typing import List, Dict, Any

def ensure_data_directory():
    """Asegura que el directorio data existe"""
    os.makedirs('data', exist_ok=True)
    print("✅ Directorio 'data/' creado/verificado")

def setup_logging():
    """Configura el sistema de logging detallado para Codespace"""
    # Crear directorio data si no existe - ESTA ES LA CLAVE
    ensure_data_directory()
    
    # Configurar logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Formato detallado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler('data/debug.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para consola (INFO y superior)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Limpiar handlers existentes y agregar los nuevos
    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log de inicio
    logging.info("=== SISTEMA DE LOGGING INICIADO ===")
    logging.info("Debug log guardado en: data/debug.log")

def save_valid_urls(urls: List[str]):
    """Guarda las URLs válidas en el archivo JSON"""
    ensure_data_directory()  # ← Asegurar que data existe
    try:
        with open('data/valid_urls.json', 'w', encoding='utf-8') as f:
            json.dump(urls, f, indent=2, ensure_ascii=False)
        logging.info(f"✅ Guardadas {len(urls)} URLs válidas en data/valid_urls.json")
    except Exception as e:
        logging.error(f"❌ Error guardando URLs válidas: {e}", exc_info=True)

def load_valid_urls() -> List[str]:
    """Carga las URLs válidas desde el archivo JSON"""
    ensure_data_directory()  # ← Asegurar que data existe
    try:
        with open('data/valid_urls.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
            logging.info(f"📁 Cargadas {len(urls)} URLs válidas existentes")
            return urls
    except FileNotFoundError:
        logging.info("📝 No se encontró archivo de URLs válidas, empezando desde cero")
        return []
    except Exception as e:
        logging.error(f"❌ Error cargando URLs válidas: {e}", exc_info=True)
        return []

def save_progress(state: Dict[str, Any]):
    """Guarda el estado del progreso"""
    ensure_data_directory()  # ← Asegurar que data existe
    try:
        with open('data/progress_state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        logging.debug("💾 Progreso guardado correctamente")
    except Exception as e:
        logging.error(f"❌ Error guardando progreso: {e}", exc_info=True)

def load_progress() -> Dict[str, Any]:
    """Carga el estado del progreso"""
    ensure_data_directory()  # ← Asegurar que data existe
    try:
        with open('data/progress_state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
            logging.info(f"🔄 Progreso cargado: índice {state['current_index']:,}")
            return state
    except FileNotFoundError:
        logging.info("🆕 No se encontró archivo de progreso, empezando desde el inicio")
        return {
            'current_index': 0,
            'total_scraped': 0,
            'valid_urls_count': 0,
            'start_time': time.time(),
            'last_save': time.time()
        }
    except Exception as e:
        logging.error(f"❌ Error cargando progreso: {e}", exc_info=True)
        return {
            'current_index': 0,
            'total_scraped': 0,
            'valid_urls_count': 0,
            'start_time': time.time(),
            'last_save': time.time()
        }

def cleanup_on_exit():
    """Limpieza antes de salir"""
    logging.info("🧹 Realizando limpieza antes de salir...")
    try:
        save_progress(load_progress())  # Forzar guardado final
        logging.info("✅ Limpieza completada")
    except Exception as e:
        logging.error(f"❌ Error en limpieza: {e}", exc_info=True)
