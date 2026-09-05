"""
A custom PySide6 installer wizard for Contact Book, replacing the default
Inno Setup UI. It copies the already-frozen app (produced by PyInstaller,
see installer/ContactBook.spec) out of its own bundled payload into a
user-chosen folder, creates shortcuts, and registers an uninstaller.

This script itself gets frozen (see installer/pyside_installer.spec) into
ContactBookSetup.exe, with the frozen app (and a prebuilt Uninstall.exe,
see uninstaller_app.py) bundled alongside it as data under a "payload"
folder.
"""
import os
import shutil
import sys
import winreg

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QProgressBar, QCheckBox, QFileDialog,
    QMessageBox, QTextEdit, QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QIcon, QFont, QPixmap

APP_NAME = "Contact Book"
APP_VERSION = "1.0.0"
PUBLISHER = "Robin Gupta"
EXE_NAME = "ContactBook.exe"
UNINSTALL_EXE_NAME = "Uninstall.exe"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ContactBook"

BG_DARK = "#0B1220"
BG_PANEL = "#111827"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
TEXT_MUTED = "#9CA3AF"

AGREEMENT_TEXT = f"""\
Before you install {APP_NAME}, please read this:

1. Local storage only
   All contacts you add are stored in a local database file on this PC,
   next to the app. Nothing is uploaded, synced, or shared with any
   server. Nobody but you (and anyone with access to this PC) can see it.

2. This is a rough address book, not a phone
   {APP_NAME} is a place to keep names, numbers, and emails organized.
   By itself it cannot place a real cellular phone call.

3. Real calls need Phone Link
   To actually place a call through a paired Android phone from this
   app, you must separately install and set up Microsoft Phone Link and
   link it to your phone first. Without that setup, the Call button can
   only hand a number off to whatever app Windows has registered for
   phone calls (or fails with a message telling you so).

By clicking "I Agree" below, you confirm you understand both points.
"""

STEP_NAMES = ["Welcome", "Agreement", "Options", "Installing", "Finish"]


