## Guardian Gate — Hardware Requirements

Overview

Guardian Gate is an embedded security monitoring system that combines a computing board, GrovePi interface, sensors, buttons, and alarm components.

The following hardware is required to reproduce the complete physical system.

Components

| Component                       |    Quantity | Purpose                                                                 |
| ------------------------------- | ----------: | ----------------------------------------------------------------------- |
| Raspberry Pi / Compatible Board |           1 | Runs the Guardian Gate Python program                                   |
| GrovePi                         |           1 | Provides the interface between the computing board and Grove components |
| Ultrasonic Sensor               |           2 | Detects nearby objects/human presence                                   |
| Push Button                     |           2 | Provides security input                                                 |
| Arm/Disarm Button               |           1 | Activates or deactivates the security system                            |
| LED                             |           1 | Visual alarm indicator                                                  |
| Buzzer                          |           1 | Audible alarm indicator                                                 |
| Jumper Wires                    | As required | Connects components                                                     |
| Power Supply                    |           1 | Provides power to the embedded system                                   |

## Pin Configuration

The current Python implementation uses the following GrovePi pins:

| Device              | Pin | Mode       |
| ------------------- | --: | ---------- |
| Ultrasonic Sensor 1 |  D2 | Ultrasonic |
| Ultrasonic Sensor 2 |  D3 | Ultrasonic |
| Arm/Disarm Button   |  D4 | Input      |
| Buzzer              |  D5 | Output     |
| LED                 |  D6 | Output     |
| Button 1            |  D7 | Input      |
| Button 2            |  D8 | Input      |


## Sensor Configuration

The system considers both ultrasonic sensors to indicate nearby presence when the measured distance is below:30 cm
The alarm remains active for:4 seconds

## Hardware Workflow

Ultrasonic Sensors
        │
        ↓
    GrovePi
        │
        ↓
Raspberry Pi / Python
        │
        ├── Human detected
        │       ↓
        │   Telegram Alert
        │
        └── Human + Button
                ↓
        Intrusion Confirmed
             /        \
            ↓          ↓
           LED       Buzzer


## Important Note

The exact wiring and physical arrangement may depend on the specific GrovePi-compatible hardware used during implementation.
The Python source code in `src/guardian_gate.py` should be used together with the corresponding hardware connections described above.
