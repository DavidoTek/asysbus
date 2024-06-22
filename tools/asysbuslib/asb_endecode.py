import re

from asysbuslib.asb_proto import AsbPacket, AsbMeta, AsbMessageType


def asb_validate_pkg(pkg: AsbPacket) -> bool:
    """
    Validate an ASB packet (check if parameters are in valid ranges)

    Parameters:
        pkg (AsbPacket): The packet to validate

    Returns:
        bool: True if the packet is valid, False otherwise
    """

    if not int(pkg.meta.mtype) in AsbMessageType._value2member_map_:
        return False

    if pkg.meta.port < -1 or pkg.meta.port > 0x1F:
        return False

    if pkg.meta.mtype != AsbMessageType.ASB_PKGTYPE_UNICAST and pkg.meta.port != -1:
        return False

    if pkg.meta.target < 0x0001 or pkg.meta.target > 0xFFFF:
        return False

    if pkg.meta.source < 0x0001 or pkg.meta.source > 0x07FF:
        return False

    if pkg.len < 0 or pkg.len > 8:
        return False

    if len(pkg.data) != pkg.len:
        return False

    # allow commands that are not defined in the enum!
    # if int(pkg.data[0]) not in AsbCommand._value2member_map_:
    #     return False

    return True


# based on tools/encoder.py
def asb_pkg_encode(pkg: AsbPacket) -> str:
    """
    Encode an ASB packet to a string to send to the serial ASB interface

    Parameters:
        pkg (AsbPacket): The packet to encode

    Returns:
        str: The encoded packet or an empty string if the packet is invalid
    """
    if not asb_validate_pkg(pkg):
        return ""

    out = chr(0x01)
    out = out + format(int(pkg.meta.mtype), 'x')
    out = out + chr(0x1F)
    out = out + format(pkg.meta.target, 'x')
    out = out + chr(0x1F)
    out = out + format(pkg.meta.source, 'x')
    out = out + chr(0x1F)
    if pkg.meta.port < 0:
        out = out + 'ff'
    else:
        out = out + format(pkg.meta.port, 'x')
    out = out + chr(0x1F)
    out = out + format(len(pkg.data), 'x')
    out = out + chr(0x02)
    for db in pkg.data:
        out = out + format(db, 'x')
        out = out + chr(0x1F)
    out = out + chr(0x04)
    out = out + "\r\n"

    return out.upper()


# based on tools/decoder.py
def asb_pkg_decode(line: str) -> AsbPacket|None:
    """
    Decode an ASB packet from a string received from the serial ASB interface

    Parameters:
        line (str): The line to decode

    Returns:
        AsbPacket|None: The decoded ASB packet or None if the line is not a valid ASB packet
    """
    m = re.search('\x01([0-9A-F]*)\x1f([0-9A-F]*)\x1f([0-9A-F]*)\x1f([0-9A-F]*)\x1f([0-9A-F]*)\x02((([0-9A-F]*)\x1f)*)\x04', line)
    if not m:
        return None

    pkg = AsbPacket(AsbMeta(AsbMessageType.ASB_PKGTYPE_BROADCAST, -1, 0, 0), -1, [])

    if not int(m.group(1), 16) in AsbMessageType._value2member_map_:
        return None
    pkg.meta.mtype = AsbMessageType(int(m.group(1), 16))
    pkg.meta.target = int(m.group(2), 16)
    pkg.meta.source = int(m.group(3), 16)
    pkg.meta.port = int(m.group(4), 16)
    pkg.len = int(m.group(5), 16)

    if pkg.len > 0:
        dm = re.findall('([0-9A-F]*)\x1f', m.group(6))

        if len(dm) < pkg.len:
            return None

        dmc = 0
        while dmc < pkg.len:
            pkg.data.append(int(dm[dmc], 16))
            dmc += 1

    return pkg


def asb_pkg_decode_arr_to_unsigned_int(arr: list[int]) -> int:
    """
    Decode an array of two bytes to an unsigned int

    Parameters:
        arr (list[int]): The array to decode (little endian, [1, 0] -> 256)
    
    Returns:
        int: The decoded unsigned int
    """
    if len(arr) != 2:
        raise ValueError("Array must have exactly 2 elements")
    if arr[0] < 0 or arr[0] > 255 or arr[1] < 0 or arr[1] > 255:
        raise ValueError("Array must contain values between 0 and 255")

    return (arr[0]<<8) + arr[1]


def asb_pkg_decode_arr_to_signed_int(arr: list[int]) -> int:
    """
    Decode an array of two bytes to a signed int

    Parameters:
        arr (list[int]): The array to decode (little endian, [1, 0] -> 256)
    
    Returns:
        int: The decoded signed int
    """

    aint = asb_pkg_decode_arr_to_unsigned_int(arr)
    if aint > 32768:  # pow(2,15)
        aint = 1-(aint-32768)

    return aint


def asb_pkg_decode_arr_to_unsigned_long(arr: list[int]) -> int:
    """
    Decode an array of four bytes to an unsigned long

    Parameters:
        arr (list[int]): The array to decode (little endian, [1, 0, 0, 0] -> 16777216)

    Returns:
        int: The decoded unsigned long
    """

    if len(arr) != 4:
        raise ValueError("Array must have exactly 2 elements")
    if arr[0] < 0 or arr[0] > 255 or arr[1] < 0 or arr[1] > 255:
        raise ValueError("Array must contain values between 0 and 255")

    return (arr[0]<<24) + (arr[1]<<16) + (arr[2]<<8) + arr[3]


def asb_pkg_decode_arr_to_signed_long(arr: list[int]) -> int:
    """
    Decode an array of four bytes to a signed long

    Parameters:
        arr (list[int]): The array to decode (little endian, [1, 0, 0, 0] -> 16777216)

    Returns:
        int: The decoded signed long
    """
    aint = asb_pkg_decode_arr_to_unsigned_long(arr)
    if aint > 2147483648:  # pow(2,31)
        aint = 1-(aint-2147483648)

    return aint
