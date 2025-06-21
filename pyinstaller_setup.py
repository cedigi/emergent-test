"""
Configuration spécialisée pour PyInstaller
Assure que toutes les dépendances sont incluses
Ce fichier sera généré automatiquement par PyInstaller
"""

# Ce fichier de configuration sera utilisé par PyInstaller
# Pour l'exécuter, utilisez: pyinstaller pyinstaller_setup.spec

# Configuration des imports cachés nécessaires
hidden_imports = [
    'tkinter',
    'tkinter.ttk', 
    'tkinter.filedialog',
    'tkinter.messagebox',
    'sqlite3',
    'reportlab.pdfgen',
    'reportlab.lib',
    'reportlab.platypus',
    'uuid',
    'datetime',
    'json',
]

# Données à inclure dans l'exécutable
datas = [
    ('resources', 'resources'),
    ('widgets', 'widgets'),
]

# Configuration pour l'exécutable final
exe_config = {
    'name': 'PetanqueManager',
    'console': False,  # Mode fenêtré
    'icon': 'resources/logo.ico',  # Si disponible
    'onefile': True,   # Un seul fichier
}

print("Configuration PyInstaller pour Pétanque Manager")
print("Utilisez build_exe.py pour créer l'exécutable automatiquement")
