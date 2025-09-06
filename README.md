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

   Task 1: Sensor Read and Print
   => Read DHT22 every 5 seconds and print the temperature and humidity with 2 decimals.
   Screenshot:

   Task 2: Telegram Send
   => Implement send_message() and post a test message to your group.
   Screenshot:

   Task 3: Bot command
   => • Implement /status to reply with current T/H and relay state.
      • Implement /on and /off to control the relay.

   Task 4: Bot Command
   => • No messages while T < 30 °C.
      • If T ≥ 30 °C and relay is OFF, send an alert every loop (5 s) until /on is received.
      • After /on, stop alerts. When T < 30 °C, turn relay OFF automatically and send a one-time “auto-OFF” notice.
   Short video

   Task 5: Robustness
   => • Auto-reconnect Wi-Fi when dropped.
      • Handle Telegram HTTP errors (print status; skip this cycle on failure).
      • Avoid crashing on DHT OSError (skip cycle).

   Task 6-Document
   => • README.md with wiring diagram/photo, configuration steps (token, chat id), and usage instructions.
      • Include a block diagram or flowchart of your loop/state.

   - Wiring Diagram/photo

   - Configuration steps:
     + Token
     + Chat id:
   
   - Usage Instruction:
  
   - Diagram and flow chart:
     
    
       
   
   
