from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from CONTACT_BOOK_MANAGER import ContactBookManager
import sys 
import os
import html

Path  = "CONTACT_BOOK_ICON.png"

class ContactBookGUI():
    def __init__(self):
        super().__init__()

        self.TableStyle = ("""QTableWidget {background-color: #2b2b2b;color: white;gridline-color: transparent;}
                           QHeaderView::section {background-color: #1f1f1f;color: white;font-weight: bold;border: none;}
                           """)

        self.InputStyle = """QLineEdit {border: 2px solid #cccccc;border-radius: 6px;padding: 6px;font-size: 14px;font-family: 'Segoe UI';font-weight:bold;}
                             QLineEdit:focus {border: 2px solid #2563EB;}"""

        self.BlueButtonStyle = """QPushButton {background-color: #2563EB;color: white;font-size: 16px;font-family: 'Segoe UI';border-radius: 8px;font-weight:bold;}
                                  QPushButton:hover {background-color: #3B82F6;}
                                  QPushButton:pressed {background-color: #1E40AF;}"""
        
        self.GreyButtonStyle = """QPushButton {background-color: #374151;color: white;font-size: 16px;font-family: 'Segoe UI';border-radius: 8px;font-weight:bold;}
                                  QPushButton:hover {background-color: #2F3745;}
                                  QPushButton:pressed {background-color: #1F2937;}"""

        self.RedButtonStyle = """QPushButton {background-color: #EF4444;color: white;font-size: 16px;font-family: 'Segoe UI';border-radius: 8px;font-weight:bold;}
                                 QPushButton:hover {background-color: #F87171;}
                                 QPushButton:pressed {background-color: #B91C1C;}"""
        
        self.Manager = ContactBookManager()

        self.ContactBookApp = QApplication(sys.argv)
        self.MainWindow = QWidget()
        self.MainWindow.setWindowTitle("Contact Book")
        self.MainWindow.resize(685,500)
        self.MainWindow.setWindowIcon(QIcon(Path))

        self.SearchEngineofContactsLabel = QLabel(self.MainWindow)
        self.SearchEngineofContactsLabel.resize(60,25)
        self.SearchEngineofContactsLabel.setText("Search -->")
        self.SearchEngineofContactsLabel.move(20,20)

        self.SearchEngineofContacts = QLineEdit(self.MainWindow)
        self.SearchEngineofContacts.resize(200,35)
        self.SearchEngineofContacts.setStyleSheet(self.InputStyle)
        self.SearchEngineofContacts.setPlaceholderText("Search Contacts")
        self.SearchEngineofContacts.move(80,20)
        self.SearchEngineofContacts.textChanged.connect(self.FilterContacts)
        self.SearchEngineofContacts.setClearButtonEnabled(True)

        # Create Fresh Table 
        self.RecentsContactTable = QTableWidget(self.MainWindow)
        self.RecentsContactTable.setShowGrid(False)
        self.RecentsContactTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.RecentsContactTable.setFocusPolicy(Qt.NoFocus)
        self.RecentsContactTable.setColumnCount(4)
        self.RecentsContactTable.setHorizontalHeaderLabels(["", "Name", "Phone No.", "Email"])
        self.RecentsContactTable.resize(650,300)
        self.RecentsContactTable.move(20,80)
        self.RecentsContactTable.verticalHeader().setVisible(False)
        self.RecentsContactTable.setColumnWidth(0,35)
        self.RecentsContactTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.RecentsContactTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.RecentsContactTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.RecentsContactTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.RecentsContactTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.RecentsContactTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.RecentsContactTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.RecentsContactTable.cellPressed.connect(self.RowClicked)
        self.RecentsContactTable.setAlternatingRowColors(True)
        self.RecentsContactTable.setRowCount(0)
        self.RecentsContactTable.setStyleSheet(self.TableStyle)

        self.SelectedRow = None
        self.LastDeletedContact = None
        self.LoadContactsIntoTable()

        self.ViewContactButton = QPushButton("👁", self.MainWindow)
        self.ViewContactButton.resize(60,50)
        self.ViewContactButton.setToolTip("View Contacts")
        self.ViewContactButton.move(130,440)
        self.ViewContactButton.setStyleSheet(self.BlueButtonStyle)
        self.ViewContactButton.clicked.connect(self.ViewContacts)

        # Add Button
        self.AddContactButton = QPushButton("➕", self.MainWindow)
        self.AddContactButton.resize(60,50)
        self.AddContactButton.setToolTip("Add Contacts")
        self.AddContactButton.move(200,440)
        self.AddContactButton.setStyleSheet(self.BlueButtonStyle)
        self.AddContactButton.clicked.connect(self.AddContacts)

        # Delete Button
        self.DeleteContactButton = QPushButton("🗑️", self.MainWindow)
        self.DeleteContactButton.resize(60,50)
        self.DeleteContactButton.setToolTip("Delete Contacts")
        self.DeleteContactButton.move(340,440)
        self.DeleteContactButton.setStyleSheet(self.RedButtonStyle)
        self.DeleteContactButton.clicked.connect(self.DeleteContacts)

        # Edit Button
        self.EditContactButton = QPushButton("✏️", self.MainWindow)
        self.EditContactButton.resize(60,50)
        self.EditContactButton.setToolTip("Edit Contacts")
        self.EditContactButton.move(270,440)
        self.EditContactButton.setStyleSheet(self.BlueButtonStyle)
        self.EditContactButton.clicked.connect(self.EditContacts)

        # Import Button
        self.ImportContactButton = QPushButton("☁↓", self.MainWindow)
        self.ImportContactButton.resize(60,50)
        self.ImportContactButton.setToolTip("Import Contacts")
        self.ImportContactButton.move(410,440)
        self.ImportContactButton.setStyleSheet(self.BlueButtonStyle)
        self.ImportContactButton.clicked.connect(self.ImportContacts)

        # Export Button
        self.ExportContactButton = QPushButton("☁↑", self.MainWindow)
        self.ExportContactButton.resize(60,50)
        self.ExportContactButton.setToolTip("Export Contacts")
        self.ExportContactButton.move(480,440)
        self.ExportContactButton.setStyleSheet(self.BlueButtonStyle)
        self.ExportContactButton.clicked.connect(self.ExportContacts)

        self.MainWindow.show()
        self.ContactBookApp.exec()

    def SaveNewContact(self):
        Contacts = self.Manager.LoadContactsJSON()
        Name = self.AsksName.text().title()
        PhoneNo = self.AskPhoneNo.text()
        Email = self.AsksEmail.text().strip()
        code = self.CountryCodeContactDropdown.currentText().split()[0]
        Full_Phone = code + " " + PhoneNo

        if not PhoneNo.isdigit():
            QMessageBox.warning(
                self.AddContactWindow,
                "Invalid Phone Number",
                "Phone number must contain only digits."
                )
            
            return
                
        if Name == "":
            QMessageBox.warning(
                self.AddContactWindow,
                "Invalid Name",
                "Name cannot be empty."
            )
            return
        
        if PhoneNo == "":
            QMessageBox.warning(
                self.AddContactWindow,
                "Invalid Phone Number",
                "Phone number cannot be empty."
                )
            return

        new_id = 1
        if Contacts:
            new_id = max(contact.get("id",0) for contact in Contacts) + 1

        digit_rules = {
            "+91": 10,
            "+1": 10,
            "+44": 10,
            "+61": 9,
            "+880": 10,
            "+55": 11,
            "+86": 11,
            "+33": 9,
            "+49": 10,
            "+62": 10,
            "+39": 10,
            # "+81": 10,
            "+60": 9,
            "+52": 10,
            "+31": 9,
            "+64": 9,
            "+92": 10,
            "+7": 10,
            "+966": 9,
            "+65": 8,
            "+27": 9,
            "+82": 10,
            "+34": 9,
            "+94": 9,
            "+971": 9
        }
        if code == "+81":
            
            if len(PhoneNo) < 9 or len(PhoneNo) > 10:
                QMessageBox.warning(
                    self.AddContactWindow,
                    "Invalid Phone Number",
                    "Japan numbers must be 9–10 digits."
                    )
                return

        if code in digit_rules:
            required = digit_rules[code]

            if len(PhoneNo) != required:
                QMessageBox.warning(
                    self.AddContactWindow,
                    "Invalid Phone Number",
                    f"{code} numbers must contain {required} digits."
                )
                return

        if Email == "":
            Email = "Email Not Added"

        else:
            Email = Email

        for contact in Contacts:
            if (Name == contact["name"] and Full_Phone == contact["phone"] and Email == contact["email"]):

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
        self.Manager.addContacts(id=new_id,name=Name, phone=Full_Phone, email=Email)

        checkbox = QCheckBox()
        Container = QWidget()
        layout = QHBoxLayout(Container)

        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0,0,0,0)

        self.RecentsContactTable.setCellWidget(InsertNewContactRowinTable,0,Container)

        item = QTableWidgetItem("   "+Name)
        item.setData(Qt.UserRole,new_id)

        self.RecentsContactTable.setItem(InsertNewContactRowinTable,1,item)
        self.RecentsContactTable.setItem(InsertNewContactRowinTable,2,QTableWidgetItem("   "+Full_Phone))  
        self.RecentsContactTable.setItem(InsertNewContactRowinTable,3,QTableWidgetItem("   "+Email)) 

        self.LoadContactsIntoTable()
        self.AddContactWindow.close()

    def GetNameFromRow(self,row):

        item = self.RecentsContactTable.item(row,1)
        if item:
            return item.text().strip()
        
        widget = self.RecentsContactTable.cellWidget(row,1)
        if widget:
            Html_Text = widget.text()

            PlainText = QTextDocumentFragment.fromHtml(Html_Text).toPlainText()
            return PlainText.strip()

        return None

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

        self.Manager.addContacts(
            id=contact_id,
            name=name,
            phone=phone,
            email=email
        )

        self.LastDeletedContact = None
        self.LoadContactsIntoTable()

    def FilterContacts(self):
        self.SelectedRow = None
        search = self.SearchEngineofContacts.text().lower().strip()
        contacts = self.Manager.LoadContactsJSON()

        contacts.sort(key=lambda x: x["name"].lower())
        self.RecentsContactTable.setRowCount(0)

        previous_group = None
        results_found = False

        for contact in contacts:
            name = contact["name"]
            phone = contact["phone"]
            email = contact["email"]

            if search and search not in (name + phone + email).lower():
                continue

            results_found = True

            first = name[0].upper() if name else "Others"
            group = first if first.isalpha() else "Others"

            if group != previous_group:
                label_row = self.RecentsContactTable.rowCount()
                self.RecentsContactTable.insertRow(label_row)

                label_item = QTableWidgetItem(group)
                font = QFont()
                font.setBold(True)
                label_item.setFont(font)
                label_item.setBackground(QColor(45,45,45))
                label_item.setFlags(Qt.NoItemFlags)

                self.RecentsContactTable.setItem(label_row,1,label_item)
                self.RecentsContactTable.setSpan(label_row,1,1,3)

                previous_group = group

            row = self.RecentsContactTable.rowCount()
            self.RecentsContactTable.insertRow(row)

            checkbox = QCheckBox()
            container = QWidget()
            layout = QHBoxLayout(container)

            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0,0,0,0)

            self.RecentsContactTable.setCellWidget(row,0,container)

            if search:
                lower = name.lower()
                start = lower.find(search)
                if start == -1:
                    start = 0
                    end = 0
                else:
                    end = start + len(search)

                highlighted = (
                    html.escape(name[:start]) +
                    "<span style='color:#2563EB;font-weight:bold;'>"
                    + html.escape(name[start:end]) +
                    "</span>"
                    "<span style='font-weight:bold;'>"
                    + html.escape(name[end:]) +
                    "</span>"
                )

                label = QLabel("   " + highlighted)
                label.setTextFormat(Qt.RichText)
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setStyleSheet("color:white;")

                self.RecentsContactTable.setCellWidget(row,1,label)
                label.setProperty("contact_id", contact.get("id"))

            else:
                item = QTableWidgetItem("   "+name)
                item.setData(Qt.UserRole, contact.get("id"))
                self.RecentsContactTable.setItem(row,1,item)

            phone_item = QTableWidgetItem("   "+phone)
            phone_item.setData(Qt.UserRole, contact.get("id"))
            self.RecentsContactTable.setItem(row,2,phone_item)
            self.RecentsContactTable.setItem(row,3,QTableWidgetItem("   "+email))

        if not results_found:
            self.RecentsContactTable.setRowCount(0)

    def LoadContactsIntoTable(self):
        self.SelectedRow = None
        self.RecentsContactTable.setRowCount(0)
        contacts = self.Manager.LoadContactsJSON()
        contacts.sort(key=lambda x: x["name"].lower())

        previous_group = None

        for contact in contacts:
            name = contact["name"]
            phone = contact["phone"]
            email = contact["email"]

            if not name:
                group = "Others"
            else:
                first = name[0].upper()

                if first.isalpha():
                    group = first
                elif first in ["#", "@"]:
                    group = first
                else:
                    group = "Others"

            if group != previous_group:
                label_row = self.RecentsContactTable.rowCount()
                self.RecentsContactTable.insertRow(label_row)
                label_item = QTableWidgetItem(group)
                font = QFont()
                font.setBold(True)
                label_item.setFont(font)
                label_item.setBackground(QColor(45,45,45))
                label_item.setFlags(Qt.NoItemFlags)

                self.RecentsContactTable.setItem(label_row,1,label_item)
                self.RecentsContactTable.setSpan(label_row,1,1,3)

                previous_group = group

            row = self.RecentsContactTable.rowCount()
            self.RecentsContactTable.insertRow(row)

            checkbox = QCheckBox()
            container = QWidget()
            layout = QHBoxLayout(container)

            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0,0,0,0)

            self.RecentsContactTable.setCellWidget(row,0,container)
            
            item = QTableWidgetItem("   "+name)
            item.setData(Qt.UserRole,contact.get("id"))
            self.RecentsContactTable.setItem(row,1,item)

            phone_item = QTableWidgetItem("   "+phone)
            phone_item.setData(Qt.UserRole, contact.get("id"))
            self.RecentsContactTable.setItem(row,2, phone_item)
            self.RecentsContactTable.setItem(row,3,QTableWidgetItem("   "+email))

    def CloseButtonLogic(self,window):
        window.close()

    def CancelWithWarning(self, window, message):
        reply = QMessageBox.question(
            window,
            "Discard Changes",
            message,
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            window.close()

    def GetSelectedRow(self):
        SelectedRow = []

        for row in range(self.RecentsContactTable.rowCount()):

            container = self.RecentsContactTable.cellWidget(row,0)

            # Skip rows that don't have checkbox (label rows)
            if container is None:
                continue

            checkbox = container.findChild(QCheckBox)

            if checkbox and checkbox.isChecked():
                SelectedRow.append(row)

        if len(SelectedRow) == 0:
            QMessageBox.warning(
                self.MainWindow,
                "No Contact Selected",
                "Please select a contact first."
            )
            return None

        if len(SelectedRow) > 1:
            QMessageBox.warning(
                self.MainWindow,
                "Multiple Contacts Selected",
                "Please select only one contact."
            )
            return None

        return SelectedRow[0]

    def RowClicked(self, row, column):
        if column == 0:
            return
        
        checkbox = self.RecentsContactTable.cellWidget(row,0).findChild(QCheckBox)
        if self.SelectedRow == row:
            checkbox.setChecked(False)
            for col in range(self.RecentsContactTable.columnCount()):
                item = self.RecentsContactTable.item(row,col)
                if item:
                    item.setBackground(QBrush())

            self.SelectedRow = None
            return

        if self.SelectedRow is not None:

            old_checkbox = self.RecentsContactTable.cellWidget(self.SelectedRow,0).findChild(QCheckBox)
            old_checkbox.setChecked(False)
            for col in range(self.RecentsContactTable.columnCount()):
                item = self.RecentsContactTable.item(self.SelectedRow,col)
                if item:
                    item.setBackground(QBrush())

        checkbox.setChecked(True)
        for col in range(self.RecentsContactTable.columnCount()):
            item = self.RecentsContactTable.item(row,col)
            if item:
                item.setBackground(QColor(37,99,235,60))
        self.SelectedRow = row

    def SaveEditedContact(self):

        Name = self.AsksName.text().title().strip()
        PhoneDigits = self.AskPhoneNo.text().strip()
        Email = self.AsksEmail.text().strip()
        code = self.CountryCodeContactDropdownforEdit.currentText().split()[0]

        digit_rules = {
            "+91":10,
            "+1":10,
            "+44":10,
            "+61":9,
            "+880":10,
            "+55":11,
            "+86":11,
            "+33":9,
            "+49":10,
            "+62":10,
            "+39":10,
            "+60":9,
            "+52":10,
            "+31":9,
            "+64":9,
            "+92":10,
            "+7":10,
            "+966":9,
            "+65":8,
            "+27":9,
            "+82":10,
            "+34":9,
            "+94":9,
            "+971":9
            }
        
        if code == "+81":
            if len(PhoneDigits) < 9 or len(PhoneDigits) > 10:
                QMessageBox.warning(self.EditContactWindow,"Invalid Phone Number","Japan numbers must be 9–10 digits.")
                return
            
        if code in digit_rules:
            required = digit_rules[code]
            if len(PhoneDigits) != required:
                QMessageBox.warning(
                    self.EditContactWindow,"Invalid Phone Number",f"{code} numbers must contain {required} digits.")
                return

        contacts = self.Manager.LoadContactsJSON()
        FullPhone = code + " " + PhoneDigits
        

        if Name == "":
            QMessageBox.warning(
                self.EditContactWindow,
                "Invalid Name",
                "Name cannot be empty."
            )
            return

        if PhoneDigits == "":
            QMessageBox.warning(
                self.EditContactWindow,
                "Invalid Phone Number",
                "Phone number cannot be empty."
            )
            return

        if not PhoneDigits.isdigit():
            QMessageBox.warning(
                self.EditContactWindow,
                "Invalid Phone Number",
                "Phone number must contain only digits."
            )
            return

        code = self.CountryCodeContactDropdownforEdit.currentText().split()[0]

        FullPhone = code + " " + PhoneDigits

        if Email == "":
            Email = "Email Not Added"

        # Duplicate check
        for contact in contacts:

            if contact.get("id") == self.EditingID:
                continue

            if (Name == contact["name"] and FullPhone == contact["phone"] and Email == contact["email"]):

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
                    index=i,
                    id=self.EditingID,
                    name=Name,
                    phone=FullPhone,
                    email=Email
                )

                break

        self.LoadContactsIntoTable()
        self.EditContactWindow.close()

    def DeleteSelectedContact(self):
        row = self.DeletingRow
        name = self.GetNameFromRow(row)
        phone = self.RecentsContactTable.item(row,2).text().strip()
        email = self.RecentsContactTable.item(row,3).text().strip()
        contact_id = self.RecentsContactTable.item(row,2).data(Qt.UserRole)
        
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
        
        self.LastDeletedContact = (contact_id,name, phone, email)
        self.RecentsContactTable.removeRow(row)
        # self.OriginalNames.remove(name)

        contacts = self.Manager.LoadContactsJSON()
        
        for i, contact in enumerate(contacts):
            if contact.get("id") == contact_id:
                self.Manager.DeleteContactJSON(index=i)
                break

        self.LoadContactsIntoTable()
        self.DeleteContactsWindow.close()
        self.ShowUndoMessage()

    def BrowseVCFFile(self):
        VCFPath,_= QFileDialog.getOpenFileName(self.ImportContactWindow,"Select VCF File","","VCF files(*.vcf);;All files(*)")

        if not VCFPath:
            return

        self.ImportPathTextBox.setText(VCFPath)
        self.ImportPathTextBox.setToolTip(VCFPath)

        file_name = os.path.basename(VCFPath)
        self.ImportSelectedFileLabel.setText(f"Selected file: {file_name}")
        self.ImportSelectedFileLabel.setToolTip(file_name)

        contacts = self.Manager.ImportAndReadVCF(VCFPath)

        self.ImportContactDetectedLabel.setText(f"Contacts detected: {len(contacts)}")
        self.ImportedContacts = contacts

    def ImportDetectedContacts(self):
        newid = 1
        existing_contacts = self.Manager.LoadContactsJSON()

        if not hasattr(self,"ImportedContacts") or not self.ImportedContacts:
            QMessageBox.warning(
                self.ImportContactWindow,
                "No File Selected",
                "Please select a VCF file first."
                )
            return

        if existing_contacts:
            newid = max(contact.get("id",0) for contact in existing_contacts) + 1

        for contact in self.ImportedContacts:
            self.Manager.addContacts(id=newid,name=contact["name"],phone=contact["phone"],email=contact["email"])
            newid += 1
        QMessageBox.information(self.ImportContactWindow,"Import Successful",f"{len(self.ImportedContacts)} contacts imported successfully.")
        self.LoadContactsIntoTable()
        self.ImportContactWindow.close()

    def ViewContacts(self):
        ViewData = self.GetSelectedRow()

        if ViewData is None:
            return
        
        #Fetch Data
        Name = self.GetNameFromRow(ViewData)
        PhoneNo = self.RecentsContactTable.item(ViewData,2).text().strip()
        Email = self.RecentsContactTable.item(ViewData,3).text().strip()

        #Create View Window
        self.ViewContactsWindow = QWidget()
        self.ViewContactsWindow.setWindowTitle("Contact Details")
        self.ViewContactsWindow.resize(420,250)
        self.ViewContactsWindow.setWindowIcon(QIcon(Path))

        #View Contact Detail Label
        self.ViewContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewContactLabel.setText("Contact Details")
        self.ViewContactLabel.setStyleSheet("font-size:24px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewContactLabel.move(85,10)

        #Name Label
        self.ViewNameLabel = QLabel(self.ViewContactsWindow)
        self.ViewNameLabel.setText("Name ->")
        self.ViewNameLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewNameLabel.move(30,80)

        #Name Data Label
        self.ViewNameContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewNameContactLabel.setText(Name)
        self.ViewNameContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewNameContactLabel.move(160,80)

        #Phone No. Label
        self.ViewPhoneNoLabel = QLabel(self.ViewContactsWindow)
        self.ViewPhoneNoLabel.setText("Phone No. ->")
        self.ViewPhoneNoLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewPhoneNoLabel.move(30,120)

        #Phone No. Data Label
        self.ViewPhoneNoContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewPhoneNoContactLabel.setText(PhoneNo)
        self.ViewPhoneNoContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewPhoneNoContactLabel.move(160,120)

        #Email Label
        self.ViewEmailLabel = QLabel(self.ViewContactsWindow)
        self.ViewEmailLabel.setText("Email ->")
        self.ViewEmailLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewEmailLabel.move(30,160)

        #Email Data Label
        self.ViewEmailContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewEmailContactLabel.setText(Email)
        self.ViewEmailContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.ViewEmailContactLabel.move(160,160)

        #Close Button
        self.CloseButton = QPushButton(self.ViewContactsWindow)
        self.CloseButton.setText("Close")
        self.CloseButton.resize(130,30)
        self.CloseButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))
        self.CloseButton.setStyleSheet(self.GreyButtonStyle)
        self.CloseButton.move(110,200)
        self.CloseButton.setDefault(True)
        self.ViewContactsWindow.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.ViewContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))

        self.ViewContactsWindow.show()

    def DeleteContacts(self):
        DeleteData = self.GetSelectedRow()

        if DeleteData is None:
            return

        self.DeletingRow = DeleteData
        
        #Fetch Data
        Name = self.GetNameFromRow(DeleteData)
        PhoneNo = self.RecentsContactTable.item(DeleteData,2).text().strip()
        Email = self.RecentsContactTable.item(DeleteData,3).text().strip()

        #Create Delete Window
        self.DeleteContactsWindow = QWidget()
        self.DeleteContactsWindow.setWindowTitle("Delete Contact Details")
        self.DeleteContactsWindow.resize(420,250)
        self.DeleteContactsWindow.setWindowIcon(QIcon(Path))

        #Delete Contact Detail Label
        self.DeleteContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteContactLabel.setText("Delete Contact")
        self.DeleteContactLabel.setStyleSheet("font-size:24px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeleteContactLabel.move(85,10)

        #Name Label
        self.DeleteNameLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteNameLabel.setText("Name ->")
        self.DeleteNameLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeleteNameLabel.move(30,80)

        #Name Data Label
        self.DeleteNameContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteNameContactLabel.setText(Name)
        self.DeleteNameContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeleteNameContactLabel.move(160,80)

        #Phone No. Label
        self.DeletePhoneNoLabel = QLabel(self.DeleteContactsWindow)
        self.DeletePhoneNoLabel.setText("Phone No. ->")
        self.DeletePhoneNoLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeletePhoneNoLabel.move(30,120)

        #Phone No. Data Label
        self.DeletePhoneNoContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeletePhoneNoContactLabel.setText(PhoneNo)
        self.DeletePhoneNoContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeletePhoneNoContactLabel.move(160,120)

        #Email Label
        self.DeleteEmailLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteEmailLabel.setText("Email ->")
        self.DeleteEmailLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeleteEmailLabel.move(30,160)

        #Email Data Label
        self.DeleteEmailContactLabel = QLabel(self.DeleteContactsWindow)
        self.DeleteEmailContactLabel.setText(Email)
        self.DeleteEmailContactLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.DeleteEmailContactLabel.move(160,160)

        #Cancel Button
        self.CancelButton = QPushButton(self.DeleteContactsWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.resize(130,30)
        self.CancelButton.move(80,210)
        self.CancelButton.setStyleSheet(self.BlueButtonStyle)
        self.CancelButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.DeleteContactsWindow))

        #Delete Button
        self.DeleteButton = QPushButton(self.DeleteContactsWindow)
        self.DeleteButton.setText("Delete")
        self.DeleteButton.resize(130,30)
        self.DeleteButton.move(240,210)
        self.DeleteButton.setStyleSheet(self.RedButtonStyle)
        self.DeleteButton.clicked.connect(self.DeleteSelectedContact)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.DeleteContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.DeleteContactsWindow.close())

        self.DeleteContactsWindow.show()

    def AddContacts(self):
        self.AddContactWindow = QWidget()
        self.AddContactWindow.setWindowTitle("Add Contacts")
        self.AddContactWindow.resize(530,250)
        self.AddContactWindow.setWindowIcon(QIcon(Path))

        #Contry Code Dropdown
        self.CountryCodeContactDropdown = QComboBox(self.AddContactWindow)
        self.CountryCodeContactDropdown.move(160,120)
        self.CountryCodeContactDropdown.resize(120,35)
        self.CountryCodeContactDropdown.addItems(["+61 Australia","+880 Bangladesh","+55 Brazil",
                                                  "+86 China","+33 France","+49 Germany",
                                                  "+91 India","+62 Indonesia","+39 Italy",
                                                  "+81 Japan","+60 Malaysia","+52 Mexico",
                                                  "+31 Netherlands","+64 New Zealand","+92 Pakistan",
                                                  "+7 Russia","+966 Saudi Arabia","+65 Singapore",
                                                  "+27 South Africa","+82 South Korea","+34 Spain",
                                                  "+94 Sri Lanka","+971 UAE","+44 United Kingdom",
                                                  "+1 USA / Canada"
                                                  ])
        
        self.CountryCodeContactDropdown.setCurrentText("+91 India")

        #New Contact Labeel
        self.AddNewContactLabel = QLabel(self.AddContactWindow)
        self.AddNewContactLabel.setText("New Contact")
        self.AddNewContactLabel.setStyleSheet("font-size:24px; font-family:'Segoe UI'; font-weight:bold;")
        self.AddNewContactLabel.move(130,20)

        # Name Label 
        self.AsksNameLabel = QLabel(self.AddContactWindow)
        self.AsksNameLabel.setText("Name --> ")
        self.AsksNameLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksNameLabel.move(40,80)

        #Phone No. Label
        self.AsksPhoneNoLabel = QLabel(self.AddContactWindow)
        self.AsksPhoneNoLabel.setText("Phone No. --> ")
        self.AsksPhoneNoLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksPhoneNoLabel.move(40,120)

        #Email Label
        self.AsksEmailLabel = QLabel(self.AddContactWindow)
        self.AsksEmailLabel.setText("Email --> ")
        self.AsksEmailLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksEmailLabel.move(40,160)

        #Name Input
        self.AsksName = QLineEdit(self.AddContactWindow)
        self.AsksName.move(290,80)
        self.AsksName.resize(200,35)
        self.AsksName.setPlaceholderText("Enter Name")
        self.AsksName.setStyleSheet(self.InputStyle)

        #Phone No. Input
        self.AskPhoneNo = QLineEdit(self.AddContactWindow)
        self.AskPhoneNo.move(290,120)
        self.AskPhoneNo.resize(200,35)
        self.AskPhoneNo.setPlaceholderText("Enter Phone Number")
        self.AskPhoneNo.setStyleSheet(self.InputStyle)

        #Email Input
        self.AsksEmail = QLineEdit(self.AddContactWindow)
        self.AsksEmail.move(290,160)
        self.AsksEmail.resize(200,35)
        self.AsksEmail.setPlaceholderText("Enter Email Address")
        self.AsksEmail.setStyleSheet(self.InputStyle)

        #Save Button
        self.SaveButton = QPushButton(self.AddContactWindow)
        self.SaveButton.setText('Save')
        self.SaveButton.resize(130,30)
        self.SaveButton.setStyleSheet(self.BlueButtonStyle)
        self.SaveButton.move(280,210)
        self.SaveButton.clicked.connect(self.SaveNewContact)

        #Cancel Button
        self.CancelButton = QPushButton(self.AddContactWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.resize(130,30)
        self.CancelButton.move(100,210)
        self.CancelButton.setStyleSheet(self.RedButtonStyle)
        self.CancelButton.clicked.connect(lambda: self.CancelWithWarning(self.AddContactWindow,"This contact has not been saved.\n\nIf you cancel now the entered data will be lost."))

        self.AddContactWindow.show()

    def EditContacts(self):
        EditData = self.GetSelectedRow()

        if EditData is None:
            return

        #Fetch Data
        Name = self.GetNameFromRow(EditData)
        PhoneNo = self.RecentsContactTable.item(EditData,2).text().strip()
        Email = self.RecentsContactTable.item(EditData,3).text().strip()
        self.EditingRow = EditData
        self.EditingID = self.RecentsContactTable.item(EditData,2).data(Qt.UserRole)
        
        # Split phone into code and number
        if " " in PhoneNo:
            code, number = PhoneNo.split(" ",1)
        else:
            code = "+91"
            number = PhoneNo

        #Edit Window
        self.EditContactWindow = QWidget()
        self.EditContactWindow.setWindowTitle("Edit Contact")
        self.EditContactWindow.setWindowIcon(QIcon(Path))
        self.EditContactWindow.resize(530,250)
        
        #Edit Contact Label
        self.EditContactLabel = QLabel(self.EditContactWindow)
        self.EditContactLabel.setText("Edit Contact")
        self.EditContactLabel.setStyleSheet("font-size:24px; font-family:'Segoe UI'; font-weight:bold;")
        self.EditContactLabel.move(130,20)

        #Contry Code Dropdown
        self.CountryCodeContactDropdownforEdit = QComboBox(self.EditContactWindow)
        self.CountryCodeContactDropdownforEdit.move(160,120)
        self.CountryCodeContactDropdownforEdit.resize(120,35)
        self.CountryCodeContactDropdownforEdit.addItems(["+61 Australia","+880 Bangladesh","+55 Brazil",
                                                  "+86 China","+33 France","+49 Germany",
                                                  "+91 India","+62 Indonesia","+39 Italy",
                                                  "+81 Japan","+60 Malaysia","+52 Mexico",
                                                  "+31 Netherlands","+64 New Zealand","+92 Pakistan",
                                                  "+7 Russia","+966 Saudi Arabia","+65 Singapore",
                                                  "+27 South Africa","+82 South Korea","+34 Spain",
                                                  "+94 Sri Lanka","+971 UAE","+44 United Kingdom",
                                                  "+1 USA / Canada"
                                                  ])
        
        self.CountryCodeContactDropdownforEdit.setCurrentText("+91 India")
        for i in range(self.CountryCodeContactDropdownforEdit.count()):
            if self.CountryCodeContactDropdownforEdit.itemText(i).startswith(code):
                self.CountryCodeContactDropdownforEdit.setCurrentIndex(i)
                break

        # Name Label 
        self.AsksNameLabel = QLabel(self.EditContactWindow)
        self.AsksNameLabel.setText("Name --> ")
        self.AsksNameLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksNameLabel.move(40,80)

        #Phone No. Label
        self.AsksPhoneNoLabel = QLabel(self.EditContactWindow)
        self.AsksPhoneNoLabel.setText("Phone No. --> ")
        self.AsksPhoneNoLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksPhoneNoLabel.move(40,120)

        #Email Label
        self.AsksEmailLabel = QLabel(self.EditContactWindow)
        self.AsksEmailLabel.setText("Email --> ")
        self.AsksEmailLabel.setStyleSheet("font-size:16px; font-family:'Segoe UI'; font-weight:bold;")
        self.AsksEmailLabel.move(40,160)

        #Name Input
        self.AsksName = QLineEdit(self.EditContactWindow)
        self.AsksName.move(290,80)
        self.AsksName.resize(200,35)
        self.AsksName.setText(Name)
        self.AsksName.setStyleSheet(self.InputStyle)

        #Phone No. Input
        self.AskPhoneNo = QLineEdit(self.EditContactWindow)
        self.AskPhoneNo.move(290,120)
        self.AskPhoneNo.resize(200,35)
        self.AskPhoneNo.setText(number)
        self.AskPhoneNo.setStyleSheet(self.InputStyle)

        #Email Input
        self.AsksEmail = QLineEdit(self.EditContactWindow)
        self.AsksEmail.move(290,160)
        self.AsksEmail.resize(200,35)
        self.AsksEmail.setText(Email)
        self.AsksEmail.setStyleSheet(self.InputStyle)

        #Save Button
        self.SaveButton = QPushButton(self.EditContactWindow)
        self.SaveButton.setText('Save')
        self.SaveButton.resize(130,30)
        self.SaveButton.setStyleSheet(self.BlueButtonStyle)
        self.SaveButton.move(280,210)
        self.SaveButton.clicked.connect(self.SaveEditedContact)

        #Cancel Button
        self.CancelButton = QPushButton(self.EditContactWindow)
        self.CancelButton.setText("Cancel")
        self.CancelButton.resize(130,30)
        self.CancelButton.move(100,210)
        self.CancelButton.setStyleSheet(self.RedButtonStyle)
        self.CancelButton.clicked.connect(lambda: self.CancelWithWarning(self.EditContactWindow,"Changes to this contact will not be saved.\n\nDo you want to discard"
                                                                         " your edits?"))
        
        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.EditContactWindow)
        self.CloseShortcut.activated.connect(self.EditContactWindow.close)

        self.EditContactWindow.show()

    def ImportContacts(self):

        self.ImportContactWindow = QWidget()
        self.ImportContactWindow.setWindowTitle("Import Contacts")
        self.ImportContactWindow.resize(420,260)
        self.ImportContactWindow.setWindowIcon(QIcon(Path))

        # Title
        self.ImportContactLabel = QLabel(self.ImportContactWindow)
        self.ImportContactLabel.setText("Import Contacts")
        self.ImportContactLabel.setStyleSheet("font-size:24px; font-family:'Segoe UI'; font-weight:bold;")
        self.ImportContactLabel.move(130,20)

        # Instruction
        self.SelectFileLabel = QLabel(self.ImportContactWindow)
        self.SelectFileLabel.setText("Select file to import")
        self.SelectFileLabel.setStyleSheet("font-size:14px; font-family:'Segoe UI';")
        self.SelectFileLabel.move(30,65)

        # Path textbox
        self.ImportPathTextBox = QLineEdit(self.ImportContactWindow)
        self.ImportPathTextBox.resize(260,32)
        self.ImportPathTextBox.move(30,95)
        self.ImportPathTextBox.setPlaceholderText("Enter or browse .vcf file path")
        self.ImportPathTextBox.setStyleSheet(self.InputStyle)

        # Browse button
        self.ImportBrowseButton = QPushButton(self.ImportContactWindow)
        self.ImportBrowseButton.setText("Browse")
        self.ImportBrowseButton.resize(80,32)
        self.ImportBrowseButton.move(300,95)
        self.ImportBrowseButton.setStyleSheet(self.GreyButtonStyle)
        self.ImportBrowseButton.clicked.connect(self.BrowseVCFFile)

        # Selected file label
        self.ImportSelectedFileLabel = QLabel(self.ImportContactWindow)
        self.ImportSelectedFileLabel.setText("Selected file: none")
        self.ImportSelectedFileLabel.setStyleSheet("font-size:13px; font-family:'Segoe UI';")
        self.ImportSelectedFileLabel.resize(300,20)
        self.ImportSelectedFileLabel.move(30,140)

        # Contacts detected label
        self.ImportContactDetectedLabel = QLabel(self.ImportContactWindow)
        self.ImportContactDetectedLabel.setText("Contacts detected: 0")
        self.ImportContactDetectedLabel.setStyleSheet("font-size:13px; font-family:'Segoe UI';")
        self.ImportContactDetectedLabel.resize(300,20)
        self.ImportContactDetectedLabel.move(30,170)

        # Cancel button
        self.ImportCancelButton = QPushButton(self.ImportContactWindow)
        self.ImportCancelButton.setText("Cancel")
        self.ImportCancelButton.resize(80,32)
        self.ImportCancelButton.move(120,210)
        self.ImportCancelButton.setStyleSheet(self.RedButtonStyle)
        self.ImportCancelButton.clicked.connect(lambda:self.CancelWithWarning(window=self.ImportContactWindow,message="Import will be cancelled. \n\nNo contacts will be added to your contact book.\n\nDo you want to continue?"))

        # Import button
        self.ImportButton = QPushButton(self.ImportContactWindow)
        self.ImportButton.setText("Import")
        self.ImportButton.resize(80,32)
        self.ImportButton.move(220,210)
        self.ImportButton.setStyleSheet(self.BlueButtonStyle)
        self.ImportButton.clicked.connect(self.ImportDetectedContacts)

        # ESC shortcut
        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.ImportContactWindow)
        self.CloseShortcut.activated.connect(lambda: self.ImportContactWindow.close)

        self.ImportContactWindow.show()

    def ExportContacts(self):
        ExportingContacts = self.Manager.LoadContactsJSON()

        if not ExportingContacts:
            QMessageBox.warning(self.MainWindow,"No Contacts","Thre is no Contacts to export")
            return
        
        path,_ = QFileDialog.getSaveFileName(self.MainWindow,"Export Contacts","contacts.vcf","VCF files (*.vcf)")

        if not path:
            return
        
        self.Manager.ExportContactsToVCF(path)
        QMessageBox.information(self.MainWindow,"Export Successfully",f"{len(ExportingContacts)} contacts exported successfully.")
