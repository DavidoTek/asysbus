from typing import Callable

import serial
import io
import threading

from asysbuslib.asb_comm import AsbComm
from asysbuslib.asb_endecode import asb_pkg_decode, asb_pkg_encode
from asysbuslib.asb_proto import AsbPacket


class AsbUart(AsbComm):

    def __init__(self, port: str, baudrate: int):
        """
        Initialize the ASB communication class

        Parameters:
            port (str): The serial port of the ASB interface (e.g. /dev/ttyUSB0)
            baudrate (int): The baudrate to use (e.g. 115200)
        """
        self._ser = serial.Serial(port, baudrate, timeout=0.01)
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._ser, self._ser))  # type: ignore

        self._callbacks: list[Callable[[AsbPacket|None], None]] = []

        self._read_thread_running = True
        self._read_thread = threading.Thread(target=self._read_task)
        self._read_thread.start()

    def stop(self) -> None:
        self._read_thread_running = False
        self._read_thread.join()
        self._ser.close()

    def _read_task(self) -> None:
        while self._read_thread_running:
            message = self._sio.readline()
            if message.strip():
                pkg = asb_pkg_decode(message)

                for callback in self._callbacks:
                    callback(pkg)

    def register_callback(self, callback: Callable[[AsbPacket|None], None]) -> None:
        self._callbacks.append(callback)

    def send_packet(self, pkg: AsbPacket) -> bool:
        message = asb_pkg_encode(pkg)
        if not message:
            return False
        self._sio.write(message)
        self._sio.flush()
        return True
