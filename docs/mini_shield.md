The MiniShield is based on the CAN-controller MCP2515. Possible transceivers include PCA82C250 and MCP2551. The size is optimized to attach to an Arduino Pro Mini compatible controller, however it can also be used standalone using jumper wires.

The Design includes a 16MHz crystal for the MCP2515, necessary bypass caps and footprints for termination resistors, input fuses etc. The CS-Pin is wired to pin 7, leaving the usually used pins 9 and 10 for PWM-applications. Also the transceivers reset circuit is connected to RX0BF of the MCP2515, this enables the µC to deactivate the output stage and save power (~8mA less). Please keep in mind this requires you to set RX0BF in GPIO mode to be able to send CAN messages - a task not implemented in 3rd party CAN libraries.

# Pinout
| MCP Pin | MCP Name | Arduino Pin |
|---------|----------|-------------|
| 18      | VDD      | +5V         |
| 17      | ^RESET   | RESET       |
| 16      | ^CS      | 7           |
| 15      | SO       | 12 / MISO   |
| 14      | SI       | 11 / MOSI   |
| 13      | SCK      | 13 / SCK    |
| 12      | ^INT     | 2 / INT0    |
| 9       | VSS      | GND         |
| -       | CAN VCC  | RAW         |