# -*- mode: python ; coding: utf-8 -*-
# Freezes uninstaller_app.py into Uninstall.exe. Build this BEFORE
# pyside_installer.spec, since that spec bundles this exe as part of its
# payload so it ends up installed alongside ContactBook.exe.

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(SPEC), ".."))

a = Analysis(
    [os.path.join(PROJECT_ROOT, "installer", "pyside_installer", "uninstaller_app.py")],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='Uninstall',
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
