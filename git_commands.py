#!/usr/bin/env python3
"""
Script Python para gestionar Git desde Codespace
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(cmd, description=""):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🔄 {description}...")
    print(f"   Comando: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Comando ejecutado correctamente")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error en comando:")
            print(f"   Stderr: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"💥 Excepción: {e}")
        return False

def update_repository():
    """Actualiza el repositorio completo"""
    print("🚀 ACTUALIZANDO REPOSITORIO GITHUB")
    print("=" * 50)
    
    # Verificar si es un repo git
    if not os.path.exists(".git"):
        print("❌ No es un repositorio Git")
        init = input("¿Quieres inicializarlo? (s/n): ")
        if init.lower() == 's':
            run_command("git init", "Inicializando repositorio Git")
        return
    
    # Mostrar estado
    run_command("git status", "Verificando estado")
    
    # Verificar cambios
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("📭 No hay cambios para subir")
        return
    
    # Mostrar cambios
    print("\n📋 Cambios detectados:")
    run_command("git status --short", "Listando archivos modificados")
    
    # Agregar cambios
    if not run_command("git add .", "Agregando todos los archivos"):
        return
    
    # Commit
    commit_msg = f"update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Geoportal scraper"
    if not run_command(f'git commit -m "{commit_msg}"', "Haciendo commit"):
        return
    
    # Push
    if run_command("git push origin main", "Subiendo a GitHub"):
        print("\n🎉 ¡REPOSITORIO ACTUALIZADO CORRECTAMENTE!")
        
        # Mostrar info adicional
        run_command("git log --oneline -3", "Últimos commits")
        
        # Obtener URL del repo
        result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            repo_url = result.stdout.strip()
            if "github.com" in repo_url:
                repo_url = repo_url.replace("git@github.com:", "https://github.com/")
                repo_url = repo_url.replace(".git", "")
                print(f"🌐 Ver en: {repo_url}")
    else:
        print("\n❌ Error al subir. Intentando con force...")
        run_command("git push --force-with-lease origin main", "Forzando subida")

def quick_update():
    """Actualización rápida sin confirmaciones"""
    commands = [
        "git add .",
        f'git commit -m "quick: {datetime.now().strftime("%H:%M:%S")}"',
        "git push origin main"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Ejecutando: {cmd}"):
            print("❌ Error en actualización rápida")
            return
    
    print("✅ Actualización rápida completada")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            quick_update()
        else:
            update_repository()
    else:
        update_repository()
