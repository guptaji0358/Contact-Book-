# Building the Windows Installer

There are two installer options in this folder:

- **`pyside_installer/`** (recommended) — a custom install wizard written in
  PySide6, so its UI matches the app instead of Inno Setup's default look.
- **`ContactBook.iss`** — the original Inno Setup wizard, kept as a fallback.

Both wrap the same frozen app, so step 1 is shared.

## 1. Freeze the app

From the project root:

```bash
python -m PyInstaller installer/ContactBook.spec --distpath dist --workpath build --noconfirm
```

This produces `dist/ContactBook/ContactBook.exe` plus its `_internal` runtime
folder. Run `dist/ContactBook/ContactBook.exe` directly to sanity-check the
build before packaging it.

## 2a. Build the PySide6 installer (recommended)

Needs `pywin32` for shortcut creation (`pip install pywin32`). Then:

```bash
python -m PyInstaller installer/pyside_installer.spec --distpath dist --workpath build --noconfirm
```

This bundles `dist/ContactBook` as the installer's payload and produces a
single `dist/ContactBookSetup.exe` — a self-contained wizard (welcome ->
choose folder/shortcuts -> progress bar -> finish) that copies the app,
creates Desktop/Start Menu shortcuts, and registers an uninstall entry
(`uninstall.bat`, listed in "Add or Remove Programs" via the registry).

The spec fails fast with a clear error if step 1 hasn't been run yet.

## 2b. Build the Inno Setup installer (fallback)

Requires [Inno Setup](https://jrsoftware.org/isinfo.php). Then either:

- Open `installer/ContactBook.iss` in the Inno Setup Compiler and click Compile, or
- Run from a terminal: `ISCC installer\ContactBook.iss`

The finished installer is written to `installer/Output/ContactBook-Setup.exe`.

## Notes

- Both installers install per-user under `%LOCALAPPDATA%\Programs\Contact Book`
  (no admin rights needed) rather than Program Files, because the app stores
  its contact databases next to its own exe at runtime and Program Files
  isn't writable by standard users.
- Bump `APP_VERSION` in `pyside_installer/app.py` (and `MyAppVersion` in
  `ContactBook.iss` if you still build that one) before cutting a release.
- `dist/`, `build/`, and `installer/Output/` are build output and are
  gitignored — only the `.spec`, `.iss`, and `pyside_installer/` source
  files are committed.
