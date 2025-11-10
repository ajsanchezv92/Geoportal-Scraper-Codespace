import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Optional, List
from config import BASE_URL, KEYWORDS, TIMEOUT, REQUEST_DELAY

class GeoportalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_url(self, url: str) -> Optional[str]:
        """Scrapea una URL y retorna el contenido si es válido"""
        try:
            time.sleep(REQUEST_DELAY)  # Delay para no saturar
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            if self.is_valid_content(response.text):
                logging.info(f"URL válida encontrada: {url}")
                return url
            else:
                return None
                
        except requests.RequestException as e:
            logging.debug(f"Error scraping {url}: {e}")
            return None
            
    def is_valid_content(self, html_content: str) -> bool:
        """Verifica si el contenido contiene la información esperada"""
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        
        # Verificar presencia de palabras clave
        keyword_count = sum(1 for keyword in KEYWORDS if keyword in text)
        
        # Considerar válido si tiene al menos 3 palabras clave
        return keyword_count >= 3
