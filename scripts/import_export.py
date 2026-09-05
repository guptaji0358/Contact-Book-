import os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_TITLE_STYLE, INPUT_STYLE, BLUE_BUTTON_STYLE, RED_BUTTON_STYLE, GREY_BUTTON_STYLE

ICON_PATH = "CONTACT_BOOK_ICON.png"


class DropTargetWidget(QWidget):
    """A QWidget that accepts a dragged-in .vcf file and forwards its path."""

    def __init__(self, on_file_dropped, parent=None):
        super().__init__(parent)
        self.on_file_dropped = on_file_dropped
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and any(
            url.toLocalFile().lower().endswith(".vcf") for url in event.mimeData().urls()
        ):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        vcf_paths = [
            url.toLocalFile() for url in event.mimeData().urls()
            if url.toLocalFile().lower().endswith(".vcf")
        ]

        if vcf_paths:
            self.on_file_dropped(vcf_paths[0])
            event.acceptProposedAction()
        else:
            event.ignore()


class ImportExportMixin:
    def LoadVCFFile(self, VCFPath):
        self.ImportPathTextBox.setText(VCFPath)
        self.ImportPathTextBox.setToolTip(VCFPath)

        file_name = os.path.basename(VCFPath)
        self.ImportSelectedFileLabel.setText(f"Selected file: {file_name}")
        self.ImportSelectedFileLabel.setToolTip(file_name)

        contacts = self.Manager.ImportAndReadVCF(VCFPath)

        self.ImportContactDetectedLabel.setText(f"Contacts detected: {len(contacts)}")
        self.ImportedContacts = contacts

    def BrowseVCFFile(self):
        VCFPath, _ = QFileDialog.getOpenFileName(self.ImportContactWindow, "Select VCF File", "", "VCF files(*.vcf);;All files(*)")

        if not VCFPath:
            return

        self.LoadVCFFile(VCFPath)

    def ImportDetectedContacts(self):
        newid = 1
        existing_contacts = self.Manager.LoadContactsJSON()

        if not hasattr(self, "ImportedContacts") or not self.ImportedContacts:
            QMessageBox.warning(self.ImportContactWindow, "No File Selected", "Please select a VCF file first.")
            return

        if existing_contacts:
            newid = max(contact.get("id", 0) for contact in existing_contacts) + 1

        for contact in self.ImportedContacts:
            self.Manager.addContacts(id=newid, name=contact["name"], phone=contact["phone"], email=contact["email"])
            newid += 1

        QMessageBox.information(
            self.ImportContactWindow,
            "Import Successful",
            f"{len(self.ImportedContacts)} contacts imported successfully."
        )

        self.LoadContactsIntoTable()
        self.ImportContactWindow.close()

    def ImportContacts(self):
        self.ImportContactWindow = DropTargetWidget(on_file_dropped=self.LoadVCFFile)
        self.ImportContactWindow.setWindowTitle("Import Contacts")
        self.ImportContactWindow.resize(420, 260)
        self.ImportContactWindow.setWindowIcon(QIcon(ICON_PATH))

        self.ImportContactLabel = QLabel(self.ImportContactWindow)
        self.ImportContactLabel.setText("Import Contacts")
        self.ImportContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.ImportContactLabel.move(130, 20)

        self.SelectFileLabel = QLabel(self.ImportContactWindow)
        self.SelectFileLabel.setText("Select file to import")
        self.SelectFileLabel.setStyleSheet("font-size:14px; font-family:'Segoe UI';")
        self.SelectFileLabel.move(30, 65)

        self.ImportPathTextBox = QLineEdit(self.ImportContactWindow)
        self.ImportPathTextBox.resize(260, 32)
        self.ImportPathTextBox.move(30, 95)
        self.ImportPathTextBox.setPlaceholderText("Enter or browse .vcf file path")
        self.ImportPathTextBox.setStyleSheet(INPUT_STYLE)

        self.ImportBrowseButton = QPushButton(self.ImportContactWindow)
        self.ImportBrowseButton.setText("Browse")
        self.ImportBrowseButton.resize(80, 32)
        self.ImportBrowseButton.move(300, 95)
        self.ImportBrowseButton.setStyleSheet(GREY_BUTTON_STYLE)
        self.ImportBrowseButton.setCursor(Qt.PointingHandCursor)
        self.ImportBrowseButton.clicked.connect(self.BrowseVCFFile)

        self.ImportSelectedFileLabel = QLabel(self.ImportContactWindow)
        self.ImportSelectedFileLabel.setText("Selected file: none")
        self.ImportSelectedFileLabel.setStyleSheet("font-size:13px; font-family:'Segoe UI';")
        self.ImportSelectedFileLabel.resize(300, 20)
        self.ImportSelectedFileLabel.move(30, 140)

        self.ImportDropHintLabel = QLabel(self.ImportContactWindow)
        self.ImportDropHintLabel.setText("or drag & drop a .vcf file anywhere in this window")
        self.ImportDropHintLabel.setStyleSheet("font-size:12px; font-family:'Segoe UI'; color:#888;")
        self.ImportDropHintLabel.resize(360, 20)
        self.ImportDropHintLabel.move(30, 190)

        self.ImportContactDetectedLabel = QLabel(self.ImportContactWindow)
        self.ImportContactDetectedLabel.setText("Contacts detected: 0")
        self.ImportContactDetectedLabel.setStyleSheet("font-size:13px; font-family:'Segoe UI';")
        self.ImportContactDetectedLabel.resize(300, 20)
        self.ImportContactDetectedLabel.move(30, 170)

        self.ImportCancelButton = QPushButton(self.ImportContactWindow)
        self.ImportCancelButton.setText("Cancel")
        self.ImportCancelButton.resize(80, 32)
        self.ImportCancelButton.move(120, 210)
        self.ImportCancelButton.setStyleSheet(RED_BUTTON_STYLE)
        self.ImportCancelButton.setCursor(Qt.PointingHandCursor)
        self.ImportCancelButton.clicked.connect(
            lambda: self.CancelWithWarning(
                window=self.ImportContactWindow,
                message="Import will be cancelled. \n\nNo contacts will be added to your contact book.\n\nDo you want to continue?"
            )
        )

        self.ImportButton = QPushButton(self.ImportContactWindow)
        self.ImportButton.setText("Import")
        self.ImportButton.resize(80, 32)
        self.ImportButton.move(220, 210)
        self.ImportButton.setStyleSheet(BLUE_BUTTON_STYLE)
        self.ImportButton.setCursor(Qt.PointingHandCursor)
        self.ImportButton.clicked.connect(self.ImportDetectedContacts)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.ImportContactWindow)
        self.CloseShortcut.activated.connect(lambda: self.ImportContactWindow.close)

        self.ImportContactWindow.show()
        self.DisableMaximizeButton(self.ImportContactWindow)

    def ExportContacts(self):
        ExportingContacts = self.Manager.LoadContactsJSON()

        if not ExportingContacts:
            QMessageBox.warning(self.MainWindow, "No Contacts", "Thre is no Contacts to export")
            return

        path, _ = QFileDialog.getSaveFileName(self.MainWindow, "Export Contacts", "contacts.vcf", "VCF files (*.vcf)")

        if not path:
            return

        self.Manager.ExportContactsToVCF(path)
        QMessageBox.information(self.MainWindow, "Export Successfully", f"{len(ExportingContacts)} contacts exported successfully.")
