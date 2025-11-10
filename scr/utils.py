import json
import logging
import time
import os
from typing import List, Dict, Any

def setup_logging():
    """Configura el sistema de logging para Codespace"""
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/scraped_urls.log'),
            logging.StreamHandler()
        ]
    )

def save_valid_urls(urls: List[str]):
    """Guarda las URLs válidas en el archivo JSON"""
    try:
        with open('data/valid_urls.json', 'w', encoding='utf-8') as f:
            json.dump(urls, f, indent=2, ensure_ascii=False)
        logging.info(f"Guardadas {len(urls)} URLs válidas")
    except Exception as e:
        logging.error(f"Error guardando URLs válidas: {e}")

def load_valid_urls() -> List[str]:
    """Carga las URLs válidas desde el archivo JSON"""
    try:
        with open('data/valid_urls.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
            logging.info(f"Cargadas {len(urls)} URLs válidas existentes")
            return urls
    except FileNotFoundError:
        logging.info("No se encontró archivo de URLs válidas, empezando desde cero")
        return []

def save_progress(state: Dict[str, Any]):
    """Guarda el estado del progreso"""
    try:
        with open('data/progress_state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        logging.debug("Progreso guardado correctamente")
    except Exception as e:
        logging.error(f"Error guardando progreso: {e}")

def load_progress() -> Dict[str, Any]:
    """Carga el estado del progreso"""
    try:
        with open('data/progress_state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
            logging.info(f"Progreso cargado: índice {state['current_index']}")
            return state
    except FileNotFoundError:
        logging.info("No se encontró archivo de progreso, empezando desde el inicio")
        return {
            'current_index': 0,
            'total_scraped': 0,
            'valid_urls_count': 0,
            'start_time': time.time(),
            'last_save': time.time()
        }

def cleanup_on_exit():
    """Limpieza antes de salir"""
    logging.info("Realizando limpieza antes de salir...")
    save_progress(load_progress())  # Forzar guardado final
