from typing import Callable

import time

from asb_comm import AsbComm
from asb_proto import AsbMessageType, AsbCommand, AsbMeta, AsbPacket


PING_TIMEOUT_SEC = 1.0


class AsbInterface:
    
    def __init__(self, node_id: int, comm: AsbComm) -> None:
        self._node_id = node_id
        self._comm = comm

        self._comm.register_callback(self._callback)

        self._pings_pending = []

    def _callback(self, pkg: AsbPacket|None) -> None:
        if pkg is None:
            return

        self._handle_ping_timeout()

        # handle incoming packets with target = self
        if pkg.meta.mtype == AsbMessageType.ASB_PKGTYPE_UNICAST and pkg.meta.target == self._node_id:
            if pkg.data[0] == AsbCommand.ASB_CMD_PONG:
                for i, source in enumerate(self._pings_pending):
                    if source["target"] == pkg.meta.source:
                        time_ms = round((time.time() - source["time"]) * 1000)
                        source["cb"](True, time_ms)
                        self._pings_pending.pop(i)

        # handle incoming packets with target = broadcast (booted, heartbeat, ...)
    def _handle_ping_timeout(self) -> None:
        """ Internal function to detect when a ping times out """
        for i, source in enumerate(self._pings_pending):
            if (time.time() - source["time"]) > PING_TIMEOUT_SEC:
                source["cb"](False, -1)
                self._pings_pending.pop(i)

        if pkg.meta.mtype == AsbMessageType.ASB_PKGTYPE_BROADCAST:
            if pkg.data[0] == AsbCommand.ASB_CMD_BOOT:
                pass  # TODO
            elif pkg.data[0] == AsbCommand.ASB_CMD_HEARTBEAT:
                pass  # TODO

        pass  # TODO: Handle incoming packets

    def asb_send_0bit(self, mtype: AsbMessageType, target: int, port: int) -> bool:
        """
        Send a 0-bit ASB command to the target

        Parameters:
            mtype (AsbMessageType): The message type
            target (int): The target address
            port (int): The port (only used in unicast mode)

        Returns:
            bool: True if the packet was sent successfully
        """
        pkg = AsbPacket(
            AsbMeta(
                mtype,
                port,
                target,
                self._node_id
            ),
            1,
            [AsbCommand.ASB_CMD_0B]
        )
        return self._comm.send_packet(pkg)

    def asb_send_1bit(self, mtype: AsbMessageType, target: int, port: int, value: bool) -> bool:
        """
        Send a 1-bit ASB command to the target

        Parameters:
            mtype (AsbMessageType): The message type
            target (int): The target address
            port (int): The port (only used in unicast mode)
            value (bool): The value to send

        Returns:
            bool: True if the packet was sent successfully
        """
        if not value in [True, False]:
            return False

        pkg = AsbPacket(
            AsbMeta(
                mtype,
                port,
                target,
                self._node_id
            ),
            2,
            [AsbCommand.ASB_CMD_1B, int(value)]
        )
        return self._comm.send_packet(pkg)

    def asb_send_percent(self, mtype: AsbMessageType, target: int, port: int, value: int) -> bool:
        """
        Send a percent ASB command to the target

        Parameters:
            mtype (AsbMessageType): The message type
            target (int): The target address
            port (int): The port (only used in unicast mode)
            value (int): The value to send (0-100)

        Returns:
            bool: True if the packet was sent successfully
        """
        if not 0 <= value <= 100:
            return False

        pkg = AsbPacket(
            AsbMeta(
                mtype,
                port,
                target,
                self._node_id
            ),
            2,
            [AsbCommand.ASB_CMD_PER, value]
        )
        return self._comm.send_packet(pkg)

    def asb_send_ping(self, target: int) -> bool:
        """
        Send a ping to the target

        Parameters:
            target (int): The target address

        Returns:
            bool: True if the packet was sent successfully
        """
        pkg = AsbPacket(
            AsbMeta(
                AsbMessageType.ASB_PKGTYPE_UNICAST,
                0,
                target,
                self._node_id
            ),
            1,
            [AsbCommand.ASB_CMD_PING]
        )
        return self._comm.send_packet(pkg)

    def asb_do_ping(self, target: int, callback: Callable[[bool, int], None]) -> bool:
        """
        Send a ping to the target and wait for a pong

        Parameters:
            target (int): The target address
            callback (function): The callback function to call when the pong is received (bool: success, int: time in ms)

        Returns:
            bool: True if the target responded to the ping
        """
        if not self.asb_send_ping(target):
            return False

        self._pings_pending.append({
            "target": target,
            "time": time.time(),
            "cb": callback
            })
