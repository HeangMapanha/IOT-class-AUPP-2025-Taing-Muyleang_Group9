# IOT-class-AUPP-2025-Taing-Muyleang_Group9

1. Overview

   In this lab, you will build a tiny IoT monitoring node with an ESP32, DHT22 temperature/humidity sensor, and a relay. The ESP32 sends Telegram        alerts when the temperature rises above a threshold and lets users control the relay via chat commands. Once the temperature drops below the          threshold again, the relay turns off automatically.

2. Learning Outcomes (CLO Alignment)
   • Design & implement an IoT system using ESP32 + MicroPython (sensing, actuation, networking).
   • Apply programming techniques for periodic sampling, debouncing, and simple state machines.
   • Develop a chat-based remote control application using Telegram Bot API (HTTP requests).
   • Document & present system design, wiring, and test evidence (screenshots/video), and reflect on reliability/ethics.
   • Evaluate performance (sampling interval, rate limits) and safety (relay loads, power isolation).
   
3. Equipment
   • ESP32 Dev Board (MicroPython firmware flashed)
   • DHT22 sensor
   • Relay module
   • jumper wires
   • USB cable + laptop with Thonny
   • Wi-Fi access (internet)

4. Wiring

5. Taks

   => Task 1: Read DHT22 every 5 seconds and print the temperature and humidity with 2 decimals.
