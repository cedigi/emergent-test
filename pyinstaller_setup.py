"""
Configuration spécialisée pour PyInstaller
Assure que toutes les dépendances sont incluses
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire de l'application au Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Configuration pour PyInstaller
a = Analysis(
    ['main.py'],
    pathex=[str(app_dir)],
    binaries=[],
    datas=[
        (str(app_dir / 'resources'), 'resources'),
        (str(app_dir / 'widgets'), 'widgets'),
    ],
    hiddenimports=[
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PetanqueManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_dir / 'resources' / 'logo.ico') if (app_dir / 'resources' / 'logo.ico').exists() else None,
)