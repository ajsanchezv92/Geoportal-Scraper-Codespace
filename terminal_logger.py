#!/usr/bin/env python3
"""
Logger que captura TODO lo del terminal automáticamente
"""

import sys
import os
import threading
import time
from datetime import datetime
from config import LOG_FILE

class TerminalLogger:
    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_file = open('data/terminal_capture.log', 'a', encoding='utf-8')
        self._capturing = False
        
    def start_capture(self):
        """Inicia la captura de todo el output del terminal"""
        if self._capturing:
            return
            
        # Crear directorio si no existe
        os.makedirs('data', exist_ok=True)
        
        # Escribir header
        self.log_file.write(f"\n{'='*60}\n")
        self.log_file.write(f"CAPTURA DE TERMINAL INICIADA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_file.write(f"{'='*60}\n\n")
        self.log_file.flush()
        
        # Redirigir stdout y stderr
        sys.stdout = self
        sys.stderr = self
        self._capturing = True
        
        print("🔴 CAPTURA DE TERMINAL ACTIVADA - Todo se guarda en data/terminal_capture.log")
        
    def write(self, text):
        """Escribe tanto en terminal original como en archivo"""
        if text.strip():  # Solo escribir si no está vacío
            self.original_stdout.write(text)
            self.log_file.write(text)
            self.log_file.flush()  # Forzar escritura inmediata
            
    def flush(self):
        """Flush para ambos outputs"""
        self.original_stdout.flush()
        self.log_file.flush()
        
    def stop_capture(self):
        """Detiene la captura"""
        if self._capturing:
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr
            
            self.log_file.write(f"\n{'='*60}\n")
            self.log_file.write(f"CAPTURA DE TERMINAL DETENIDA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log_file.write(f"{'='*60}\n\n")
            self.log_file.close()
            self._capturing = False
            
            print("🟢 CAPTURA DE TERMINAL DETENIDA")

# Instancia global
terminal_logger = TerminalLogger()

def start_terminal_capture():
    """Inicia la captura del terminal"""
    terminal_logger.start_capture()

def stop_terminal_capture():
    """Detiene la captura del terminal"""
    terminal_logger.stop_capture()

def get_terminal_log():
    """Devuelve el contenido del log del terminal"""
    try:
        with open('data/terminal_capture.log', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "No se encontró el archivo de log del terminal"

def view_recent_log(lines=50):
    """Muestra las últimas líneas del log"""
    try:
        with open('data/terminal_capture.log', 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            print(''.join(recent_lines))
    except FileNotFoundError:
        print("❌ No se encontró data/terminal_capture.log")
