from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.books_registry import ListBooks, CreateBook, RenameBook, DeleteBook, EnsureDefaultBook


class BooksMixin:
    def InitBooks(self):
        self.Books = EnsureDefaultBook()
        self.ActiveBookID = self.Books[0]["id"]
        self.ActiveBookPath = self.Books[0]["file_path"]

    def RefreshBookSelector(self):
        self.BookSelector.blockSignals(True)
        self.BookSelector.clear()

        for book in self.Books:
            self.BookSelector.addItem(book["name"], book["id"])

        index = self.BookSelector.findData(self.ActiveBookID)
        if index != -1:
            self.BookSelector.setCurrentIndex(index)

        self.BookSelector.blockSignals(False)

    def SwitchActiveBook(self):
        book_id = self.BookSelector.currentData()

        if book_id is None or book_id == self.ActiveBookID:
            return

        book = next((b for b in self.Books if b["id"] == book_id), None)
        if book is None:
            return

        self.ActiveBookID = book["id"]
        self.ActiveBookPath = book["file_path"]
        self.Manager.SetDatabase(book["file_path"])
        self.LoadContactsIntoTable()

    def CreateNewBook(self):
        name, ok = QInputDialog.getText(self.MainWindow, "New Book", "Book name:")

        if not ok or not name.strip():
            return

        try:
            new_book = CreateBook(name.strip())
        except Exception:
            QMessageBox.warning(self.MainWindow, "Could Not Create Book", "A book with that name already exists.")
            return

        self.Books = ListBooks()
        self.ActiveBookID = next(b["id"] for b in self.Books if b["file_path"] == new_book["file_path"])
        self.ActiveBookPath = new_book["file_path"]
        self.Manager.SetDatabase(self.ActiveBookPath)

        self.RefreshBookSelector()
        self.LoadContactsIntoTable()

    def ShowBookContextMenu(self, position):
        menu = QMenu(self.BookSelector)
        rename_action = menu.addAction("Rename Book")
        delete_action = menu.addAction("Delete Book")

        action = menu.exec(self.BookSelector.mapToGlobal(position))

        if action == rename_action:
            self.RenameActiveBook()
        elif action == delete_action:
            self.DeleteActiveBook()

    def RenameActiveBook(self):
        current_name = self.BookSelector.currentText()
        new_name, ok = QInputDialog.getText(self.MainWindow, "Rename Book", "New name:", text=current_name)

        if not ok or not new_name.strip():
            return

        try:
            RenameBook(self.ActiveBookID, new_name.strip())
        except Exception:
            QMessageBox.warning(self.MainWindow, "Could Not Rename Book", "A book with that name already exists.")
            return

        self.Books = ListBooks()
        self.RefreshBookSelector()

    def DeleteActiveBook(self):
        if len(self.Books) <= 1:
            QMessageBox.warning(self.MainWindow, "Cannot Delete", "You must keep at least one contact book.")
            return

        reply = QMessageBox.warning(
            self.MainWindow,
            "Delete Book",
            f"Permanently delete the book \"{self.BookSelector.currentText()}\" and all its contacts?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        DeleteBook(self.ActiveBookID)
        self.Books = ListBooks()
        self.ActiveBookID = self.Books[0]["id"]
        self.ActiveBookPath = self.Books[0]["file_path"]
        self.Manager.SetDatabase(self.ActiveBookPath)

        self.RefreshBookSelector()
        self.LoadContactsIntoTable()
