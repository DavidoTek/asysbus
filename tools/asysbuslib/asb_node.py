from dataclasses import dataclass


@dataclass
class AsbNode:
    """ Data class for representing an ASB node """
    id: int

    boot_time: int
    last_seen: int
    reported_uptime_days: int
