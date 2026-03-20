# Contact-Book
DAY - 42/100 - Project - Contact Book

# 📒 Contact Book Desktop Application

A **Desktop Contact Management Application** built using **Python and PySide6**.

This application allows users to **add, edit, delete, search, import, and export contacts** using a simple and intuitive graphical interface.

Contacts are stored in **JSON format**, and the application supports **VCF (vCard)** files for importing and exporting contacts.

---

# 🚀 Features

## Contact Management

- Add new contacts
- Edit existing contacts
- Delete contacts
- Undo deleted contacts

## Search

- Real-time search filtering
- Highlights matched names

## Import Contacts

- Import contacts from **VCF (.vcf)** files
- Detects number of contacts before importing
- Supports bulk imports

## Export Contacts

- Export all contacts to **VCF format**
- Compatible with phones and contact applications

## Phone Number Validation

- Country code support
- Digit validation rules
- Special handling for Japan numbers

## Data Storage

Contacts are stored locally using **JSON**.

Advantages:

- Fast loading
- Easy modification
- Lightweight storage

---

# 🏗 Application Architecture

The project follows a **modular architecture** separating GUI and logic.


main file
│
├── CONTACT_BOOK_GUI.py
│ (User Interface)
│
├── CONTACT_BOOK_MANAGER.py
│ (Contact Logic + File Handling)
│
└── CONTACT_BOOK_CONTACTS.json
(Contact Database)


---

# 📂 Project Structure


ContactBook
│
├── 42_CONTACTS_BOOK.py
├── CONTACT_BOOK_GUI.py
├── CONTACT_BOOK_MANAGER.py
├── CONTACT_BOOK_CONTACTS.json
├── CONTACTS.vcf
└── README.md


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
git clone https://github.com/YOUR_USERNAME/contact-book.git
cd contact-book
Install Dependencies
pip install PySide6
Run the Application
python 42_CONTACTS_BOOK.py

The main application file is:

42_CONTACTS_BOOK.py

This file starts the application and loads the GUI.

The main script imports the GUI and Manager modules.
See implementation in:

🖥 Application Interface

Main window includes:

Search bar

Contact table

Add button

Edit button

Delete button

Import button

Export button

The UI is implemented in:

📥 Import Contacts

The application can import contacts from VCF files.

Example VCF format:

BEGIN:VCARD
VERSION:3.0
FN:Naruto Uzumaki
TEL:+81 9012345678
EMAIL:naruto@leaf.com
END:VCARD

The import logic reads and parses VCF lines and extracts:

Name

Phone

Email

Implementation located in:

📤 Export Contacts

Contacts can be exported into a VCF file compatible with:

Android

iPhone

Google Contacts

Outlook

Example exported contact:

BEGIN:VCARD
VERSION:3.0
FN:Gojo Satoru
TEL:+81 9012345679
EMAIL:gojo@jujutsu.com
END:VCARD
🔍 Search Functionality

The application supports dynamic search filtering.

Features:

Real-time filtering

Highlighted matching text

Case-insensitive search

🧪 Testing

The application has been tested with:

Small datasets (25 contacts)

Medium datasets (200 contacts)

Large datasets (1000+ contacts)

Edge cases handled:

Missing phone numbers

Missing emails

Duplicate contacts

📈 Future Improvements

Possible future enhancements:

Dark mode theme

Contact groups

Contact images

SQLite database storage

Drag-and-drop VCF import

Sorting contacts

👨‍💻 Author

Robin Gupta

Python Developer
Learning GUI Application Development

📜 License

This project is licensed under the MIT License.

⭐ Acknowledgements

Python Community

PySide6 Documentation

Open Source Learning Resources
