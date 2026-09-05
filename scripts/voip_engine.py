import json
import socket
import threading

import numpy as np
import sounddevice as sd

from PySide6.QtCore import QObject, Signal

CONTROL_PORT = 51888
AUDIO_PORT = 51889
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 960


class VoipEngine(QObject):
    incoming_call = Signal(str, str, str)
    call_rejected = Signal()
    call_failed = Signal(str)

    def __init__(self):
        super().__init__()
        self.PeerIP = None
        self.PendingConn = None
        self.InStream = None
        self.OutStream = None
        self.AudioSocket = None
        self.CallActive = False
        self.Muted = False
        self._StartControlServer()

    def _StartControlServer(self):
        threading.Thread(target=self._ControlServerLoop, daemon=True).start()

    def _ControlServerLoop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(("0.0.0.0", CONTROL_PORT))
            server.listen(5)
        except OSError:
            return

        while True:
            try:
                conn, addr = server.accept()
            except OSError:
                break
            threading.Thread(target=self._HandleIncoming, args=(conn, addr), daemon=True).start()

    def _HandleIncoming(self, conn, addr):
        try:
            data = conn.recv(4096)
            message = json.loads(data.decode("utf-8"))
        except Exception:
            conn.close()
            return

        if message.get("type") != "ring":
            conn.close()
            return

        self.PendingConn = conn
        self.PeerIP = addr[0]
        self.incoming_call.emit(message.get("name", "Unknown"), message.get("number", ""), addr[0])

    def AcceptIncomingCall(self):
        if not self.PendingConn:
            return
        try:
            self.PendingConn.sendall(json.dumps({"type": "accept"}).encode("utf-8"))
        except OSError:
            return
        self._StartAudio(self.PeerIP)

    def RejectIncomingCall(self):
        if not self.PendingConn:
            return
        try:
            self.PendingConn.sendall(json.dumps({"type": "reject"}).encode("utf-8"))
            self.PendingConn.close()
        except OSError:
            pass
        self.PendingConn = None

    def PlaceCall(self, PeerIP, MyName, MyNumber):
        try:
            control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            control.settimeout(10)
            control.connect((PeerIP, CONTROL_PORT))
            control.sendall(json.dumps({"type": "ring", "name": MyName, "number": MyNumber}).encode("utf-8"))
            response = json.loads(control.recv(4096).decode("utf-8"))
            control.close()
        except Exception as error:
            self.call_failed.emit(str(error))
            return False

        if response.get("type") != "accept":
            self.call_rejected.emit()
            return False

        self.PeerIP = PeerIP
        self._StartAudio(PeerIP)
        return True

    def _StartAudio(self, PeerIP):
        self.CallActive = True
        self.Muted = False

        self.AudioSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.AudioSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.AudioSocket.bind(("0.0.0.0", AUDIO_PORT))
        self.AudioSocket.settimeout(1)

        def send_callback(indata, frames, time_info, status):
            if not self.CallActive or self.Muted:
                return
            try:
                self.AudioSocket.sendto(indata.tobytes(), (PeerIP, AUDIO_PORT))
            except OSError:
                pass

        self.InStream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16",
            blocksize=BLOCK_SIZE, callback=send_callback
        )
        self.InStream.start()

        self.OutStream = sd.OutputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16", blocksize=BLOCK_SIZE
        )
        self.OutStream.start()

        threading.Thread(target=self._ReceiveLoop, daemon=True).start()

    def _ReceiveLoop(self):
        while self.CallActive:
            try:
                data, _ = self.AudioSocket.recvfrom(8192)
            except (socket.timeout, OSError):
                continue
            try:
                samples = np.frombuffer(data, dtype="int16").reshape(-1, CHANNELS)
                self.OutStream.write(samples)
            except Exception:
                continue

    def SetMuted(self, muted):
        self.Muted = muted

    def EndCall(self):
        self.CallActive = False

        for stream in (self.InStream, self.OutStream):
            if stream:
                try:
                    stream.stop()
                    stream.close()
                except Exception:
                    pass

        self.InStream = None
        self.OutStream = None

        if self.AudioSocket:
            try:
                self.AudioSocket.close()
            except OSError:
                pass
        self.AudioSocket = None
        self.PendingConn = None
