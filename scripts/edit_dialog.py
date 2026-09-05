from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_TITLE_STYLE, DIALOG_LABEL_STYLE, INPUT_STYLE, BLUE_BUTTON_STYLE, RED_BUTTON_STYLE
from scripts.phone_rules import COUNTRY_CODES, validate_phone

ICON_PATH = "CONTACT_BOOK_ICON.png"


class EditDialogMixin:
    def SaveEditedContact(self):
        Name = self.AsksName.text().title().strip()
        PhoneDigits = self.AskPhoneNo.text().strip()
        Email = self.AsksEmail.text().strip()
        DeviceIP = self.AsksDeviceIP.text().strip()
        code = self.CountryCodeContactDropdownforEdit.currentText().split()[0]

        if not validate_phone(code, PhoneDigits, self.EditContactWindow, QMessageBox):
            return

        contacts = self.Manager.LoadContactsJSON()

        if Name == "":
            QMessageBox.warning(self.EditContactWindow, "Invalid Name", "Name cannot be empty.")
            return

        if PhoneDigits == "":
            QMessageBox.warning(self.EditContactWindow, "Invalid Phone Number", "Phone number cannot be empty.")
            return

        if not PhoneDigits.isdigit():
            QMessageBox.warning(self.EditContactWindow, "Invalid Phone Number", "Phone number must contain only digits.")
            return

        FullPhone = code + " " + PhoneDigits

        if Email == "":
            Email = "Email Not Added"

        for contact in contacts:
            if contact.get("id") == self.EditingID:
                continue

            if Name == contact["name"] and FullPhone == contact["phone"] and Email == contact["email"]:
                reply = QMessageBox.question(
                    self.EditContactWindow,
                    "Duplicate Contact",
                    "Bro this contact already exists.\n\nDo you want to save it as a duplicate?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.No:
                    return

                break

        for i, contact in enumerate(contacts):
            if contact.get("id") == self.EditingID:
                self.Manager.EditCoontactJSON(
                    index=i, id=self.EditingID, name=Name, phone=FullPhone, email=Email, device_ip=DeviceIP
                )
                break

        self.LoadContactsIntoTable()
        self.EditContactWindow.close()

    def EditContacts(self):
        EditData = self.GetSelectedRow()

        if EditData is None:
            return

        Name = self.GetNameFromRow(EditData)
        PhoneNo = self.RecentsContactTable.item(EditData, 2).text().strip()
        Email = self.RecentsContactTable.item(EditData, 3).text().strip()
        self.EditingRow = EditData
        self.EditingID = self.RecentsContactTable.item(EditData, 2).data(Qt.UserRole)

        DeviceIP = ""
        for contact in self.Manager.LoadContactsJSON():
            if contact.get("id") == self.EditingID:
                DeviceIP = contact.get("device_ip", "")
                break

        if " " in PhoneNo:
            code, number = PhoneNo.split(" ", 1)
        else:
            code = "+91"
            number = PhoneNo

        self.EditContactWindow = QWidget()
        self.EditContactWindow.setWindowTitle("Edit Contact")
        self.EditContactWindow.setWindowIcon(QIcon(ICON_PATH))
        self.EditContactWindow.resize(530, 290)

        MainLayout = QVBoxLayout(self.EditContactWindow)
        MainLayout.setContentsMargins(40, 20, 40, 20)
        MainLayout.setSpacing(15)

        self.EditContactLabel = QLabel(self.EditContactWindow)
        self.EditContactLabel.setText("Edit Contact")
        self.EditContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.EditContactLabel.setAlignment(Qt.AlignCenter)
        MainLayout.addWidget(self.EditContactLabel)

        FormLayout = QFormLayout()
        FormLayout.setSpacing(12)
        FormLayout.setLabelAlignment(Qt.AlignLeft)

        self.AsksNameLabel = QLabel("Name --> ")
        self.AsksNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksName = QLineEdit(self.EditContactWindow)
        self.AsksName.setFixedHeight(35)
        self.AsksName.setText(Name)
        self.AsksName.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksNameLabel, self.AsksName)

        self.AsksPhoneNoLabel = QLabel("Phone No. --> ")
        self.AsksPhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        PhoneRow = QHBoxLayout()
        self.CountryCodeContactDropdownforEdit = QComboBox(self.EditContactWindow)
        self.CountryCodeContactDropdownforEdit.setFixedHeight(35)
        self.CountryCodeContactDropdownforEdit.addItems(COUNTRY_CODES)

        self.CountryCodeContactDropdownforEdit.setCurrentText("+91 India")
        for i in range(self.CountryCodeContactDropdownforEdit.count()):
            if self.CountryCodeContactDropdownforEdit.itemText(i).startswith(code):
                self.CountryCodeContactDropdownforEdit.setCurrentIndex(i)
                break
        PhoneRow.addWidget(self.CountryCodeContactDropdownforEdit)

        self.AskPhoneNo = QLineEdit(self.EditContactWindow)
        self.AskPhoneNo.setFixedHeight(35)
        self.AskPhoneNo.setText(number)
        self.AskPhoneNo.setStyleSheet(INPUT_STYLE)
        PhoneRow.addWidget(self.AskPhoneNo)
        FormLayout.addRow(self.AsksPhoneNoLabel, PhoneRow)

        self.AsksEmailLabel = QLabel("Email --> ")
        self.AsksEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksEmail = QLineEdit(self.EditContactWindow)
        self.AsksEmail.setFixedHeight(35)
        self.AsksEmail.setText(Email)
        self.AsksEmail.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksEmailLabel, self.AsksEmail)

        self.AsksDeviceIPLabel = QLabel("Device IP --> ")
        self.AsksDeviceIPLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksDeviceIP = QLineEdit(self.EditContactWindow)
        self.AsksDeviceIP.setFixedHeight(35)
        self.AsksDeviceIP.setPlaceholderText("Optional, for real voice calls")
        self.AsksDeviceIP.setText(DeviceIP)
        self.AsksDeviceIP.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksDeviceIPLabel, self.AsksDeviceIP)

        MainLayout.addLayout(FormLayout)
        MainLayout.addStretch(1)

        ButtonRow = QHBoxLayout()
        ButtonRow.addStretch(1)

        self.CancelButton = QPushButton(self.EditContactWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.setFixedSize(130, 30)
        self.CancelButton.setStyleSheet(RED_BUTTON_STYLE)
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.clicked.connect(
            lambda: self.CancelWithWarning(
                self.EditContactWindow,
                "Changes to this contact will not be saved.\n\nDo you want to discard your edits?"
            )
        )
        ButtonRow.addWidget(self.CancelButton)

        self.SaveButton = QPushButton(self.EditContactWindow)
        self.SaveButton.setText('Save')
        self.SaveButton.setFixedSize(130, 30)
        self.SaveButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.SaveButton.setCursor(Qt.PointingHandCursor)
        self.SaveButton.clicked.connect(self.SaveEditedContact)
        ButtonRow.addWidget(self.SaveButton)

        MainLayout.addLayout(ButtonRow)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.EditContactWindow)
        self.CloseShortcut.activated.connect(self.EditContactWindow.close)

        self.EditContactWindow.show()
        self.DisableMaximizeButton(self.EditContactWindow)
