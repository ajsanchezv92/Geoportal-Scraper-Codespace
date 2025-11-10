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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logging.info("🕷️ Scraper inicializado con sesión requests")
        
    def scrape_url(self, url: str) -> Optional[str]:
        """Scrapea una URL y retorna el contenido si es válido"""
        try:
            logging.debug(f"🔍 Probando URL: {url}")
            time.sleep(REQUEST_DELAY)  # Delay para no saturar
            
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            if self.is_valid_content(response.text):
                logging.info(f"✅ URL VÁLIDA ENCONTRADA: {url}")
                return url
            else:
                logging.debug(f"❌ Contenido no válido: {url}")
                return None
                
        except requests.exceptions.Timeout:
            logging.warning(f"⏰ Timeout en URL: {url}")
            return None
        except requests.exceptions.ConnectionError:
            logging.warning(f"🔌 Error de conexión en URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logging.debug(f"🌐 HTTP Error {response.status_code} en {url}")
            return None
        except requests.RequestException as e:
            logging.warning(f"⚠️ Error en request {url}: {e}")
            return None
        except Exception as e:
            logging.error(f"💥 Error inesperado scraping {url}: {e}", exc_info=True)
            return None
            
    def is_valid_content(self, html_content: str) -> bool:
        """Verifica si el contenido contiene la información esperada"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            
            # Verificar presencia de palabras clave
            keyword_count = sum(1 for keyword in KEYWORDS if keyword in text)
            
            # Considerar válido si tiene al menos 3 palabras clave
            is_valid = keyword_count >= 3
            
            if is_valid:
                logging.debug(f"📊 Contenido válido con {keyword_count}/6 palabras clave")
            
            return is_valid
            
        except Exception as e:
            logging.error(f"💥 Error validando contenido: {e}", exc_info=True)
            return False
