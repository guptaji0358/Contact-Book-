import os
import re
import sqlite3

REGISTRY_DB = "CONTACT_BOOKS.db"
BOOKS_DIR = "books"


def _Connect():
    conn = sqlite3.connect(REGISTRY_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            file_path TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def _SafeFileName(name):
    safe = re.sub(r"[^A-Za-z0-9 _-]", "", name).strip()
    return safe or "Book"


def ListBooks():
    conn = _Connect()
    rows = conn.execute("SELECT id, name, file_path FROM books ORDER BY name").fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "file_path": row[2]} for row in rows]


def CreateBook(name):
    os.makedirs(BOOKS_DIR, exist_ok=True)

    file_stub = _SafeFileName(name)
    file_path = os.path.join(BOOKS_DIR, f"{file_stub}.db")
    suffix = 1

    while os.path.exists(file_path):
        suffix += 1
        file_path = os.path.join(BOOKS_DIR, f"{file_stub}_{suffix}.db")

    conn = _Connect()
    conn.execute("INSERT INTO books (name, file_path) VALUES (?, ?)", (name, file_path))
    conn.commit()
    conn.close()

    schema_conn = sqlite3.connect(file_path)
    schema_conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            device_ip TEXT DEFAULT ''
        )
    """)
    schema_conn.commit()
    schema_conn.close()

    return {"name": name, "file_path": file_path}


def RenameBook(book_id, new_name):
    conn = _Connect()
    conn.execute("UPDATE books SET name=? WHERE id=?", (new_name, book_id))
    conn.commit()
    conn.close()


def DeleteBook(book_id):
    conn = _Connect()
    row = conn.execute("SELECT file_path FROM books WHERE id=?", (book_id,)).fetchone()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    if row and os.path.exists(row[0]):
        os.remove(row[0])


def EnsureDefaultBook():
    books = ListBooks()

    if books:
        return books

    CreateBook("Default")
    return ListBooks()
