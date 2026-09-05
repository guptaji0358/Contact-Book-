# -*- mode: python ; coding: utf-8 -*-
# Freezes the PySide6 installer wizard (pyside_installer/app.py) into
# ContactBookSetup.exe, bundling the already-frozen app (dist/ContactBook,
# built via installer/ContactBook.spec) as its "payload" data folder.
#
# Build order:
#   1. python -m PyInstaller installer/ContactBook.spec --distpath dist --workpath build
#   2. python -m PyInstaller installer/pyside_installer.spec --distpath dist --workpath build

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(SPEC), ".."))
FROZEN_APP_DIR = os.path.join(PROJECT_ROOT, "dist", "ContactBook")

if not os.path.isdir(FROZEN_APP_DIR):
    raise SystemExit(
        f"Frozen app not found at {FROZEN_APP_DIR}. "
        "Build installer/ContactBook.spec first."
    )

a = Analysis(
    [os.path.join(PROJECT_ROOT, "installer", "pyside_installer", "app.py")],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=[
        (FROZEN_APP_DIR, "payload"),
        (os.path.join(PROJECT_ROOT, "CONTACT_BOOK_ICON.ico"), "payload"),
    ],
    hiddenimports=["win32com.client", "winreg"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ContactBookSetup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(PROJECT_ROOT, "CONTACT_BOOK_ICON.ico")],
)
