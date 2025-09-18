# 1. Overview

In this lab, students will design an ESP32-based IoT system with MicroPython that integrates a
web interface and an LCD display. The system will allow users to control an LED, read sensors,
and send custom messages to the LCD through a webserver.
This lab emphasizes interaction between web UI and hardware, giving students practice in event-
driven IoT design.

# 2. Learning Outcomes ( (CLO Alignment)
By the end of this lab, students will be able to:
- Implement a MicroPython webserver to serve HTML controls.
- Control an LED from the web page.
- Read data from DHT11 and ultrasonic sensors and expose it on the webserver.
- Use web buttons to selectively show temperature and distance on an LCD (I²C).
- Send custom text from a textbox to display on the LCD.
- Document wiring, interface behavior, and system operation.

# 3. Equipment
- ESP32 Dev Board (MicroPython firmware flashed)
- DHT11 sensor (temperature/humidity)
- HC-SR04 ultrasonic distance sensor
- LCD 16×2 with I²C backpack
- Breadboard, jumper wires
- USB cable + laptop with Thonny
- Wi-Fi access

# 4. Wiring

# 5. Tasks & Checkpoints

## Task 1 - LED Control (15 pts)
• Add two buttons (ON/OFF) on the web page.
• When clicked, LED on GPIO2 should turn ON or OFF.
• Evidence: short video showing button click → LED changes
