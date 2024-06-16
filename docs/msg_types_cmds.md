# Message Types

## Unicast

Message targets a single node. Used for configuration.

## Multicast

Message targets a group. Used for control messages.

## Broadcast

Message targets all nodes. Used for informational messages.

# Commands

Messages can carry command + max 7 bytes of payload

| Command | Length (bytes) | Purpose                                 |
|---------|----------------|-----------------------------------------|
| 0x21    | 0              | Node has booted                         |
| 0x22    | 2              | Heartbeat (sent periodically by controller) |
| 0x40    | 0              | Request state                           |
| 0x50    | 0              | 0 Bit Message (e.g. S0-Sensor)          |
| 0x51    | 1              | 1 Bit Message (e.g. on/off)             |
| 0x52    | 1              | percent Message (e.g. dimmer,position)  |
| 0x70    | 0              | PING                                    |
| 0x71    | 0              | PONG                                    |
| 0x80    | 2              | READ_CONFIG                             |
| 0x81    | 3              | WRITE_CONFIG                            |
| 0x82    | 2              | COMMIT CONFIG                           |
| 0x85    | 2              | REIDENT                                 |
| 0xA0    | 2              | Temperature                             |
| 0xA1    | 2              | Humidity                                |
| 0xA2    | 2              | Pressure                                |
| 0xA5    | 4              | Lux                                     |
| 0xA6    | 2              | UV-Index                                |
| 0xA7    | 4              | IR |
| 0xB0    | ??             | PM2.5 |
| 0xB1    | ??             | PM10 |
| 0xC0    | 2              | Voltage |
| 0xC1    | 2             | Ampere |
| 0xC2    | 2              | Power (W/VA)                             |
| 0xD0    | 1              | Generic % (Valve, etc)            |
| 0xD1    | 2              | Generic ‰ |
| 0xD2    | 2              | Parts per million            |
| 0xD5    | 2              | something per year |
| 0xD6    | 2              | something per month |
| 0xD7    | 2              | something per day |
| 0xD8    | 2              | something per hour |
| 0xD9    | 2              | something per minute |
| 0xDA    | 2              | something per second |