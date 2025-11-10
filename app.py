from flask import Flask, render_template, jsonify
import json
import os
import time

# Importar después de posibles inicializaciones
try:
    from src.progress_tracker import ProgressTracker
    progress_tracker = ProgressTracker()
except:
    # Fallback para cuando el scraper no ha inicializado
    progress_tracker = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('progress.html')

@app.route('/progress')
def get_progress():
    if progress_tracker:
        progress = progress_tracker.get_progress()
    else:
        # Datos por defecto si el tracker no está disponible
        progress = {
            'current_index': 0,
            'total_scraped': 0,
            'valid_urls_count': 0,
            'elapsed_time': 0,
            'estimated_remaining': 0,
            'progress_percentage': 0,
            'total_urls': 10000000 + 19 * 10000,
            'urls_per_hour': 0,
            'last_update': time.time()
        }
    return jsonify(progress)

@app.route('/valid_urls')
def get_valid_urls():
    try:
        with open('data/valid_urls.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
        return jsonify({'count': len(urls), 'urls': urls[:100]})  # Mostrar solo primeras 100
    except FileNotFoundError:
        return jsonify({'count': 0, 'urls': []})

@app.route('/status')
def status():
    """Endpoint simple para mantener activo el Codespace"""
    return jsonify({'status': 'active', 'timestamp': time.time()})

def keep_alive():
    """Función para mantener el servidor activo"""
    try:
        # Este endpoint se puede llamar periódicamente
        with app.test_client() as client:
            client.get('/status')
    except:
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
