## 1. Overview

In this lab, we will create a mobile application using MIT App Inventor to remotely control a DC motor through an ESP32 running MicroPython. The ESP32 will provide HTTP endpoints "forward", "backward", "stop", which our app will use to send commands over Wi-Fi to manage the motor’s direction and speed. Additionally, all motor control actions and speed changes will be logged to an IoT dashboard using InfluxDB and Grafana, allowing us to monitor and analyze them in real time.

## 2. Learning Outcome
- Design and build a complete IoT actuation system that combines hardware (ESP32 + L298N), a mobile application, and a cloud dashboard.
- Create a custom mobile interface with MIT App Inventor to send REST commands to the ESP32.
- Program a lightweight web API in MicroPython to control the motor.
- Set up InfluxDB and Grafana to record and visualize actuator data, including speed, direction, and timestamps.
- Assess system performance, including response latency and data accuracy, and suggest possible improvements.

## 3. Equipments
- ESP32 Dev Board (MicroPython flashed)
- L298N motor driver
- DC motor + power supply (7–12 V)
- Jumper wires + breadboard
- Laptop with Thonny IDE
- Android phone with MIT App Inventor installed
- Wi-Fi access point
- Grafana Cloud account or local InfluxDB server
  
## 4. Wiring & Flowchart

### Wiring

![Lab5 Wiring](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/cc1c803bde24b97658e2263fe94546a1d148b9cc/Lab5/Lab5-wiring.jpg)

### Flowchart


## 5. Tasks and Checkpoints

### Task 1: ESP32 Web Server

### Task 2 : Mobile App Design
![Lab5 Photo](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/main/Lab5/photo_2025-12-07%2023.27.03.jpeg)

### Task 3 : Data Logging to InfluxDB

### Task 4 : Grafana Dashboard
![Lab5 Photo](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/main/Lab5/photo_2025-12-07%2023.27.05.jpeg)

## 6. Submission and Academic Integrity

[![My YouTube Video](https://img.youtube.com/vi/tP01OilUORk/hqdefault.jpg)](https://www.youtube.com/watch?v=tP01OilUORk)








