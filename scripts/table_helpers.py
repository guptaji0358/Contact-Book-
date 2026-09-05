import ctypes
import html

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TableMixin:
    def GetNameFromRow(self, row):
        item = self.RecentsContactTable.item(row, 1)
        if item:
            return item.text().strip()

        widget = self.RecentsContactTable.cellWidget(row, 1)
        if widget:
            Html_Text = widget.text()
            PlainText = QTextDocumentFragment.fromHtml(Html_Text).toPlainText()
            return PlainText.strip()

        return None

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
                label_item.setBackground(QColor(45, 45, 45))
                label_item.setFlags(Qt.NoItemFlags)

                self.RecentsContactTable.setItem(label_row, 1, label_item)
                self.RecentsContactTable.setSpan(label_row, 1, 1, 3)

                previous_group = group

            row = self.RecentsContactTable.rowCount()
            self.RecentsContactTable.insertRow(row)

            checkbox = QCheckBox()
            container = QWidget()
            layout = QHBoxLayout(container)

            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            self.RecentsContactTable.setCellWidget(row, 0, container)

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

                self.RecentsContactTable.setCellWidget(row, 1, label)
                label.setProperty("contact_id", contact.get("id"))

            else:
                item = QTableWidgetItem("   " + name)
                item.setData(Qt.UserRole, contact.get("id"))
                self.RecentsContactTable.setItem(row, 1, item)

            phone_item = QTableWidgetItem("   " + phone)
            phone_item.setData(Qt.UserRole, contact.get("id"))
            self.RecentsContactTable.setItem(row, 2, phone_item)
            self.RecentsContactTable.setItem(row, 3, QTableWidgetItem("   " + email))

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
                label_item.setBackground(QColor(45, 45, 45))
                label_item.setFlags(Qt.NoItemFlags)

                self.RecentsContactTable.setItem(label_row, 1, label_item)
                self.RecentsContactTable.setSpan(label_row, 1, 1, 3)

                previous_group = group

            row = self.RecentsContactTable.rowCount()
            self.RecentsContactTable.insertRow(row)

            checkbox = QCheckBox()
            container = QWidget()
            layout = QHBoxLayout(container)

            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            self.RecentsContactTable.setCellWidget(row, 0, container)

            item = QTableWidgetItem("   " + name)
            item.setData(Qt.UserRole, contact.get("id"))
            self.RecentsContactTable.setItem(row, 1, item)

            phone_item = QTableWidgetItem("   " + phone)
            phone_item.setData(Qt.UserRole, contact.get("id"))
            self.RecentsContactTable.setItem(row, 2, phone_item)
            self.RecentsContactTable.setItem(row, 3, QTableWidgetItem("   " + email))

    def CloseButtonLogic(self, window):
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
            container = self.RecentsContactTable.cellWidget(row, 0)

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

        checkbox = self.RecentsContactTable.cellWidget(row, 0).findChild(QCheckBox)
        if self.SelectedRow == row:
            checkbox.setChecked(False)

            for col in range(self.RecentsContactTable.columnCount()):
                item = self.RecentsContactTable.item(row, col)

                if item:
                    item.setBackground(QBrush())

            self.SelectedRow = None
            return

        if self.SelectedRow is not None:
            old_checkbox = self.RecentsContactTable.cellWidget(self.SelectedRow, 0).findChild(QCheckBox)
            old_checkbox.setChecked(False)

            for col in range(self.RecentsContactTable.columnCount()):
                item = self.RecentsContactTable.item(self.SelectedRow, col)

                if item:
                    item.setBackground(QBrush())

        checkbox.setChecked(True)
        for col in range(self.RecentsContactTable.columnCount()):
            item = self.RecentsContactTable.item(row, col)

            if item:
                item.setBackground(QColor(37, 99, 235, 60))

        self.SelectedRow = row

    def DisableMaximizeButton(self, window):
        hwnd = int(window.winId())
        GWL_STYLE = -16
        WS_MAXIMIZEBOX = 0x00010000

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        style &= ~WS_MAXIMIZEBOX
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        ctypes.windll.user32.SetWindowPos(
            hwnd,
            0,
            0, 0, 0, 0,
            0x0027
        )
