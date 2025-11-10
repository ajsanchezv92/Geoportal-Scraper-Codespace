#!/usr/bin/env python3
"""
Script para solucionar problemas de Git con el repositorio
"""

import subprocess
import os
import sys

def run_cmd(cmd):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🚀 Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Éxito: {result.stdout.strip()}")
        return True, result.stdout
    else:
        print(f"❌ Error: {result.stderr.strip()}")
        return False, result.stderr

def fix_git_issues():
    """Soluciona problemas comunes de Git"""
    print("🔧 SOLUCIONANDO PROBLEMAS DE GIT...")
    print("=" * 50)
    
    # Verificar si existe .git
    if not os.path.exists(".git"):
        print("❌ No hay repositorio Git. Inicializando...")
        run_cmd("git init")
        run_cmd("git remote add origin https://github.com/ajsanchezv92/Geoportal-Scraper-Codespace.git")
    
    # Verificar remote
    success, output = run_cmd("git remote -v")
    if not success or "origin" not in output:
        print("🔧 Configurando remote...")
        run_cmd("git remote add origin https://github.com/ajsanchezv92/Geoportal-Scraper-Codespace.git")
    
    # Verificar rama
    run_cmd("git branch -M main")
    
    # Agregar archivos
    print("📁 Agregando archivos...")
    run_cmd("git add .")
    
    # Hacer commit
    print("💾 Haciendo commit...")
    run_cmd('git commit -m "Initial commit: complete geoportal scraper"')
    
    # Intentar push normal
    print("⬆️ Intentando push normal...")
    success, output = run_cmd("git push -u origin main")
    
    if not success:
        if "failed to push" in output or "rejected" in output:
            print("🔄 Intentando push forzado...")
            run_cmd("git push -f origin main")
        elif "couldn't find remote ref" in output:
            print("🌿 Creando rama main en remote...")
            run_cmd("git push -u origin main")
        elif "Updates were rejected" in output:
            print("🔄 Haciendo pull primero...")
            run_cmd("git pull origin main --allow-unrelated-histories")
            run_cmd("git push origin main")
    
    print("✅ Proceso completado!")
    run_cmd("git status")

if __name__ == "__main__":
    fix_git_issues()
