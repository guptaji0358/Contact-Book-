# Contact-Book
DAY - 42/100 - Project - Contact Book
# 📒 Contact Book Desktop Application

A **Desktop Contact Management Application** built using **Python and PySide6**.

This application allows users to **add, edit, delete, search, import, and export contacts** using a simple graphical interface.

Contacts are stored in **JSON format**, and the application supports **VCF (vCard)** files for importing and exporting contacts.

---

# 🚀 Features

## Contact Management

- Add new contacts
- Edit existing contacts
- Delete contacts
- Undo deleted contacts

## Search

- Real-time contact search
- Highlight matching names

## Import Contacts

- Import contacts from **VCF (.vcf)** files
- Detect number of contacts before importing
- Supports bulk imports

## Export Contacts

- Export contacts to **VCF format**
- Compatible with phone contact apps

## Phone Validation

- Country code support
- Digit validation rules
- Special rule for Japan numbers

## Data Storage

Contacts are stored locally using **JSON**.

Advantages:

- Fast loading
- Lightweight storage
- Easy modification

---

# 🏗 Project Architecture

The project follows a **modular architecture** separating UI and logic.

```
main file
│
├── CONTACT_BOOK_GUI.py
│     (User Interface)
│
├── CONTACT_BOOK_MANAGER.py
│     (Contact Logic + File Handling)
│
└── CONTACT_BOOK_CONTACTS.json
      (Contact Database)
```

---

# 📂 Project Structure

```
ContactBook
│
├── 42_CONTACTS_BOOK.py
├── CONTACT_BOOK_GUI.py
├── CONTACT_BOOK_MANAGER.py
├── CONTACT_BOOK_CONTACTS.json
├── CONTACTS.vcf
└── README.md
```

---

# 🧰 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Programming Language |
| PySide6 | GUI Framework |
| JSON | Data Storage |
| VCF | Contact Import/Export Format |

---

# ⚙ Installation

## Clone the Repository

```bash
git clone https://github.com/guptaji0358/Contact-Book-.git
cd Contact-Book-
```

---

## Install Dependencies

```bash
pip install PySide6
```

---

## Run the Application

```bash
python 42_CONTACTS_BOOK.py
```

The main application file is:

```
42_CONTACTS_BOOK.py
```

This file starts the application and loads the GUI.

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

The application supports **dynamic search filtering**.

Features:

- Case-insensitive search
- Highlighted matching text
- Fast filtering

---

# 🧪 Testing

The application has been tested with:

- 25 contacts
- 1000 contacts

Edge cases handled:

- Missing phone numbers
- Missing emails
- Duplicate contacts
---

# 🔓 Customization & Contributions

This project is open for customization and learning.

Anyone can download the source code and modify it according to their needs.

Possible things you can do:

- Improve the UI
- Add new features
- Change validation rules
- Connect a database
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
