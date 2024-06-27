import asyncio
from functools import partial
import serial_asyncio

from asysbuslib.asb_comm_async import AsbCommAsync
from asysbuslib.asb_endecode import asb_pkg_decode, asb_pkg_encode
from asysbuslib.asb_proto import AsbPacket


class AsbUartProtocol(asyncio.Protocol):

    def __init__(self, queueRX: asyncio.Queue, queueTX: asyncio.Queue) -> None:
        super().__init__()
        self.queueRX = queueRX
        self.queueTX = queueTX
        self.transport: serial_asyncio.SerialTransport
        self.buf: bytes

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.buf = bytes()
        asyncio.ensure_future(self._send_task())

    def data_received(self, data) -> None:
        self.buf += data
        if b'\n' in self.buf:
            lines = self.buf.split(b'\n')
            self.buf = lines[-1] # whatever was left over
            for line in lines[:-1]:
                asyncio.ensure_future(self.queueRX.put(line))

    def connection_lost(self, exc) -> None:
        asyncio.get_event_loop().stop()

    async def _send_task(self) -> None:
        while True:
            msg = await self.queueTX.get()
            self.transport.serial.write(msg)


class AsbUartAsync(AsbCommAsync):

    def __init__(self, port: str, baudrate: int) -> None:
        """
        Initialize the async ASB communication class

        Parameters:
            port (str): The serial port of the ASB interface (e.g. /dev/ttyUSB0)
            baudrate (int): The baudrate to use (e.g. 115200)
        """
        self.port = port
        self.baudrate = baudrate

        self.queueRX: asyncio.Queue = asyncio.Queue()
        self.queueTX: asyncio.Queue = asyncio.Queue()

        loop = asyncio.get_event_loop()

        asb_proto_partial = partial(AsbUartProtocol, self.queueRX, self.queueTX)
        ser_coro = serial_asyncio.create_serial_connection(loop, asb_proto_partial, port, baudrate=baudrate)
        asyncio.ensure_future(ser_coro)

    async def send_packet(self, pkg: AsbPacket) -> bool:
        message = asb_pkg_encode(pkg)
        if not message:
            return False
        await self.queueTX.put(bytes(message, 'ascii'))
        return True

    async def receive_packet(self) -> AsbPacket|None:
        message: bytes = await self.queueRX.get()
        return asb_pkg_decode(message.decode('ascii'))
