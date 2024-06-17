from dataclasses import dataclass
from enum import Enum


class AsbIoModuleType(Enum):
    """ ASB I/O module types """
    ASB_IO_DIN = 1
    ASB_IO_DOUT = 2


@dataclass
class AsbIoModule:
    """
    Data class for representing an ASB I/O module
    
    Attributes:
        cfg_id (int): Config ID of the ASB I/O module
        mod_type (AsbIoModuleType): Module type if known
    """
    cfg_id: int
    mod_type: AsbIoModuleType


@dataclass
class AsbNode:
    """
    Data class for representing an ASB node
    
    Attributes:
        id (int): Node ID
        boot_time (int): UNIX timestamp of the boot message or -1
        last_seen (int): UNIX timestamp of the last message received from the node or -1
        reported_uptime_days (int): Uptime in days reported by the node or -1
        io_modules (list[AsbIoModule]): List of ASB I/O modules of the node
    """
    id: int

    boot_time: int
    last_seen: int
    reported_uptime_days: int

    io_modules: list[AsbIoModule]
