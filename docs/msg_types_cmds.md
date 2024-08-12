# Message Types

## Unicast

Message targets a single node. Used for configuration.

## Multicast

Message targets a group. Used for control messages.

## Broadcast

Message targets all nodes. Used for informational messages.

# Commands

Messages can carry command + max 7 bytes of payload

| Command | Length (bytes) | Purpose                                 | Payload (0-8 bytes)
|---------|----------------|-----------------------------------------|---------------------------------------
| 0x21    | 0              | Node has booted                         | -
| 0x22    | 2              | Heartbeat (sent periodically)           | `uptime_ms >> 24` , `uptime_ms >> 32`
| 0x40    | 0              | Request state                           | -
| 0x50    | 0              | 0 Bit Message (e.g. S0-Sensor)          | -
| 0x51    | 1              | 1 Bit Message (e.g. on/off)             | `state` (0 or 1)
| 0x52    | 1              | percent Message (e.g. dimmer,position)  | `value` (0-100)
| 0x70    | 0              | PING                                    | -
| 0x71    | 0              | PONG                                    | -
| 0x80    | 2              | READ_CONFIG                             | `addr_high`, `addr_low`
| 0x81    | 3              | WRITE_CONFIG                            | `addr_high`, `addr_low` , `value`
| 0x83    | 3              | READ_CONFIG_RESPONSE                    | `addr_high`, `addr_low` , `value`
| 0x86    | 0              | Request list of I/O modules             | -
| 0x87    | 5              | Responses to I/O modules request        | `mod_cfg_id` , `mod_type` , `addr_high` , `addr_low` , `cfg_len`
| 0x85    | 2              | REIDENT                                 | `node_id_high` , `node_id_low`
| 0xA0    | 2              | Temperature                             | `temp_high` , `temp_low`
| 0xA1    | 2              | Humidity                                | `humid_high` , `humid_low`
| 0xA2    | 2              | Pressure                                | `pressure_high` , `pressure_low`
| 0xA5    | 4              | Lux                                     | `lux>>24` , `lux>>16` , `lux>>8` , `lux`
| 0xA6    | 2              | UV-Index                                | `uv_high` , `uv_low`
| 0xA7    | 4              | IR                                      | `ir>>24` , `ir>>16` , `ir>>8` , `ir`
| 0xB0    | ??             | PM2.5                                   | ??
| 0xB1    | ??             | PM10                                    | ??
| 0xC0    | 2              | Voltage                                 | `voltage_high` , `voltage_low`
| 0xC1    | 2              | Ampere                                  | `ampere_high` , `ampere_low`
| 0xC2    | 2              | Power (W/VA)                            | `power_high` , `power_low`
| 0xD0    | 1              | Generic % (Valve, etc)                  | `value` (0-100)
| 0xD1    | 2              | Generic ‰                               | `value_high` , `value_low` (0-1000)
| 0xD2    | 2              | Parts per million                       | `value_high` , `value_low` (0-65535)
| 0xD5    | 2              | something per year                      | `n_high` , `n_low`
| 0xD6    | 2              | something per month                     | `n_high` , `n_low`
| 0xD7    | 2              | something per day                       | `n_high` , `n_low`
| 0xD8    | 2              | something per hour                      | `n_high` , `n_low`
| 0xD9    | 2              | something per minute                    | `n_high` , `n_low`
| 0xDA    | 2              | something per second                    | `n_high` , `n_low`


# ASB I/O Modules

The module types as specified in response to the I/O module request (0x86/0x87).

| Type | Module         |
|------|----------------|
| 0x01 | ASB_IO_DIN     |
| 0x02 | ASB_IO_DOUT    |
