# Building the Windows Installer

Two steps: freeze the app with PyInstaller, then wrap it with Inno Setup.

## 1. Freeze the app

From the project root:

```bash
python -m PyInstaller installer/ContactBook.spec --distpath dist --workpath build --noconfirm
```

This produces `dist/ContactBook/ContactBook.exe` plus its `_internal` runtime
folder. Run `dist/ContactBook/ContactBook.exe` directly to sanity-check the
build before packaging it.

## 2. Build the installer

Requires [Inno Setup](https://jrsoftware.org/isinfo.php) (free). Install it,
then either:

- Open `installer/ContactBook.iss` in the Inno Setup Compiler and click Compile, or
- Run from a terminal: `ISCC installer\ContactBook.iss`

The finished installer is written to `installer/Output/ContactBook-Setup.exe`.

## Notes

- The installer installs per-user under `%LOCALAPPDATA%\Programs\Contact Book`
  (no admin rights needed) rather than Program Files, because the app stores
  its contact databases next to its own exe at runtime and Program Files
  isn't writable by standard users.
- Bump `MyAppVersion` in `ContactBook.iss` before cutting a new release.
- `dist/`, `build/`, and `installer/Output/` are build output and are
  gitignored — only the `.spec` and `.iss` source files are committed.
