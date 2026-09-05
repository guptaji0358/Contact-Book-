from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_TITLE_STYLE, DIALOG_LABEL_STYLE, INPUT_STYLE, BLUE_BUTTON_STYLE, RED_BUTTON_STYLE
from scripts.phone_rules import COUNTRY_CODES, validate_phone

ICON_PATH = "CONTACT_BOOK_ICON.png"


class AddDialogMixin:
    def SaveNewContact(self):
        Contacts = self.Manager.LoadContactsJSON()
        Name = self.AsksName.text().title()
        PhoneNo = self.AskPhoneNo.text()
        Email = self.AsksEmail.text().strip()
        DeviceIP = self.AsksDeviceIP.text().strip()
        code = self.CountryCodeContactDropdown.currentText().split()[0]
        Full_Phone = code + " " + PhoneNo

        if not PhoneNo.isdigit():
            QMessageBox.warning(self.AddContactWindow, "Invalid Phone Number", "Phone number must contain only digits.")
            return

        if Name == "":
            QMessageBox.warning(self.AddContactWindow, "Invalid Name", "Name cannot be empty.")
            return

        if PhoneNo == "":
            QMessageBox.warning(self.AddContactWindow, "Invalid Phone Number", "Phone number cannot be empty.")
            return

        if not validate_phone(code, PhoneNo, self.AddContactWindow, QMessageBox):
            return

        new_id = 1
        if Contacts:
            new_id = max(contact.get("id", 0) for contact in Contacts) + 1

        if Email == "":
            Email = "Email Not Added"

        for contact in Contacts:
            if Name == contact["name"] and Full_Phone == contact["phone"] and Email == contact["email"]:
                reply = QMessageBox.question(
                    self.AddContactWindow,
                    "Duplicate Contact",
                    "Bro this contact already exists.\n\nDo you want to save it as a duplicate?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.No:
                    return

                break

        InsertNewContactRowinTable = self.RecentsContactTable.rowCount()
        self.Manager.addContacts(id=new_id, name=Name, phone=Full_Phone, email=Email, device_ip=DeviceIP)

        checkbox = QCheckBox()
        Container = QWidget()
        layout = QHBoxLayout(Container)

        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.RecentsContactTable.setCellWidget(InsertNewContactRowinTable, 0, Container)

        item = QTableWidgetItem("   " + Name)
        item.setData(Qt.UserRole, new_id)

        self.RecentsContactTable.setItem(InsertNewContactRowinTable, 1, item)
        self.RecentsContactTable.setItem(InsertNewContactRowinTable, 2, QTableWidgetItem("   " + Full_Phone))
        self.RecentsContactTable.setItem(InsertNewContactRowinTable, 3, QTableWidgetItem("   " + Email))
        self.RecentsContactTable.setCursor(Qt.PointingHandCursor)

        self.LoadContactsIntoTable()
        self.AddContactWindow.close()

    def AddContacts(self):
        self.AddContactWindow = QWidget()
        self.AddContactWindow.setWindowTitle("Add Contacts")
        self.AddContactWindow.resize(530, 290)
        self.AddContactWindow.setWindowIcon(QIcon(ICON_PATH))

        self.CountryCodeContactDropdown = QComboBox(self.AddContactWindow)
        self.CountryCodeContactDropdown.move(160, 120)
        self.CountryCodeContactDropdown.resize(120, 35)
        self.CountryCodeContactDropdown.addItems(COUNTRY_CODES)
        self.CountryCodeContactDropdown.setCurrentText("+91 India")

        self.AddNewContactLabel = QLabel(self.AddContactWindow)
        self.AddNewContactLabel.setText("New Contact")
        self.AddNewContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.AddNewContactLabel.move(130, 20)

        self.AsksNameLabel = QLabel(self.AddContactWindow)
        self.AsksNameLabel.setText("Name --> ")
        self.AsksNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.AsksNameLabel.move(40, 80)

        self.AsksPhoneNoLabel = QLabel(self.AddContactWindow)
        self.AsksPhoneNoLabel.setText("Phone No. --> ")
        self.AsksPhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.AsksPhoneNoLabel.move(40, 120)

        self.AsksEmailLabel = QLabel(self.AddContactWindow)
        self.AsksEmailLabel.setText("Email --> ")
        self.AsksEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.AsksEmailLabel.move(40, 160)

        self.AsksName = QLineEdit(self.AddContactWindow)
        self.AsksName.move(290, 80)
        self.AsksName.resize(200, 35)
        self.AsksName.setPlaceholderText("Enter Name")
        self.AsksName.setStyleSheet(INPUT_STYLE)

        self.AskPhoneNo = QLineEdit(self.AddContactWindow)
        self.AskPhoneNo.move(290, 120)
        self.AskPhoneNo.resize(200, 35)
        self.AskPhoneNo.setPlaceholderText("Enter Phone Number")
        self.AskPhoneNo.setStyleSheet(INPUT_STYLE)

        self.AsksEmail = QLineEdit(self.AddContactWindow)
        self.AsksEmail.move(290, 160)
        self.AsksEmail.resize(200, 35)
        self.AsksEmail.setPlaceholderText("Enter Email Address")
        self.AsksEmail.setStyleSheet(INPUT_STYLE)

        self.AsksDeviceIPLabel = QLabel(self.AddContactWindow)
        self.AsksDeviceIPLabel.setText("Device IP --> ")
        self.AsksDeviceIPLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.AsksDeviceIPLabel.move(40, 200)

        self.AsksDeviceIP = QLineEdit(self.AddContactWindow)
        self.AsksDeviceIP.move(290, 200)
        self.AsksDeviceIP.resize(200, 35)
        self.AsksDeviceIP.setPlaceholderText("Optional, for real voice calls")
        self.AsksDeviceIP.setStyleSheet(INPUT_STYLE)

        self.SaveButton = QPushButton(self.AddContactWindow)
        self.SaveButton.setText('Save')
        self.SaveButton.resize(130, 30)
        self.SaveButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.SaveButton.move(280, 250)
        self.SaveButton.setCursor(Qt.PointingHandCursor)
        self.SaveButton.clicked.connect(self.SaveNewContact)

        self.CancelButton = QPushButton(self.AddContactWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.resize(130, 30)
        self.CancelButton.move(100, 250)
        self.CancelButton.setStyleSheet(RED_BUTTON_STYLE)
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.clicked.connect(
            lambda: self.CancelWithWarning(
                self.AddContactWindow,
                "This contact has not been saved.\n\nIf you cancel now the entered data will be lost."
            )
        )

        self.AddContactWindow.show()
        self.DisableMaximizeButton(self.AddContactWindow)
