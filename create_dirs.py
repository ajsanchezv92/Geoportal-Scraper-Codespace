#!/usr/bin/env python3
"""
Script para crear todos los directorios necesarios
"""

import os

def create_directories():
    """Crea todos los directorios necesarios"""
    directories = [
        'data',
        'templates', 
        'src'
    ]
    
    print("📁 CREANDO DIRECTORIOS...")
    print("=" * 30)
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Creado: {directory}/")
        else:
            print(f"📂 Ya existe: {directory}/")
    
    # Verificar estructura
    print("\n📋 ESTRUCTURA ACTUAL:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Mostrar primeros 5 archivos
            if file.endswith(('.py', '.html', '.txt', '.json', '.md')):
                print(f"{subindent}{file}")
    
    print(f"\n🎯 Directorio actual: {os.getcwd()}")
    print("✅ Todos los directorios están listos")

if __name__ == "__main__":
    create_directories()
