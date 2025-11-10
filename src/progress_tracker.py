import time
from typing import Dict, Any
from threading import Lock
from config import TOTAL_URLS

class ProgressTracker:
    def __init__(self):
        self.lock = Lock()
        self.current_index = 0
        self.total_scraped = 0
        self.valid_urls_count = 0
        self.start_time = time.time()
        self.last_update = time.time()
        
    def update_progress(self, current_index: int, total_scraped: int, valid_urls_count: int):
        """Actualiza el progreso actual"""
        with self.lock:
            self.current_index = current_index
            self.total_scraped = total_scraped
            self.valid_urls_count = valid_urls_count
            self.last_update = time.time()
            
    def get_progress(self) -> Dict[str, Any]:
        """Obtiene el estado actual del progreso"""
        with self.lock:
            elapsed_time = time.time() - self.start_time
            
            if self.total_scraped > 0:
                avg_time_per_url = elapsed_time / self.total_scraped
                remaining_urls = TOTAL_URLS - self.current_index
                estimated_remaining = avg_time_per_url * remaining_urls
                
                # Velocidad actual (URLs por hora)
                urls_per_hour = (self.total_scraped / elapsed_time) * 3600 if elapsed_time > 0 else 0
            else:
                estimated_remaining = 0
                urls_per_hour = 0
                
            progress_percentage = (self.current_index / TOTAL_URLS) * 100
            
            return {
                'current_index': self.current_index,
                'total_scraped': self.total_scraped,
                'valid_urls_count': self.valid_urls_count,
                'elapsed_time': elapsed_time,
                'estimated_remaining': estimated_remaining,
                'progress_percentage': progress_percentage,
                'total_urls': TOTAL_URLS,
                'urls_per_hour': urls_per_hour,
                'last_update': self.last_update
            }
