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

        MainLayout = QVBoxLayout(self.DeleteContactsWindow)
        MainLayout.setContentsMargins(30, 15, 30, 15)
        MainLayout.setSpacing(15)

        self.DeleteContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteContactLabel.setText("Delete Contact")
        self.DeleteContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.DeleteContactLabel.setAlignment(Qt.AlignCenter)
        MainLayout.addWidget(self.DeleteContactLabel)

        FormLayout = QFormLayout()
        FormLayout.setSpacing(12)
        FormLayout.setLabelAlignment(Qt.AlignLeft)

        self.DeleteNameLabel = QLabel("Name ->")
        self.DeleteNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteNameContactLabel = QLabel(Name)
        self.DeleteNameContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.DeleteNameLabel, self.DeleteNameContactLabel)

        self.DeletePhoneNoLabel = QLabel("Phone No. ->")
        self.DeletePhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeletePhoneNoContactLabel = QLabel(PhoneNo)
        self.DeletePhoneNoContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.DeletePhoneNoLabel, self.DeletePhoneNoContactLabel)

        self.DeleteEmailLabel = QLabel("Email ->")
        self.DeleteEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.DeleteEmailContactLabel = QLabel(Email)
        self.DeleteEmailContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.DeleteEmailLabel, self.DeleteEmailContactLabel)

        MainLayout.addLayout(FormLayout)
        MainLayout.addStretch(1)

        ButtonRow = QHBoxLayout()
        ButtonRow.addStretch(1)

        self.CancelButton = QPushButton(self.DeleteContactsWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.setFixedSize(130, 30)
        self.CancelButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.DeleteContactsWindow))
        ButtonRow.addWidget(self.CancelButton)

        self.DeleteButton = QPushButton(self.DeleteContactsWindow)
        self.DeleteButton.setText("Delete")
        self.DeleteButton.setFixedSize(130, 30)
        self.DeleteButton.setStyleSheet(RED_BUTTON_STYLE)
        self.DeleteButton.setCursor(Qt.PointingHandCursor)
        self.DeleteButton.clicked.connect(self.DeleteSelectedContact)
        ButtonRow.addWidget(self.DeleteButton)

        MainLayout.addLayout(ButtonRow)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.DeleteContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.DeleteContactsWindow.close())

        self.DeleteContactsWindow.show()
        self.DisableMaximizeButton(self.DeleteContactsWindow)
