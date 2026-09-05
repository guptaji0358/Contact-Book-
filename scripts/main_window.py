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
        button.setFixedSize(60, 50)
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

        MainLayout = QVBoxLayout(self.MainWindow)
        MainLayout.setContentsMargins(20, 20, 20, 20)
        MainLayout.setSpacing(15)

        TopRow = QHBoxLayout()
        TopRow.setSpacing(10)

        self.SearchEngineofContactsLabel = QLabel(self.MainWindow)
        self.SearchEngineofContactsLabel.setText("Search -->")
        TopRow.addWidget(self.SearchEngineofContactsLabel)

        self.SearchEngineofContacts = QLineEdit(self.MainWindow)
        self.SearchEngineofContacts.setFixedHeight(35)
        self.SearchEngineofContacts.setStyleSheet(INPUT_STYLE)
        self.SearchEngineofContacts.setPlaceholderText("Search Contacts")
        self.SearchEngineofContacts.textChanged.connect(self.FilterContacts)
        self.SearchEngineofContacts.setClearButtonEnabled(True)
        TopRow.addWidget(self.SearchEngineofContacts, 1)

        self.BookSelector = QComboBox(self.MainWindow)
        self.BookSelector.setFixedHeight(35)
        self.BookSelector.setMinimumWidth(180)
        self.BookSelector.setStyleSheet(INPUT_STYLE)
        self.BookSelector.setContextMenuPolicy(Qt.CustomContextMenu)
        self.BookSelector.customContextMenuRequested.connect(self.ShowBookContextMenu)
        self.RefreshBookSelector()
        self.BookSelector.currentIndexChanged.connect(self.SwitchActiveBook)
        TopRow.addWidget(self.BookSelector)

        self.NewBookButton = self._make_icon_button(
            self.MainWindow, ICON_BOOK, "New Book", ICON_GREY_BUTTON_STYLE, self.CreateNewBook
        )
        self.NewBookButton.setFixedSize(40, 35)
        TopRow.addWidget(self.NewBookButton)

        MainLayout.addLayout(TopRow)

        self.RecentsContactTable = QTableWidget(self.MainWindow)
        self.RecentsContactTable.setShowGrid(False)
        self.RecentsContactTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.RecentsContactTable.setFocusPolicy(Qt.NoFocus)
        self.RecentsContactTable.setColumnCount(4)
        self.RecentsContactTable.setHorizontalHeaderLabels(["", "Name", "Phone No.", "Email"])
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
        MainLayout.addWidget(self.RecentsContactTable, 1)

        self.SelectedRow = None
        self.LastDeletedContact = None
        self.LoadContactsIntoTable()
        self.InitVoipEngine()

        ButtonRow = QHBoxLayout()
        ButtonRow.setSpacing(10)
        ButtonRow.addStretch(1)

        self.ViewContactButton = self._make_icon_button(
            self.MainWindow, ICON_EYE, "View Contacts", ICON_BLUE_BUTTON_STYLE, self.ViewContacts
        )
        ButtonRow.addWidget(self.ViewContactButton)

        self.AddContactButton = self._make_icon_button(
            self.MainWindow, ICON_PLUS, "Add Contacts", ICON_BLUE_BUTTON_STYLE, self.AddContacts
        )
        ButtonRow.addWidget(self.AddContactButton)

        self.EditContactButton = self._make_icon_button(
            self.MainWindow, ICON_PENCIL, "Edit Contacts", ICON_BLUE_BUTTON_STYLE, self.EditContacts
        )
        ButtonRow.addWidget(self.EditContactButton)

        self.DeleteContactButton = self._make_icon_button(
            self.MainWindow, ICON_TRASH, "Delete Contacts", ICON_RED_BUTTON_STYLE, self.DeleteContacts
        )
        ButtonRow.addWidget(self.DeleteContactButton)

        self.ImportContactButton = self._make_icon_button(
            self.MainWindow, ICON_CLOUD_DOWN, "Import Contacts", ICON_GREY_BUTTON_STYLE, self.ImportContacts
        )
        ButtonRow.addWidget(self.ImportContactButton)

        self.ExportContactButton = self._make_icon_button(
            self.MainWindow, ICON_CLOUD_UP, "Export Contacts", ICON_GREY_BUTTON_STYLE, self.ExportContacts
        )
        ButtonRow.addWidget(self.ExportContactButton)

        self.CallContactButton = self._make_icon_button(
            self.MainWindow, ICON_PHONE, "Call Contact", ICON_GREEN_BUTTON_STYLE, self.CallContact
        )
        ButtonRow.addWidget(self.CallContactButton)

        ButtonRow.addStretch(1)
        MainLayout.addLayout(ButtonRow)

        self.MainWindow.show()
        self.DisableMaximizeButton(self.MainWindow)
        self.ContactBookApp.exec()
