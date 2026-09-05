import ctypes
import getpass
import re

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_LABEL_STYLE
from scripts.voip_engine import VoipEngine

ICON_PATH = "CONTACT_BOOK_ICON.png"


class CallScreenWidget(QWidget):
    """A QWidget that reports when it is closed, so ending a call by
    closing the window cleans up VOIP resources the same as an explicit
    End Call action would."""

    def __init__(self, on_closed, parent=None):
        super().__init__(parent)
        self.on_closed = on_closed

    def closeEvent(self, event):
        self.on_closed()
        super().closeEvent(event)


class CallMixin:
    def InitVoipEngine(self):
        self.Voip = VoipEngine()
        self.Voip.incoming_call.connect(self._OnIncomingCall)
        self.Voip.call_rejected.connect(self._OnCallRejected)
        self.Voip.call_failed.connect(self._OnCallFailed)

    def CallContact(self):
        CallData = self.GetSelectedRow()

        if CallData is None:
            return

        Name = self.GetNameFromRow(CallData)
        PhoneNo = self.RecentsContactTable.item(CallData, 2).text().strip()
        ContactID = self.RecentsContactTable.item(CallData, 2).data(Qt.UserRole)
        DialNumber = re.sub(r"[^0-9+]", "", PhoneNo)

        if not DialNumber:
            QMessageBox.warning(self.MainWindow, "Invalid Number", "This contact has no callable phone number.")
            return

        DeviceIP = ""
        for contact in self.Manager.LoadContactsJSON():
            if contact.get("id") == ContactID:
                DeviceIP = contact.get("device_ip", "").strip()
                break

        if DeviceIP:
            self._PlaceVoipCall(Name, PhoneNo, DeviceIP)
        else:
            HandoffOK = self._DialLaptopTelephony(DialNumber)
            if not HandoffOK:
                QApplication.clipboard().setText(DialNumber)
                QMessageBox.warning(
                    self.MainWindow,
                    "No Calling App Found",
                    "No app is registered to handle phone calls (tel: links) on this PC.\n\n"
                    "Install/open Phone Link and link your Android phone, then try again.\n\n"
                    f"{DialNumber} has been copied to your clipboard instead."
                )
                return

            self._OpenCallScreen(Name, PhoneNo, voip=False)

    def _DialLaptopTelephony(self, DialNumber):
        # Invokes the tel: handler registered in Windows directly (ShellExecute),
        # so it goes straight to whatever app owns tel: links (e.g. Phone Link)
        # instead of ever routing through a browser. SW_SHOWMINNOACTIVATE launches
        # it minimized in the background without stealing focus/foreground from
        # this window — it's not a hand-off, Contact Book stays in front.
        # Returns True only if Windows actually found a registered handler.
        SW_SHOWMINNOACTIVATE = 7
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "open", f"tel:{DialNumber}", None, None, SW_SHOWMINNOACTIVATE
        )
        return int(result) > 32

    def _PlaceVoipCall(self, Name, PhoneNo, DeviceIP):
        self._OpenCallScreen(Name, PhoneNo, voip=True)
        self.CallStatusLabel.setText("Calling...")

        MyName = getpass.getuser()
        connected = self.Voip.PlaceCall(DeviceIP, MyName, "")
        if connected:
            self._MarkCallConnected()

    def _OnCallRejected(self):
        if hasattr(self, "CallScreen") and self.CallScreen.isVisible():
            self.CallStatusLabel.setText("Call Declined")
            QTimer.singleShot(1500, self._EndCall)

    def _OnCallFailed(self, error):
        if hasattr(self, "CallScreen") and self.CallScreen.isVisible():
            self.CallStatusLabel.setText("Could not connect")
            QTimer.singleShot(1500, self._EndCall)

    def _OnIncomingCall(self, Name, Number, PeerIP):
        reply = QMessageBox.question(
            self.MainWindow,
            "Incoming Call",
            f"Incoming call from {Name} ({Number or PeerIP})",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.Voip.AcceptIncomingCall()
            self._OpenCallScreen(Name, Number or PeerIP, voip=True)
            self._MarkCallConnected()
        else:
            self.Voip.RejectIncomingCall()

    def _OpenCallScreen(self, Name, PhoneNo, voip):
        self.CallIsVoip = voip
        self._CallEnded = False

        self.CallScreen = CallScreenWidget(on_closed=self._EndCall)
        self.CallScreen.setWindowTitle("Ongoing Call")
        self.CallScreen.resize(320, 420)
        self.CallScreen.setWindowIcon(QIcon(ICON_PATH))
        self.CallScreen.setStyleSheet("background-color:#111827;")
        self.CallScreen.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        MainLayout = QVBoxLayout(self.CallScreen)
        MainLayout.setContentsMargins(20, 40, 20, 30)
        MainLayout.setSpacing(10)

        Initial = Name[0].upper() if Name else "?"

        self.CallAvatarLabel = QLabel(Initial, self.CallScreen)
        self.CallAvatarLabel.setFixedSize(100, 100)
        self.CallAvatarLabel.setAlignment(Qt.AlignCenter)
        self.CallAvatarLabel.setStyleSheet(
            "background-color:#2563EB; color:white; border-radius:50px; "
            "font-size:36px; font-family:'Segoe UI'; font-weight:bold;"
        )
        MainLayout.addWidget(self.CallAvatarLabel, alignment=Qt.AlignHCenter)
        MainLayout.addSpacing(10)

        self.CallNameLabel = QLabel(Name, self.CallScreen)
        self.CallNameLabel.setAlignment(Qt.AlignCenter)
        self.CallNameLabel.setStyleSheet(DIALOG_LABEL_STYLE + "color:white;")
        MainLayout.addWidget(self.CallNameLabel)

        self.CallNumberLabel = QLabel(PhoneNo, self.CallScreen)
        self.CallNumberLabel.setAlignment(Qt.AlignCenter)
        self.CallNumberLabel.setStyleSheet("color:#9CA3AF; font-size:13px; font-family:'Segoe UI';")
        MainLayout.addWidget(self.CallNumberLabel)

        StatusText = "Calling..." if voip else "Phone Link dialing in background"
        self.CallStatusLabel = QLabel(StatusText, self.CallScreen)
        self.CallStatusLabel.setAlignment(Qt.AlignCenter)
        self.CallStatusLabel.setStyleSheet("color:#22C55E; font-size:14px; font-family:'Segoe UI'; font-weight:bold;")
        MainLayout.addWidget(self.CallStatusLabel)

        self.CallSeconds = 0
        self.CallTimer = QTimer(self.CallScreen)
        self.CallTimer.timeout.connect(self._TickCallTimer)

        if not voip:
            # We only handed the number to an external app (Phone Link/Skype).
            # There's no way for us to know if a call actually connected there,
            # so we don't fake "Connected"/a timer here — just say what we know.
            self.CallNoteLabel = QLabel(
                "Check your phone/Phone Link for the actual call status.\nThis window doesn't track that call.",
                self.CallScreen
            )
            self.CallNoteLabel.setAlignment(Qt.AlignCenter)
            self.CallNoteLabel.setWordWrap(True)
            self.CallNoteLabel.setStyleSheet("color:#9CA3AF; font-size:11px; font-family:'Segoe UI';")
            MainLayout.addWidget(self.CallNoteLabel)

        MainLayout.addStretch(1)

        self.CallScreen.show()

    def _MarkCallConnected(self):
        self.CallStatusLabel.setText("Connected")
        self.CallTimer.start(1000)

    def _TickCallTimer(self):
        self.CallSeconds += 1
        minutes = self.CallSeconds // 60
        seconds = self.CallSeconds % 60
        self.CallStatusLabel.setText(f"{minutes:02d}:{seconds:02d}")

    def _EndCall(self):
        if getattr(self, "_CallEnded", False):
            return
        self._CallEnded = True

        self.CallTimer.stop()

        if hasattr(self, "CallConnectTimer"):
            self.CallConnectTimer.stop()

        if getattr(self, "CallIsVoip", False):
            self.Voip.EndCall()

        self.CallScreen.close()
