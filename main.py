#!/usr/bin/env python3
"""
Pétanque Manager - Application de gestion de tournois de pétanque
Point d'entrée principal de l'application
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
from gui import MainWindow

def main():
    """Fonction principale de l'application"""
    # Création de la fenêtre racine
    root = tk.Tk()
    root.title("Pétanque Manager v1.0")
    root.geometry("1200x800")
    
    # Configuration pour les écrans haute résolution
    try:
        root.tk.call('tk', 'scaling', 1.2)
    except tk.TclError:
        pass  # Ignore si la commande n'est pas supportée
    
    # Icône de l'application
    icon_path = 'resources/logo.png'
    if os.path.exists(icon_path):
        try:
            root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except tk.TclError:
            pass  # Ignore si l'icône ne peut pas être chargée
    
    # Style moderne
    style = ttk.Style()
    style.theme_use('clam')  # Thème moderne
    
    # Configuration des couleurs personnalisées
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    style.configure('Custom.Treeview', rowheight=25)
    
    # Création et configuration de la fenêtre principale
    app = MainWindow(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Lancement de la boucle d'événements
    root.mainloop()

if __name__ == '__main__':
    main()