def resource_path(*parts):
    """Path to a bundled resource, working both frozen (PyInstaller) and unfrozen."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def default_install_dir():
    return os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", APP_NAME)


class CopyWorker(QObject):
    progress = Signal(int, str)
    finished = Signal()
    failed = Signal(str)

    def __init__(self, source_dir, target_dir):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir

    def run(self):
        try:
            file_list = []
            for root, _dirs, files in os.walk(self.source_dir):
                for name in files:
                    file_list.append(os.path.join(root, name))

            total = max(len(file_list), 1)
            os.makedirs(self.target_dir, exist_ok=True)

            for i, src_path in enumerate(file_list, start=1):
                rel_path = os.path.relpath(src_path, self.source_dir)
                dest_path = os.path.join(self.target_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                self.progress.emit(int(i * 100 / total), rel_path)

            self._register_uninstall_entry()
            self.finished.emit()
        except Exception as error:
            self.failed.emit(str(error))

    def _register_uninstall_entry(self):
        exe_path = os.path.join(self.target_dir, EXE_NAME)
        uninstaller_path = os.path.join(self.target_dir, UNINSTALL_EXE_NAME)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY) as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, APP_VERSION)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, PUBLISHER)
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, exe_path)
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.target_dir)
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstaller_path}"')
            winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)


def create_shortcut(shortcut_path, target_path, working_dir, icon_path):
    import win32com.client

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = working_dir
    shortcut.IconLocation = icon_path
    shortcut.Save()


class WizardPage(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setStyleSheet(f"background-color:{BG_DARK}; color:white;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(36, 30, 36, 20)
        self.layout.setSpacing(14)

        title_label = QLabel(title)
        font = QFont("Segoe UI", 16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color:white;")
        self.layout.addWidget(title_label)

        rule = QFrame()
        rule.setFrameShape(QFrame.HLine)
        rule.setStyleSheet(f"background-color:{ACCENT}; max-height:2px; border:none;")
        self.layout.addWidget(rule)
        self.layout.addSpacing(6)


class WelcomePage(WizardPage):
    def __init__(self):
        super().__init__(f"Welcome to {APP_NAME}")

        icon_path = resource_path("payload", "CONTACT_BOOK_ICON.png")
        if os.path.exists(icon_path):
            logo = QLabel()
            pixmap = QPixmap(icon_path).scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignHCenter)
            self.layout.addWidget(logo)
            self.layout.addSpacing(10)

        text = QLabel(
            f"This wizard will install {APP_NAME} {APP_VERSION} on your computer.\n\n"
            "It's recommended you close any other applications before continuing."
        )
        text.setWordWrap(True)
        text.setStyleSheet(f"color:{TEXT_MUTED}; font-size:13px;")
        self.layout.addWidget(text)
        self.layout.addStretch(1)


class AgreementPage(WizardPage):
    def __init__(self):
        super().__init__("License & Data Agreement")

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        text_box.setPlainText(AGREEMENT_TEXT)
        text_box.setStyleSheet(
            f"background-color:{BG_PANEL}; color:white; border:1px solid #1F2937; "
            "border-radius:6px; padding:10px; font-size:12px;"
        )
        self.layout.addWidget(text_box, 1)

        self.AgreeCheck = QCheckBox("I have read and agree to the terms above")
        self.AgreeCheck.setStyleSheet("color:white; font-size:13px;")
        self.layout.addWidget(self.AgreeCheck)


class OptionsPage(WizardPage):
    def __init__(self):
        super().__init__("Choose Install Options")

        location_label = QLabel("Install folder:")
        location_label.setStyleSheet(f"color:{TEXT_MUTED};")
        self.layout.addWidget(location_label)

        LocationRow = QHBoxLayout()
        self.LocationEdit = QLineEdit(default_install_dir())
        self.LocationEdit.setStyleSheet(
            f"background-color:{BG_PANEL}; color:white; border:1px solid #1F2937; "
            "border-radius:4px; padding:6px;"
        )
        LocationRow.addWidget(self.LocationEdit, 1)

        BrowseButton = QPushButton("Browse")
        BrowseButton.setCursor(Qt.PointingHandCursor)
        BrowseButton.clicked.connect(self._browse)
        LocationRow.addWidget(BrowseButton)
        self.layout.addLayout(LocationRow)

        self.layout.addSpacing(10)

        self.DesktopShortcutCheck = QCheckBox("Create a desktop shortcut")
        self.DesktopShortcutCheck.setChecked(True)
        self.DesktopShortcutCheck.setStyleSheet("color:white;")
        self.layout.addWidget(self.DesktopShortcutCheck)

        self.StartMenuShortcutCheck = QCheckBox("Create a Start Menu shortcut")
        self.StartMenuShortcutCheck.setChecked(True)
        self.StartMenuShortcutCheck.setStyleSheet("color:white;")
        self.layout.addWidget(self.StartMenuShortcutCheck)

        self.layout.addStretch(1)

    def _browse(self):
        chosen = QFileDialog.getExistingDirectory(self, "Choose Install Folder", self.LocationEdit.text())
        if chosen:
            self.LocationEdit.setText(os.path.join(chosen, APP_NAME))


class InstallingPage(WizardPage):
    def __init__(self):
        super().__init__("Installing")

        self.StatusLabel = QLabel("Preparing...")
        self.StatusLabel.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        self.layout.addWidget(self.StatusLabel)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setTextVisible(True)
        self.ProgressBar.setStyleSheet(f"""
            QProgressBar {{
                background-color:{BG_PANEL}; border:1px solid #1F2937; border-radius:6px;
                color:white; text-align:center; height:22px;
            }}
            QProgressBar::chunk {{
                background-color:{ACCENT}; border-radius:6px;
            }}
        """)
        self.layout.addWidget(self.ProgressBar)

        self.layout.addStretch(1)


class FinishPage(WizardPage):
    def __init__(self):
        super().__init__("Setup Complete")

        self.SummaryLabel = QLabel(f"{APP_NAME} has been installed successfully.")
        self.SummaryLabel.setWordWrap(True)
        self.SummaryLabel.setStyleSheet(f"color:{TEXT_MUTED}; font-size:13px;")
        self.layout.addWidget(self.SummaryLabel)

        self.LaunchCheck = QCheckBox(f"Launch {APP_NAME} now")
        self.LaunchCheck.setChecked(True)
        self.LaunchCheck.setStyleSheet("color:white;")
        self.layout.addWidget(self.LaunchCheck)

        self.layout.addStretch(1)


class StepSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(170)
        self.setStyleSheet(f"background-color:{BG_PANEL};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 16, 20)
        layout.setSpacing(18)

        icon_path = resource_path("payload", "CONTACT_BOOK_ICON.png")
        if os.path.exists(icon_path):
            logo = QLabel()
            pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            layout.addWidget(logo)

        name_label = QLabel(APP_NAME)
        name_label.setStyleSheet("color:white; font-size:15px; font-weight:bold;")
        layout.addWidget(name_label)
        layout.addSpacing(10)

        self._step_labels = []
        for name in STEP_NAMES:
            label = QLabel(f"○  {name}")
            label.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
            layout.addWidget(label)
            self._step_labels.append(label)

        layout.addStretch(1)

    def set_active_step(self, index):
        for i, label in enumerate(self._step_labels):
            name = STEP_NAMES[i]
            if i < index:
                label.setText(f"●  {name}")
                label.setStyleSheet(f"color:{ACCENT}; font-size:12px;")
            elif i == index:
                label.setText(f"➤  {name}")
                label.setStyleSheet("color:white; font-size:12px; font-weight:bold;")
            else:
                label.setText(f"○  {name}")
                label.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")


BUTTON_STYLE = f"""
    QPushButton {{
        background-color:{ACCENT}; color:white; border:none; border-radius:5px;
        padding:8px 18px; font-size:13px;
    }}
    QPushButton:hover {{ background-color:{ACCENT_HOVER}; }}
    QPushButton:disabled {{ background-color:#374151; color:#6B7280; }}
"""
GHOST_BUTTON_STYLE = f"""
    QPushButton {{
        background-color:transparent; color:{TEXT_MUTED}; border:1px solid #374151;
        border-radius:5px; padding:8px 18px; font-size:13px;
    }}
    QPushButton:hover {{ color:white; border-color:{ACCENT}; }}
    QPushButton:disabled {{ color:#374151; border-color:#1F2937; }}
"""


class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Setup")
        self.resize(680, 460)
        self.setMinimumSize(620, 420)

        icon_path = resource_path("payload", "CONTACT_BOOK_ICON.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central = QWidget()
        central.setStyleSheet(f"background-color:{BG_DARK};")
        self.setCentralWidget(central)

        RootLayout = QHBoxLayout(central)
        RootLayout.setContentsMargins(0, 0, 0, 0)
        RootLayout.setSpacing(0)

        self.Sidebar = StepSidebar()
        RootLayout.addWidget(self.Sidebar)

        RightColumn = QVBoxLayout()
        RightColumn.setContentsMargins(0, 0, 0, 0)
        RightColumn.setSpacing(0)

        self.Stack = QStackedWidget()
        self.WelcomePage = WelcomePage()
        self.AgreementPage = AgreementPage()
        self.OptionsPage = OptionsPage()
        self.InstallingPage = InstallingPage()
        self.FinishPage = FinishPage()

        for page in (self.WelcomePage, self.AgreementPage, self.OptionsPage, self.InstallingPage, self.FinishPage):
            self.Stack.addWidget(page)

        RightColumn.addWidget(self.Stack, 1)

        NavRow = QHBoxLayout()
        NavRow.setContentsMargins(24, 14, 24, 14)
        self.BackButton = QPushButton("Back")
        self.NextButton = QPushButton("Next")
        self.CancelButton = QPushButton("Cancel")

        for btn in (self.BackButton, self.CancelButton):
            btn.setStyleSheet(GHOST_BUTTON_STYLE)
            btn.setCursor(Qt.PointingHandCursor)
        self.NextButton.setStyleSheet(BUTTON_STYLE)
        self.NextButton.setCursor(Qt.PointingHandCursor)

        self.BackButton.clicked.connect(self._go_back)
        self.NextButton.clicked.connect(self._go_next)
        self.CancelButton.clicked.connect(self.close)

        NavRow.addWidget(self.BackButton)
        NavRow.addStretch(1)
        NavRow.addWidget(self.NextButton)
        NavRow.addWidget(self.CancelButton)
        RightColumn.addLayout(NavRow)

        RootLayout.addLayout(RightColumn, 1)

        self.statusBar().setStyleSheet(
            f"background-color:{BG_PANEL}; color:{TEXT_MUTED}; font-size:11px; padding:4px 10px;"
        )
        self.statusBar().showMessage("Ready to install.")

        self.BackButton.setEnabled(False)
        self._install_thread = None
        self.Sidebar.set_active_step(0)

        self.AgreementPage.AgreeCheck.toggled.connect(self._sync_next_enabled)

    def _current_index(self):
        return self.Stack.currentIndex()

    def _sync_next_enabled(self):
        if self.Stack.currentWidget() is self.AgreementPage:
            self.NextButton.setEnabled(self.AgreementPage.AgreeCheck.isChecked())

    def _go_back(self):
        index = self._current_index()
        if index > 0:
            self.Stack.setCurrentIndex(index - 1)
        self.BackButton.setEnabled(self._current_index() > 0)
        self.Sidebar.set_active_step(self._current_index())
        self._sync_next_enabled()
        self.statusBar().showMessage(f"Step {self._current_index() + 1} of {len(STEP_NAMES)} — {STEP_NAMES[self._current_index()]}")

    def _go_next(self):
        index = self._current_index()

        if self.Stack.currentWidget() is self.AgreementPage and not self.AgreementPage.AgreeCheck.isChecked():
            return

        if self.Stack.currentWidget() is self.OptionsPage:
            self._start_install()
            return

        if self.Stack.currentWidget() is self.FinishPage:
            self._finish()
            return

        self.Stack.setCurrentIndex(index + 1)
        self.BackButton.setEnabled(self._current_index() > 0)
        self.Sidebar.set_active_step(self._current_index())
        self._sync_next_enabled()
        self.statusBar().showMessage(f"Step {self._current_index() + 1} of {len(STEP_NAMES)} — {STEP_NAMES[self._current_index()]}")

        if self.Stack.currentWidget() is self.FinishPage:
            self.NextButton.setText("Finish")
            self.CancelButton.setEnabled(False)
            self.BackButton.setEnabled(False)

    def _start_install(self):
        target_dir = self.OptionsPage.LocationEdit.text().strip()

        if not target_dir:
            QMessageBox.warning(self, "Invalid Folder", "Please choose an install folder.")
            return

        self.Stack.setCurrentIndex(self.Stack.indexOf(self.InstallingPage))
        self.Sidebar.set_active_step(self._current_index())
        self.BackButton.setEnabled(False)
        self.NextButton.setEnabled(False)
        self.CancelButton.setEnabled(False)
        self.statusBar().showMessage("Installing... this may take a moment.")

        self._target_dir = target_dir
        source_dir = resource_path("payload")

        self._install_thread = QThread(self)
        self._worker = CopyWorker(source_dir, target_dir)
        self._worker.moveToThread(self._install_thread)

        self._install_thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_install_finished)
        self._worker.failed.connect(self._on_install_failed)
        self._worker.finished.connect(self._install_thread.quit)
        self._worker.failed.connect(self._install_thread.quit)

        self._install_thread.start()

    def _on_progress(self, percent, current_file):
        self.InstallingPage.ProgressBar.setValue(percent)
        self.InstallingPage.StatusLabel.setText(f"Copying {current_file}")
        self.statusBar().showMessage(f"Installing... {percent}%")

    def _on_install_failed(self, error_message):
        self.statusBar().showMessage("Installation failed.")
        QMessageBox.critical(self, "Installation Failed", error_message)
        self.close()

    def _on_install_finished(self):
        self._create_shortcuts()

        self.Stack.setCurrentIndex(self.Stack.indexOf(self.FinishPage))
        self.Sidebar.set_active_step(self._current_index())
        self.NextButton.setText("Finish")
        self.NextButton.setEnabled(True)
        self.statusBar().showMessage("Installation complete.")

    def _create_shortcuts(self):
        exe_path = os.path.join(self._target_dir, EXE_NAME)
        # Point at the icon file already copied into the install folder, NOT
        # the one under resource_path() - that lives in the installer's own
        # temp extraction folder (sys._MEIPASS), which is deleted the moment
        # this installer process exits, leaving the shortcut's icon reference
        # dangling (shows as a blank/generic icon afterwards).
        icon_path = os.path.join(self._target_dir, "CONTACT_BOOK_ICON.ico")
        if not os.path.exists(icon_path):
            icon_path = exe_path

        try:
            if self.OptionsPage.DesktopShortcutCheck.isChecked():
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                create_shortcut(
                    os.path.join(desktop, f"{APP_NAME}.lnk"), exe_path, self._target_dir, icon_path
                )

            if self.OptionsPage.StartMenuShortcutCheck.isChecked():
                start_menu = os.path.join(
                    os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"
                )
                os.makedirs(start_menu, exist_ok=True)
                create_shortcut(
                    os.path.join(start_menu, f"{APP_NAME}.lnk"), exe_path, self._target_dir, icon_path
                )
        except Exception as error:
            QMessageBox.warning(self, "Shortcut Creation Failed", str(error))

    def _finish(self):
        if self.FinishPage.LaunchCheck.isChecked():
            exe_path = os.path.join(self._target_dir, EXE_NAME)
            try:
                os.startfile(exe_path)
            except OSError as error:
                QMessageBox.warning(self, "Could Not Launch", str(error))

        self.close()


def main():
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
