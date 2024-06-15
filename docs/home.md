# Welcome to the ASysBus wiki!

## What is aSysBus

ASysBus aims to provide a CAN based network for Arduino based microcontrollers. The protocol is mostly based on [iSysBus](http://wiki.isysbus.de), a german project for home automation which started in 2005.

This is ATM mostly just a scratchpad for my ideas. Sources will follow once basic functionality is in place.

### Parts of ASysBus

ASysBus consists of three main parts:

* MCP2515 based MiniShield
  * Description: A PCB featuring all components required for CAN communication which can be attached to an Arduino Pro Mini or compatible controller. Other µCs can be attached using jumper wires.
  * State: First PCB designs done, prototype built. 
* ASysBus-Library
  * Description: A Arduino library handling CAN communication, protocol handling, etc
  * State: First contact to MCP2515 OK, receiving and sending valid bus-messages OK 
* Modules
  * Description: A module consists of an PCB and protocol description enabling advanced control scenarios like blind or roller shutter motor control, GUI control, etc. Also modules can act as gateway to other networks like radio based control systems or ethernet.
  * State: Heap of cables representing roller shutter motor control dangling from a window… 

### Differences to iSysBus

The original iSysBus aimed to provide prebuild, task specific, modules with an advanced management set. Nodes where flashed and managed using a own, java based, control application. Firmware updates could be applied over the CAN network, etc. The tight integration between the firmware and management software made it hard to adapt the system for customized needs. Also the official design was based on the ATMega16 leading to memory issues.

This design does not feature an µC itself but is optimized for Boards similar to an Arduino pro mini. Those boards are produced with an ATMega328 or ATMega168 allowing to choose between cheap controllers or space for more complex logic. Both controllers feature more PWM outputs than the original ATMega16 allowing advanced LED control scenarios. While iSysBus was aimed at professional installations this project focuses on easy customization and adaption to own control requirements.

While the protocol used by aSysBus is similar to iSysBus and may be used on the same bus a communication between both systems is not intended.