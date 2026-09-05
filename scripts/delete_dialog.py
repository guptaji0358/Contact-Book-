from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_TITLE_STYLE, DIALOG_LABEL_STYLE, BLUE_BUTTON_STYLE, RED_BUTTON_STYLE

ICON_PATH = "CONTACT_BOOK_ICON.png"


class DeleteDialogMixin:
    def ShowUndoMessage(self):
        msg = QMessageBox(self.MainWindow)
        msg.setWindowTitle("Contact Deleted")
        msg.setText("Contact deleted successfully.")

        undo_btn = msg.addButton("Undo", QMessageBox.ActionRole)
        msg.addButton("OK", QMessageBox.AcceptRole)
        msg.exec()

        if msg.clickedButton() == undo_btn:
            self.UndoDelete()

    def UndoDelete(self):
        if self.LastDeletedContact is None:
            return

        contact_id, name, phone, email = self.LastDeletedContact

        self.Manager.addContacts(id=contact_id, name=name, phone=phone, email=email)

        self.LastDeletedContact = None
        self.LoadContactsIntoTable()

    def DeleteSelectedContact(self):
        row = self.DeletingRow
        name = self.GetNameFromRow(row)
        phone = self.RecentsContactTable.item(row, 2).text().strip()
        email = self.RecentsContactTable.item(row, 3).text().strip()
        contact_id = self.RecentsContactTable.item(row, 2).data(Qt.UserRole)

        reply = QMessageBox.warning(
            self.DeleteContactsWindow,
            "Confirm Delete",
            f"This Contact will permanently delete:\n{name}\n\nRecovery is not guaranteed.\n"
            "The creator is not responsible for lost contacts.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        self.LastDeletedContact = (contact_id, name, phone, email)
        self.RecentsContactTable.removeRow(row)

        contacts = self.Manager.LoadContactsJSON()

        for i, contact in enumerate(contacts):
            if contact.get("id") == contact_id:
                self.Manager.DeleteContactJSON(index=i)
                break

        self.LoadContactsIntoTable()
        self.DeleteContactsWindow.close()
        self.ShowUndoMessage()

    def DeleteContacts(self):
        DeleteData = self.GetSelectedRow()

        if DeleteData is None:
            return

        self.DeletingRow = DeleteData

        Name = self.GetNameFromRow(DeleteData)
        PhoneNo = self.RecentsContactTable.item(DeleteData, 2).text().strip()
        Email = self.RecentsContactTable.item(DeleteData, 3).text().strip()

        self.DeleteContactsWindow = QWidget()
        self.DeleteContactsWindow.setWindowTitle("Delete Contact Details")
        self.DeleteContactsWindow.resize(420, 250)
        self.DeleteContactsWindow.setWindowIcon(QIcon(ICON_PATH))

        self.DeleteContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteContactLabel.setText("Delete Contact")
        self.DeleteContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.DeleteContactLabel.move(85, 10)

        self.DeleteNameLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteNameLabel.setText("Name ->")
        self.DeleteNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteNameLabel.move(30, 80)

        self.DeleteNameContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteNameContactLabel.setText(Name)
        self.DeleteNameContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteNameContactLabel.move(160, 80)

        self.DeletePhoneNoLabel = QLabel(self.DeleteContactsWindow)
        self.DeletePhoneNoLabel.setText("Phone No. ->")
        self.DeletePhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeletePhoneNoLabel.move(30, 120)

        self.DeletePhoneNoContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeletePhoneNoContactLabel.setText(PhoneNo)
        self.DeletePhoneNoContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeletePhoneNoContactLabel.move(160, 120)

        self.DeleteEmailLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteEmailLabel.setText("Email ->")
        self.DeleteEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteEmailLabel.move(30, 160)

        self.DeleteEmailContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteEmailContactLabel.setText(Email)
        self.DeleteEmailContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteEmailContactLabel.move(160, 160)

        self.CancelButton = QPushButton(self.DeleteContactsWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.resize(130, 30)
        self.CancelButton.move(80, 210)
        self.CancelButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.DeleteContactsWindow))

        self.DeleteButton = QPushButton(self.DeleteContactsWindow)
        self.DeleteButton.setText("Delete")
        self.DeleteButton.resize(130, 30)
        self.DeleteButton.move(240, 210)
        self.DeleteButton.setStyleSheet(RED_BUTTON_STYLE)
        self.DeleteButton.setCursor(Qt.PointingHandCursor)
        self.DeleteButton.clicked.connect(self.DeleteSelectedContact)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.DeleteContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.DeleteContactsWindow.close())

        self.DeleteContactsWindow.show()
        self.DisableMaximizeButton(self.DeleteContactsWindow)
