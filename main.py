from src.worker_manager import WorkerManager
from src.utils import setup_logging
import logging
import threading
import time

def run_flask_app():
    """Ejecuta la app Flask en un hilo separado"""
    from app import app, keep_alive
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    setup_logging()
    
    # Iniciar Flask en segundo plano
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    logging.info("Servidor Flask iniciado en segundo plano")
    time.sleep(2)  # Dar tiempo a que Flask inicie
    
    try:
        manager = WorkerManager()
        manager.run()
    except KeyboardInterrupt:
        logging.info("Proceso interrumpido por el usuario")
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")
    finally:
        # Mantener el script vivo para que Flask siga funcionando
        try:
            while True:
                time.sleep(60)
                logging.info("Scraper completado - Codespace activo")
        except KeyboardInterrupt:
            logging.info("Cerrando Codespace...")

if __name__ == "__main__":
    main()
