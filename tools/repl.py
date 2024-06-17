#!/usr/bin/env python3
# Repl for aSysBus. Usage: python repl.py <node id> <serial port> <baudrate>
import sys
from datetime import datetime
import time

from asysbuslib.asb_interface import AsbInterface
from asysbuslib.asb_proto import AsbCommand, AsbMessageType
from asysbuslib.asb_uart import AsbUart


def _parse_target(target: str) -> tuple[AsbMessageType, int]:
    if target[0] == "u":
        return AsbMessageType.ASB_PKGTYPE_UNICAST, int(target[1:], 16)
    elif target[0] == "m":
        return AsbMessageType.ASB_PKGTYPE_MULTICAST, int(target[1:], 16)
    elif target[0] == "b":
        return AsbMessageType.ASB_PKGTYPE_BROADCAST, 0
    else:
        raise ValueError("Invalid target")


def main(node_id: int, serial_port: str, baudrate: int):
    comm = AsbUart(serial_port, baudrate)
    interface = AsbInterface(node_id, comm)

    print("aSysBus REPL - Type 'help' for a list of commands")

    while True:
        inp = input("> ").lower()
        inp_split = inp.split()

        try:
            if "help" in inp:
                print(" === Commands ===")
                print("help - Show this help")
                print("exit - Exit the REPL")
                print("nodes - List all nodes")
                print("modules <target> - List all I/O modules of a node")
                print("ping <target> - Ping a node")
                print("0bit <target> <port> - Send a 0-bit command")
                print("1bit <target> <port> <value> - Send a 1-bit command")
                print("percent <target> <port> <value> - Send a percent command")
                print("- The target must start with the domain. U0x0001=Unicast, M0x0001=Multicast, B=Broadcast")
                print("- The addresses and values must be in hexadecimal")

            elif "exit" in inp:
                break

            elif "nodes" in inp:
                nodes = interface.get_nodes()
                for node in nodes:
                    booted = datetime.fromtimestamp(node.boot_time).strftime("%Y-%m-%d %H:%M:%S") if node.boot_time != -1 else "?"
                    uptime = node.reported_uptime_days if node.reported_uptime_days != -1 else "?"
                    print(f"Node {hex(node.id)}: booted {booted}, up {uptime} days")

            elif "modules" in inp:
                if len(inp_split) != 2:
                    print("Usage: modules <target>")
                    continue
                mtype, target = _parse_target(inp_split[1])
                if mtype != AsbMessageType.ASB_PKGTYPE_UNICAST:
                    print("Only unicast targets have modules")
                    continue
                node = None
                for n in interface.get_nodes():
                    if n.id == target:
                        node = n
                        break
                if node is None:
                    print("Node not found")
                    continue
                print(f"Node {hex(node.id)} has the following modules:")
                for module in node.io_modules:
                    print(f"  - Config ID: {hex(module.cfg_id)}")
                    print(f"    Type: {module.mod_type.name if module.mod_type is not None else '?'}")
                    print(f"    Address: {hex(module.address)}")
                    print(f"    Target: {hex(module.target)}")

            elif "ping" in inp:
                if len(inp_split) != 2:
                    print("Usage: ping <target>")
                    continue
                mtype, target = _parse_target(inp_split[1])
                if not mtype == AsbMessageType.ASB_PKGTYPE_UNICAST:
                    print("Only unicast targets can be pinged")
                    continue
                interface.asb_do_ping(target, lambda s,t: print(f"Pong from {hex(target)}: {t}ms" if s else f"Ping Timeout from {hex(target)}"))
                time.sleep(0.1)

            elif "0bit" in inp:
                if len(inp_split) != 3:
                    print("Usage: 0bit <target> <port>")
                    continue
                mtype, target = _parse_target(inp_split[1])
                port = int(inp_split[2], 16)
                interface.asb_send_0bit(mtype, target, port)

            elif "1bit" in inp:
                if len(inp_split) != 4:
                    print("Usage: 1bit <target> <port> <value>")
                    continue
                mtype, target = _parse_target(inp_split[1])
                port = int(inp_split[2], 16)
                value = int(inp_split[3], 16)
                interface.asb_send_1bit(mtype, target, port, value)

            elif "percent" in inp:
                if len(inp_split) != 4:
                    print("Usage: percent <target> <port> <value>")
                    continue
                mtype, target = _parse_target(inp_split[1])
                port = int(inp_split[2], 16)
                value = int(inp_split[3], 16)
                interface.asb_send_percent(mtype, target, port, value)
        except Exception as e:
            print("Command Error:", e)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python repl.py <node id> <serial port> <baudrate>")
        sys.exit(1)

    if not sys.argv[1].isdecimal():
        print("Node ID must be a number")
        sys.exit(1)

    if not sys.argv[3].isdecimal():
        print("Baudrate must be a number")
        sys.exit(1)

    main(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))


# Example usage:
# python repl.py 10 /dev/ttyUSB0 115200
# > nodes
# Node 0x123: booted 2024-06-16 23:10:01, up ? days
# Node 0x124: booted ?, up 5 days
# > ping U0x123
# Pong from 0x123: 5ms
# > 1bit M0x1001 -1 1
# > exit
