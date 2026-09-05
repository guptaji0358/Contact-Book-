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

        self.ViewContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewContactLabel.setText("Contact Details")
        self.ViewContactLabel.setStyleSheet(DIALOG_TITLE_STYLE)
        self.ViewContactLabel.move(85, 10)

        self.ViewNameLabel = QLabel(self.ViewContactsWindow)
        self.ViewNameLabel.setText("Name ->")
        self.ViewNameLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewNameLabel.move(30, 80)

        self.ViewNameContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewNameContactLabel.setText(Name)
        self.ViewNameContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewNameContactLabel.move(160, 80)

        self.ViewPhoneNoLabel = QLabel(self.ViewContactsWindow)
        self.ViewPhoneNoLabel.setText("Phone No. ->")
        self.ViewPhoneNoLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewPhoneNoLabel.move(30, 120)

        self.ViewPhoneNoContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewPhoneNoContactLabel.setText(PhoneNo)
        self.ViewPhoneNoContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewPhoneNoContactLabel.move(160, 120)

        self.ViewEmailLabel = QLabel(self.ViewContactsWindow)
        self.ViewEmailLabel.setText("Email ->")
        self.ViewEmailLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewEmailLabel.move(30, 160)

        self.ViewEmailContactLabel = QLabel(self.ViewContactsWindow)
        self.ViewEmailContactLabel.setText(Email)
        self.ViewEmailContactLabel.setStyleSheet(DIALOG_LABEL_STYLE)
        self.ViewEmailContactLabel.move(160, 160)

        self.CloseButton = QPushButton(self.ViewContactsWindow)
        self.CloseButton.setText("Close")
        self.CloseButton.resize(130, 30)
        self.CloseButton.clicked.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))
        self.CloseButton.setStyleSheet(GREY_BUTTON_STYLE)
        self.CloseButton.move(110, 200)
        self.CloseButton.setDefault(True)
        self.CloseButton.setCursor(Qt.PointingHandCursor)
        self.ViewContactsWindow.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.CloseShortcut = QShortcut(QKeySequence("Esc"), self.ViewContactsWindow)
        self.CloseShortcut.activated.connect(lambda: self.CloseButtonLogic(window=self.ViewContactsWindow))

        self.ViewContactsWindow.show()
        self.DisableMaximizeButton(self.ViewContactsWindow)
