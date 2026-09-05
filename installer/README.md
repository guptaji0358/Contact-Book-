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

Needs `pywin32` for shortcut creation (`pip install pywin32`). Build order:

```bash
python -m PyInstaller installer/uninstaller.spec --distpath dist --workpath build --noconfirm
python -m PyInstaller installer/pyside_installer.spec --distpath dist --workpath build --noconfirm
```

The first command freezes `pyside_installer/uninstaller_app.py` into
`dist/Uninstall.exe`. The second bundles `dist/ContactBook` *and*
`dist/Uninstall.exe` as the installer's payload, producing a single
`dist/ContactBookSetup.exe` — a wizard with its own dark, branded UI
(a step sidebar + status bar, not Inno Setup's default look):

1. **Welcome**
2. **License & Data Agreement** — states that contacts are stored locally
   only, that the app is a "rough book" and can't place real calls on its
   own, and that Phone Link must be set up separately for that. Next is
   disabled until the user checks "I agree".
3. **Options** — install folder, Desktop/Start Menu shortcut checkboxes
4. **Installing** — live progress bar + per-file status
5. **Finish** — optional "launch now"

It installs `Uninstall.exe` alongside the app and registers it (not a
`.bat`) as the "Add or Remove Programs" uninstall entry — running it kills
the app if open, removes shortcuts and the registry entry, then deletes
the install folder itself via a short delayed background command (since an
exe can't delete its own containing folder while running).

Both specs fail fast with a clear error if their prerequisite build hasn't
run yet.

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
