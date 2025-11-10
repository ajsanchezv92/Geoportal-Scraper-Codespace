#!/usr/bin/env python3
"""
Script para ver los logs capturados del terminal
"""

import os
import sys
from datetime import datetime

def view_terminal_log(lines=100):
    """Muestra el log del terminal"""
    log_file = 'data/terminal_capture.log'
    
    if not os.path.exists(log_file):
        print("❌ No se encontró data/terminal_capture.log")
        print("💡 Ejecuta primero: python main.py")
        return
        
    print(f"📋 LOG COMPLETO DEL TERMINAL (últimas {lines} líneas)")
    print("=" * 70)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
        total_lines = len(all_lines)
        
        if lines == 'all':
            lines_to_show = all_lines
        else:
            lines_to_show = all_lines[-lines:]
            
        print(f"📊 Total de líneas en log: {total_lines:,}")
        print(f"📅 Archivo modificado: {datetime.fromtimestamp(os.path.getmtime(log_file))}")
        print("=" * 70)
        print()
        
        print(''.join(lines_to_show))

def view_errors_only():
    """Muestra solo las líneas con errores"""
    log_file = 'data/terminal_capture.log'
    
    if not os.path.exists(log_file):
        print("❌ No se encontró data/terminal_capture.log")
        return
        
    print("🚨 ERRORES ENCONTRADOS EN EL LOG")
    print("=" * 70)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line_lower = line.lower()
            if any(error in line_lower for error in ['error', 'exception', 'traceback', 'failed', '❌', '💥']):
                print(line.rstrip())

def get_log_stats():
    """Muestra estadísticas del log"""
    log_file = 'data/terminal_capture.log'
    
    if not os.path.exists(log_file):
        print("❌ No se encontró data/terminal_capture.log")
        return
        
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    error_count = sum(1 for line in lines if any(error in line.lower() for error in ['error', '❌', '💥']))
    warning_count = sum(1 for line in lines if any(warn in line.lower() for warn in ['warning', '⚠️']))
    success_count = sum(1 for line in lines if any(success in line.lower() for success in ['success', '✅', 'encontrada', 'válida']))
    
    print("📊 ESTADÍSTICAS DEL LOG")
    print("=" * 70)
    print(f"📈 Total de líneas: {len(lines):,}")
    print(f"🚨 Errores: {error_count}")
    print(f"⚠️  Advertencias: {warning_count}")
    print(f"✅ Éxitos: {success_count}")
    print(f"📁 Tamaño archivo: {os.path.getsize(log_file) / 1024 / 1024:.2f} MB")
    print(f"📅 Última modificación: {datetime.fromtimestamp(os.path.getmtime(log_file))}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "errors":
            view_errors_only()
        elif sys.argv[1] == "stats":
            get_log_stats()
        elif sys.argv[1] == "all":
            view_terminal_log('all')
        else:
            try:
                lines = int(sys.argv[1])
                view_terminal_log(lines)
            except:
                view_terminal_log(100)
    else:
        view_terminal_log(100)
