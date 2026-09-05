<div align="center">

<img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/banner.png" alt="Contact Book" width="720">

<br><br>

[![Release](https://img.shields.io/github/v/release/guptaji0358/Contact-Book-?color=2563EB&label=release&style=flat-square)](https://github.com/guptaji0358/Contact-Book-/releases/latest)
[![Python](https://img.shields.io/badge/python-3.11%2B-2563EB?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-2563EB?logo=qt&logoColor=white&style=flat-square)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/platform-Windows-2563EB?logo=windows&logoColor=white&style=flat-square)](#-installation)
[![License](https://img.shields.io/badge/license-MIT-2563EB?style=flat-square)](#-license)

**A local-first desktop address book** — multiple contact books, VCF import/export
with drag-and-drop, and calling via Phone Link or direct LAN voice, all in a
clean PySide6 GUI. Your contacts never leave your machine.

[Download](#-download) · [Features](#-features) · [Architecture](#-architecture) · [Build from source](#-installation)

</div>

---

## 📥 Download

<table>
<tr>
<td width="56"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-download.png" width="40"></td>
<td>

Grab the latest Windows installer from the **[Releases page](https://github.com/guptaji0358/Contact-Book-/releases/latest)**
— download `ContactBookSetup.exe` and run it. No Python required.

It's a self-contained wizard that installs per-user (no admin rights needed),
creates Desktop/Start Menu shortcuts, and registers a proper uninstaller in
"Add or Remove Programs". See [`installer/README.md`](installer/README.md)
if you'd rather build it yourself.

</td>
</tr>
</table>

---

## 🚀 Features

<table>
<tr>
<td width="56" align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-books.png" width="40"></td>
<td width="45%">

**Multiple Contact Books**
Keep separate books (personal, work, whatever) and switch between them from
the book selector. Create, rename, and delete on the fly.

</td>
<td width="56" align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-search.png" width="40"></td>
<td>

**Fast, Live Search**
Filter contacts as you type, with the matching part of the name
highlighted — plus undo for accidental deletes.

</td>
</tr>
<tr>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-import.png" width="40"></td>
<td>

**VCF Import & Export**
Import from `.vcf` — browse, or just **drag and drop** the file onto the
window (with a pulsing drop-zone animation). Export back out anytime.

</td>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-call.png" width="40"></td>
<td>

**Calling**
Hand a number off to Phone Link (`tel:` links) for a real cellular call,
or place a direct LAN voice call to another device also running Contact
Book.

</td>
</tr>
<tr>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-lock.png" width="40"></td>
<td>

**Local-Only Storage**
Every contact lives in a SQLite file on your disk. Nothing is uploaded,
synced, or phoned home — ever.

</td>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/guptaji0358/Contact-Book-@main/assets/readme/icon-installer.png" width="40"></td>
<td>

**Real Windows Installer**
A custom-built PySide6 install wizard with its own license/data agreement
page, progress bar, and a proper GUI uninstaller.

</td>
</tr>
</table>

---

## 🏗 Architecture

The app is a `scripts/` package of PySide6 mixins, composed together into
one `ContactBookGUI` class:

```
42_CONTACT_BOOK.py          entry point
│
scripts/
├── gui.py                  composes all the mixins below
├── main_window.py          main window layout & wiring
├── table_helpers.py        contact table, search/filter, selection
├── add_dialog.py / edit_dialog.py / view_dialog.py / delete_dialog.py
├── import_export.py        VCF import/export + drag-and-drop
├── call_dialog.py          call screen + tel: handoff
├── voip_engine.py          LAN voice calling (sockets + sounddevice)
├── books_ui.py / books_registry.py   multiple contact books
├── phone_rules.py          country codes & validation
└── icons.py / styles.py    SVG icons & Qt stylesheets
```

Each contact book is its own SQLite file under `books/`, tracked in a small
registry database (`CONTACT_BOOKS.db`) that maps book name → file path.

---

## 🧰 Tech Stack

<div align="left">

![Python](https://img.shields.io/badge/Python-language-2563EB?logo=python&logoColor=white&style=flat-square)
![PySide6](https://img.shields.io/badge/PySide6-GUI-2563EB?logo=qt&logoColor=white&style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-storage-2563EB?logo=sqlite&logoColor=white&style=flat-square)
![sounddevice](https://img.shields.io/badge/sounddevice-audio-2563EB?style=flat-square)
![pywin32](https://img.shields.io/badge/pywin32-Windows%20shortcuts-2563EB?style=flat-square)
![PyInstaller](https://img.shields.io/badge/PyInstaller-packaging-2563EB?style=flat-square)

</div>

| Technology | Purpose |
|---|---|
| Python | Programming language |
| PySide6 | GUI framework (Qt for Python) |
| SQLite | Per-book contact storage |
| sounddevice / numpy | LAN voice calling audio |
| pywin32 | Windows shortcuts (installer) |
| PyInstaller | Freezing the app into an `.exe` |
| VCF | Contact import/export format |

---

## ⚙ Installation

### Option A — Download the installer (recommended)

Download `ContactBookSetup.exe` from the **[latest release](https://github.com/guptaji0358/Contact-Book-/releases/latest)**
and run it.

### Option B — Run from source

```bash
git clone https://github.com/guptaji0358/Contact-Book-.git
cd Contact-Book-
pip install PySide6 sounddevice numpy pywin32
python 42_CONTACT_BOOK.py
```

---

## 📥 Import Example

```
BEGIN:VCARD
VERSION:3.0
FN:Naruto Uzumaki
TEL:+81 9012345678
EMAIL:naruto@leaf.com
END:VCARD
```

The Import window shows how many contacts it detected before you commit:

```
Contacts detected: 25
```

## 📤 Export Example

```
BEGIN:VCARD
VERSION:3.0
FN:Gojo Satoru
TEL:+81 9012345679
EMAIL:gojo@jujutsu.com
END:VCARD
```

---

## 🔓 Customization & Contributions

This project is open for customization and learning. Fork it, poke at it,
break it, rebuild it — ideas welcome:

- Improve the UI
- Add new features
- Change validation rules
- Extend import/export formats

---

## 👨‍💻 Author

**Robin Gupta** — Python developer, learning desktop GUI development.

## 📜 License

MIT License
