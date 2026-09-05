import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.manager import ContactBookManager
from scripts.styles import (
    TABLE_STYLE, INPUT_STYLE,
    ICON_BLUE_BUTTON_STYLE, ICON_GREY_BUTTON_STYLE, ICON_RED_BUTTON_STYLE, ICON_GREEN_BUTTON_STYLE,
)
from scripts.icons import (
    svg_icon, ICON_EYE, ICON_PLUS, ICON_TRASH, ICON_PENCIL, ICON_CLOUD_DOWN, ICON_CLOUD_UP, ICON_PHONE, ICON_BOOK,
)

ICON_PATH = "CONTACT_BOOK_ICON.png"
BUTTON_ICON_SIZE = 24


class MainWindowMixin:
    def _make_icon_button(self, parent, icon_svg, tooltip, style, slot):
        button = QPushButton(parent)
        button.setIcon(svg_icon(icon_svg, color="#ffffff", size=BUTTON_ICON_SIZE))
        button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        button.resize(60, 50)
        button.setToolTip(tooltip)
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(slot)
        return button

    def BuildMainWindow(self):
        self.ContactBookApp = QApplication(sys.argv)

        self.MainWindow = QWidget()
        self.MainWindow.setWindowTitle("Contact Book")
        self.MainWindow.resize(685, 500)
        self.MainWindow.setWindowIcon(QIcon(ICON_PATH))

        self.InitBooks()
        self.Manager = ContactBookManager(db_path=self.ActiveBookPath)

        self.SearchEngineofContactsLabel = QLabel(self.MainWindow)
        self.SearchEngineofContactsLabel.resize(60, 25)
        self.SearchEngineofContactsLabel.setText("Search -->")
        self.SearchEngineofContactsLabel.move(20, 20)

        self.SearchEngineofContacts = QLineEdit(self.MainWindow)
        self.SearchEngineofContacts.resize(150, 35)
        self.SearchEngineofContacts.setStyleSheet(INPUT_STYLE)
        self.SearchEngineofContacts.setPlaceholderText("Search Contacts")
        self.SearchEngineofContacts.move(80, 20)
        self.SearchEngineofContacts.textChanged.connect(self.FilterContacts)
        self.SearchEngineofContacts.setClearButtonEnabled(True)

        self.BookSelector = QComboBox(self.MainWindow)
        self.BookSelector.resize(180, 35)
        self.BookSelector.move(260, 20)
        self.BookSelector.setStyleSheet(INPUT_STYLE)
        self.BookSelector.setContextMenuPolicy(Qt.CustomContextMenu)
        self.BookSelector.customContextMenuRequested.connect(self.ShowBookContextMenu)
        self.RefreshBookSelector()
        self.BookSelector.currentIndexChanged.connect(self.SwitchActiveBook)

        self.NewBookButton = self._make_icon_button(
            self.MainWindow, ICON_BOOK, "New Book", ICON_GREY_BUTTON_STYLE, self.CreateNewBook
        )
        self.NewBookButton.resize(40, 35)
        self.NewBookButton.move(450, 20)

        self.RecentsContactTable = QTableWidget(self.MainWindow)
        self.RecentsContactTable.setShowGrid(False)
        self.RecentsContactTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.RecentsContactTable.setFocusPolicy(Qt.NoFocus)
        self.RecentsContactTable.setColumnCount(4)
        self.RecentsContactTable.setHorizontalHeaderLabels(["", "Name", "Phone No.", "Email"])
        self.RecentsContactTable.resize(650, 300)
        self.RecentsContactTable.move(20, 80)
        self.RecentsContactTable.verticalHeader().setVisible(False)
        self.RecentsContactTable.setColumnWidth(0, 35)
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
        self.RecentsContactTable.setStyleSheet(TABLE_STYLE)

        self.SelectedRow = None
        self.LastDeletedContact = None
        self.LoadContactsIntoTable()
        self.InitVoipEngine()

        self.ViewContactButton = self._make_icon_button(
            self.MainWindow, ICON_EYE, "View Contacts", ICON_BLUE_BUTTON_STYLE, self.ViewContacts
        )
        self.ViewContactButton.move(130, 440)

        self.AddContactButton = self._make_icon_button(
            self.MainWindow, ICON_PLUS, "Add Contacts", ICON_BLUE_BUTTON_STYLE, self.AddContacts
        )
        self.AddContactButton.move(200, 440)

        self.EditContactButton = self._make_icon_button(
            self.MainWindow, ICON_PENCIL, "Edit Contacts", ICON_BLUE_BUTTON_STYLE, self.EditContacts
        )
        self.EditContactButton.move(270, 440)

        self.DeleteContactButton = self._make_icon_button(
            self.MainWindow, ICON_TRASH, "Delete Contacts", ICON_RED_BUTTON_STYLE, self.DeleteContacts
        )
        self.DeleteContactButton.move(340, 440)

        self.ImportContactButton = self._make_icon_button(
            self.MainWindow, ICON_CLOUD_DOWN, "Import Contacts", ICON_GREY_BUTTON_STYLE, self.ImportContacts
        )
        self.ImportContactButton.move(410, 440)

        self.ExportContactButton = self._make_icon_button(
            self.MainWindow, ICON_CLOUD_UP, "Export Contacts", ICON_GREY_BUTTON_STYLE, self.ExportContacts
        )
        self.ExportContactButton.move(480, 440)

        self.CallContactButton = self._make_icon_button(
            self.MainWindow, ICON_PHONE, "Call Contact", ICON_GREEN_BUTTON_STYLE, self.CallContact
        )
        self.CallContactButton.move(550, 440)

        self.MainWindow.show()
        self.DisableMaximizeButton(self.MainWindow)
        self.ContactBookApp.exec()
