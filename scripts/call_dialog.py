import ctypes
import getpass
import re

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from scripts.styles import DIALOG_LABEL_STYLE, CALL_TOGGLE_BUTTON_STYLE, CALL_END_BUTTON_STYLE
from scripts.icons import svg_icon, ICON_MIC, ICON_MIC_OFF, ICON_SPEAKER, ICON_END_CALL
from scripts.voip_engine import VoipEngine

ICON_PATH = "CONTACT_BOOK_ICON.png"


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

        self.CallScreen = QWidget()
        self.CallScreen.setWindowTitle("Ongoing Call")
        self.CallScreen.resize(320, 420)
        self.CallScreen.setWindowIcon(QIcon(ICON_PATH))
        self.CallScreen.setStyleSheet("background-color:#111827;")
        self.CallScreen.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        Initial = Name[0].upper() if Name else "?"

        self.CallAvatarLabel = QLabel(Initial, self.CallScreen)
        self.CallAvatarLabel.resize(100, 100)
        self.CallAvatarLabel.move(110, 40)
        self.CallAvatarLabel.setAlignment(Qt.AlignCenter)
        self.CallAvatarLabel.setStyleSheet(
            "background-color:#2563EB; color:white; border-radius:50px; "
            "font-size:36px; font-family:'Segoe UI'; font-weight:bold;"
        )

        self.CallNameLabel = QLabel(Name, self.CallScreen)
        self.CallNameLabel.resize(300, 30)
        self.CallNameLabel.move(10, 155)
        self.CallNameLabel.setAlignment(Qt.AlignCenter)
        self.CallNameLabel.setStyleSheet(DIALOG_LABEL_STYLE + "color:white;")

        self.CallNumberLabel = QLabel(PhoneNo, self.CallScreen)
        self.CallNumberLabel.resize(300, 25)
        self.CallNumberLabel.move(10, 185)
        self.CallNumberLabel.setAlignment(Qt.AlignCenter)
        self.CallNumberLabel.setStyleSheet("color:#9CA3AF; font-size:13px; font-family:'Segoe UI';")

        StatusText = "Calling..." if voip else "Phone Link dialing in background"
        self.CallStatusLabel = QLabel(StatusText, self.CallScreen)
        self.CallStatusLabel.resize(300, 25)
        self.CallStatusLabel.move(10, 215)
        self.CallStatusLabel.setAlignment(Qt.AlignCenter)
        self.CallStatusLabel.setStyleSheet("color:#22C55E; font-size:14px; font-family:'Segoe UI'; font-weight:bold;")

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
            self.CallNoteLabel.resize(280, 40)
            self.CallNoteLabel.move(20, 245)
            self.CallNoteLabel.setAlignment(Qt.AlignCenter)
            self.CallNoteLabel.setWordWrap(True)
            self.CallNoteLabel.setStyleSheet("color:#9CA3AF; font-size:11px; font-family:'Segoe UI';")

        self.MuteButton = self._make_round_call_button(
            self.CallScreen, ICON_MIC, "Mute", CALL_TOGGLE_BUTTON_STYLE, checkable=True
        )
        self.MuteButton.move(50, 300)
        self.MuteButton.toggled.connect(self._ToggleMute)
        self.MuteButton.setEnabled(voip)

        self.EndCallButton = self._make_round_call_button(
            self.CallScreen, ICON_END_CALL, "End Call", CALL_END_BUTTON_STYLE, size=64
        )
        self.EndCallButton.move(128, 295)
        self.EndCallButton.clicked.connect(self._EndCall)

        self.SpeakerButton = self._make_round_call_button(
            self.CallScreen, ICON_SPEAKER, "Speaker", CALL_TOGGLE_BUTTON_STYLE, checkable=True
        )
        self.SpeakerButton.move(220, 300)
        self.SpeakerButton.setEnabled(voip)

        self.CallScreen.show()

    def _make_round_call_button(self, parent, icon_svg, tooltip, style, checkable=False, size=60):
        button = QPushButton(parent)
        button.resize(size, size)
        button.setIcon(svg_icon(icon_svg, color="#ffffff", size=int(size * 0.4)))
        button.setIconSize(QSize(int(size * 0.4), int(size * 0.4)))
        button.setToolTip(tooltip)
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.setCheckable(checkable)
        return button

    def _ToggleMute(self, checked):
        icon = ICON_MIC_OFF if checked else ICON_MIC
        self.MuteButton.setIcon(svg_icon(icon, color="#ffffff", size=24))

        if getattr(self, "CallIsVoip", False):
            self.Voip.SetMuted(checked)

    def _MarkCallConnected(self):
        self.CallStatusLabel.setText("Connected")
        self.CallTimer.start(1000)

    def _TickCallTimer(self):
        self.CallSeconds += 1
        minutes = self.CallSeconds // 60
        seconds = self.CallSeconds % 60
        self.CallStatusLabel.setText(f"{minutes:02d}:{seconds:02d}")

    def _EndCall(self):
        self.CallTimer.stop()

        if hasattr(self, "CallConnectTimer"):
            self.CallConnectTimer.stop()

        if getattr(self, "CallIsVoip", False):
            self.Voip.EndCall()

        self.CallScreen.close()
