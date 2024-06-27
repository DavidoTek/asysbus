from typing import Callable
from abc import ABC, abstractmethod

from asysbuslib.asb_proto import AsbPacket


class AsbCommAsync(ABC):

    @abstractmethod
    async def send_packet(self, pkg: AsbPacket) -> bool:
        """
        Send an ASB package

        Parameters:
            pkg (AsbPacket): The package to send

        Returns:
            bool: True if the package was sent successfully
        """
        pass

    @abstractmethod
    async def receive_packet(self) -> AsbPacket|None:
        """
        Receive an ASB package from the bus

        Returns:
            AsbPacket|None: The received packet or None if an invalid packet was received
        """
        pass
