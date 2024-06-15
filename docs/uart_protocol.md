# CAN Frames

Values are ASCII-HEX, Packet must end with LF or CRLF

| Field name     | Bytes | Value                                 |
|----------------|---------------|-----------------------------------------|
| Start of Heading | 1 | 0x01 |
| Type   | 1 | 0x00 = Broadcast, 0x01 = Multicast, 0x02 = Unicast |
| Unit Separator | 1 | 0x1F |
| Target   | 1-4 | Target address (0x0001-0x07FF for Unicast, 0x0001-0xFFFF for other Types) |
| Unit Separator | 1 | 0x1F |
| Soruce | 1-3 | Source address (0x000-0x7FF) |
| Unit Separator | 1 | 0x1F |
| Port | 1 | 0x01-0x1F for Unicast, 0xFF for other types |
| Unit Separator | 1 | 0x1F |
| Length | 1 | Length of following payload in bytes, 0-8 |
| Start of Text | 1 | 0x02 |
| Payload | 1 | Data (if length>0) |
| Unit Separator | 1 | 0x1F (if length>0) - Repeat Payload/Separator for len bytes |
| End of transmission | 1 | 0x04 |
