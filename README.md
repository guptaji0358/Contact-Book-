# Contact-Book
DAY - 42/100 - Project - Contact Book
# 📒 Contact Book Desktop Application

A **Desktop Contact Management Application** built using **Python and PySide6**.

It supports **multiple contact books, add/edit/delete/search, VCF import & export (including drag-and-drop), and LAN voice calling** between two devices both running Contact Book, all in a simple graphical interface.

Contacts are stored locally in **SQLite** databases — nothing is uploaded anywhere.

---

# 📥 Download

Grab the latest Windows installer from the [Releases page](https://github.com/guptaji0358/Contact-Book-/releases/latest) —
download `ContactBookSetup.exe` and run it. It's a self-contained wizard
(no Python install required) that installs per-user, creates shortcuts,
and registers a proper uninstaller — see [Installation](#-installation) below
for details and for running from source instead.

---

# 🚀 Features

## Contact Management

- Add new contacts
- Edit existing contacts
- Delete contacts (with Undo)
- Real-time search with highlighted matches

## Multiple Contact Books

- Keep separate books (e.g. personal, work) and switch between them
- Create, rename, and delete books from the book selector

## Import / Export

- Import contacts from **VCF (.vcf)** files — browse, or just **drag and drop**
  the file onto the Import window (with a pulsing drop-zone animation)
- Detects the number of contacts before importing
- Export contacts back to VCF, compatible with phone contact apps

## Phone Validation

- Country code support
- Digit validation rules per country
- Special rule for Japan numbers

## Calling

- Dial a contact's number through whatever app Windows has registered for
  `tel:` links (e.g. Microsoft Phone Link, once you've linked your phone) —
  the app hands the number off in the background without stealing focus
- Or place a direct LAN voice call to another device also running Contact
  Book, if that contact has a Device IP set

## Data Storage

Contacts are stored locally per-book in **SQLite** databases under `books/`.
Nothing is synced or uploaded — see the installer's License & Data
Agreement page for the full statement.

---

# 🏗 Project Architecture

The app is a `scripts/` package of PySide6 mixins, composed together in
`ContactBookGUI`:

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
├── icons.py / styles.py    SVG icons & Qt stylesheets
```

Each contact book is its own SQLite file under `books/`, tracked in a
small registry database (`CONTACT_BOOKS.db`) that maps book name -> file.

---

# 🧰 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Programming language |
| PySide6 | GUI framework |
| SQLite | Per-book contact storage |
| sounddevice / numpy | LAN voice calling audio |
| pywin32 | Windows shortcuts (installer) |
| PyInstaller | Freezing the app into an .exe |
| VCF | Contact import/export format |

---

# ⚙ Installation

## Option A: Download the installer (recommended)

Download `ContactBookSetup.exe` from the [latest release](https://github.com/guptaji0358/Contact-Book-/releases/latest)
and run it. See `installer/README.md` if you want to build it yourself.

## Option B: Run from source

```bash
git clone https://github.com/guptaji0358/Contact-Book-.git
cd Contact-Book-
pip install PySide6 sounddevice numpy pywin32
python 42_CONTACT_BOOK.py
```

---

# 📥 Import Example

Example VCF format:

```
BEGIN:VCARD
VERSION:3.0
FN:Naruto Uzumaki
TEL:+81 9012345678
EMAIL:naruto@leaf.com
END:VCARD
```

During import the application shows detection:

```
Contacts detected: 25
```

---

# 📤 Export Example

Exported contact format:

```
BEGIN:VCARD
VERSION:3.0
FN:Gojo Satoru
TEL:+81 9012345679
EMAIL:gojo@jujutsu.com
END:VCARD
```

---

# 🔍 Search

The application supports **dynamic search filtering** across name, phone,
and email, with the matching part of the name highlighted.

---

# 🔓 Customization & Contributions

This project is open for customization and learning.

Anyone can download the source code and modify it according to their needs.

Possible things you can do:

- Improve the UI
- Add new features
- Change validation rules
- Extend import/export formats

If you have ideas or improvements, feel free to modify the project or suggest enhancements.

This project is meant for **learning, experimentation, and further development**.

---

# 👨‍💻 Author

Robin Gupta

Python Developer
Learning Desktop GUI Development

---

# 📜 License

MIT License
