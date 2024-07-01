# Hardware Compatibility

This page contains a list of tested and working hardware configurations.


| Microcontroller       | CAN controller   | CAN transceiver   | Comment
|-----------------------|------------------|-------------------|-------------------------
| Atmega328P            | MCP2515          | MCP2551           | -
| "                     | "                | TJA1050           | CAN module from a random eBay seller
| "                     | MCP2518FD        | MCP2561FD         | MCP2518FD requires a build flag. Add the following to platformio.ini: `build_flags = -DCAN_2518FD`
| AVR32DA28             | MCP2515          | TJA1050           | -