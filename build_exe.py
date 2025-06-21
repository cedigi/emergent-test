#!/usr/bin/env python3
"""
Script de construction d'exécutable pour Pétanque Manager
Utilise PyInstaller pour créer un exécutable Windows
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("✓ PyInstaller déjà installé")
        return True
    except ImportError:
        print("📦 Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("✗ Échec de l'installation de PyInstaller")
            return False

def create_exe():
    """Crée l'exécutable avec PyInstaller"""
    print("🔨 Création de l'exécutable...")
    
    # Paramètres PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Un seul fichier exécutable
        "--windowed",                   # Mode fenêtré (pas de console)
        "--name=PetanqueManager",       # Nom de l'exécutable
        "--distpath=dist",              # Dossier de sortie
        "--workpath=build",             # Dossier de travail
        "--specpath=.",                 # Dossier du fichier .spec
        "main.py"                       # Fichier principal
    ]
    
    # Ajouter l'icône si disponible
    icon_path = Path("resources/logo.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    # Ajouter les données nécessaires
    cmd.extend([
        "--add-data", "resources;resources",  # Inclure le dossier resources
    ])
    
    try:
        subprocess.check_call(cmd)
        print("✓ Exécutable créé avec succès dans le dossier 'dist'")
        return True
    except subprocess.CalledProcessError:
        print("✗ Échec de la création de l'exécutable")
        return False

def create_installer_script():
    """Crée un script d'installation simple"""
    installer_content = '''@echo off
echo ==================================================
echo        PÉTANQUE MANAGER - Installation
echo ==================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8+ depuis https://python.org
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo ✓ Python détecté

REM Installer les dépendances
echo 📦 Installation des dépendances...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Échec de l'installation des dépendances
    pause
    exit /b 1
)

echo ✓ Dépendances installées

REM Tester l'application
echo 🧪 Test de l'application...
python test_console.py

if %errorlevel% neq 0 (
    echo ❌ Échec du test de l'application
    pause
    exit /b 1
)

echo.
echo ✅ Installation terminée avec succès!
echo.
echo Pour lancer l'application:
echo   python main.py
echo.
echo Pour créer un exécutable:
echo   python build_exe.py
echo.
pause
'''
    
    with open("install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✓ Script d'installation créé: install.bat")

def create_launcher_script():
    """Crée un script de lancement simple"""
    launcher_content = '''@echo off
echo 🎯 Lancement de Pétanque Manager...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors du lancement
    echo Vérifiez que Python et les dépendances sont installés
    echo Exécutez install.bat si nécessaire
    pause
)
'''
    
    with open("launch.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✓ Script de lancement créé: launch.bat")

def main():
    """Fonction principale de construction"""
    print("🏗️  PÉTANQUE MANAGER - Constructeur d'Exécutable")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("main.py").exists():
        print("❌ Fichier main.py introuvable")
        print("Assurez-vous d'être dans le répertoire de l'application")
        return False
    
    # Créer les scripts d'installation et de lancement
    create_installer_script()
    create_launcher_script()
    
    # Demander si l'utilisateur veut créer l'exécutable
    print("\n" + "=" * 60)
    print("Options disponibles:")
    print("1. Créer un exécutable Windows (.exe)")
    print("2. Quitter")
    
    try:
        choice = input("\nVotre choix (1-2): ").strip()
        
        if choice == "1":
            if install_pyinstaller():
                if create_exe():
                    print("\n" + "=" * 60)
                    print("🎉 Construction terminée!")
                    print(f"📁 Exécutable disponible dans: {Path('dist').absolute()}")
                    print("\nFichiers créés:")
                    print("- PetanqueManager.exe (exécutable principal)")
                    print("- install.bat (script d'installation)")
                    print("- launch.bat (script de lancement)")
                else:
                    return False
            else:
                return False
        
        elif choice == "2":
            print("👋 Au revoir!")
            return True
        
        else:
            print("❌ Choix invalide")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
        return True
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)