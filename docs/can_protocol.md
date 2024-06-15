# CAN Frames

ASysBus uses extended CAN frames:

| Field name     | Length (bits) | Purpose                                 |
|----------------|---------------|-----------------------------------------|
| Start-of-frame | 1             | Denotes the start of frame transmission |
| Identifier A   | 11            | First part of the (unique) identifier which also represents the message priority |
| Substitute remote request (SRR) | 1 | Must be recessive (1) |
| Identifier extension bit (IDE) | 1 | Must be recessive (1) for extended frame format with 29-bit identifiers |
| Identifier B | 18 | Second part of the (unique) identifier which also represents the message priority |
| Remote transmission request (RTR) | 1 | Must be dominant (0) for data frames and recessive (1) for remote request frames |
| Reserved bits (r1, r0) | 2 | Reserved bits which must be set dominant (0), but accepted as either dominant or recessive |
| Data length code (DLC) | 4 | Number of bytes of data (0–8 bytes) |
| Data field         | 0–64 (0-8 bytes) | Data to be transmitted (length dictated by DLC field) |
| CRC                | 15 | Cyclic redundancy check |
| CRC delimiter      | 1 | Must be recessive (1) |
| ACK slot           | 1 | Transmitter sends recessive (1) and any receiver can assert a dominant (0) |
| ACK delimiter      | 1 | Must be recessive (1) |
| End-of-frame (EOF) | 7 | Must be recessive (1) |
(Table Source: [Wikipedia](https://en.wikipedia.org/wiki/CAN_bus#Data_frame); CC-BY-SA)

# Identifier Encoding

ASysBus uses the Identifier to encode packet type, source and destination. A node address is 11 bit, multicast groups use a 16 bit address. Due to the concept of CAN lower addresses inherit a higher transmission priority.

## Packet Types

There are three packet types defined. Please note this definitions differ from the original iSysBus-Protocol.

### Unicast

Unicast are sent by a device and addressed to a specific node. These frames are usually only used for management

| A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | SSR | IDE | B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 | B11 | B12 | B13 | B14 | B15 | B16 | B17 |
|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|-----|-----|-----|
| =1 | =0 | P  | O  | R  | T  | !  | TA | R | G  | E   | CAN | CAN | T  | A  | DD | R  | E  | S  | S  | S  | O  | U  | R   | C   | E   | A   | DD  | RE  | S   | S   |

### Multicast

Multicast packages are sent to a group of devices. This includes usual control commands like "group light kitchen: light on".

| A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | SSR | IDE | B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 | B11 | B12 | B13 | B14 | B15 | B16 | B17 |
|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|-----|-----|-----|
| =0 | =1 | M  | U  | L  | T  | I  | C  | A | S  | T   | CAN | CAN | A  | D  | D  | R  | E  | S  | S  | S  | O  | U  | R   | C   | E   | A   | DR  | E   | S   | S   |

### Broadcast

Broadcast packages are sent to all devices on the bus. This type is rarely used, example would be "reboot all nodes"

| A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | SSR | IDE | B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 | B11 | B12 | B13 | B14 | B15 | B16 | B17 |
|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|-----|-----|-----|
| =0 | =0 | B  | R  | O  | A  | D  | C  | A | S  | T   | CAN | CAN | A  | D  | D  | R  | E  | S  | S  | S  | O  | U  | R   | C   | E   | A   | DR  | E   | S   | S   |

###

## Credits

The basic protocol is based on [iSysBus](http://wiki.isysbus.org/w/Paketaufbau_CAN)
 