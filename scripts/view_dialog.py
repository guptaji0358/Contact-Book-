from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_TITLE_STYLE, DIALOG_LABEL_STYLE, GREY_BUTTON_STYLE

ICON_PATH = "CONTACT_BOOK_ICON.png"


class ViewDialogMixin:
    def ViewContacts(self):
        ViewData = self.GetSelectedRow()

        if ViewData is None:
            return

        Name = self.GetNameFromRow(ViewData)
        PhoneNo = self.RecentsContactTable.item(ViewData, 2).text().strip()
        Email = self.RecentsContactTable.item(ViewData, 3).text().strip()

        self.ViewContactsWindow = QWidget()
        self.ViewContactsWindow.setWindowTitle("Contact Details")
        self.ViewContactsWindow.resize(420, 250)
        self.ViewContactsWindow.setWindowIcon(QIcon(ICON_PATH))

        MainLayout = QVBoxLayout(self.ViewContactsWindow)
        MainLayout.setContentsMargins(30, 15, 30, 15)
        MainLayout.setSpacing(15)

        self.ViewContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewContactLabel.setText("Contact Details")
        self.ViewContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.ViewContactLabel.setAlignment(Qt.AlignCenter)
        MainLayout.addWidget(self.ViewContactLabel)

        FormLayout = QFormLayout()
        FormLayout.setSpacing(12)
        FormLayout.setLabelAlignment(Qt.AlignLeft)

        self.ViewNameLabel = QLabel("Name ->")
        self.ViewNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewNameContactLabel = QLabel(Name)
        self.ViewNameContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.ViewNameLabel, self.ViewNameContactLabel)

        self.ViewPhoneNoLabel = QLabel("Phone No. ->")
        self.ViewPhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewPhoneNoContactLabel = QLabel(PhoneNo)
        self.ViewPhoneNoContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.ViewPhoneNoLabel, self.ViewPhoneNoContactLabel)

        self.ViewEmailLabel = QLabel("Email ->")
        self.ViewEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewEmailContactLabel = QLabel(Email)
        self.ViewEmailContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        FormLayout.addRow(self.ViewEmailLabel, self.ViewEmailContactLabel)

        MainLayout.addLayout(FormLayout)
        MainLayout.addStretch(1)

        ButtonRow = QHBoxLayout()
        ButtonRow.addStretch(1)

        self.CloseButton = QPushButton(self.ViewContactsWindow)
        self.CloseButton.setText("Close")
        self.CloseButton.setFixedSize(130, 30)
        self.CloseButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))
        self.CloseButton.setStyleSheet(GREY_BUTTON_STYLE)
        self.CloseButton.setDefault(True)
        self.CloseButton.setCursor(Qt.PointingHandCursor)
        self.ViewContactsWindow.setWindowFlag(Qt.WindowCloseButtonHint, True)
        ButtonRow.addWidget(self.CloseButton)
        ButtonRow.addStretch(1)

        MainLayout.addLayout(ButtonRow)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.ViewContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))

        self.ViewContactsWindow.show()
        self.DisableMaximizeButton(self.ViewContactsWindow)
