# IOT-class-AUPP-2025-Taing-Muyleang_Group9

# 1. Overview

   In this lab, you will build a tiny IoT monitoring node with an ESP32, DHT22 temperature/humidity sensor, and a relay. The ESP32 sends Telegram        alerts when the temperature rises above a threshold and lets users control the relay via chat commands. Once the temperature drops below the          threshold again, the relay turns off automatically.

# 2. Learning Outcomes (CLO Alignment)
   - Design & implement an IoT system using ESP32 + MicroPython (sensing, actuation, networking).
   - Apply programming techniques for periodic sampling, debouncing, and simple state machines.
   - Develop a chat-based remote control application using Telegram Bot API (HTTP requests).
   - Document & present system design, wiring, and test evidence (screenshots/video), and reflect on reliability/ethics.
   - Evaluate performance (sampling interval, rate limits) and safety (relay loads, power isolation).
   
# 3. Equipment
   - ESP32 Dev Board (MicroPython firmware flashed)
   - DHT22 sensor
   - Relay module
   - jumper wires
   - USB cable + laptop with Thonny
   - Wi-Fi access (internet)

# 4. Wiring
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/3e9533d3627f43133aee09351c6accf982601428/image_2025-09-06_11-31-06.png?raw=true)


# 5. Taks

   ### Task 1: Sensor Read and Print
   > Read DHT22 every 5 seconds and print the temperature and humidity with 2 decimals.
   Serial Screenshot:
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/e098ae2c716a547fd1198646a2a06bc965191cbd/photo_2025-09-07%2002.03.32.jpeg?raw=true)
   

   ### Task 2: Telegram Send
   > Implement send_message() and post a test message to your group.
   Screenshot:
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/56084c11b654ecd1c7e6fbe1dd89d855e5a60d1e/photo_2025-09-07%2002.40.51.jpeg?raw=true)

   
   ### Task 3: Bot command
   > - Implement /status to reply with current T/H and relay state.
   > - Implement /on and /off to control the relay.

   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/cd12c23a5856e967bcdd0e9e0a8801b3e3b0ecb7/photo_2025-09-07%2002.08.02.jpeg?raw=true)
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/cd12c23a5856e967bcdd0e9e0a8801b3e3b0ecb7/photo_2025-09-07%2002.08.04.jpeg?raw=true)


   ### Task 4: Bot Command
   > - No messages while T < 30 °C.
      - If T ≥ 30 °C and relay is OFF, send an alert every loop (5 s) until /on is received.
      - After /on, stop alerts. When T < 30 °C, turn relay OFF automatically and send a one-time “auto-OFF” notice.
   Short video: N/A ( will provide later)

   ### Task 5: Robustness
   > - Auto-reconnect Wi-Fi when dropped.
      - Handle Telegram HTTP errors (print status; skip this cycle on failure).
      - Avoid crashing on DHT OSError (skip cycle).
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/e3ee5d5986bfefa181bc6db933031cc0e6afd2d5/photo_2025-09-07%2002.45.51.jpeg?raw=true)


   ### Task 6-Document
   > - README.md with wiring diagram/photo, configuration steps (token, chat id), and usage instructions.
   > - Include a block diagram or flowchart of your loop/state.

   - Wiring diagram
 +---------------------+
 |       ESP32         |
 |                     |
 |  3V3 --------> VCC  |   DHT22
 |  GND --------> GND  |
 |  GPIO4 ------> DATA |
 |                     |
 |  GPIO2 ------> Relay Module IN
 |  GND --------> Relay GND
 |  5V  --------> Relay VCC
 +---------------------+
   ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/76d06ba6967dacfb8dab99e71992fb94c977d9fa/wiring.png?raw=true)


   - Configuration steps:
     + Token: 7591180638:AAF7Kol0RyDsgbh3airP0NA7dEtF0i-FlGE
     + Chat id: -4936918510
   
   - Usage Instruction:
     1. Upload code to ESP32 and run.
     2. Connect ESP32 to Wi-Fi.
     3. Use Telegram commands:
        + /on → Stop alerts
        + /off → Relay OFF
        + /status → Show relay + T/H
        + /temp → Get current T/H
        + /whoami → Get your chat ID
      4. Temperature Alerts:
         + ≥ 30°C → Alert every 5s until /on
         + < 30°C → Relay auto-OFF, one-time message
      5. Robustness:
         + Auto Wi-Fi reconnect
         + Skip DHT sensor errors
         + Telegram HTTP error handled
  
   - Diagram and flow chart:
     + block diagram:
        +-----------+       +-----------+
 | Telegram  | <---> | ESP32     |
 |   App     |       |  Bot Code |
 +-----------+       +-----------+
                        | GPIO4 (DHT Data)
                        v
                     +-------+
                     | DHT11 |
                     | Temp  |
                     | Humid |
                     +-------+
                        |
                        | GPIO2
                        v
                     +-------+
                     | Relay |
                     +-------+


       + flow chart
      
       ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/b09777d789e0c4d1f8a53f7005c2dd504b27cec4/photo_2025-09-07%2002.29.17.jpeg?raw=true)

    
       
   
   
