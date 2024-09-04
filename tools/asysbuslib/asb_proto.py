# This file contains the ASB protocol definitions
# Based on asb_proto.h - partly generated with read_proto_from_c.py

from dataclasses import dataclass
from enum import IntEnum


class AsbMessageType(IntEnum):
    ASB_PKGTYPE_BROADCAST = 0x00
    ASB_PKGTYPE_MULTICAST = 0x01
    ASB_PKGTYPE_UNICAST = 0x02


class AsbCommand(IntEnum):
    ASB_CMD_LEGACY_8B = 0x02
    ASB_CMD_BOOT = 0x21
    ASB_CMD_HEARTBEAT = 0x22
    ASB_CMD_REQ = 0x40
    ASB_CMD_0B = 0x50  # 0-Bit, generic pulse
    ASB_CMD_1B = 0x51  # 1-Bit, on/off
    ASB_CMD_PER = 0x52  # %
    ASB_CMD_PING = 0x70
    ASB_CMD_PONG = 0x71
    ASB_CMD_CFG_READ = 0x80  # 2-byte address
    ASB_CMD_CFG_WRITE = 0x81  # 2-byte-address + data
    ASB_CMD_CFG_READ_RES = 0x83  # 2-byte-address + data
    ASB_CMD_REQ_MODULES = 0x86
    ASB_CMD_RES_MODULES = 0x87
    ASB_CMD_IDENT = 0x85  # Change local address, 2-byte-address
    ASB_CMD_S_TEMP = 0xA0  # x*0.1°C, int
    ASB_CMD_S_HUM = 0xA1  # x*0.1%RH, unsigned int
    ASB_CMD_S_PRS = 0xA2  # x*0.1hPa, unsigned int
    ASB_CMD_S_LUX = 0xA5  # unsigned long
    ASB_CMD_S_UV = 0xA6  # *0.1, unsigned int
    ASB_CMD_S_IR = 0xA7  # unsigned long
    ASB_CMD_S_PM25 = 0xB0  # µg/m³, unsigned long
    ASB_CMD_S_PM10 = 0xB1  # µg/m³, unsigned long
    ASB_CMD_S_VOLT = 0xC0  # x*0.01V, int
    ASB_CMD_S_AMP = 0xC1  # x*0.01A, int
    ASB_CMD_S_PWR = 0xC2  # x*0.1W or VA, long
    ASB_CMD_S_PER = 0xD0  # %, byte
    ASB_CMD_S_PML = 0xD1  # ‰, unsingned int
    ASB_CMD_S_PPM = 0xD2  # Parts per million, unsingned int
    ASB_CMD_S_PY = 0xD5  # smth per Year, unsinged int
    ASB_CMD_S_PMo = 0xD6  # smth per Month, unsinged int
    ASB_CMD_S_PD = 0xD7  # smth per Day, unsinged int
    ASB_CMD_S_PH = 0xD8  # smth per Hour, unsinged int
    ASB_CMD_S_PM = 0xD9  # smth per Minute, unsinged int (RPM, Pulse PM, etc)
    ASB_CMD_S_PS = 0xDA  # smth per Second, unsinged int


@dataclass
class AsbMeta:
    """
    Packet metadata
    Contains all data except things related to the actual payload

    Attributes:
        type (int): Message Type (0 -> Broadcast, 1 -> Multicast, 2 -> Unicast)
        port (int): Port (0x00 - 0x1F, only used in Unicast Mode, otherwise -1)
        target (int): Target address (Unicast: 0x0001 - 0x07FF, Multicast/Broadcast: 0x0001 - 0xFFFF, 0x0000 = invalid packet)
        source (int): Source address (0x0001 - 0x07FF, 0x0000 = invalid packet)
    """

    mtype: AsbMessageType
    port: int
    target: int
    source: int
#    busId: int


@dataclass
class AsbPacket:
    """
    Complete packet

    Attributes:
        meta (AsbMeta): Packet metadata
        len (int): Length in bytes, 0-8. -1 indicates invalid packet
        data (list[int]): Payload
    """

    meta: AsbMeta
    len: int
    data: list[int]
