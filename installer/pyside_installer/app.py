"""
A small PySide6 installer wizard for Contact Book, replacing the default
Inno Setup UI. It copies the already-frozen app (produced by PyInstaller,
see installer/ContactBook.spec) out of its own bundled payload into a
user-chosen folder, creates shortcuts, and registers an uninstaller.

This script itself gets frozen (see installer/pyside_installer.spec) into
ContactBookSetup.exe, with the frozen app bundled alongside it as data
under a "payload" folder.
"""
import os
import shutil
import sys
import winreg

from PySide6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QProgressBar, QCheckBox, QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QIcon, QFont

APP_NAME = "Contact Book"
APP_VERSION = "1.0.0"
PUBLISHER = "Robin Gupta"
EXE_NAME = "ContactBook.exe"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ContactBook"


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

            self._write_uninstaller()
            self._register_uninstall_entry()
            self.finished.emit()
        except Exception as error:
            self.failed.emit(str(error))

    def _write_uninstaller(self):
        uninstall_bat = os.path.join(self.target_dir, "uninstall.bat")
        with open(uninstall_bat, "w", encoding="utf-8") as f:
            f.write(
                "@echo off\n"
                "setlocal\n"
                'set "APPDIR=%~dp0"\n'
                'taskkill /F /IM "{exe}" >nul 2>nul\n'
                "timeout /t 1 /nobreak >nul\n"
                'del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app}.lnk" 2>nul\n'
                'del "%USERPROFILE%\\Desktop\\{app}.lnk" 2>nul\n'
                'reg delete "HKCU\\{key}" /f >nul 2>nul\n'
                'cd /d "%TEMP%"\n'
                'rmdir /S /Q "%APPDIR%"\n'
                "endlocal\n".format(exe=EXE_NAME, app=APP_NAME, key=UNINSTALL_KEY)
            )

    def _register_uninstall_entry(self):
        exe_path = os.path.join(self.target_dir, EXE_NAME)
        uninstall_bat = os.path.join(self.target_dir, "uninstall.bat")

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY) as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, APP_VERSION)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, PUBLISHER)
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, exe_path)
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.target_dir)
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'cmd /c ""{uninstall_bat}""')
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
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 25, 30, 20)
        self.layout.setSpacing(12)

        title_label = QLabel(title)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)
        self.layout.addWidget(title_label)


class WelcomePage(WizardPage):
    def __init__(self):
        super().__init__(f"Welcome to {APP_NAME} Setup")
        text = QLabel(
            f"This wizard will install {APP_NAME} {APP_VERSION} on your computer.\n\n"
            "It's recommended you close any other applications before continuing."
        )
        text.setWordWrap(True)
        self.layout.addWidget(text)
        self.layout.addStretch(1)


class OptionsPage(WizardPage):
    def __init__(self):
        super().__init__("Choose Install Options")

        location_label = QLabel("Install folder:")
        self.layout.addWidget(location_label)

        LocationRow = QHBoxLayout()
        self.LocationEdit = QLineEdit(default_install_dir())
        LocationRow.addWidget(self.LocationEdit, 1)

        BrowseButton = QPushButton("Browse")
        BrowseButton.clicked.connect(self._browse)
        LocationRow.addWidget(BrowseButton)
        self.layout.addLayout(LocationRow)

        self.layout.addSpacing(10)

        self.DesktopShortcutCheck = QCheckBox("Create a desktop shortcut")
        self.DesktopShortcutCheck.setChecked(True)
        self.layout.addWidget(self.DesktopShortcutCheck)

        self.StartMenuShortcutCheck = QCheckBox("Create a Start Menu shortcut")
        self.StartMenuShortcutCheck.setChecked(True)
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
        self.layout.addWidget(self.StatusLabel)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setRange(0, 100)
        self.layout.addWidget(self.ProgressBar)

        self.layout.addStretch(1)


class FinishPage(WizardPage):
    def __init__(self):
        super().__init__(f"{APP_NAME} Setup Complete")

        self.SummaryLabel = QLabel(f"{APP_NAME} has been installed successfully.")
        self.SummaryLabel.setWordWrap(True)
        self.layout.addWidget(self.SummaryLabel)

        self.LaunchCheck = QCheckBox(f"Launch {APP_NAME} now")
        self.LaunchCheck.setChecked(True)
        self.layout.addWidget(self.LaunchCheck)

        self.layout.addStretch(1)


class InstallerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Setup")
        self.resize(520, 380)

        icon_path = resource_path("payload", "CONTACT_BOOK_ICON.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        OuterLayout = QVBoxLayout(self)
        OuterLayout.setContentsMargins(0, 0, 0, 0)
        OuterLayout.setSpacing(0)

        self.Stack = QStackedWidget()
        self.WelcomePage = WelcomePage()
        self.OptionsPage = OptionsPage()
        self.InstallingPage = InstallingPage()
        self.FinishPage = FinishPage()

        for page in (self.WelcomePage, self.OptionsPage, self.InstallingPage, self.FinishPage):
            self.Stack.addWidget(page)

        OuterLayout.addWidget(self.Stack, 1)

        NavRow = QHBoxLayout()
        NavRow.setContentsMargins(20, 10, 20, 15)
        self.BackButton = QPushButton("Back")
        self.NextButton = QPushButton("Next")
        self.CancelButton = QPushButton("Cancel")

        self.BackButton.clicked.connect(self._go_back)
        self.NextButton.clicked.connect(self._go_next)
        self.CancelButton.clicked.connect(self.close)

        NavRow.addWidget(self.BackButton)
        NavRow.addStretch(1)
        NavRow.addWidget(self.NextButton)
        NavRow.addWidget(self.CancelButton)
        OuterLayout.addLayout(NavRow)

        self.BackButton.setEnabled(False)
        self._install_thread = None

    def _current_index(self):
        return self.Stack.currentIndex()

    def _go_back(self):
        index = self._current_index()
        if index > 0:
            self.Stack.setCurrentIndex(index - 1)
        self.BackButton.setEnabled(self._current_index() > 0)

    def _go_next(self):
        index = self._current_index()

        if self.Stack.currentWidget() is self.OptionsPage:
            self._start_install()
            return

        if self.Stack.currentWidget() is self.FinishPage:
            self._finish()
            return

        self.Stack.setCurrentIndex(index + 1)
        self.BackButton.setEnabled(self._current_index() > 0)

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
        self.BackButton.setEnabled(False)
        self.NextButton.setEnabled(False)
        self.CancelButton.setEnabled(False)

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

    def _on_install_failed(self, error_message):
        QMessageBox.critical(self, "Installation Failed", error_message)
        self.close()

    def _on_install_finished(self):
        self._create_shortcuts()

        self.Stack.setCurrentIndex(self.Stack.indexOf(self.FinishPage))
        self.NextButton.setText("Finish")
        self.NextButton.setEnabled(True)

    def _create_shortcuts(self):
        exe_path = os.path.join(self._target_dir, EXE_NAME)
        icon_path = resource_path("payload", "CONTACT_BOOK_ICON.ico")
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
