from typing import Callable
from abc import ABC, abstractmethod

from asysbuslib.asb_proto import AsbPacket


class AsbComm(ABC):

    @abstractmethod
    def register_callback(self, callback: Callable[[AsbPacket|None], None]) -> None:
        """
        Register a callback function to be called when a new ASB package is received

        Parameters:
            callback (function): The callback function to call
        """
        pass

    @abstractmethod
    def send_packet(self, pkg: AsbPacket) -> bool:
        """
        Send an ASB package

        Parameters:
            pkg (AsbPacket): The package to send

        Returns:
            bool: True if the package was sent successfully
        """
        pass

