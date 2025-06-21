#!/usr/bin/env python3
"""
Pétanque Manager - Application de gestion de tournois de pétanque
Point d'entrée principal de l'application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from gui import MainWindow

def setup_high_dpi():
    """Configure l'application pour les écrans haute résolution"""
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def load_stylesheet(app, theme='light'):
    """Charge la feuille de style selon le thème"""
    theme_file = f'styles/{theme}_theme.qss'
    if os.path.exists(theme_file):
        with open(theme_file, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

def main():
    """Fonction principale de l'application"""
    # Configuration haute DPI
    setup_high_dpi()
    
    # Création de l'application
    app = QApplication(sys.argv)
    app.setApplicationName("Pétanque Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Pétanque Manager")
    
    # Chargement du thème par défaut
    load_stylesheet(app, 'light')
    
    # Icône de l'application
    icon_path = 'resources/logo.png'
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Création et affichage de la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Lancement de la boucle d'événements
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()