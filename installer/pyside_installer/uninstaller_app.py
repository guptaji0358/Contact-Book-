"""
A small PySide6 uninstaller GUI for Contact Book. This gets frozen (see
installer/uninstaller.spec) into Uninstall.exe, which the main installer
copies into the app's own install folder and points the Windows
"Add or Remove Programs" entry at.

Deleting the folder this exe itself lives in while it's still running is
not possible directly, so on confirm it does everything else (kill the
running app, remove shortcuts, remove the registry entry) itself, then
hands off a short delayed `rmdir` to a detached cmd process and exits -
by the time that runs, this exe's file lock is already released.
"""
import os
import subprocess
import sys
import winreg

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont

APP_NAME = "Contact Book"
EXE_NAME = "ContactBook.exe"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ContactBook"

BG_DARK = "#0B1220"
BG_PANEL = "#111827"
ACCENT = "#DC2626"
TEXT_MUTED = "#9CA3AF"


def install_dir():
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def remove_shortcuts():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop", f"{APP_NAME}.lnk")
    start_menu = os.path.join(
        os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", f"{APP_NAME}.lnk"
    )
    for path in (desktop, start_menu):
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


def remove_registry_entry():
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY)
    except FileNotFoundError:
        pass


class UninstallWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Uninstall {APP_NAME}")
        self.resize(420, 240)
        self.setStyleSheet(f"background-color:{BG_DARK}; color:white;")

        icon_path = os.path.join(install_dir(), "CONTACT_BOOK_ICON.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 20)
        layout.setSpacing(14)

        title = QLabel(f"Uninstall {APP_NAME}")
        font = QFont("Segoe UI", 14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        self.MessageLabel = QLabel(
            f"This will remove {APP_NAME} and its shortcuts from this computer.\n\n"
            "Your contact databases live inside the install folder and will be "
            "deleted too. If you want to keep them, back up the install folder "
            "first, then continue."
        )
        self.MessageLabel.setWordWrap(True)
        self.MessageLabel.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        layout.addWidget(self.MessageLabel)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setRange(0, 0)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setStyleSheet(f"""
            QProgressBar {{
                background-color:{BG_PANEL}; border:1px solid #1F2937; border-radius:6px; height:16px;
            }}
            QProgressBar::chunk {{ background-color:{ACCENT}; border-radius:6px; }}
        """)
        self.ProgressBar.hide()
        layout.addWidget(self.ProgressBar)

        layout.addStretch(1)

        ButtonRow = QHBoxLayout()
        ButtonRow.addStretch(1)

        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.setCursor(Qt.PointingHandCursor)
        self.CancelButton.setStyleSheet(
            "QPushButton { background-color:transparent; color:#9CA3AF; border:1px solid #374151; "
            "border-radius:5px; padding:8px 18px; } QPushButton:hover { color:white; }"
        )
        self.CancelButton.clicked.connect(self.close)
        ButtonRow.addWidget(self.CancelButton)

        self.UninstallButton = QPushButton("Uninstall")
        self.UninstallButton.setCursor(Qt.PointingHandCursor)
        self.UninstallButton.setStyleSheet(
            f"QPushButton {{ background-color:{ACCENT}; color:white; border:none; "
            "border-radius:5px; padding:8px 18px; } QPushButton:hover { background-color:#B91C1C; }"
        )
        self.UninstallButton.clicked.connect(self._start_uninstall)
        ButtonRow.addWidget(self.UninstallButton)

        layout.addLayout(ButtonRow)

    def _start_uninstall(self):
        self.UninstallButton.setEnabled(False)
        self.CancelButton.setEnabled(False)
        self.ProgressBar.show()
        self.MessageLabel.setText("Removing files, shortcuts, and registry entries...")
        QTimer.singleShot(200, self._perform_removal)

    def _perform_removal(self):
        target_dir = install_dir()

        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", EXE_NAME],
                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception:
            pass

        remove_shortcuts()
        remove_registry_entry()

        # Show (and let the user dismiss) the confirmation BEFORE scheduling
        # the self-delete below. This dialog blocks until clicked, and while
        # it's up this exe is still running - so if the delete had already
        # been scheduled at this point, it would fire and find Uninstall.exe
        # itself still locked, deleting everything else but leaving that one
        # file behind (the exact bug this ordering fixes).
        QMessageBox.information(self, "Uninstalled", f"{APP_NAME} has been uninstalled.")

        # This exe can't delete its own containing folder while running, so
        # hand off a delayed, retrying delete to a background cmd process and
        # exit immediately after - `self.close()` below returns control to
        # Qt's event loop essentially at once, releasing this exe's file lock
        # well within the first retry. `ping` is used for the delay (not
        # `timeout`, which needs a console and silently no-ops without one).
        # The retry loop (rather than one fixed delay) also covers PyInstaller
        # onefile's bootloader-parent + child process teardown taking longer
        # than expected, e.g. under antivirus scanning. DETACHED_PROCESS is
        # deliberately NOT combined with shell=True here - together they
        # silently made the spawned cmd exit without ever running rmdir.
        delete_cmd = (
            'cmd /c "ping -n 2 127.0.0.1 >nul & '
            f'for /l %n in (1,1,30) do (rmdir /s /q \"{target_dir}\" 2>nul & '
            f'if not exist \"{target_dir}\" exit /b 0 & ping -n 2 127.0.0.1 >nul)"'
        )
        subprocess.Popen(delete_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

        self.close()


def main():
    app = QApplication(sys.argv)
    window = UninstallWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
