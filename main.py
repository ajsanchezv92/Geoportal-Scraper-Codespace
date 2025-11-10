from src.worker_manager import WorkerManager
from src.utils import setup_logging
from terminal_logger import start_terminal_capture, stop_terminal_capture
import logging
import threading
import time
import traceback
import atexit

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
    """Función principal con captura completa de terminal"""
    try:
        # INICIAR CAPTURA DE TERMINAL (LO PRIMERO)
        start_terminal_capture()
        
        print("=" * 70)
        print("🚀 GEOPORTAL SCRAPER CODESPACE - INICIANDO")
        print("📝 TODO EL OUTPUT SE GUARDA EN: data/terminal_capture.log")
        print("=" * 70)
        
        # Registrar función de limpieza al salir
        atexit.register(stop_terminal_capture)
        
        setup_logging()
        
        # Iniciar Flask en segundo plano
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()
        
        print("✅ Servidor Flask iniciado en segundo plano")
        time.sleep(2)
        
        # Iniciar el scraper
        manager = WorkerManager()
        manager.run()
        
    except KeyboardInterrupt:
        print("\n⏹️ Proceso interrumpido por el usuario (Ctrl+C)")
    except Exception as e:
        print(f"💥 ERROR CRÍTICO EN MAIN: {e}")
        print(traceback.format_exc())
    finally:
        print("🔚 Ejecución finalizada")
        stop_terminal_capture()
        
        # Mantener el script vivo
        try:
            while True:
                time.sleep(60)
                print("💤 Scraper completado - Codespace activo (Ctrl+C para salir)")
        except KeyboardInterrupt:
            print("👋 Cerrando Codespace...")

if __name__ == "__main__":
    main()
