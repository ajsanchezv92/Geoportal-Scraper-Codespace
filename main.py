from src.worker_manager import WorkerManager
from src.utils import setup_logging
import logging
import threading
import time
import traceback

def run_flask_app():
    """Ejecuta la app Flask en un hilo separado"""
    try:
        from app import app
        import os
        port = int(os.environ.get('PORT', 5000))
        logging.info(f"🌐 Iniciando servidor Flask en puerto {port}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"💥 Error en servidor Flask: {e}")
        logging.error(traceback.format_exc())

def main():
    """Función principal con manejo completo de errores"""
    try:
        setup_logging()
        logging.info("🚀 INICIANDO GEOPORTAL SCRAPER CODESPACE")
        
        # Iniciar Flask en segundo plano
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()
        
        logging.info("✅ Servidor Flask iniciado en segundo plano")
        time.sleep(2)  # Dar tiempo a que Flask inicie
        
        # Iniciar el scraper
        manager = WorkerManager()
        manager.run()
        
    except KeyboardInterrupt:
        logging.info("⏹️ Proceso interrumpido por el usuario (Ctrl+C)")
    except Exception as e:
        logging.error(f"💥 ERROR CRÍTICO EN MAIN: {e}")
        logging.error(traceback.format_exc())
    finally:
        logging.info("🔚 Ejecución finalizada")
        
        # Mantener el script vivo para que Flask siga funcionando
        try:
            while True:
                time.sleep(60)
                logging.info("💤 Scraper completado - Codespace activo (Ctrl+C para salir)")
        except KeyboardInterrupt:
            logging.info("👋 Cerrando Codespace...")

if __name__ == "__main__":
    main()
