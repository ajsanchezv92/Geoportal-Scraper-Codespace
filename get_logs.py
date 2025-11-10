#!/usr/bin/env python3
"""
Script para extraer y mostrar logs de forma amigable para Android
"""

import os
import sys
from datetime import datetime

def show_recent_logs():
    """Muestra los logs más recientes de forma legible"""
    
    log_files = [
        'data/debug.log',
        'data/scraped_urls.log'
    ]
    
    print("=" * 60)
    print("📋 LOGS DEL GEOPORTAL SCRAPER")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"📁 ARCHIVO: {log_file}")
            print("-" * 40)
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Mostrar últimas 50 líneas
                    for line in lines[-50:]:
                        print(line.strip())
            except Exception as e:
                print(f"❌ Error leyendo {log_file}: {e}")
            print()
        else:
            print(f"⚠️ Archivo no encontrado: {log_file}")
            print()

def show_errors_only():
    """Muestra solo los errores"""
    print("=" * 60)
    print("🚨 ERRORES ENCONTRADOS")
    print("=" * 60)
    
    if os.path.exists('data/debug.log'):
        try:
            with open('data/debug.log', 'r', encoding='utf-8') as f:
                for line in f:
                    if 'ERROR' in line or 'Error' in line or 'error' in line:
                        print(line.strip())
        except Exception as e:
            print(f"Error leyendo logs: {e}")
    else:
        print("No se encontró el archivo debug.log")

def show_progress():
    """Muestra el progreso actual"""
    print("=" * 60)
    print("📊 PROGRESO ACTUAL")
    print("=" * 60)
    
    # Mostrar URLs válidas
    if os.path.exists('data/valid_urls.json'):
        try:
            with open('data/valid_urls.json', 'r', encoding='utf-8') as f:
                import json
                urls = json.load(f)
                print(f"✅ URLs válidas encontradas: {len(urls)}")
                if urls:
                    print("Últimas 5 URLs:")
                    for url in urls[-5:]:
                        print(f"  - {url}")
        except Exception as e:
            print(f"Error leyendo URLs válidas: {e}")
    
    # Mostrar progreso
    if os.path.exists('data/progress_state.json'):
        try:
            with open('data/progress_state.json', 'r', encoding='utf-8') as f:
                import json
                progress = json.load(f)
                print(f"📈 Progreso: {progress.get('current_index', 0):,} / 10,190,000")
                print(f"🕒 Tiempo inicio: {datetime.fromtimestamp(progress.get('start_time', 0))}")
        except Exception as e:
            print(f"Error leyendo progreso: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "errors":
            show_errors_only()
        elif sys.argv[1] == "progress":
            show_progress()
        else:
            show_recent_logs()
    else:
        show_recent_logs()
