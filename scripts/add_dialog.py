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

        MainLayout = QVBoxLayout(self.AddContactWindow)
        MainLayout.setContentsMargins(40, 20, 40, 20)
        MainLayout.setSpacing(15)

        self.AddNewContactLabel = QLabel(self.AddContactWindow)
        self.AddNewContactLabel.setText("New Contact")
        self.AddNewContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.AddNewContactLabel.setAlignment(Qt.AlignCenter)
        MainLayout.addWidget(self.AddNewContactLabel)

        FormLayout = QFormLayout()
        FormLayout.setSpacing(12)
        FormLayout.setLabelAlignment(Qt.AlignLeft)

        self.AsksNameLabel = QLabel("Name --> ")
        self.AsksNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksName = QLineEdit(self.AddContactWindow)
        self.AsksName.setFixedHeight(35)
        self.AsksName.setPlaceholderText("Enter Name")
        self.AsksName.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksNameLabel, self.AsksName)

        self.AsksPhoneNoLabel = QLabel("Phone No. --> ")
        self.AsksPhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        PhoneRow = QHBoxLayout()
        self.CountryCodeContactDropdown = QComboBox(self.AddContactWindow)
        self.CountryCodeContactDropdown.setFixedHeight(35)
        self.CountryCodeContactDropdown.addItems(COUNTRY_CODES)
        self.CountryCodeContactDropdown.setCurrentText("+91 India")
        PhoneRow.addWidget(self.CountryCodeContactDropdown)

        self.AskPhoneNo = QLineEdit(self.AddContactWindow)
        self.AskPhoneNo.setFixedHeight(35)
        self.AskPhoneNo.setPlaceholderText("Enter Phone Number")
        self.AskPhoneNo.setStyleSheet(INPUT_STYLE)
        PhoneRow.addWidget(self.AskPhoneNo)
        FormLayout.addRow(self.AsksPhoneNoLabel, PhoneRow)

        self.AsksEmailLabel = QLabel("Email --> ")
        self.AsksEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksEmail = QLineEdit(self.AddContactWindow)
        self.AsksEmail.setFixedHeight(35)
        self.AsksEmail.setPlaceholderText("Enter Email Address")
        self.AsksEmail.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksEmailLabel, self.AsksEmail)

        self.AsksDeviceIPLabel = QLabel("Device IP --> ")
        self.AsksDeviceIPLabel.setStyleSheet(DIALOG_LABEL_STYLE)

        self.AsksDeviceIP = QLineEdit(self.AddContactWindow)
        self.AsksDeviceIP.setFixedHeight(35)
        self.AsksDeviceIP.setPlaceholderText("Optional, for real voice calls")
        self.AsksDeviceIP.setStyleSheet(INPUT_STYLE)
        FormLayout.addRow(self.AsksDeviceIPLabel, self.AsksDeviceIP)

        MainLayout.addLayout(FormLayout)
        MainLayout.addStretch(1)

        ButtonRow = QHBoxLayout()
        ButtonRow.addStretch(1)

        self.CancelButton = QPushButton(self.AddContactWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.setFixedSize(130, 30)
        self.CancelButton.setStyleSheet(RED_BUTTON_STYLE)
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.clicked.connect(
            lambda: self.CancelWithWarning(
                self.AddContactWindow,
                "This contact has not been saved.\n\nIf you cancel now the entered data will be lost."
            )
        )
        ButtonRow.addWidget(self.CancelButton)

        self.SaveButton = QPushButton(self.AddContactWindow)
        self.SaveButton.setText('Save')
        self.SaveButton.setFixedSize(130, 30)
        self.SaveButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.SaveButton.setCursor(Qt.PointingHandCursor)
        self.SaveButton.clicked.connect(self.SaveNewContact)
        ButtonRow.addWidget(self.SaveButton)

        MainLayout.addLayout(ButtonRow)

        self.AddContactWindow.show()
        self.DisableMaximizeButton(self.AddContactWindow)
