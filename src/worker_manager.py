import concurrent.futures
import logging
import time
import signal
import sys
from typing import List
from config import ALL_CODES, BASE_URL, MAX_WORKERS, BATCH_SIZE, AUTO_SAVE_INTERVAL
from .scraper import GeoportalScraper
from .progress_tracker import ProgressTracker
from .utils import save_valid_urls, load_valid_urls, save_progress, cleanup_on_exit

class WorkerManager:
    def __init__(self):
        self.scraper = GeoportalScraper()
        self.progress_tracker = ProgressTracker()
        self.valid_urls = load_valid_urls()
        self.progress_state = load_progress()
        self.is_running = True
        
        # Configurar manejo de señales para Codespace
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Maneja señales de interrupción"""
        logging.info(f"Recibida señal {signum}, guardando estado...")
        self.is_running = False
        cleanup_on_exit()
        sys.exit(0)
    
    def process_batch(self, start_index: int) -> int:
        """Procesa un lote de URLs"""
        end_index = min(start_index + BATCH_SIZE, len(ALL_CODES))
        batch_codes = ALL_CODES[start_index:end_index]
        batch_urls = [f"{BASE_URL}{code}" for code in batch_codes]
        
        valid_count = 0
        processed_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(self.scraper.scrape_url, url): url for url in batch_urls}
            
            for future in concurrent.futures.as_completed(future_to_url):
                if not self.is_running:
                    break
                    
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        self.valid_urls.append(result)
                        valid_count += 1
                except Exception as e:
                    logging.error(f"Error procesando {url}: {e}")
                
                processed_count += 1
                current_global_index = start_index + processed_count
                
                # Actualizar progreso
                self.progress_state.update({
                    'current_index': current_global_index,
                    'total_scraped': self.progress_state.get('total_scraped', 0) + 1,
                    'valid_urls_count': len(self.valid_urls),
                    'last_save': time.time()
                })
                
                self.progress_tracker.update_progress(
                    current_global_index,
                    self.progress_state['total_scraped'],
                    len(self.valid_urls)
                )
                
                # Guardar automáticamente cada cierto intervalo
                if processed_count % AUTO_SAVE_INTERVAL == 0:
                    save_valid_urls(self.valid_urls)
                    save_progress(self.progress_state)
                    logging.info(f"Auto-guardado: Índice {current_global_index}/{len(ALL_CODES)}")
        
        return valid_count
    
    def run(self):
        """Ejecuta el proceso completo de scraping"""
        logging.info(f"Iniciando proceso de scraping para {len(ALL_CODES)} URLs...")
        logging.info(f"Workers: {MAX_WORKERS}, Batch size: {BATCH_SIZE}")
        
        start_index = self.progress_state.get('current_index', 0)
        
        for batch_start in range(start_index, len(ALL_CODES), BATCH_SIZE):
            if not self.is_running:
                break
                
            logging.info(f"Procesando lote {batch_start} a {min(batch_start + BATCH_SIZE, len(ALL_CODES))}")
            
            valid_count = self.process_batch(batch_start)
            
            # Guardar después de cada lote
            save_valid_urls(self.valid_urls)
            save_progress(self.progress_state)
            
            logging.info(f"Lote completado. URLs válidas encontradas: {valid_count}")
            
            # Pequeña pausa entre lotes
            time.sleep(1)
        
        if self.is_running:
            logging.info("Proceso de scraping completado!")
            logging.info(f"Total URLs válidas encontradas: {len(self.valid_urls)}")
        else:
            logging.info("Proceso interrumpido, estado guardado.")
