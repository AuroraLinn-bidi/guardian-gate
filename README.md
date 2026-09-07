🛡️ Guardian Gate

An embedded security and monitoring system designed to detect human presence and identify potential intrusion using ultrasonic sensors, physical buttons, LED/buzzer alerts, and Telegram notifications.

📌 Project Overview

Guardian Gate is an embedded systems project that combines hardware sensors with Python-based control logic to provide a simple automated security monitoring system.

The system monitors the area near a protected entrance using two ultrasonic sensors. When a person is detected, the system can send a notification through Telegram. If human presence is detected together with a button-triggered event, the system treats the situation as a confirmed intrusion and activates both an LED and buzzer alarm.

The system can also be manually switched between ACTIVE and STOPPED modes using an arm/disarm button.

✨ Features

* 🔊 Dual ultrasonic sensor monitoring
* 👤 Human presence detection
* 🔘 Two physical security buttons
* 🔐 Arm/Disarm system control
* 🚨 LED and buzzer alarm
* 📱 Telegram notifications
* ⏱️ Notification and alarm cooldown periods
* 🐍 Python-based control program
* 🔧 GrovePi hardware integration

 🛠️ Technologies

* Python
* GrovePi
* Raspberry Pi / Compatible Embedded Platform
* Ultrasonic Sensors
* Digital Buttons
* LED
* Buzzer
* Telegram Bot API

🔌 Hardware Components

| Component                       | Quantity | Purpose                           |
| ------------------------------- | -------: | --------------------------------- |
| Ultrasonic Sensor               |        2 | Detect nearby human presence      |
| Push Button                     |        2 | Security input                    |
| Arm/Disarm Button               |        1 | Activate or deactivate the system |
| LED                             |        1 | Visual alarm indicator            |
| Buzzer                          |        1 | Audible alarm                     |
| GrovePi                         |        1 | Hardware interface                |
| Raspberry Pi / Compatible Board |        1 | Runs the Python program           |

 ⚙️ System Logic


                    Guardian Gate
                         │
                Arm / Disarm Button
                         │
                  ┌──────┴──────┐
                  │             │
               ACTIVE        STOPPED
                  │
                  ↓
          Read Sensors & Buttons
                  │
          ┌───────┴────────┐
          │                │
     Ultrasonic 1     Ultrasonic 2
          │                │
          └───────┬────────┘
                  │
          Human Detected?
             │          │
            No         Yes
             │          │
             │          ↓
             │    Telegram Alert
             │          │
             │          ↓
             │    Button Pressed?
             │          │
             │         Yes
             │          ↓
             │    Intruder Confirmed
             │          │
             │     ┌────┴────┐
             │     ↓         ↓
             │    LED      Buzzer
             │
             └──── Continue Monitoring


 📂 Project Structure

guardian-gate/
│
├── README.md
│
├── requirements.txt
│
└── src/
    └── guardian_gate.py


🚀 Installation

Clone the repository:
git clone https://github.com/AuroaLinn-bidi/guardian-gate.git

Move into the project directory:
cd guardian-gate

Install the required Python packages:
pip install -r requirements.txt

🔐 Telegram Configuration

Telegram credentials are intentionally not stored in the source code.

The application reads the credentials from environment variables:
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

Configure these variables on the device running the Guardian Gate system before starting the application.

 ▶️ Running the System

Run the main Python program:
python src/guardian_gate.py

The system starts in the STOPPED state.

Press the Arm/Disarm button to activate monitoring.

📱 Notification Behavior

When the system is active:
 Human Presence

If both ultrasonic sensors detect a nearby object within the configured distance, the system sends:
"Someone is in front of the door."


Confirmed Intrusion

If human presence is detected together with either security button being pressed, the system:

1. Sends a Telegram alert.
2. Activates the LED.
3. Activates the buzzer.
4. Keeps the alarm active for the configured duration.
5. Turns the LED and buzzer off.

⚠️ Hardware Requirement

This project depends on physical embedded hardware and cannot be fully tested using a normal PC alone.

The repository contains the Python source code, software dependencies, and project documentation. The complete system requires the corresponding GrovePi-compatible hardware and connected sensors/actuators.

🔒 Security

Sensitive Telegram credentials should never be committed to GitHub.

The project uses environment variables instead of storing the Telegram bot token directly in the source code.

📌 Project Status

Completed — Academic Embedded Systems Project

👩‍💻 Author

A Mi Mi Soe

Software Engineering Student
Interested in Full Stack Development, Android Development, and Embedded Systems.

