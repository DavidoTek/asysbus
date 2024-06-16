from dataclasses import dataclass
from enum import Enum


class AsbIoModuleType(Enum):
    """ ASB I/O module types """
    ASB_IO_DIN = 1
    ASB_IO_DOUT = 2


@dataclass
class AsbIoModule:
    """ Data class for representing an ASB I/O module """
    cfg_id: int
    mod_type: AsbIoModuleType


@dataclass
class AsbNode:
    """ Data class for representing an ASB node """
    id: int

    boot_time: int
    last_seen: int
    reported_uptime_days: int

    io_modules: list[AsbIoModule]
